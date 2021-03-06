import os

import cv2
from PyQt5 import QtWidgets, QtGui
from simple_logger import Logger

import thermography as tg
from gui.design import Ui_Save_images_dialog


class SaveImageDialog(QtWidgets.QDialog, Ui_Save_images_dialog):
    """This class implements a dialog which allows to save all data collected by the
    :class:`~gui.dialogs.create_dataset_dialog.CreateDatasetGUI` class to disk.
    """
    def __init__(self, working_modules: dict, broken_modules: dict, misdetected_modules: dict, parent=None):
        """Initializes the dialog with the files to save to disk.

        :param working_modules: Dictionary of working modules.
        :param broken_modules: Dictionary of broken modules.
        :param misdetected_modules: Dictionary of misdetected modules.
        :param parent: Parent window of this dialog.
        """
        super(self.__class__, self).__init__(parent=parent)

        Logger.debug("Opened 'Save Images' dialog")

        self.setupUi(self)
        self.__set_logo_icon()

        self.working_modules = working_modules
        self.broken_modules = broken_modules
        self.misdetected_modules = misdetected_modules

        self.output_directory = " "

        self.choose_directory_button.clicked.connect(self.__open_directory_dialog)
        self.save_button.clicked.connect(self.__save_module_dataset)
        self.progress_bar_all_frames.setMinimum(0)
        self.progress_bar_all_frames.setMaximum(
            len(self.working_modules.keys()) + len(self.broken_modules.keys()) + len(
                self.misdetected_modules.keys()) - 1)

    def __set_logo_icon(self):
        """Sets the default logo to the dialog."""
        gui_path = os.path.join(os.path.join(tg.settings.get_thermography_root_dir(), os.pardir), "gui")
        logo_path = os.path.join(gui_path, "img/logo.png")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(logo_path), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)

    def __open_directory_dialog(self):
        """Opens a file explorer to select the destination of the files to store to disk."""
        output_directory = QtWidgets.QFileDialog.getExistingDirectory(caption="Select dataset output directory")
        Logger.debug("Selected <{}> directory to store all images".format(output_directory))
        if output_directory == "":
            return

        self.output_directory = output_directory

        if len(os.listdir(self.output_directory)) > 0:
            Logger.warning("Directory {} is not empty!".format(self.output_directory))
            QtWidgets.QMessageBox.warning(self, "Non empty directory",
                                          "Directory {} not empty! Select an empty directory!".format(
                                              self.output_directory), QtWidgets.QMessageBox.Ok,
                                          QtWidgets.QMessageBox.Ok)
            self.__open_directory_dialog()
        else:
            self.save_directory_label.setText('Saving to directory: "{}"'.format(self.output_directory))
            self.save_button.setEnabled(True)

    def __save_module_dataset(self):
        """Saves the data to the directory selected when opening the file explorer."""
        self.progress_bar_all_frames.setEnabled(True)
        self.progress_bar_intra_frame.setEnabled(True)
        button_reply = QtWidgets.QMessageBox.question(self, 'Save dataset',
                                                      "Want to save dataset to {}?".format(self.output_directory),
                                                      QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                      QtWidgets.QMessageBox.No)
        if button_reply == QtWidgets.QMessageBox.No:
            Logger.warning("Rejected directory <{}> for saving all images".format(self.output_directory))
            self.output_directory = None
            self.__save_module_dataset()
        else:
            Logger.info("Saving all images to <{}>".format(self.output_directory))
            Logger.warning("If dialog freezes, check log file, but DON'T close the window!")
            working_modules_output_dir = os.path.join(self.output_directory, "working")
            broken_modules_output_dir = os.path.join(self.output_directory, "broken")
            misdetected_modules_output_dir = os.path.join(self.output_directory, "misdetected")

            overall_iter = 0

            def save_modules_into_directory(module_dict: dict, directory: str):
                global overall_iter

                os.mkdir(os.path.abspath(directory))
                for module_number, (module_id, registered_modules) in enumerate(module_dict.items()):
                    Logger.debug("Saving all views of module ID {}: view {}/{}".format(module_id, module_number,
                                                                                       len(module_dict.keys()) - 1))
                    self.progress_bar_all_frames.setValue(self.progress_bar_all_frames.value() + 1)
                    self.progress_bar_intra_frame.setValue(0)
                    self.progress_bar_intra_frame.setMaximum(len(registered_modules))
                    for m_index, m in enumerate(registered_modules):
                        name = "id_{0:05d}_frame_{1:05d}.jpg".format(module_id, m["frame_id"])
                        path = os.path.join(directory, name)
                        img = cv2.cvtColor(m["image"], cv2.COLOR_RGB2BGR)
                        cv2.imwrite(path, img)
                        self.progress_bar_intra_frame.setValue(m_index + 1)

            Logger.info("Saving working modules to <{}>".format(working_modules_output_dir))
            save_modules_into_directory(self.working_modules, working_modules_output_dir)
            Logger.info("Saved all working modules to <{}>".format(working_modules_output_dir))
            Logger.info("Saving broken modules to <{}>".format(broken_modules_output_dir))
            save_modules_into_directory(self.broken_modules, broken_modules_output_dir)
            Logger.info("Saved all broken modules to <{}>".format(broken_modules_output_dir))
            Logger.info("Saving misdetected modules to <{}>".format(misdetected_modules_output_dir))
            save_modules_into_directory(self.misdetected_modules, misdetected_modules_output_dir)
            Logger.info("Saved all misdetected modules to <{}>".format(misdetected_modules_output_dir))

        _ = QtWidgets.QMessageBox.information(self, "Saved!", "Saved all modules to {}".format(self.output_directory),
                                              QtWidgets.QMessageBox.Ok)
        self.close()
