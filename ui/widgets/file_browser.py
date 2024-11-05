import os

import paramiko
from PyQt5.QtCore import QMimeData, Qt
from PyQt5.QtGui import QDrag
from PyQt5.QtWidgets import (QFileSystemModel, QInputDialog, QMessageBox,
                             QPushButton, QTreeView, QVBoxLayout, QWidget)


class RemoteFileSystemModel(QFileSystemModel):
    def __init__(self, sftp):
        """Initialize the SFTP client wrapper.
        
        Args:
            sftp (paramiko.SFTPClient): An instance of the SFTP client from paramiko.
        
        Returns:
            None
        
        Raises:
            TypeError: If sftp is not an instance of paramiko.SFTPClient.
        """
        super().__init__()
        self.sftp = sftp
        self.setRootPath("/")

    def fetchMore(self, parent):
        """Fetches more items for the given parent directory in a remote SFTP connection.
        
        Args:
            parent: The parent directory for which to fetch more items.
        
        Returns:
            None
        
        Raises:
            IOError: If there's an issue accessing the remote directory.
        """
        path = self.filePath(parent)
        try:
            for entry in self.sftp.listdir_attr(path):
                child = self.index(os.path.join(path, entry.filename), 0, parent)
                self.dataChanged.emit(child, child)
        except IOError:
            pass


class DraggableTreeView(QTreeView):
    def mouseMoveEvent(self, e):
        """Handles mouse move events for drag and drop functionality.
        
        Args:
            self: The instance of the class containing this method.
            e (QMouseEvent): The mouse event object containing information about the mouse movement.
        
        Returns:
            None
        
        Notes:
            This method initiates a drag operation when the left mouse button is pressed and moved.
            It sets up a QDrag object with the file path of the currently selected item as the drag data.
        """
        if e.buttons() != Qt.LeftButton:
            return

        drag = QDrag(self)
        mime = QMimeData()
        mime.setUrls([self.model().filePath(self.currentIndex())])
        drag.setMimeData(mime)
        drag.exec_(Qt.CopyAction | Qt.MoveAction)


class FileBrowser(QWidget):
    def __init__(self, parent, ssh_client):
        """Initialize a new instance of the class.
        
        Args:
            parent (object): The parent object or widget to which this instance belongs.
            ssh_client (paramiko.SSHClient): The SSH client used for remote connections.
        
        Returns:
            None: This method doesn't return anything.
        """
        super().__init__(parent)
        self.ssh_client = ssh_client
        self.sftp = ssh_client.open_sftp()
        self.init_ui()

    def init_ui(self):
        """Initializes the user interface for the SFTP file system viewer.
        
        Args:
            self: The instance of the class containing this method.
        
        Returns:
            None: This method doesn't return anything, it sets up the UI elements.
        
        This method sets up the main layout of the SFTP file system viewer. It creates a vertical layout
        and populates it with a tree view for displaying the remote file system, and buttons for
        uploading and downloading files. The tree view uses a custom model (RemoteFileSystemModel)
        and is set up to allow drag and drop operations. The upload and download buttons are connected
        to their respective methods.
        """
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
        """Upload a file to the remote server using SFTP.
        
        This method opens a file dialog for the user to select a local file,
        then prompts for a remote path. It attempts to upload the file to the
        specified remote path using SFTP. If successful, it refreshes the file
        tree view. If an error occurs during upload, it displays a warning message.
        
        Args:
            self: The instance of the class containing this method.
        
        Returns:
            None
        
        Raises:
            Exception: If there's an error during the file upload process.
        """
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
        """Download a selected file from the remote server to the local machine.
        
        Args:
            self: The instance of the class containing this method.
        
        Returns:
            None
        
        Raises:
            Exception: If there's an error during the file download process.
        """
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
