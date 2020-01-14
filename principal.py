import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic

qt_tela_inicial = "tela_principal.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qt_tela_inicial)


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        #CONFIG BOTOES
        self.btn_ingredientes_adicionar.pressed.connect(lambda: self.abrir_tela_adicionar('ingredientes'))
        self.btn_ingredientes_gerenciar.pressed.connect(lambda: self.abrir_tela_gerenciar('ingredientes'))

        self.btn_receitas_adicionar.pressed.connect(lambda: self.abrir_tela_adicionar('receitas'))
        self.btn_receitas_gerenciar.pressed.connect(lambda: self.abrir_tela_gerenciar('receitas'))

        self.btn_fabricacoes_adicionar.pressed.connect(lambda: self.abrir_tela_adicionar('fabricacoes'))
        self.btn_fabricacoes_gerenciar.pressed.connect(lambda: self.abrir_tela_gerenciar('fabricacoes'))

        self.btn_vendas_adicionar.pressed.connect(lambda: self.abrir_tela_adicionar('vendas'))
        self.btn_vendas_gerenciar.pressed.connect(lambda: self.abrir_tela_gerenciar('vendas'))

        #CONFIG ACTIONS
        self.action_ingredientes_adicionar.triggered.connect(lambda: self.abrir_tela_adicionar('ingredientes'))
        self.action_ingredientes_gerenciar.triggered.connect(lambda: self.abrir_tela_gerenciar('ingredientes'))

        self.action_receitas_adicionar.triggered.connect(lambda: self.abrir_tela_adicionar('receitas'))
        self.action_receitas_gerenciar.triggered.connect(lambda: self.abrir_tela_gerenciar('receitas'))

        self.action_fabricacoes_adicionar.triggered.connect(lambda: self.abrir_tela_adicionar('fabricacoes'))
        self.action_fabricacoes_gerenciar.triggered.connect(lambda: self.abrir_tela_gerenciar('fabricacoes'))

        self.action_vendas_adicionar.triggered.connect(lambda: self.abrir_tela_adicionar('vendas'))
        self.action_vendas_gerenciar.triggered.connect(lambda: self.abrir_tela_gerenciar('vendas'))

    def abrir_tela_adicionar(self, nomeTela):
        print('TROCAR PARA TELA ADICIONAR',str(nomeTela))
    
    def abrir_tela_gerenciar(self, nomeTela):
        print('TROCAR PARA TELA GERENCIAR',str(nomeTela))

    def txt_to_btn(self, texto):
        self.addButton.setText(texto)
    
    def list_to_btn(self):
        indexes = self.todoView.selectedIndexes()
        if indexes:
            # Indexes is a list of a single item in single-select mode.
            index = indexes[0]
            item_data = index.data(0)
            
            self.addButton.setText(item_data)

            # Clear the selection (as it is no longer valid).
            self.todoView.clearSelection()
    
    def add(self):
        """
        Add an item to our todo list, getting the text from the QLineEdit .todoEdit
        and then clearing it.
        """
        text = self.todoEdit.text()
        
        if text: # Don't add empty strings.
            # Access the list via the model.
            self.model.todos.append((False, text))
            # Trigger refresh.        
            self.model.layoutChanged.emit()
            # Empty the input
            self.todoEdit.setText("")

    def delete(self):
        indexes = self.todoView.selectedIndexes()
        if indexes:
            # Indexes is a list of a single item in single-select mode.
            index = indexes[0]
            # Remove the item and refresh.
            del self.model.todos[index.row()]
            self.model.layoutChanged.emit()
            # Clear the selection (as it is no longer valid).
            self.todoView.clearSelection()

    def complete(self):
        indexes = self.todoView.selectedIndexes()
        if indexes:
            index = indexes[0]
            row = index.row()
            status, text = self.model.todos[row]
            self.model.todos[row] = (True, text)
            # .dataChanged takes top-left and bottom right, which are equal 
            # for a single selection.
            self.model.dataChanged.emit(index, index)
            # Clear the selection (as it is no longer valid).
            self.todoView.clearSelection()



app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()