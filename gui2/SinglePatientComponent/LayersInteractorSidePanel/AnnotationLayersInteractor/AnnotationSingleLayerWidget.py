from PySide2.QtWidgets import QWidget, QLabel, QHBoxLayout, QLineEdit, QComboBox, QGridLayout, QPushButton,\
    QRadioButton, QMenu, QAction, QSlider, QColorDialog, QVBoxLayout, QSpacerItem, QSizePolicy
from PySide2.QtCore import Qt, QSize, Signal
from PySide2.QtGui import QPixmap, QIcon, QColor
import os
import logging
from gui2.UtilsWidgets.CustomQGroupBox.QCollapsibleGroupBox import QCollapsibleGroupBox

from utils.software_config import SoftwareConfigResources
from utils.patient_parameters import MRISequenceType


class AnnotationSingleLayerWidget(QWidget):
    """

    """
    visibility_toggled = Signal(str, bool)
    display_name_changed = Signal(str, str)
    opacity_value_changed = Signal(str, int)
    color_value_changed = Signal(str, QColor)
    resizeRequested = Signal()

    def __init__(self, uid, parent=None):
        super(AnnotationSingleLayerWidget, self).__init__(parent)
        self.parent = parent
        self.uid = uid
        self.__set_interface()
        self.__set_layout_dimensions()
        self.__set_connections()
        self.__set_stylesheets()
        self.__init_from_parameters()

    def __set_interface(self):
        self.setAttribute(Qt.WA_StyledBackground, True)  # Enables to set e.g. background-color for the QWidget

        # create context menu
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.options_menu = QMenu(self)
        self.options_menu.addAction(QAction('Remove', self))
        self.options_menu.addSeparator()

        # self.content_label = QLabel(self)
        self.layout = QVBoxLayout(self)
        # self.content_label.setLayout(self.layout)
        self.name_layout = QHBoxLayout()
        self.icon_label = QLabel()
        self.icon_label.setScaledContents(True)  # Will force the pixmap inside to rescale to the label size
        pix = QPixmap(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../../../Images/file_icon.png'))
        self.icon_label.setPixmap(pix)
        self.display_name_lineedit = QLineEdit()
        self.display_name_lineedit.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)
        self.display_toggle_pushbutton = QPushButton()
        self.display_toggle_pushbutton.setCheckable(True)
        self.closed_eye_icon = QIcon(QPixmap(os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                           '../../../Images/closed_eye_icon.png')))
        self.open_eye_icon = QIcon(QPixmap(os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                           '../../../Images/opened_eye_icon.png')))
        self.display_toggle_pushbutton.setIcon(self.closed_eye_icon)
        self.name_layout.addWidget(self.icon_label)
        self.name_layout.addWidget(self.display_name_lineedit)
        self.name_layout.addWidget(self.display_toggle_pushbutton)

        self.parent_layout = QHBoxLayout()
        self.parent_image_label = QLabel("Parent MRI")
        self.parent_image_combobox = QComboBox()
        self.parent_layout.addWidget(self.parent_image_label)
        self.parent_layout.addWidget(self.parent_image_combobox)

        self.annotation_type_layout = QHBoxLayout()
        self.annotation_type_label = QLabel("Annotation of ")
        self.annotation_type_combobox = QComboBox()
        self.annotation_type_combobox.addItems(["Brain", "Tumor"])
        self.annotation_type_layout.addWidget(self.annotation_type_label)
        self.annotation_type_layout.addWidget(self.annotation_type_combobox)

        self.__set_interface_advanced_options()

        self.layout.addLayout(self.name_layout)
        self.layout.addLayout(self.parent_layout)
        self.layout.addLayout(self.annotation_type_layout)
        self.layout.addWidget(self.advanced_options_collapsible)

    def __set_interface_advanced_options(self):
        self.advanced_options_collapsible = QCollapsibleGroupBox(uid=self.uid + '_advanced', parent=self)
        self.advanced_options_collapsible.header_pushbutton.setText("Advanced options")
        self.opacity_label = QLabel("Opacity ")
        self.opacity_slider = QSlider(Qt.Orientation.Horizontal)
        self.opacity_slider.setMinimum(0)
        self.opacity_slider.setMaximum(100)
        self.opacity_slider.setTickInterval(1)
        self.opacity_slider.setSliderPosition(50)
        self.opacity_slider.setEnabled(False)
        self.opacity_layout = QHBoxLayout()
        self.opacity_layout.addWidget(self.opacity_label)
        self.opacity_layout.addWidget(self.opacity_slider)
        self.opacity_layout.addStretch(1)
        self.advanced_options_collapsible.content_label_layout.addLayout(self.opacity_layout)

        self.color_label = QLabel("Color ")
        self.color_dialogpushbutton = QPushButton()
        self.color_dialogpushbutton.setEnabled(False)
        self.color_dialog = QColorDialog(parent=self.parent)  # @FIXME. GtkDialog mapped without a transient parent. This is discouraged.
        self.color_layout = QHBoxLayout()
        self.color_layout.addWidget(self.color_label)
        self.color_layout.addWidget(self.color_dialogpushbutton)
        self.color_layout.addStretch(1)
        self.advanced_options_collapsible.content_label_layout.addLayout(self.color_layout)

    def __set_layout_dimensions(self):
        self.icon_label.setFixedSize(QSize(15, 20))
        self.display_name_lineedit.setFixedHeight(20)
        self.parent_image_label.setFixedHeight(20)
        self.parent_image_combobox.setFixedHeight(20)
        self.annotation_type_label.setFixedHeight(20)
        self.annotation_type_combobox.setFixedHeight(20)
        self.display_toggle_pushbutton.setFixedSize(QSize(20, 20))
        self.display_toggle_pushbutton.setIconSize(QSize(20, 20))

        ############## ADVANCED OPTIONS ################
        self.opacity_label.setFixedHeight(20)
        self.opacity_slider.setFixedHeight(10)
        self.color_label.setFixedHeight(20)
        self.color_dialogpushbutton.setFixedHeight(10)
        self.advanced_options_collapsible.content_label.setFixedHeight(50) #.adjustSize()

    def __set_connections(self):
        self.customContextMenuRequested.connect(self.on_right_clicked)
        self.display_name_lineedit.textEdited.connect(self.on_name_changed)
        self.display_toggle_pushbutton.toggled.connect(self.on_visibility_toggled)
        # self.sequence_type_combobox.currentTextChanged.connect(self.on_sequence_type_changed)
        self.advanced_options_collapsible.header_pushbutton.clicked.connect(self.on_advanced_options_clicked)
        self.opacity_slider.valueChanged.connect(self.__on_opacity_changed)
        self.color_dialogpushbutton.clicked.connect(self.__on_color_selector_clicked)

    def __set_stylesheets(self):
        self.setStyleSheet("""AnnotationSingleLayerWidget{background-color: rgba(248, 248, 248, 1);}""")
        self.color_dialogpushbutton_base_ss = """ QPushButton{border-color:rgb(0, 0, 0); border-width:2px;} """
        self.display_name_lineedit.setStyleSheet("""
        QLineEdit{
        color: rgba(67, 88, 90, 1);
        font: 14px;
        }""")

        self.advanced_options_collapsible.content_label.setStyleSheet("""
        QLabel{background-color: rgba(235, 235, 235, 1);
        }""")

    def __init_from_parameters(self):
        params = SoftwareConfigResources.getInstance().get_active_patient().annotation_volumes[self.uid]
        self.display_name_lineedit.setText(params.display_name)
        self.opacity_slider.blockSignals(True)
        self.opacity_slider.setSliderPosition(params.display_opacity)
        self.opacity_slider.blockSignals(False)
        self.color_dialog.setCurrentColor(QColor.fromRgb(params.display_color[0],
                                                         params.display_color[1],
                                                         params.display_color[2],
                                                         params.display_color[3]))
        custom_color_str = "background-color:rgb({}, {}, {})".format(params.display_color[0],
                                                                     params.display_color[1],
                                                                     params.display_color[2])
        custom_ss = "QPushButton{" + custom_color_str + ";}"
        self.color_dialogpushbutton.setStyleSheet(self.color_dialogpushbutton_base_ss + custom_ss)

    def adjustSize(self):
        items = (self.layout.itemAt(i) for i in range(self.layout.count()))
        actual_height = 0
        for w in items:
            if (w.__class__ == QHBoxLayout) or (w.__class__ == QVBoxLayout):
                max_height = 0
                sub_items = [w.itemAt(i) for i in range(w.count())]
                for sw in sub_items:
                    if sw.__class__ != QSpacerItem:
                        if sw.wid.sizeHint().height() > max_height:
                            max_height = sw.wid.sizeHint().height()
                actual_height += max_height
            elif w.__class__ == QGridLayout:
                pass
            # elif w.__class__ == QCollapsibleGroupBox:
            #     size = w.wid.content_label.size()
            #     actual_height += size.height()
            elif w.__class__ != QSpacerItem:
                size = w.wid.sizeHint()
                actual_height += size.height()
            else:
                pass
        self.setFixedSize(QSize(self.size().width(), actual_height))
        logging.debug("Single annotation container set to {}.\n".format(QSize(self.size().width(), actual_height)))
        self.resizeRequested.emit()

    def on_right_clicked(self, point):
        self.options_menu.exec_(self.mapToGlobal(point))

    def on_advanced_options_clicked(self):
        self.adjustSize()

    def on_visibility_toggled(self, state):
        if state:
            self.display_toggle_pushbutton.setIcon(self.open_eye_icon)
            self.opacity_slider.setEnabled(True)
            self.color_dialogpushbutton.setEnabled(True)
        else:
            self.display_toggle_pushbutton.setIcon(self.closed_eye_icon)
            self.opacity_slider.setEnabled(False)
            self.color_dialogpushbutton.setEnabled(False)

        self.visibility_toggled.emit(self.uid, state)

    def on_name_changed(self, text):
        self.display_name_changed.emit(self.uid, text)

    def __on_opacity_changed(self, value):
        self.opacity_value_changed.emit(self.uid, value)

    def __on_color_selector_clicked(self):
        code = self.color_dialog.exec_()
        if code == QColorDialog.Accepted:
            color = self.color_dialog.currentColor()
            self.color_value_changed.emit(self.uid, color)
            custom_color_str = "background-color:rgb({}, {}, {})".format(color.red(), color.green(), color.blue())
            custom_ss = "QPushButton{" + custom_color_str + ";}"
            self.color_dialogpushbutton.setStyleSheet(self.color_dialogpushbutton_base_ss + custom_ss)
