from PyQt5.QtWidgets import QGraphicsView
from PyQt5.QtGui import QMouseEvent, QColor
from PyQt5.QtCore import *
import math
from MyItem import MyItem


class MyCanvas(QGraphicsView):
    """
    画布窗体类，继承自QGraphicsView，采用QGraphicsView、QGraphicsScene、QGraphicsItem的绘图框架
    """
    def __init__(self, *args):
        super().__init__(*args)
        self.main_window = None
        self.list_widget = None
        self.item_dict = {}
        self.selected_id = ''

        self.status = ''
        self.temp_algorithm = ''
        self.temp_id = ''
        self.temp_item = None
        self.temp_rect = None
        self.pen_color = Qt.black
        self.pen_width = 2
        self.last_x = 0
        self.last_y = 0
        self.flags = {'translate': False, 'rotate': False, 'scale': False, 'clip': False}

    def get_id(self):
        _id = str(len(self.item_dict) + 1)
        return _id

    def reset_canvas(self):
        self.status = ''
        self.temp_algorithm = ''
        self.temp_id = ''
        self.item_dict = {}
        self.temp_item = None

    def set_pen_color(self, c: QColor):
        self.pen_color = c

    def set_pen_width(self, w: int):
        self.pen_width = w

    def start_draw_line(self, algorithm):
        self.finish_draw()
        self.status = 'line'
        self.temp_algorithm = algorithm

    def start_draw_polygon(self, algorithm):
        self.finish_draw()
        self.status = 'polygon'
        self.temp_algorithm = algorithm

    def start_draw_ellipse(self):
        self.finish_draw()
        self.status = 'ellipse'

    def start_draw_curve(self, algorithm):
        self.finish_draw()
        self.status = 'curve'
        self.temp_algorithm = algorithm

    def start_translate(self):
        self.finish_draw()
        self.status = 'translate'

    def start_rotate(self):
        self.finish_draw()
        self.status = 'rotate'

    def start_scale(self):
        self.finish_draw()
        self.status = 'scale'

    def start_clip(self, algorithm):
        self.finish_draw()
        self.status = 'clip'
        self.temp_algorithm = algorithm

    def finish_draw(self):
        if self.status in ['line', 'ellipse', 'polygon', 'curve'] and self.temp_item is not None:
            self.list_widget.addItem(self.temp_id)
            self.item_dict[self.temp_id] = self.temp_item
        self.temp_item = None
        self.temp_id = self.get_id()

    def clear_selection(self):
        if self.selected_id != '':
            self.item_dict[self.selected_id].selected = False
            self.selected_id = ''

    def selection_changed(self, selected):
        self.main_window.statusBar().showMessage('图元选择： %s' % selected)
        if self.selected_id != '':
            self.item_dict[self.selected_id].selected = False
            self.item_dict[self.selected_id].update()
        self.selected_id = selected
        self.item_dict[selected].selected = True
        self.item_dict[selected].update()
        self.updateScene([self.sceneRect()])

    def mousePressEvent(self, event: QMouseEvent) -> None:
        pos = self.mapToScene(event.localPos().toPoint())
        x = int(pos.x())
        y = int(pos.y())
        if self.status == 'line':
            self.temp_item = MyItem(self.temp_id, self.status, [[x, y], [x, y]], self.pen_color, self.pen_width, self.temp_algorithm)
            self.scene().addItem(self.temp_item)
        elif self.status == 'ellipse':
            self.temp_item = MyItem(self.temp_id, self.status, [[x, y], [x, y]], self.pen_color, self.pen_width)
            self.scene().addItem(self.temp_item)
        elif self.status in ['polygon', 'curve']:
            if self.temp_item is None:
                self.temp_item = MyItem(self.temp_id, self.status, [[x, y]], self.pen_color, self.pen_width, self.temp_algorithm)
                self.scene().addItem(self.temp_item)
            else:
                if event.button() == Qt.RightButton:
                    self.finish_draw()
                    self.temp_item = None
                else:
                    self.temp_item.p_list.append([x, y])

        elif self.status in ['translate', 'rotate', 'scale'] and self.selected_id in self.item_dict:
            if not (self.status == 'rotate' and self.item_dict[self.selected_id].item_type == 'ellipse'):
                self.temp_id = self.selected_id
                self.temp_item = self.item_dict[self.temp_id]
                self.flags[self.status] = True
                self.last_x, self.last_y = x, y

        elif self.status == 'clip' and self.selected_id in self.item_dict and \
                self.item_dict[self.selected_id].item_type == 'line':
            self.temp_id = self.selected_id
            self.temp_item = self.item_dict[self.temp_id]
            self.flags['clip'] = True
            self.last_x, self.last_y = x, y
            self.temp_rect = MyItem(self.temp_id, 'rect', [[x, y], [x, y]], Qt.blue, 1)
            self.scene().addItem(self.temp_rect)

        self.updateScene([self.sceneRect()])
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        pos = self.mapToScene(event.localPos().toPoint())
        x = int(pos.x())
        y = int(pos.y())
        if self.status in ['line', 'ellipse']:
            self.temp_item.p_list[1] = [x, y]
        elif self.status == 'translate' and self.flags[self.status]:
            self.temp_item.translate(x - self.last_x, y - self.last_y)
            self.last_x, self.last_y = x, y
        elif self.status == 'rotate' and self.flags[self.status]:
            cx, cy = self.temp_item.get_center()
            theta = (math.atan2(y - cy, x - cx) - \
                    math.atan2(self.last_y - cy, self.last_x - cx)) * 180 / math.pi
            self.temp_item.rotate(theta)
            self.last_x, self.last_y = x, y
        elif self.status == 'scale' and self.flags[self.status]:
            cx, cy = self.temp_item.get_center()
            last_len = math.sqrt((self.last_x - cx) ** 2 + (self.last_y - cy) ** 2)
            now_len = math.sqrt((x - cx) ** 2 + (y - cy) ** 2)
            s = float(now_len / last_len)
            self.last_x, self.last_y = x, y
            self.temp_item.scale(s)
        elif self.status == 'clip' and self.flags[self.status]:
            self.temp_rect.p_list[1] = [x, y]

        self.updateScene([self.sceneRect()])
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        pos = self.mapToScene(event.localPos().toPoint())
        x = int(pos.x())
        y = int(pos.y())
        if self.status in ['line', 'ellipse']:
            self.finish_draw()
        elif self.status in ['translate', 'rotate', 'scale']:
            self.flags[self.status] = False
            self.finish_draw()
        elif self.status == 'clip':
            self.flags[self.status] = False
            self.temp_item.clip([[self.last_x, self.last_y], [x, y]], self.temp_algorithm)
            self.scene().removeItem(self.temp_rect)
            p_list = self.temp_item.p_list
            if p_list[0][0] == p_list[1][0] and p_list[0][1] == p_list[1][1]:
                self.scene().removeItem(self.temp_item)
            self.finish_draw()
        self.updateScene([self.sceneRect()])
        super().mouseReleaseEvent(event)
