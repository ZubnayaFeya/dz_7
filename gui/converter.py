from PyQt5 import uic


window = uic.loadUi('имя файла.ui')
Form, Base = uic.loadUiType('имя файла.ui', self)


if __name__ == '__main__':
    # pyuic5 ui_file.ui -o py_form.py