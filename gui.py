import sys
from pathlib import Path
 
from qtpy.QtWidgets import QGroupBox, QFormLayout, QVBoxLayout, QWidget, QScrollArea, QPushButton, QPlainTextEdit, QApplication, QMainWindow, QAction, QMessageBox, QLabel, QDialog 
from qtpy.QtGui import QIcon
from qtpy.QtCore import Slot
import qtpy.QtCore, qtpy.QtGui
import qtawesome as qta
import scraper as scraper
import tokenizer as tk
from qtpy import QtCore, QtWidgets
import json
import os
 
 
class VentanaPrincipal(QMainWindow):
    def __init__(self, parent=None ):
        QMainWindow.__init__(self, parent)
        self.setup_ui()
        self.show_home()

    def setup_ui(self):
        self.resize(500, 100)
        self.move((1920/2) - (500/2), (1080/2) - (100/2))
        self.setWindowTitle('Buscador')
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
        self.text_edit.move(10,40)

        search_button = QPushButton(self)
        search_button.setFixedWidth(70)
        search_button.setText("Buscar")
        search_button.move(420, 40)
        search_button.clicked.connect(self.buscar)
        

    def buscar(self):
        # abrir dialogo carga aqui
        lista = tk.search(self.text_edit.toPlainText())
        # cerrar
        self.abrirVentanaLista(lista)
            #Aqui hay que meter los titulos de cada archivo en el {self.scroll_area} en una lista scrollable

    def abrirVentanaLista(self, lista):
        Dialog = QDialog()
        ui = Ui_Dialog(Dialog)
        ui.setupUi(lista)

class Ui_Dialog(QDialog):
    def __init__(self, parent):
        QDialog.__init__(self, parent)

    def setupUi(self, lista):
        
        formLayout = QFormLayout()
        groupBox = QGroupBox("Resultado de la búsqueda")
        labelLis = []
        comboList = []
        for i in range(len(lista)):
            f = open(lista[i]['name'], 'r', encoding='utf-8')
            jsonData = json.loads(f.read())
            f.close()
            labelLis.append(QLabel(f'{jsonData["title"]} --- {lista[i]["distance"]}'))
            button = QPushButton("Abrir noticia")
            button.clicked.connect(self.make_openFile(lista[i]["name"]))
            comboList.append(button)
            formLayout.addRow(labelLis[i], comboList[i])
        groupBox.setLayout(formLayout)
        scroll = QScrollArea(self)
        scroll.setWidget(groupBox)
        scroll.setWidgetResizable(True)
        scroll.setMinimumHeight(600)
        scroll.setMinimumWidth(1200)
        layout = QVBoxLayout(self)
        layout.addWidget(scroll)
        self.setWindowTitle("Noticias")
        self.resize(1200, 600)

        self.show()
        self.exec_()

    def make_openFile(self, path):
        def openFile():
            Dialog = QDialog()
            ui = Noticia_Dialog(Dialog)
            ui.setupUi(path)
        return openFile
        

class Noticia_Dialog(QDialog):
    def __init__(self, parent):
        QDialog.__init__(self, parent)

    def setupUi(self, path):
        f = open(path, 'r', encoding='utf-8')
        jsonData = json.loads(f.read())
        noticia = jsonData["noticia"]
        titulo = jsonData["title"]
        fecha = jsonData["fecha"]
        f.close()
        textArea = QPlainTextEdit(noticia, self)
        textArea.setReadOnly(True)
        textArea.move(10,50)
        textArea.setFixedSize(1200, 600)
        labelTit = QLabel(titulo, self)
        labelTit.move(10, 20)
        labelFecha = QLabel(fecha, self)
        labelFecha.move(10, 670)
        self.setWindowTitle("Texto de la noticia")
        self.setMinimumSize(1220, 700)
        self.show()
        self.exec_()

def main():
 
    app = QApplication(sys.argv)
    w = VentanaPrincipal()
    w.show()
  
    sys.exit(app.exec_())

main()