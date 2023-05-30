from PyQt5.QtWidgets import QApplication

from gui import App

if __name__ == "__main__":
    # Create QApplication instance
    app = QApplication([])

    # Create App instance and show it
    host = "localhost"
    user = "erfan"
    password = "erfanmysql"
    database = "university"
    my_app = App(host, user, password, database)
    my_app.show()

    # Run the event loop
    app.exec_()
