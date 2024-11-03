from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QSplitter, QTabWidget, QVBoxLayout, QWidget


class SplitView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.splitter = QSplitter(Qt.Horizontal)
        self.layout.addWidget(self.splitter)

        self.left_tab_widget = QTabWidget()
        self.right_tab_widget = QTabWidget()

        self.splitter.addWidget(self.left_tab_widget)
        self.splitter.addWidget(self.right_tab_widget)
        self.right_tab_widget.hide()  # Initially hide the right tab widget

    def add_tab(self, widget, title):
        if self.right_tab_widget.isHidden():
            self.left_tab_widget.addTab(widget, title)
        else:
            self.right_tab_widget.addTab(widget, title)

    def split_view(self):
        if self.right_tab_widget.isHidden():
            self.right_tab_widget.show()
        else:
            self.right_tab_widget.hide()

    def move_tab_to_other_side(self, from_left=True):
        if from_left:
            source = self.left_tab_widget
            target = self.right_tab_widget
        else:
            source = self.right_tab_widget
            target = self.left_tab_widget

        if source.count() > 0:
            index = source.currentIndex()
            widget = source.widget(index)
            title = source.tabText(index)
            source.removeTab(index)
            target.addTab(widget, title)

    def get_current_tab(self):
        if self.right_tab_widget.isHidden() or self.left_tab_widget.hasFocus():
            return self.left_tab_widget.currentWidget()
        else:
            return self.right_tab_widget.currentWidget()
