#!/usr/bin/env
"""
MarkdownViewer
* Description: MarkdownViewer is a simple Markdown file viewer written in
  Python. I wanted an easy way to view Markdown files, so I hacked this
  together...it isn't pretty, but it is functional. The view will be refreshed
  when the opened file is saved allowing you to use whatever editor you'd like
  and see the results immediately.

* Dependencies: PyQt4 and Markdown (the Python package).

* Usage: python MarkdownViewer.py <file>
  To automatically open a Markdown file with this viewer in Windows, associate
  the filetype with the included .bat file. You can apply themes by dropping
  your stylesheets in the stylesheets/ directory next to this script and
  selecting one from the Style menu.

* Note: Feel free to make improvements. Fork and send me a pull request.
  http://

* Links
 - PyQt4: http://www.riverbankcomputing.com/software/pyqt/download
 - Markdown (available via PIP): http://pypi.python.org/pypi/Markdown
 - Learn more about Markdown and the Markdown syntax here:
   http://daringfireball.net/projects/markdown/
 - Installed stylesheets from https://github.com/jasonm23/markdown-css-themes

Matthew Borgerson <mborgerson@gmail.com>
"""
import sys, time, os, markdown
from PyQt4 import QtCore, QtGui, QtWebKit

script_dir = os.path.dirname(os.path.realpath(__file__))
stylesheet_dir = os.path.join(script_dir, 'stylesheets/')
stylesheet_default = 'default.css'

class App(QtGui.QMainWindow):
    def __init__(self, parent=None, filename=''):
        QtGui.QMainWindow.__init__(self, parent)

        # Configure the window
        self.setGeometry(300, 300, 800, 600)
        self.setWindowTitle('MarkdownViewer')

        # Add the WebView control
        self.web_view = QtWebKit.QWebView()
        self.setCentralWidget(self.web_view)

        # Setup menu bar
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        exitAction = QtGui.QAction('E&xit', self)
        exitAction.setShortcut('ESC')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(QtGui.qApp.quit)
        fileMenu.addAction(exitAction)

        # Add style menu
        if os.path.exists(stylesheet_dir):
            default = ''
            sheets = []
            for f in os.listdir(stylesheet_dir):
                if not f.endswith('.css'): continue
                sheets.append(QtGui.QAction(f, self))
                if len(sheets) < 10:
                    sheets[-1].setShortcut('Ctrl+%d' % len(sheets))
                sheets[-1].triggered.connect(
                    lambda x, stylesheet=f: self.set_stylesheet(stylesheet))
            styleMenu = menubar.addMenu('&Style')
            for item in sheets:
                styleMenu.addAction(item)
            self.set_stylesheet(stylesheet_default)

        # Start the File Watcher Thread
        thread = WatcherThread(filename)
        self.connect(thread, QtCore.SIGNAL('update(QString)'), self.update)
        thread.start()

        self.update('')

    def update(self, text):
        self.web_view.setHtml(text)

    def set_stylesheet(self, stylesheet='default.css'):
        # QT only works when the slashes are forward??
        full_path = 'file://' + os.path.join(stylesheet_dir, stylesheet)
        full_path = full_path.replace('\\', '/')
        url = QtCore.QUrl(full_path)
        self.web_view.settings().setUserStyleSheetUrl(url)

class WatcherThread(QtCore.QThread):
    def __init__(self, filename):
        QtCore.QThread.__init__(self)
        self.filename = filename

    def __del__(self):
        self.wait()

    def run(self):
        last_modified = 0
        while True:
            current_modified = os.path.getmtime(self.filename)
            if last_modified != current_modified:
                last_modified = current_modified
                f = open(self.filename)
                html = markdown.markdown(f.read())
                f.close()
                self.emit(QtCore.SIGNAL('update(QString)'), html)
            time.sleep(0.5)

def main():
    if len(sys.argv) != 2: return
    app = QtGui.QApplication(sys.argv)
    test = App(filename=sys.argv[1])
    test.show()
    app.exec_()

if __name__ == '__main__':
    main()