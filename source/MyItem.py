import cg_algorithms as alg
from typing import Optional
from PyQt5.QtWidgets import (
    QGraphicsItem,
    QWidget,
    QStyleOptionGraphicsItem)
from PyQt5.QtGui import QPainter, QPen, QColor
from PyQt5.QtCore import *


class MyItem(QGraphicsItem):
    """
    自定义图元类，继承自QGraphicsItem
    """
    def __init__(self, item_id: str, item_type: str, p_list: list, pen_color: QColor = Qt.black, pen_width: int = 2,
                 algorithm: str = '', parent: QGraphicsItem = None):
        """

        :param item_id: 图元ID
        :param item_type: 图元类型，'line'、'polygon'、'ellipse'、'curve'等
        :param p_list: 图元参数
        :param algorithm: 绘制算法，'DDA'、'Bresenham'、'Bezier'、'B-spline'等
        :param parent:
        """
        super().__init__(parent)
        self.id = item_id           # 图元ID
        self.item_type = item_type  # 图元类型，'line'、'polygon'、'ellipse'、'curve'等
        self.p_list = p_list        # 图元参数
        self.algorithm = algorithm  # 绘制算法，'DDA'、'Bresenham'、'Bezier'、'B-spline'等
        self.pen = QPen()
        self.pen.setColor(pen_color)
        self.pen.setWidth(pen_width)
        self.selected = False

    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: Optional[QWidget] = ...) -> None:
        painter.setPen(self.pen)
        if self.item_type == 'line':
            item_pixels = alg.draw_line(self.p_list, self.algorithm)
            for p in item_pixels:
                painter.drawPoint(*p)

        elif self.item_type == 'polygon':
            if len(self.p_list) > 1:
                print('start')
                item_pixels = alg.draw_polygon(self.p_list, self.algorithm)
                print('end')
                for p in item_pixels:
                    painter.drawPoint(*p)

        elif self.item_type == 'ellipse':
            x0, y0 = self.p_list[0]
            x1, y1 = self.p_list[1]

            item_pixels = alg.draw_ellipse([[min(x0, x1), max(y0, y1)], [max(x0, x1), min(y0, y1)]])
            for p in item_pixels:
                painter.drawPoint(*p)

        elif self.item_type == 'curve':
            item_pixels = alg.draw_curve(self.p_list, self.algorithm)
            for p in item_pixels:
                painter.drawPoint(*p)
            for p in self.p_list:
                painter.drawPoint(*p)

        elif self.item_type == 'rect':
            painter.drawRect(self.boundingRect())

        if self.selected:
            painter.setPen(QColor(255, 0, 0))
            painter.drawRect(self.boundingRect())

    def get_center(self):
        x_list = [p[0] for p in self.p_list]
        y_list = [p[1] for p in self.p_list]
        x = (max(x_list) + min(x_list)) / 2
        y = (max(y_list) + min(y_list)) / 2
        return [x, y]

    def translate(self, dx, dy):
        self.p_list = alg.translate(self.p_list, dx, dy)

    def rotate(self, a):
        cx, cy = self.get_center()
        self.p_list = alg.rotate(self.p_list, cx, cy, a)

    def scale(self, s):
        cx, cy = self.get_center()
        self.p_list = alg.scale(self.p_list, cx, cy, s)

    def clip(self, p_list, algorithm):
        xmin = min(p_list[0][0], p_list[1][0])
        ymin = min(p_list[0][1], p_list[1][1])
        xmax = max(p_list[0][0], p_list[1][0])
        ymax = max(p_list[0][1], p_list[1][1])
        self.p_list = alg.clip(self.p_list, xmin, ymin, xmax, ymax, algorithm)

    def boundingRect(self) -> QRectF:
        if self.item_type in ['line', 'ellipse', 'rect']:
            x0, y0 = self.p_list[0]
            x1, y1 = self.p_list[1]
            x = min(x0, x1)
            y = min(y0, y1)
            w = max(x0, x1) - x
            h = max(y0, y1) - y
            return QRectF(x - 1, y - 1, w + 2, h + 2)
        elif self.item_type in ['polygon', 'curve']:
            if len(self.p_list) == 0:
                return QRectF(0, 0, 0, 0)
            if len(self.p_list) < 2:
                x0, y0 = self.p_list[0]
                return QRectF(x0 - 1, y0 - 1, x0 + 1, y0 + 1)
            x_list = []
            y_list = []
            for [x0, y0] in self.p_list:
                x_list.append(x0)
                y_list.append(y0)
            x = min(x_list)
            y = min(y_list)
            w = max(x_list) - x
            h = max(y_list) - y
            return QRectF(x - 1, y - 1, w + 2, h + 2)

