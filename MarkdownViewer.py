#!/usr/bin/env
"""Simple Markdown file viewer."""
# Copyright (C) 2013 Matthew Borgerson <mborgerson@gmail.com>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
import codecs, sys, time, os, markdown
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
                f = codecs.open(self.filename, encoding='utf-8')
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
