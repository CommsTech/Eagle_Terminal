from PyQt5.QtCore import QModelIndex, Qt
from PyQt5.QtGui import QStandardItem, QStandardItemModel
from PyQt5.QtWidgets import QFileSystemModel, QTreeView, QVBoxLayout, QWidget


class FileBrowser(QWidget):
    def __init__(self, ssh_manager):
        super().__init__()
        self.ssh_manager = ssh_manager
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(["Name", "Size", "Type"])
        self.tree_view = QTreeView()
        self.tree_view.setModel(self.model)
        self.tree_view.setUniformRowHeights(True)
        self.tree_view.setAlternatingRowColors(True)
        self.tree_view.setSortingEnabled(True)
        self.tree_view.setExpandsOnDoubleClick(False)
        self.tree_view.doubleClicked.connect(self.item_double_clicked)
        layout.addWidget(self.tree_view)

    def refresh(self):
        self.model.clear()
        self.model.setHorizontalHeaderLabels(["Name", "Size", "Type"])
        root_path = self.ssh_manager.get_home_directory()
        self.populate_tree(root_path, self.model.invisibleRootItem())

    def populate_tree(self, path, parent):
        file_list = self.ssh_manager.list_files(path)
        for line in file_list.splitlines()[1:]:  # Skip the total line
            parts = line.split()
            if len(parts) < 9:
                continue
            permissions, _, _, _, size, _, _, _, name = parts[:9]
            item = QStandardItem(name)
            item.setData(path, Qt.UserRole)
            size_item = QStandardItem(size)
            type_item = QStandardItem(
                "Directory" if permissions.startswith("d") else "File"
            )
            parent.appendRow([item, size_item, type_item])

    def item_double_clicked(self, index):
        item = self.model.itemFromIndex(index)
        path = item.data(Qt.UserRole)
        if path:
            full_path = f"{path}/{item.text()}"
            self.populate_tree(full_path, item)
