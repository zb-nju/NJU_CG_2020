from PyQt5.QtWidgets import (
    QMainWindow,
    qApp,
    QGraphicsScene,
    QListWidget,
    QHBoxLayout,
    QWidget,
    QColorDialog,
    QInputDialog
)
from MyCanvas import MyCanvas


class MainWindow(QMainWindow):
    """
    主窗口类
    """
    def __init__(self):
        super().__init__()
        self.item_cnt = 0

        # 使用QListWidget来记录已有的图元，并用于选择图元。注：这是图元选择的简单实现方法，更好的实现是在画布中直接用鼠标选择图元
        self.list_widget = QListWidget(self)
        self.list_widget.setMinimumWidth(200)

        # 使用QGraphicsView作为画布
        self.scene = QGraphicsScene(self)
        self.scene.setSceneRect(0, 0, 600, 600)
        self.canvas_widget = MyCanvas(self.scene, self)
        self.canvas_widget.setFixedSize(600, 600)
        self.canvas_widget.main_window = self
        self.canvas_widget.list_widget = self.list_widget

        # 设置菜单栏
        menubar = self.menuBar()
        file_menu = menubar.addMenu('文件')
        set_pen_menu = file_menu.addMenu('设置画笔')
        set_pen_color_act = set_pen_menu.addAction('设置画笔颜色')
        set_pen_width_act = set_pen_menu.addAction('设置画笔粗细')
        reset_canvas_act = file_menu.addAction('重置画布')
        exit_act = file_menu.addAction('退出')
        draw_menu = menubar.addMenu('绘制')
        line_menu = draw_menu.addMenu('线段')
        line_naive_act = line_menu.addAction('Naive')
        line_dda_act = line_menu.addAction('DDA')
        line_bresenham_act = line_menu.addAction('Bresenham')
        polygon_menu = draw_menu.addMenu('多边形')
        polygon_dda_act = polygon_menu.addAction('DDA')
        polygon_bresenham_act = polygon_menu.addAction('Bresenham')
        ellipse_act = draw_menu.addAction('椭圆')
        curve_menu = draw_menu.addMenu('曲线')
        curve_bezier_act = curve_menu.addAction('Bezier')
        curve_b_spline_act = curve_menu.addAction('B-spline')
        edit_menu = menubar.addMenu('编辑')
        translate_act = edit_menu.addAction('平移')
        rotate_act = edit_menu.addAction('旋转')
        scale_act = edit_menu.addAction('缩放')
        clip_menu = edit_menu.addMenu('裁剪')
        clip_cohen_sutherland_act = clip_menu.addAction('Cohen-Sutherland')
        clip_liang_barsky_act = clip_menu.addAction('Liang-Barsky')

        # 连接信号和槽函数
        exit_act.triggered.connect(qApp.quit)
        line_naive_act.triggered.connect(self.line_naive_action)
        line_dda_act.triggered.connect(self.line_dda_action)
        line_bresenham_act.triggered.connect(self.line_bresenham_action)
        polygon_dda_act.triggered.connect(self.polygon_dda_action)
        polygon_bresenham_act.triggered.connect(self.polygon_bresenham_action)
        ellipse_act.triggered.connect(self.ellipse_action)
        curve_b_spline_act.triggered.connect(self.curve_b_spline_action)
        curve_bezier_act.triggered.connect(self.curve_bezier_action)
        translate_act.triggered.connect(self.translate_action)
        rotate_act.triggered.connect(self.rotate_action)
        scale_act.triggered.connect(self.scale_action)
        clip_cohen_sutherland_act.triggered.connect(self.clip_cohen_sutherland_action)
        clip_liang_barsky_act.triggered.connect(self.clip_liang_barsky_action)
        set_pen_color_act.triggered.connect(self.set_pen_color_action)
        set_pen_width_act.triggered.connect(self.set_pen_width_action)
        reset_canvas_act.triggered.connect(self.reset_canvas_action)

        self.list_widget.currentTextChanged.connect(self.canvas_widget.selection_changed)

        # 设置主窗口的布局
        self.hbox_layout = QHBoxLayout()
        self.hbox_layout.addWidget(self.canvas_widget)
        self.hbox_layout.addWidget(self.list_widget, stretch=1)
        self.central_widget = QWidget()
        self.central_widget.setLayout(self.hbox_layout)
        self.setCentralWidget(self.central_widget)
        self.statusBar().showMessage('空闲')
        self.resize(600, 600)
        self.setWindowTitle('CG Demo')

    def line_naive_action(self):
        self.canvas_widget.start_draw_line('Naive')
        self.statusBar().showMessage('Naive算法绘制线段，按住鼠标左键并移动以绘制直线，松开以结束绘制')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()

    def line_dda_action(self):
        self.canvas_widget.start_draw_line('DDA')
        self.statusBar().showMessage('DDA算法绘制线段，按住鼠标左键并移动以绘制直线，松开以结束绘制')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()

    def line_bresenham_action(self):
        self.canvas_widget.start_draw_line('Bresenham')
        self.statusBar().showMessage('Bresenham算法绘制线段，按住鼠标左键并移动以绘制直线，松开以结束绘制')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()

    def polygon_dda_action(self):
        self.canvas_widget.start_draw_polygon('DDA')
        self.statusBar().showMessage('DDA算法绘制多边形，点击左键设置控制点，点击右键结束绘制')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()

    def polygon_bresenham_action(self):
        self.canvas_widget.start_draw_polygon('Bresenham')
        self.statusBar().showMessage('Bresenham算法绘制多边形，点击左键设置控制点，点击右键结束绘制')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()

    def ellipse_action(self):
        self.canvas_widget.start_draw_ellipse()
        self.statusBar().showMessage('中点圆生成算法绘制椭圆，按住鼠标左键并移动以绘制椭圆，松开以结束绘制')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()

    def curve_bezier_action(self):
        self.canvas_widget.start_draw_curve('Bezier')
        self.statusBar().showMessage('Bezier算法绘制曲线，点击左键设置控制点，点击右键结束绘制')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()

    def curve_b_spline_action(self):
        self.canvas_widget.start_draw_curve('B-spline')
        self.statusBar().showMessage('B-spline算法绘制曲线，点击左键设置控制点，点击右键结束绘制')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()

    def translate_action(self):
        self.canvas_widget.start_translate()
        self.statusBar().showMessage('按住鼠标左键并移动以平移图元，松开以结束平移')

    def rotate_action(self):
        self.canvas_widget.start_rotate()
        self.statusBar().showMessage('按住鼠标左键并移动以旋转图元，松开以结束旋转')

    def scale_action(self):
        self.canvas_widget.start_scale()
        self.statusBar().showMessage('按住鼠标左键并移动以缩放图元，松开以结束缩放')

    def clip_cohen_sutherland_action(self):
        self.canvas_widget.start_clip('Cohen-Sutherland')
        self.statusBar().showMessage('按住鼠标左键并移动以产生裁剪框，松开以裁剪线段')

    def clip_liang_barsky_action(self):
        self.canvas_widget.start_clip('Liang-Barsky')
        self.statusBar().showMessage('按住鼠标左键并移动以产生裁剪框，松开以裁剪线段')

    def set_pen_color_action(self):
        c = QColorDialog.getColor()
        self.canvas_widget.set_pen_color(c)

    def set_pen_width_action(self):
        w, ok = QInputDialog.getInt(self, '调整粗细', '输入画笔粗细', value=self.canvas_widget.pen_width)
        if ok and w:
            self.canvas_widget.set_pen_width(w)

    def reset_canvas_action(self):
        self.item_cnt = 0
        self.canvas_widget.reset_canvas()
        self.list_widget.currentTextChanged.disconnect(self.canvas_widget.selection_changed)
        self.list_widget.clear()
        self.list_widget.currentTextChanged.connect(self.canvas_widget.selection_changed)
        self.scene.clear()
