import os

from PyQt5 import QtGui, QtCore, QtWidgets
from simple_logger import Logger

import thermography as tg


class AboutDialog(QtWidgets.QMessageBox):
    """This class represents the dialog that opens when the user clicks on `File->About` when using the graphical
    interface."""
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent=parent)
        Logger.debug("Opened About dialog")
        self.setWindowTitle("Thermography - About")
        self.setTextFormat(QtCore.Qt.RichText)
        gui_directory = os.path.join(os.path.join(tg.settings.get_thermography_root_dir(), os.pardir), "gui")
        rich_text_path = os.path.join(gui_directory, "about/about_rich_text.html")
        logo_path = os.path.join(gui_directory, "img/logo_small.png")
        with open(rich_text_path, 'r') as rich_text_file:
            text = rich_text_file.read()
            self.setText(text.format(logo_path=logo_path))

        self.__set_logo_icon()

    def __set_logo_icon(self):
        """Sets the default logo to the dialog."""
        gui_path = os.path.join(os.path.join(tg.settings.get_thermography_root_dir(), os.pardir), "gui")
        logo_path = os.path.join(gui_path, "img/logo.png")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(logo_path), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)
