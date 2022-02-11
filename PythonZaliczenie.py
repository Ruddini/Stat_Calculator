
import statistics as s
import sys
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QWidget, QDialog
from PyQt5.QtGui import QIcon, QPixmap, QFont
from PyQt5.QtWidgets import QLabel, QGridLayout, QPlainTextEdit
from PyQt5.QtWidgets import QLineEdit, QPushButton, QHBoxLayout
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import Qt
lista = []

class KalkStat(QWidget):
    
    def __init__(self, parent=None):
        super().__init__(parent)

        self.interface()
        

    def interface(self):

        # etykiety
        lb1 = QLabel("Podaj liczbę", self)
        lb2 = QLabel("Średnia arytmetyczna:", self)
        lb3 = QLabel("Mediana:", self)
        lb4 = QLabel("Wariancja:", self)
        lb5 = QLabel("Wpisane liczby:", self)
        lb5.setFont(QFont('Arial',12))
        lb5.setAlignment(Qt.AlignCenter)
        potw = QPushButton("&Dodaj liczbę", self)
        
        self.wpisane = QPlainTextEdit()
        self.wpisane.readonly = True
        

        # przypisanie widgetów do układu tabelarycznego
        tab = QGridLayout()
        tab.addWidget(lb1, 0, 0)
        tab.addWidget(lb2, 1, 0)
        tab.addWidget(lb3, 2, 0)
        tab.addWidget(lb4, 3, 0)
        tab.addWidget(lb5, 0, 4)
        tab.addWidget(potw, 0, 3)
        #tab.addWidget(self.wpisane, 1, 4)
        # 1-liniowe pola edycyjne
        self.liczby = QLineEdit()
        self.sred = QLineEdit()
        self.med = QLineEdit()
        self.war = QLineEdit()
        
        self.liczby.setToolTip('Wpisz dane')
        
        self.sred.readonly = True
        self.sred.setToolTip('Aby uzyskać wynik podaj dane')
        
        self.med.readonly = True
        self.med.setToolTip('Aby uzyskać wynik podaj dane')
        
        self.war.readonly = True
        self.war.setToolTip('Aby uzyskać wynik podaj dane')

        tab.addWidget(self.liczby, 0, 2)
        tab.addWidget(self.sred, 1, 2)
        tab.addWidget(self.med, 2, 2)
        tab.addWidget(self.war, 3, 2)

        # przyciski
        oblicz = QPushButton("&Oblicz", self)
        graf = QPushButton("&Pokaż reprezentację graficzną", self)
        czysc = QPushButton ("&Wyczyść wpisane dane", self)

        box = QHBoxLayout()
        box.addWidget(oblicz)
        box.addWidget(graf)

        tab.addLayout(box, 4, 0, 1, 5)
        
        box2 = QHBoxLayout()
        box2.addWidget(self.wpisane)
        
        tab.addLayout(box2, 1, 4, 3, 1)
        
        tab.addWidget(czysc, 5, 0, 1, 5)

        # przypisanie utworzonego układu do okna
        self.setLayout(tab)

        oblicz.clicked.connect(self.obliczenia)
        graf.clicked.connect(self.wykresy)
        potw.clicked.connect(self.dodaj)
        czysc.clicked.connect(self.czyszcz)
        
        self.liczby.setFocus()
        self.setGeometry(100, 100, 600, 400)
        self.setWindowIcon(QIcon('kalkulator.png'))
        self.setWindowTitle("Prosty kalkulator statystyczny")
        self.show()

    def koniec(self):
        self.close()


    def closeEvent(self, event):

        odp = QMessageBox.question(
            self, 'Komunikat',
            "Czy na pewno chcesz zamknąć kalkulator?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if odp == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

            
    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()
    
    def obliczenia(self):
        
        if len(lista)>0:
            a = s.mean(lista)
            ap = round(a,5)
            b = s.median(lista)
            bp = round(b,5)
            c = s.pvariance(lista)
            cp = round(c,5)
            self.sred.setText(str(ap))
            self.med.setText(str(bp))
            self.war.setText(str(cp))
        
        else:
            QMessageBox.warning(self, "Błąd", "Nie podałeś danych!", QMessageBox.Ok)
            

    def wykresy(self):
        x = []
        y = []
        
        sred1 = []
        sredl = s.mean(lista)
        
        med1 = []
        medl = s.median(lista)
        
        std1 = []
        std2 = []
        stdl = s.pstdev(lista)
        
        wynik1 = sredl-stdl
        wynik2 = stdl+sredl
        
        for i in range(len(lista)):
            y.append(lista[i])
            x.append(i)
            sred1.append(sredl)
            med1.append(medl)
            std1.append(wynik1)
            std2.append(wynik2)
            
        plt.figure(figsize = (17,6))
        plt.scatter(x, y, label = 'Wprowadzone dane', s = 200, color = 'green',
            alpha = 0.8, marker = '.', edgecolors='black')
        
        plt.plot(sred1, label = 'Średnia')
        
        if medl!=sredl:
            plt.plot(med1, label = 'Mediana', color = 'orange')
        
        plt.plot(std1, label = 'Zakres 2 odchyleń standardowych od sredniej', color = 'red' )
        plt.plot(std2, color = 'red')
        
        plt.xlabel('Numer wprowadzonej liczby', fontsize = 16)
        plt.ylabel('Warość danej liczby', fontsize = 16)

        plt.title('Graficzna reprezentacja podanych danych', fontsize = 16)
        plt.grid(axis = 'y')
        plt.grid(axis = 'x')
        plt.legend()
        plt.savefig("wykres")
        plt.show()
        plt.clf()
        
        self.b = okieneczko()
        self.b.show()
        
    def dodaj(self):
        try: 
            dane = float(self.liczby.text())

        except ValueError:
            QMessageBox.warning(self, "Błąd", "Podaj poprawnie liczbę", QMessageBox.Ok)
        
        else:
            lista.append(dane)
            self.wpisane.insertPlainText(self.liczby.text()+", ")
            self.liczby.clear()
            
    def czyszcz (self):
        lista.clear()
        self.sred.clear()
        self.med.clear()
        self.war.clear()
        self.wpisane.clear()
        
        
class okieneczko(QDialog):
    
    def __init__(self, parent=None):
        super().__init__()

        self.interface()
    
    def interface(self):

        pic = QLabel(self)
        pics = QPixmap("wykres.png")
        pic.setPixmap(pics)
        
        pic.show()
        self.resize(pics.width(),pics.height())
        
        self.setWindowTitle("Wizualizacja danych")
        self.show()
        
        

    def koniec(self):
        self.close()


    def closeEvent(self, event):

        odp = QMessageBox.question(
            self, 'Komunikat',
            "Zamknąć wykres?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if odp == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

            
    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()
        
            

if __name__ == '__main__':

    lstt = []
    app = QApplication(sys.argv)
    okno = KalkStat()
    sys.exit(app.exec_())
