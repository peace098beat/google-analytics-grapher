import sys
import os

print "---- HelloAnalytics_gui ----"
print __file__
print sys.argv[0]
print os.path.dirname(__file__)


from Ui_2 import *

# ------------------------------------------------ #
# matplotlib and PySide
# ------------------------------------------------ #
import matplotlib

matplotlib.rcParams['backend.qt4'] = 'PySide'
matplotlib.use('Qt4Agg')
# from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas

# ------------------------------------------------ #
# PySide
# ------------------------------------------------ #
from PySide.QtCore import *
from PySide.QtGui import *
# import matplotlib.pyplot as plt


# ------------------------------------------------ #
# user
# ------------------------------------------------ #
import pprint
from GoogleAnalyticsManager import initGoogleApis


###########################################
# sub function
###########################################

def print_results(results):
    # Print data nicely for the user.
    if results:
        import pprint
        pprint.pprint(results)

        print 'View (Profile): %s' % results.get('profileInfo').get('profileName')
        print 'result value: %s' % results.get('rows')[0][0]

    else:
        print 'No results found'


###########################################
# main function
###########################################
def getResults(service, profile_id, metrics, dimensions=None):
    results = service.data().ga().get(
        ids='ga:' + profile_id,
        start_date='2015-01-01',
        end_date='today',
        dimensions=dimensions,
        metrics=metrics).execute()
    return results


###########################################
# main window
###########################################
class MainWindow(QMainWindow, Ui_MainWindow):
    dataLoaded = Signal()

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.ga_email = None
        self.ga_key = None
        self.progressBar = QProgressBar()
        self.statusBar().addPermanentWidget(self.progressBar)

    @Slot()
    def changeGAEmail(self, email):
        self.ga_email = email
        print self.ga_email

    @Slot()
    def changeGAKey(self, key):
        self.ga_key = key
        print self.ga_key

    @Slot()
    def getAnaData(self):
        print 'getAnaData'
        self.statusbar.showMessage("Please wait .. getting goooogle analytics data")

        # ---- progress bar -----
        self.progressBar.setValue(20)
        # try:
        fname, filt = QFileDialog.getOpenFileName(self, 'Open file', '/home', 'Wave Files (*.wav);; All Files (*)')
        self.ga_key = fname

        service, profile_id = initGoogleApis(email=self.ga_email, keyfile=self.ga_key)
        # except:
        #     self.statusbar.showMessage("Error!!! Please check Email and keyfile....")
        #     return

        # ---- progress bar -----
        self.progressBar.setValue(50)

        results = getResults(service=service, profile_id=profile_id, metrics='ga:users, ga:sessions',
                             dimensions='ga:date')

        # ---- progress bar -----
        self.progressBar.setValue(80)

        r = results.get('rows')
        pprint.pprint(r)
        self.day = []
        self.users = []
        self.sessions = []
        for list in r:
            [a, b, session] = list
            self.day.append(int(a))
            self.users.append(int(b))
            self.sessions.append(int(session))

        # ---- progress bar -----
        self.progressBar.setValue(100)

        self.dataLoaded.emit()

        # ---- progress bar -----
        self.progressBar.reset()

    @Slot()
    def setDataForFigure(self):
        self.statusbar.showMessage("set Data For Figure analytics data")
        self.widget.update_figure(xdata=self.day, ydata=self.users)


if __name__ == "__main__":
    app = QApplication([])
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())
