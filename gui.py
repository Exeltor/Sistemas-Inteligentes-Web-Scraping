import sys, qtpy.QtCore, qtpy.QtGui, json, os
 
from qtpy.QtWidgets import QGroupBox, QFormLayout, QVBoxLayout, QWidget, QScrollArea, QPushButton, QPlainTextEdit, QApplication, QMainWindow, QAction, QMessageBox, QLabel, QDialog, QFileDialog 
from qtpy.QtGui import QIcon
from qtpy.QtCore import Slot
import qtawesome as qta
import scraper as scraper
from qtpy import QtCore
import procesador as procesador
 
class VentanaPrincipal(QMainWindow):
    def __init__(self, parent=None ):
        QMainWindow.__init__(self, parent)
        self.setup_ui()
        self.show_home()

    def setup_ui(self):
        self.resize(580, 200)
        self.setFixedHeight(140)
        self.setFixedWidth(580)
        self.move((1920/2) - (500/2), (1080/2) - (200/2))
        self.setWindowTitle('Buscador')
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
        labelBusqueda = QLabel('Tu busqueda', self)
        labelBusqueda.move(10, 25)
        self.text_edit = QPlainTextEdit(self)
        self.text_edit.setFixedHeight(30)
        self.text_edit.setFixedWidth(400)
        self.text_edit.move(10,60)
        
        labelnum = QLabel('Numero de articulos', self)
        labelnum.move(420, 25)
        labelnum.setFixedWidth(150)
        self.text_edit_num = QPlainTextEdit("5", self)
        self.text_edit_num.setFixedHeight(30)
        self.text_edit_num.setFixedWidth(150)
        self.text_edit_num.move(420,60)
        

        search_button = QPushButton(self)
        search_button.setFixedWidth(70)
        search_button.setText("Buscar")
        search_button.move(500, 100)
        search_button.clicked.connect(self.buscar)

        openDirButton = QPushButton(self)
        openDirButton.setFixedWidth(110)
        openDirButton.setText("Abrir Directorio")
        openDirButton.move(380, 100)
        openDirButton.clicked.connect(self.getFile)

    def getfile(self):
        fname = QFileDialog.getOpenFileName(self, "Open Image", "/home")
        Dialog = QDialog()
       # self.reject()
        ui = Noticia_Dialog(Dialog)
        ui.setupUi(fname)

    def getFile(self):
        dialog = FileDialog()

        

    def buscar(self):
        # abrir dialogo carga aqui
        lista = procesador.search(self.text_edit.toPlainText(), self.text_edit_num.toPlainText())
        # cerrar
        self.abrirVentanaLista(lista, self.text_edit.toPlainText())
            #Aqui hay que meter los titulos de cada archivo en el {self.scroll_area} en una lista scrollable

    def abrirVentanaLista(self, lista, query):
        Dialog = QDialog()
        ui = Ui_Dialog(Dialog)
        ui.setupUi(lista, query)

class FileDialog(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'Explorador de noticias'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        
        self.openFileNameDialog()
        
        self.show()
    
    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"Elige tu archivo", "","Text Files (*.txt)", options=options)
        if fileName:
            Dialog = QDialog()
            ui = Noticia_Dialog(Dialog)
            ui.setupUi(fileName)


class Ui_Dialog(QDialog):
    def __init__(self, parent):
        QDialog.__init__(self, parent)

    def setupUi(self, lista, query):
        
        formLayout = QFormLayout()
        groupBox = QGroupBox(f"Resultado de la búsqueda: {query}")
        labelLis = []
        comboList = []
        for i in range(len(lista)):
            
            f = open(lista[i]['name'], 'r', encoding='utf-8')
            jsonData = json.loads(f.read())
            f.close()
            labelLis.append(QLabel(f'{jsonData["title"]} --- {round(float(lista[i]["distance"])*100, 2)}% --- {jsonData["categoria"]}'))
            buttonOpen = QPushButton("Abrir noticia")
            buttonOpen.clicked.connect(self.make_openFile(lista[i]["name"]))
            comboList.append(buttonOpen)
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
            self.reject()
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
        tags = ""
        for tag in jsonData["tags"]:
            tags += tag + " | "
        f.close()
        textArea = QPlainTextEdit(noticia, self)
        textArea.setReadOnly(True)
        textArea.move(10,60)
        textArea.setFixedSize(1200, 600)
        labelTit = QLabel(titulo, self)
        labelTit.move(10, 30)
        labelFecha = QLabel(fecha, self)
        labelFecha.move(10, 670)
        labelTags = QLabel(tags[:-3], self)
        labelTags.move(300, 670)
        buttonSearchSim = QPushButton("Buscar noticias similares (text)", self)
        buttonSearchSim.move(1000, 30)
        buttonSearchSim.clicked.connect(self.make_searchSim(path))
        buttonTagsSim = QPushButton("Buscar noticias similares (tags)", self)
        buttonTagsSim.move(1000, 5)
        buttonTagsSim.clicked.connect(self.make_tagsSim(path))
        self.setWindowTitle("Texto de la noticia")
        self.setMinimumSize(1220, 705)
        self.show()
        self.exec_()

    def make_searchSim(self, path):
        def searchSim():
            self.reject()
            Dialog = QDialog()
            file = open(path,"r", encoding="utf8", errors='ignore')
            jsonContent = json.loads(file.read().strip())
            file.close()
            lista = procesador.search(str(jsonContent["noticia"]))
            ui = Ui_Dialog(Dialog)
            ui.setupUi(lista, path)
        return searchSim

    def make_tagsSim(self, path):
        def tagsSim():
            self.reject()
            Dialog = QDialog()
            file = open(path,"r", encoding="utf8", errors='ignore')
            jsonContent = json.loads(file.read().strip())
            file.close()
            lista = procesador.similaritiesTAGS(str(jsonContent["tags"]))
            ui = Ui_Dialog(Dialog)
            ui.setupUi(lista, path)
        return tagsSim
def main():
 
    app = QApplication(sys.argv)
    w = VentanaPrincipal()
    w.show()
  
    sys.exit(app.exec_())

main()