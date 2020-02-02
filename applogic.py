from PyQt5.QtWidgets import QMainWindow, QWidget, QLabel, QPushButton
from PyQt5.QtCore import Qt, QPoint, pyqtSignal, QTimer, pyqtSlot
from PyQt5.QtGui import QFont, QImage, QPixmap, QPainter, QPen, QBrush


class Application(QMainWindow):
    def __init__(self, w, h, caption, scaled_w, scaled_h, net):
        self.w = w
        self.h = h
        self.scaled_w = scaled_w
        self.scaled_h = scaled_h
        self.caption = caption
        self.net = net

        super().__init__()
        self.setFixedSize(w, h)
        self.setWindowTitle(caption)

        self.canvas = Canvas(h, h, self)
        self.sidebar = SideBar(w - h, h, self, 'rgba(100,100,100,100%)',
                               self.canvas)

        self.show()


class Canvas(QWidget):
    def __init__(self, w, h, parent):
        self.w = w
        self.h = h
        self.app = parent

        super().__init__()

        self.setFixedSize(w, h)
        self.setParent(parent)
        self.setStyleSheet('background-color: rgba(0,0,0, 100%)')

        self.brush_color = Qt.black
        self.drawing = False
        self.brush_size = h / 10
        self.last_point = QPoint()

        self.image = QImage(w, h, QImage.Format_RGB32)
        self.image.fill(Qt.white)
        self.canvas = QLabel(self)
        self.canvas.setFixedSize(w, h)
        self.canvas.setPixmap(QPixmap.fromImage(self.image))
        self.canvas.show()

        self.show()

    def set_brush(self):
        self.brush_color = Qt.black

    def set_eraser(self):
        self.brush_color = Qt.white

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = True
            self.last_point = event.pos()
            painter = QPainter(self.image)
            painter.setPen(QPen(self.brush_color, 1,
                                Qt.SolidLine, Qt.RoundCap,
                                Qt.RoundJoin))
            painter.setBrush(QBrush(self.brush_color, Qt.SolidPattern))
            painter.drawEllipse(event.pos(), self.brush_size / 2,
                                self.brush_size / 2)
            self.redraw()

    def mouseMoveEvent(self, event):
        if (event.buttons() & Qt.LeftButton) & self.drawing:
            painter = QPainter(self.image)
            painter.setPen(QPen(self.brush_color, self.brush_size,
                                Qt.SolidLine, Qt.RoundCap,
                                Qt.RoundJoin))
            painter.drawLine(self.last_point, event.pos())
        self.last_point = event.pos()
        self.redraw()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = False

    def redraw(self):
        self.canvas.setPixmap(QPixmap.fromImage(self.image))

    def clear(self):
        self.image.fill(Qt.white)
        self.redraw()


class SideBar(QWidget):
    def __init__(self, w, h, parent, bg, canvas):
        self.w = w
        self.h = h
        self.bg = bg
        padding = 10
        self.canvas = canvas

        super().__init__()
        self.setParent(parent)
        self.setFixedSize(w, h)
        self.move(parent.w - w, 0)

        self.bg = QLabel(self)
        self.bg.setFixedSize(w, h)
        self.setStyleSheet('background-color: {}'.format(bg))
        self.bg.show()

        cap = QLabel(self)
        cap.setFixedSize(w - padding * 2, h / 6 - padding * 1.5)
        cap.move(padding, padding)
        cap.setText('DRAW LETTER & \nPRESS DONE!')
        cap.setStyleSheet('color: white')
        cap.setAlignment(Qt.AlignCenter)
        font = QFont()
        font.setBold(True)
        font.setPointSize(h / 6 / 4)
        cap.setFont(font)
        self.top_cap = cap
        self.top_cap.show()

        cap = QLabel(self)
        cap.setFixedSize(w - padding * 2, h / 3 - padding)
        cap.move(padding, h / 6 + padding * 0.5)
        cap.setText('W')
        cap.setStyleSheet('background-color: white')
        cap.setAlignment(Qt.AlignCenter)
        font = QFont()
        font.setBold(True)
        font.setPointSize(h / 3)
        cap.setFont(font)
        self.box = cap
        self.box.show()

        btn = QPushButton(self)
        btn.setFixedSize(w - padding * 2, h / 6 - padding)
        btn.move(padding, h / 2 + padding * 0.5)
        btn.setText('Mode : Training')
        btn.setStyleSheet('background-color: rgba(200,200,200,100%)')
        font = QFont()
        font.setBold(True)
        font.setPointSize(h / 6 / 5)
        btn.setFont(font)
        self.mode = btn
        self.mode.show()

        btn = QPushButton(self)
        btn.setFixedSize(w / 2 - padding * 1.5, h / 6 - padding)
        btn.move(padding, h / 3 * 2 + padding * 0.5)
        btn.setText('🖌')
        btn.setStyleSheet('background-color: rgba(200,200,200,100%)')
        font = QFont()
        font.setBold(True)
        font.setPointSize(h / 6 / 2)
        btn.setFont(font)
        btn.clicked.connect(self.canvas.set_brush)
        self.brush = btn
        self.brush.show()

        btn = QDoubleButton(self)
        btn.setFixedSize(w / 2 - padding * 1.5, h / 6 - padding)
        btn.move(w / 2 + padding * 0.5, h / 3 * 2 + padding * 0.5)
        btn.setText('⌫')
        btn.setStyleSheet('background-color: rgba(200,200,200,100%)')
        font = QFont()
        font.setBold(True)
        font.setPointSize(h / 6 / 1.5)
        btn.setFont(font)
        btn.clicked.connect(self.on_click)
        btn.doubleClicked.connect(self.on_double_click)
        self.eraser = btn
        self.eraser.show()

        btn = QPushButton(self)
        btn.setFixedSize(w - padding * 2, h / 6 - padding * 1.5)
        btn.move(padding, h / 6 * 5 + padding * 0.5)
        btn.setText('Done!')
        btn.setStyleSheet('background-color: rgba(200,200,200,100%)')
        font = QFont()
        font.setBold(True)
        font.setPointSize(h / 6 / 1.5)
        btn.setFont(font)
        self.done = btn
        self.done.show()

        self.show()

    @pyqtSlot()
    def on_click(self):
        self.canvas.set_eraser()

    @pyqtSlot()
    def on_double_click(self):
        self.canvas.clear()


class QDoubleButton(QPushButton):
    clicked = pyqtSignal()
    doubleClicked = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.clicked.emit)
        super().clicked.connect(self.checkDoubleClick)

    @pyqtSlot()
    def checkDoubleClick(self):
        if self.timer.isActive():
            self.doubleClicked.emit()
            self.timer.stop()
        else:
            self.timer.start(250)
