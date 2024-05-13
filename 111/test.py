from PyQt5.QtWidgets import QApplication
import sys
#from ui import MainWindow
#from controller import Controller
from curvesForm import CurvesForm

app = QApplication(sys.argv)
#w = MainWindow()
cf = CurvesForm()
#c = Controller(w,cf)

#main window
#w.show()
#curves window
cf.show()


sys.exit(app.exec())

