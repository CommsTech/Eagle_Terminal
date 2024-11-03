import os

import paramiko
from PyQt5.QtCore import QMimeData, Qt
from PyQt5.QtGui import QDrag
from PyQt5.QtWidgets import (
    QFileSystemModel,
    QInputDialog,
    QMessageBox,
    QPushButton,
    QTreeView,
    QVBoxLayout,
    QWidget,
)


class RemoteFileSystemModel(QFileSystemModel):
    def __init__(self, sftp):
        super().__init__()
        self.sftp = sftp
        self.setRootPath("/")

    def fetchMore(self, parent):
        path = self.filePath(parent)
        try:
            for entry in self.sftp.listdir_attr(path):
                child = self.index(os.path.join(path, entry.filename), 0, parent)
                self.dataChanged.emit(child, child)
        except IOError:
            pass


class DraggableTreeView(QTreeView):
    def mouseMoveEvent(self, e):
        if e.buttons() != Qt.LeftButton:
            return

        drag = QDrag(self)
        mime = QMimeData()
        mime.setUrls([self.model().filePath(self.currentIndex())])
        drag.setMimeData(mime)
        drag.exec_(Qt.CopyAction | Qt.MoveAction)


class FileBrowser(QWidget):
    def __init__(self, parent, ssh_client):
        super().__init__(parent)
        self.ssh_client = ssh_client
        self.sftp = ssh_client.open_sftp()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        self.model = RemoteFileSystemModel(self.sftp)
        self.tree = DraggableTreeView()
        self.tree.setModel(self.model)
        self.tree.setRootIndex(self.model.index("/"))
        self.tree.setDragEnabled(True)
        self.tree.setAcceptDrops(True)
        self.tree.setDropIndicatorShown(True)

        layout.addWidget(self.tree)

        upload_button = QPushButton("Upload File")
        upload_button.clicked.connect(self.upload_file)
        layout.addWidget(upload_button)

        download_button = QPushButton("Download File")
        download_button.clicked.connect(self.download_file)
        layout.addWidget(download_button)

    def upload_file(self):
        local_path, _ = QFileDialog.getOpenFileName(self, "Select File to Upload")
        if local_path:
            remote_path, ok = QInputDialog.getText(
                self, "Remote Path", "Enter remote path:"
            )
            if ok:
                try:
                    self.sftp.put(local_path, remote_path)
                    self.model.fetchMore(self.tree.rootIndex())
                except Exception as e:
                    QMessageBox.warning(
                        self, "Upload Error", f"Failed to upload file: {str(e)}"
                    )

    def download_file(self):
        index = self.tree.currentIndex()
        if index.isValid():
            remote_path = self.model.filePath(index)
            local_path, _ = QFileDialog.getSaveFileName(self, "Save File As")
            if local_path:
                try:
                    self.sftp.get(remote_path, local_path)
                except Exception as e:
                    QMessageBox.warning(
                        self, "Download Error", f"Failed to download file: {str(e)}"
                    )
