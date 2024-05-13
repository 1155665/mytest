#for a better understand of this class
from rich import traceback
from controller import Controller
traceback.install()

from PyQt5.QtWidgets import QApplication
import sys
app = QApplication(sys.argv)

from curvesForm import CurvesForm

cf = CurvesForm()
Controller(None,cf)
cf.show()

sys.exit(app.exec())
