import getopt, traceback
# macOS relevant
import os
from pathlib import PurePath
os.environ['LC_CTYPE'] = "en_US.UTF-8"
os.environ['LANG'] = "en_US.UTF-8"

# macOS Big Sur related: https://stackoverflow.com/questions/64818879/is-there-any-solution-regarding-to-pyqt-library-doesnt-work-in-mac-os-big-sur/64856281
os.environ['QT_MAC_WANTS_LAYER'] = '1'

# relevant for PySide, Qt stuff. See issue here: https://www.programmersought.com/article/8605863159/
import PySide2
dirname = os.path.dirname(PySide2.__file__)
plugin_path = os.path.join(dirname, 'plugins', 'platforms')
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path

import sys
from PySide2.QtWidgets import QApplication
from gui2.RaidionicsMainWindow import RaidionicsMainWindow
import logging


def main(argv):
    gui_usage = 1
    try:
        opts, args = getopt.getopt(argv, "hg:", ["gui=1"])
    except getopt.GetoptError:
        print('main.py')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('main.py')
            sys.exit()
        # elif opt in ("-g", "--use_gui"):
        #     gui_usage = int(arg)
    try:
        from utils.software_config import SoftwareConfigResources
        logging.basicConfig(filename=SoftwareConfigResources.getInstance().get_session_log_filename(), filemode='w')  # stream=sys.stdout
        logging.getLogger().setLevel(logging.DEBUG)
        if gui_usage == 1:
            app = QApplication(sys.argv)
            window = RaidionicsMainWindow(application=app)
            window.show()
            app.exec_()

            #@TODO. Windows-specific stuff to check.
            # # ifdef Q_OS_WIN //this is Windows specific code, not portable
            # QWindowsWindowFunctions::setWindowActivationBehavior(QWindowsWindowFunctions::AlwaysActivateWindow);
            # # endif
            # For mac, try: window.raise()
    except Exception as e:
        print('Process could not proceed. Caught error: {}'.format(e.args[0]))
        print('{}'.format(traceback.format_exc()))
        logging.critical(traceback.format_exc())


if __name__ == "__main__":
    main(sys.argv[1:])
