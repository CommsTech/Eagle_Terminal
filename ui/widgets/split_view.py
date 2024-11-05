from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QSplitter, QTabWidget, QVBoxLayout, QWidget


class SplitView(QWidget):
    def __init__(self, parent=None):
        """
        Initialize a custom widget with a splitter and tab widgets.
        
        This method sets up the layout for a widget containing a horizontal splitter
        with two tab widgets. The right tab widget is initially hidden.
        
        Args:
            parent (QWidget, optional): The parent widget. Defaults to None.
        
        Returns:
            None
        
        """
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
        """Adds a widget as a new tab to either the left or right tab widget.
        
        Args:
            widget (QWidget): The widget to be added as a new tab.
            title (str): The title of the new tab.
        
        Returns:
            None
        
        """
        if self.right_tab_widget.isHidden():
            self.left_tab_widget.addTab(widget, title)
        else:
            self.right_tab_widget.addTab(widget, title)

    def split_view(self):
        """Toggles the visibility of the right tab widget.
        
        This method switches the visibility state of the right_tab_widget. If the widget
        is currently hidden, it will be shown. If it's visible, it will be hidden.
        
        Args:
            self: The instance of the class containing this method.
        
        Returns:
            None: This method doesn't return any value.
        """
        if self.right_tab_widget.isHidden():
            self.right_tab_widget.show()
        else:
            self.right_tab_widget.hide()

    def move_tab_to_other_side(self, from_left=True):
        """Move a tab from one side of the interface to the other.
        
        Args:
            from_left (bool, optional): Determines the direction of the move. If True (default), moves a tab from the left side to the right. If False, moves a tab from the right side to the left.
        
        Returns:
            None
        
        """
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
        """Get the current active tab widget.
        
        Returns:
            QWidget: The currently active tab widget. It could be either from the left tab widget
                     or the right tab widget, depending on which one is currently in focus or visible.
        """
        if self.right_tab_widget.isHidden() or self.left_tab_widget.hasFocus():
            return self.left_tab_widget.currentWidget()
        else:
            return self.right_tab_widget.currentWidget()
