import sys
from PyQt5 import QtWidgets
from ADFGVX import ADFGVXApp
from ADFGX import ADFGXApp

class MainApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("ADFG(V)X Encryption Tool")
        self.resize(800, 720)

        # Centrální widget pro aplikace
        central_widget = QtWidgets.QStackedWidget()
        self.setCentralWidget(central_widget)

        # Inicializace aplikací ADFGVX a ADFGX
        self.adfgvx_app = ADFGVXApp()
        self.adfgvx_app.ui.tabWidget.setCurrentIndex(0)
        self.adfgvx_app.ui.tabWidget.removeTab(1)

        self.adfgx_app = ADFGXApp()
        self.adfgx_app.ui.tabWidget.setCurrentIndex(1)

        # Přidání obou aplikací do centrálního widgetu
        central_widget.addWidget(self.adfgvx_app)
        central_widget.addWidget(self.adfgx_app)

        # Tlačítka pro přepínání mezi ADFGVX a ADFGX
        switch_buttons = QtWidgets.QWidget()
        switch_layout = QtWidgets.QHBoxLayout()
        switch_buttons.setLayout(switch_layout)

        adfgvx_button = QtWidgets.QPushButton("ADFGVX")  # Tlačítko pro přepnutí na ADFGVX
        adfgvx_button.clicked.connect(lambda: central_widget.setCurrentWidget(self.adfgvx_app))

        adfgx_button = QtWidgets.QPushButton("ADFGX")  # Tlačítko pro přepnutí na ADFGX
        adfgx_button.clicked.connect(lambda: central_widget.setCurrentWidget(self.adfgx_app))

        switch_layout.addWidget(adfgvx_button)
        switch_layout.addWidget(adfgx_button)

        self.setMenuWidget(switch_buttons)  # Nastavení přepínače jako menu widgetu

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainApp()
    main_window.show()
    sys.exit(app.exec_())