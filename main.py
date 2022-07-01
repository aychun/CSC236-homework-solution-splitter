"""
Ensure that the latest version of PyPDF2 package is installed.
You may use, share, or modify the files freely.

All the testings were done ONLY on a MacOS and the users are responsible for any type of unexpected bugs or errors.

Written by Andrew Yooeun Chun <https://github.com/aychun>
2022/July/01
"""

import pkg_resources
import gui

dependencies = ["PyPDF2>=1.27.5"]

if __name__ == "__main__":
    pkg_resources.require(dependencies)

    gui.showMenu()
