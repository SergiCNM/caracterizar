from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

class CircularProgress(QWidget):
	def __init__(self):
		QWidget.__init__(self)

		#custom properties
		self.value = 0
		self.width = 200
		self.height = 200
		self.progress_width = 10
		self.progress_rounded_cap = True
		self.max_value = 100
		self.progress_color = 0xff79c6 #QColor(233, 220, 150)
		# Text
		self.enable_text = True
		self.font_family = "Segoe UI"
		self.font_size = 12
		self.suffix = "%"
		self.text_color = 0xff79c6
		#self.enable_shadow = True
		# BG
		self.enable_bg = True
		self.bg_color = 0x44475a

		# set default size without layout
		self.resize(self.width, self.height)

	def add_shadow(self,enable):
		if enable:
			self.shadow = QGraphicsDropShadowEffect(self)
			self.shadow.setBlurRadius(15)
			self.shadow.setXOffset(0)
			self.shadow.setYOffset(0)
			self.shadow.setColor(QColor(0, 0 , 0, 120))
			self.setGraphicsEffect(self.shadow)



	def set_value(self, value):
		self.value = value
		self.repaint() # Render progress bar after change value

	# Paint event (design your circular progress here)
	def paintEvent(self, e):
		# set progress parameters
		width = self.width - self.progress_width
		height = self.height - self.progress_width
		margin = self.progress_width / 2
		value = self.value * 360 / self.max_value

		# painter
		paint = QPainter()
		paint.begin(self)
		paint.setRenderHint(QPainter.Antialiasing) # remove pixelated edges
		paint.setFont(QFont(self.font_family, self.font_size))

		# create rectangle
		rect = QRect(0, 0, self.width, self.height)
		paint.setPen(Qt.NoPen)
		paint.drawRect(rect)

		# add pend
		pen = QPen()
		#pen.setColor(QColor(self.progress_color))
		pen.setWidth(self.progress_width)
		# Set Round Cap
		if self.progress_rounded_cap:
			pen.setCapStyle(Qt.RoundCap)

		# enable BG
		if self.enable_bg:
			pen.setColor(QColor(self.bg_color))
			paint.setPen(pen)
			paint.drawArc(margin, margin, width, height, 0, 360*16)

		# Create ARC / Circular progress
		pen.setColor(QColor(self.progress_color))
		paint.setPen(pen)
		paint.drawArc(margin, margin, width, height, -90 * 16, -value * 16) # Ark 360º is equal to 360*6 in the Qt, or 5760 / 16

		# Create text
		pen.setColor(QColor(self.text_color))
		paint.setPen(pen)
		paint.drawText(rect, Qt.AlignCenter, f"{self.value}{self.suffix}")

		# end
		paint.end()

