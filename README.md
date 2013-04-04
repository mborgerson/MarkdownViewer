MarkdownViewer
==============
MarkdownViewer is a simple Markdown file viewer written in Python. I wanted an
easy way to view Markdown files, so I hacked this together...it isn't pretty,
but it is functional. The view will be refreshed when the opened file is saved,
allowing you to use whatever editor you'd like and see the results immediately.

Features
--------
* Cross platform
* Automatically updates when the file is changed
* CSS support

Dependencies
------------
* [Python](http://python.org/) 2.6 or 2.7
* [PyQt4](http://www.riverbankcomputing.com/software/pyqt/download)
* [Markdown Python Package](http://pypi.python.org/pypi/Markdown) (Available
  via PIP)

Usage
-----
```
$ python MarkdownViewer.py <file>
```

To automatically open a Markdown file with this viewer in Windows, associate
the filetype with the included .bat file. You can apply styles by dropping your
stylesheets in the stylesheets/ directory next to this script then selecting
one from the Style menu.

Contributing
------------
Feel free to make improvements. Fork and send me a pull request. Don't forget
to add your name to the Contributors section of this document.

Credit
------
The bundled default.css style came from here: [https://github.com/simonlc/Markdown-CSS](https://github.com/simonlc/Markdown-CSS).

More Info
---------
Learn more about Markdown and the Markdown syntax here: [http://daringfireball.net/pr
ojects/markdown/](http://daringfireball.net/projects/markdown/).

Unicode
-------
This tool supports UTF-8 encoded files (❍ ❑ ■ □ ☐ ▪ ▫ – — ≡ → ›). Consequently,
it also supports ASCII files.

License
-------
This program is free software; you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation; either version 2 of the License, or (at your option) any later
version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE.  See the GNU General Public License for more details.

Contributors
------------
Matthew Borgerson <mborgerson@gmail.com>
