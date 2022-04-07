import sys
from PyQt5.QtWidgets import (QApplication,  QLineEdit, QVBoxLayout, QListView, QWidget, QMessageBox,)
from PyQt5.QtCore import Qt, QSortFilterProxyModel
from PyQt5.QtGui import QStandardItemModel, QStandardItem
import pandas as pd
from dados import quizzDate


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Foxy Quizz")
        self.resize(1000, 800)
        #dados
        date = quizzDate()

        pf = pd.DataFrame(date)
        
        model = QStandardItemModel(0, 1)
        view = QListView()

        # Filtro
        filter_proxy_model = QSortFilterProxyModel()
        filter_proxy_model.setSourceModel(model)
        filter_proxy_model.setFilterCaseSensitivity(Qt.CaseInsensitive)
        filter_proxy_model.setFilterKeyColumn(0)
        view.setModel(filter_proxy_model)
        #Logica
        for question, status in zip(pf["Perguntas"], pf["Respostas"]):
            item = QStandardItem(question)
            self.setStyleSheet('font-size: 16px; background-color: rgb(35, 35, 35); ')
            item.setForeground(Qt.green if status else Qt.red)
            item.setEditable(False)
            model.appendRow(item)

        search_box = QLineEdit()
        search_box.setStyleSheet('color: white;')
        search_box.textChanged.connect(filter_proxy_model.setFilterRegExp)
        mainlayout = QVBoxLayout(self)
        mainlayout.addWidget(search_box)
        mainlayout.addWidget(view)

    
    def closeEvent(self, e):
        e.ignore()
        question_close = QMessageBox.question(self, "Fechamento", "Deseja realmente fechar a aplicação?",
                                              QMessageBox.Yes, QMessageBox.No)
        if question_close == QMessageBox.Yes:
            exit(0)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    demo = MainWindow()
    demo.show()

    sys.exit(app.exec_())
