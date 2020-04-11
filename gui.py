import sys
from pathlib import Path
 
from qtpy.QtWidgets import QScrollArea, QPushButton, QPlainTextEdit, QApplication, QMainWindow, QAction, QMessageBox, QLabel 
from qtpy.QtGui import QIcon
from qtpy.QtCore import Slot 
import qtawesome as qta
import scraper as scraper
import tokenizer as tk
 
 
class VentanaPrincipal(QMainWindow):
    def __init__(self, parent=None ):
        QMainWindow.__init__(self, parent)
        self.setup_ui()
        self.show_home()

    def setup_ui(self):
        self.resize(500, 300)
        self.move(0, 0)
        self.setWindowTitle('Hola Mundo')
        ruta_icono =  Path('.', 'images', 'homepage.png')
        self.setWindowIcon(QIcon(str(ruta_icono)))
        self.statusBar().showMessage('Listo')
        self.setup_menu()

    def setup_menu(self):
        menubar = self.menuBar()

        file_menu = menubar.addMenu('&Archivo')

        refresh_action = QAction(qta.icon('fa5s.sync'),  '&Actualizar',  self) 
        refresh_action.setShortcut('Ctrl+A') 
        refresh_action.setStatusTip('Actualizando Base de Datos de Artículos....')
        refresh_action.triggered.connect( scraper.scrapeAll ) # Llamar al método de scrapper
        file_menu.addAction(refresh_action) 

        exit_action = QAction(qta.icon('fa5.times-circle'),  '&Salir',  self) 
        exit_action.setShortcut('Ctrl+Q') 
        exit_action.setStatusTip('Saliendo de la aplicación....')
        exit_action.triggered.connect( QApplication.instance().closeAllWindows ) 
        file_menu.addAction(exit_action) 


        help_menu = menubar.addMenu('&Ayuda') 
        about_action = QAction(qta.icon('fa5s.info-circle'), '&Acerca de',self) 
        about_action.setShortcut('Ctrl+I')
        about_action.setStatusTip('Acerca de...')
        about_action.triggered.connect( self.show_about_dialog) 
        help_menu.addAction(about_action)

    @Slot()
    def show_about_dialog(self): ## NUEVA LÍNEA
        msg_box = QMessageBox() 
        msg_box.setIcon(QMessageBox.Information) 
        msg_box.setText("Aplicación de Scrapper y búsqueda en 20 Minutos, El Mundo y El Pais \n\n por Ignacio Triguero y Alexey Zhelezov") 
        msg_box.setWindowTitle("Acerca de") 
        msg_box.setStandardButtons(QMessageBox.Close) 
        msg_box.exec_()

    def show_home(self):
        self.text_edit = QPlainTextEdit(self)
        self.text_edit.setFixedHeight(30)
        self.text_edit.setFixedWidth(400)
        self.text_edit.move(10,30)

        search_button = QPushButton(self)
        search_button.setFixedWidth(70)
        search_button.setText("Buscar")
        search_button.move(420, 30)
        search_button.clicked.connect(self.buscar)

        self.scroll_area = QScrollArea(self)
        self.scroll_area.move(10,70)
        self.scroll_area.setFixedSize(480, 200)

    def buscar(self):
        lista = tk.search(self.text_edit.toPlainText())
        for item in lista:
            print(f'{item["name"]} --- {item["distance"]}')
        #Aqui hay que meter los titulos de cada archivo en el {self.scroll_area} en una lista scrollable



def main():
 
    app = QApplication(sys.argv)
    w = VentanaPrincipal()
    w.show()
  
    sys.exit(app.exec_())

main()