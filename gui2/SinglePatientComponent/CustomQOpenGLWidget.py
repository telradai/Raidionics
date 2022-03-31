from PySide2.QtWidgets import QWidget, QOpenGLWidget, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem
from PySide2.QtGui import QPixmap, QImage, QPainter, QPen, QColor, QTransform
from PySide2.QtCore import Qt, QSize, Signal, QPoint
from PySide2 import QtOpenGL
import numpy as np

# from OpenGL.GL import *
import nibabel as nib
from nibabel.processing import resample_to_output
from scipy.ndimage import rotate


# class CustomQOpenGLWidget(QOpenGLWidget):
class CustomQOpenGLWidget(QGraphicsView):
    """

    """
    coordinates_changed = Signal(int, int)

    def __init__(self, view_type='axial', parent=None):
        super(CustomQOpenGLWidget, self).__init__()
        self.parent = parent
        self.view_type = view_type
        self.scene = QGraphicsScene(self)

        image_2d = np.zeros((150, 150), dtype="uint8")
        h, w = image_2d.shape
        bytes_per_line = 3 * w
        color_image = np.stack([image_2d]*3, axis=-1)
        qimage = QImage(color_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
        qimage = qimage.convertToFormat(QImage.Format_RGBA8888)
        self.map_transform = QTransform()
        # Equivalent to keep aspect ratio. Has to be recomputed everytime a new 3D volume is loaded
        scale_ratio = min((self.parent.size().width() / 2) / qimage.size().width(), (self.parent.size().height() / 2) / qimage.size().height())
        self.map_transform = self.map_transform.scale(scale_ratio, scale_ratio)
        self.inverse_map_transform, _ = self.map_transform.inverted()
        qimage = qimage.transformed(self.map_transform)
        self.pixmap = QPixmap.fromImage(qimage)
        # self.pixmap = self.pixmap.scaled(QSize(int(self.parent.size().width() / 2), int(self.parent.size().height() / 2)), Qt.KeepAspectRatio)
        self.image_item = QGraphicsPixmapItem(self.pixmap)
        self.scene.addItem(self.image_item)

        pen = QPen()
        pen.setColor(QColor(0, 0, 255))
        #self.line1 = self.scene.addLine(350, 0, 350, 400, pen)
        self.line1 = self.scene.addLine(int(self.pixmap.size().width()/2), 0, int(self.pixmap.size().width()/2), self.pixmap.size().height(), pen)
        self.line2 = self.scene.addLine(0, int(self.pixmap.size().height()/2), self.pixmap.size().width(), int(self.pixmap.size().height()/2), pen)
        self.setStyleSheet("QGraphicsView{background-color:rgb(0,0,0);}")
        self.setScene(self.scene)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.width_diff = int(self.parent.size().width() / 2) - self.pixmap.width()
        self.height_diff = int(self.parent.size().height() / 2) - self.pixmap.height()
        self.right_button_on_hold = False

        #
        # image_nib = nib.load("/media/dbouget/ihdb/Studies/Neuro/NeuroRADS/Article-Q1-2022/200_MR_T1_pre_311_typical_meningioma.nii.gz")
        # anno_nib = nib.load("/media/dbouget/ihdb/Data/Neuro3/1/200/segmentations/200_MR_T1_pre_311_label_tumor.nii.gz")
        # # image = image_nib.get_data()[:]
        # resampled_input_ni = resample_to_output(image_nib, (1.0, 1.0, 1.0), order=1)
        # image = resampled_input_ni.get_data()[:]
        # resampled_anno_ni = resample_to_output(anno_nib, (1.0, 1.0, 1.0), order=0)
        # anno = resampled_anno_ni.get_data()[:]
        # # self.input_volume = input_volume_ni.get_data()[:]
        # min_val = np.min(image)
        # max_val = np.max(image)
        # if (max_val - min_val) != 0:
        #     tmp = (image - min_val) / (max_val - min_val)
        #     image = tmp * 255.
        #
        # # data = np.ascontiguousarray(np.stack((image[:,:,150], image[:,:,150], image[:,:,150]), axis=0).transpose((1,2,0))).astype(("uint8"))
        # image_2d = image[:, :, 116].astype('uint8')
        # image_2d = rotate(image_2d, 90)
        # anno_2d = anno[:, :, 116].astype('uint8')
        # anno_2d[anno_2d == 1] = 255
        # anno_2d = rotate(anno_2d, 90)
        # h, w = image_2d.shape
        # bytes_per_line = 3 * w
        # color_image = np.stack([image_2d]*3, axis=-1)
        # qimage = QImage(color_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
        # # qimage = QImage(image_2d.data, w, h, w, QImage.Format_Grayscale8)
        # qimage = qimage.convertToFormat(QImage.Format_RGBA8888)
        # # img = img.convertToFormat(QImage.Format_ARGB32)
        # color_anno = np.stack([np.zeros(anno_2d.shape, dtype=np.uint8)] * 4, axis=-1)
        # color_anno[..., 0][anno_2d != 0] = 255.
        # color_anno[..., 3][anno_2d != 0] = 255.
        # qanno = QImage(color_anno.data, w, h, QImage.Format_RGBA8888)
        # # qanno = qanno.convertToFormat(QImage.Format_RGBA8888)
        #
        # self.pixmap = QPixmap.fromImage(qimage)
        # self.pixmap_anno = QPixmap.fromImage(qanno)
        # # data = np.zeros((250, 250, 3), dtype="uint8") #image[:, :, 150]
        # # qimage = QImage(data, data.shape[1], data.shape[0], QImage.Format_RGB888)
        # # self.pixmap = QPixmap(qimage)
        # self.pixmap = self.pixmap.scaled(QSize(int(self.parent.size().width() / 2), int(self.parent.size().height() / 2)), Qt.KeepAspectRatio)
        # self.pixmap_anno = self.pixmap_anno.scaled(QSize(int(self.parent.size().width() / 2), int(self.parent.size().height() / 2)), Qt.KeepAspectRatio)
        #
        # self.image_item = QGraphicsPixmapItem(self.pixmap)
        # self.anno_item = QGraphicsPixmapItem(self.pixmap_anno)
        # self.anno_item.setOpacity(0.5)
        # self.scene.addItem(self.image_item)
        # self.scene.addItem(self.anno_item)
        #
        # pen = QPen()
        # pen.setColor(QColor(0, 0, 255))
        # #self.line1 = self.scene.addLine(350, 0, 350, 400, pen)
        # self.line1 = self.scene.addLine(int(self.pixmap.size().width()/2), 0, int(self.pixmap.size().width()/2), self.pixmap.size().height(), pen)
        # self.line2 = self.scene.addLine(0, int(self.pixmap.size().height()/2), self.pixmap.size().width(), int(self.pixmap.size().height()/2), pen)
        # self.setStyleSheet("QGraphicsView{background-color:rgb(0,0,0);}")
        # self.setScene(self.scene)
        # self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        #
        # self.width_diff = int(self.parent.size().width() / 2) - self.pixmap.width()
        # self.height_diff = int(self.parent.size().height() / 2) - self.pixmap.height()
        # self.right_button_on_hold = False
        # # self.initializeGL()
        # # self.paintGL()

    # def initializeGL(self):
    #     """Set up the rendering context, define display lists etc."""
    #     glEnable(GL_DEPTH_TEST)
    #     # self.shape1 = self.make_shape()
    #     glEnable(GL_NORMALIZE)
    #     glClearColor(0.0, 0.0, 0.0, 1.0)
    #
    #
    # def paintGL(self):
    #     """draw the scene:"""
    #     image_nib = nib.load("/media/dbouget/ihdb/Studies/Neuro/NeuroRADS/Article-Q1-2022/200_MR_T1_pre_311_typical_meningioma.nii.gz")
    #     image = image_nib.get_data()[:]
    #     data = image[:, :, 150]
    #
    #     # create a buffer and bind it to the 'data' array
    #     self.bufferID = glGenBuffers(1)
    #     glBindBuffer(GL_ARRAY_BUFFER, self.bufferID)
    #     glBufferData(GL_ARRAY_BUFFER, data.nbytes, data, GL_DYNAMIC_DRAW)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.right_button_on_hold = True
            graphics_item_point = self.mapToScene(QPoint(event.localPos().x(), event.localPos().y()))
            self.__update_point_clicker_lines(graphics_item_point.x(), graphics_item_point.y())
            # max_dim_point = self.image_item.boundingRect()

            actual_x = graphics_item_point.x() # event.localPos().x() - int(self.width_diff / 2)
            # if event.localPos().x() - int(self.width_diff / 2) < 0:
            if actual_x < 0:
                actual_x = 0
            # elif event.localPos().x() >= self.pixmap.size().width(): # + int(self.width_diff / 2):
            elif actual_x >= self.pixmap.size().width():  # + int(self.width_diff / 2):
                actual_x = self.pixmap.size().width() - 1 # + int(self.width_diff / 2)
            # self.line1.setLine(actual_x, 0, actual_x, self.pixmap.size().height())

            actual_y = graphics_item_point.y() #event.localPos().y() - int(self.height_diff / 2)
            # if event.localPos().y() - int(self.height_diff / 2) < 0:
            if actual_y < 0:
                actual_y = 0
            #elif event.localPos().y() >= self.pixmap.size().height(): # + int(self.height_diff / 2):
            elif actual_y >= self.pixmap.size().height():  # + int(self.height_diff / 2):
                actual_y = self.pixmap.size().height() - 1#+ int(self.height_diff / 2)
            # self.line2.setLine(0, actual_y, self.pixmap.size().width(), actual_y)

            raw_actual_point = self.inverse_map_transform.map(graphics_item_point)
            actualy = raw_actual_point.y()
            # if self.view_type != 'axial':
            #     extremity_inv = self.inverse_map_transform.map(QPoint(self.pixmap.size().height(), self.pixmap.size().height()))
            #     actualy = extremity_inv.x() - raw_actual_point.y()
            # else:
            #     rawy = raw_actual_point.y()
            # self.coordinates_changed.emit(actual_x, actual_y)
            self.coordinates_changed.emit(raw_actual_point.x(), actualy)
            # print("Local pos: {}".format(event.localPos()))
            # print("MapToScene pos: {}".format(self.mapToScene(QPoint(event.localPos().x(), event.localPos().y()))))
            # print("Pixmap from scene pos: {}".format(self.image_item.mapFromScene(self.mapToScene(QPoint(event.localPos().x(), event.localPos().y()))).toPoint()))

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.right_button_on_hold = False

    def mouseMoveEvent(self, event):
        if self.right_button_on_hold:
            graphics_item_point = self.mapToScene(QPoint(event.localPos().x(), event.localPos().y()))

            self.__update_point_clicker_lines(graphics_item_point.x(), graphics_item_point.y())
            actual_x = graphics_item_point.x() # event.localPos().x() - int(self.width_diff / 2)
            #if event.localPos().x() - int(self.width_diff / 2) < 0:
            if actual_x < 0:
                actual_x = 0
            # elif event.localPos().x() >= self.pixmap.size().width() + int(self.width_diff / 2):
            elif actual_x >= self.pixmap.size().width():# + int(self.width_diff / 2):
                actual_x = self.pixmap.size().width() - 1  # + int(self.width_diff / 2)
            # self.line1.setLine(actual_x, 0, actual_x, self.pixmap.size().height())

            actual_y = graphics_item_point.y() # event.localPos().y() - int(self.height_diff / 2)
            # if event.localPos().y() - int(self.height_diff / 2) < 0:
            if actual_y < 0:
                actual_y = 0
            #elif event.localPos().y() >= self.pixmap.size().height() + int(self.height_diff / 2):
            elif actual_y >= self.pixmap.size().height():# + int(self.height_diff / 2):
                actual_y = self.pixmap.size().height() - 1  # + int(self.height_diff / 2)
            # self.line2.setLine(0, actual_y, self.pixmap.size().width(), actual_y)

            raw_actual_point = self.inverse_map_transform.map(graphics_item_point)
            actualy = raw_actual_point.y()
            # if self.view_type != 'axial':
            #     extremity_inv = self.inverse_map_transform.map(QPoint(self.pixmap.size().height(), self.pixmap.size().height()))
            #     actualy = extremity_inv.x() - raw_actual_point.y()
            # self.coordinates_changed.emit(actual_x, actual_y)
            self.coordinates_changed.emit(raw_actual_point.x(), actualy)

    def __update_point_clicker_lines(self, posx, posy):
        if posx < 0:
            posx = 0
        elif posx >= self.pixmap.size().width():
            posx = self.pixmap.size().width() - 1
        self.line1.setLine(posx, 0, posx, self.pixmap.size().height())

        if posy < 0:
            posy = 0
        elif posy >= self.pixmap.size().height():
            posy = self.pixmap.size().height() - 1
        # if self.view_type != 'axial':
        #     posy = self.pixmap.size().height() - posy
        self.line2.setLine(0, posy, self.pixmap.size().width(), posy)

    def update_slice_view(self, slice, x, y):
        # image_2d = rotate(slice, 90).astype('uint8')
        # if self.view_type == 'axial':
        image_2d = rotate(slice, 90).astype('uint8')
        image_2d = image_2d[:, ::-1]
        # image_2d = slice[:, ::-1].astype('uint8')
        # image_2d = slice.astype('uint8')
        h, w = image_2d.shape
        bytes_per_line = 3 * w
        color_image = np.stack([image_2d] * 3, axis=-1)
        qimage = QImage(color_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
        qimage = qimage.convertToFormat(QImage.Format_RGBA8888)
        scale_ratio = min((self.parent.size().width() / 2) / qimage.size().width(), (self.parent.size().height() / 2) / qimage.size().height())

        self.map_transform = QTransform()
        # self.map_transform = self.map_transform.translate(-int(self.pixmap.size().width() / 2), -int(self.pixmap.size().height() / 2))
        # self.map_transform = self.map_transform.translate(-int(self.size().width() / 2), -int(self.size().height() / 2))
        self.map_transform = self.map_transform * QTransform().scale(scale_ratio, scale_ratio)
        # if self.view_type == 'sagittal' or self.view_type == 'coronal':
        #     self.map_transform = self.map_transform * QTransform().rotate(90.)
        # else:
        #     self.map_transform = self.map_transform * QTransform().rotate(-90.)
        #self.map_transform = self.map_transform * QTransform().translate(int(self.pixmap.size().width() / 2), int(self.pixmap.size().height() / 2))
        # self.map_transform = self.map_transform * QTransform().translate(int(self.size().width() / 2), int(self.size().height() / 2))
        self.inverse_map_transform, _ = self.map_transform.inverted()
        qimage = qimage.transformed(self.map_transform)
        self.pixmap = QPixmap.fromImage(qimage)
        # self.pixmap = self.pixmap.scaled(QSize(int(self.parent.size().width() / 2), int(self.parent.size().height() / 2)), Qt.KeepAspectRatio)



        # self.map_transform = QTransform()
        # self.map_transform = self.map_transform.scale(scale_ratio, scale_ratio)
        # # self.map_transform = self.map_transform.translate(-int(self.pixmap.size().width()/2), -int(self.pixmap.size().height()/2))
        # # self.map_transform = self.map_transform.rotate(90., Qt.XAxis)
        # # self.map_transform = self.map_transform.translate(int(self.pixmap.size().width() / 2), int(self.pixmap.size().height() / 2))
        # self.inverse_map_transform, _ = self.map_transform.inverted()
        # # qimage = qimage.transformed(QTransform().translate(-int(self.pixmap.size().width()/2), -int(self.pixmap.size().height()/2)))
        # qimage = qimage.transformed(self.map_transform)
        # # qimage = qimage.transformed(QTransform().translate(int(self.pixmap.size().width() / 2), int(self.pixmap.size().height() / 2)))
        # self.pixmap = QPixmap.fromImage(qimage)
        # # self.pixmap = self.pixmap.scaled(QSize(int(self.parent.size().width() / 2), int(self.parent.size().height() / 2)), Qt.KeepAspectRatio)

        self.image_item.setPixmap(self.pixmap)
        graphics_point = self.map_transform.map(QPoint(x, y))
        # self.__update_point_clicker_lines(int(self.pixmap.size().width()/2), int(self.pixmap.size().height()/2))
        self.__update_point_clicker_lines(graphics_point.x(), graphics_point.y())

        # actualy = slice.shape[1] - y
        # adjx, adjy = rotate_custom(origin=[slice.shape[0]/2, slice.shape[1]/2], point=[x, actualy], angle=90)
        # graphics_point = self.map_transform.map(QPoint(adjx, adjy))
        # self.__update_point_clicker_lines(graphics_point.x(), graphics_point.y())


def rotate_custom(origin, point, angle):
    """
    Rotate a point counterclockwise by a given angle around a given origin.

    The angle should be given in radians.
    """
    import math
    ox, oy = origin
    px, py = point

    qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
    qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
    return qx, qy