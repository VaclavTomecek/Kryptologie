import string
import random
import sys
from unidecode import unidecode
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication
from ADFGVX_ADFGX_ui import Ui_ADFGVX
import json

SPACE_HOLDER = "XMEZERAX"

'''
number_mapping = {
    "0": "NULA",
    "1": "JEDNA",
    "2": "DVA",
    "3": "TRI",
    "4": "CTYRI",
    "5": "PET",
    "6": "SEST",
    "7": "SEDM",
    "8": "OSM",
    "9": "DEVET"
}

reverse_number_mapping = {v: k for k, v in number_mapping.items()}
'''

def odstranit_diakritiku_a_spec_znaky(text):
    # Odstraní diakritiku z textu a převede jej na velká písmena.
    text = unidecode(text)
    text = text.upper()
    return ''.join(SPACE_HOLDER if c == ' ' else c for c in text if c in (string.ascii_uppercase + string.digits + ' '))

def obnovit_mezery(text):
    return text.replace(SPACE_HOLDER, ' ')

def rozdel_do_skupin(text, key):
    # Rozdělí text na skupiny znaků podle délky klíče.
    # Pokud je délka klíče nulová, vyvolá chybu.
    velikost = len(key)
    if velikost == 0:
        raise ValueError("Klíč pro rozdělení skupin nesmí být prázdný.")
    text = text.replace(" ", "").strip()
    skupiny = [text[i:i + velikost] for i in range(0, len(text), velikost)]
    return ' '.join(skupiny)

def vytvorit_adfgvx_matici():
    # Vytvoří náhodně zamíchanou šifrovací matici ADFGVX.
    alphabet = list(string.ascii_uppercase) + list(string.digits)
    random.seed()
    random.shuffle(alphabet)
    adfgvx_matrix = [["X" for _ in range(7)] for _ in range(7)]  # Inicializace prázdné matice 7x7
    characters = 'ADFGVX'
    for i in range(6):
        adfgvx_matrix[0][i + 1] = characters[i]
        adfgvx_matrix[i + 1][0] = characters[i]
    for i in range(1, 7):
        for j in range(1, 7):
            if alphabet:
                adfgvx_matrix[i][j] = alphabet.pop(0)
    return adfgvx_matrix

def najit_pozici_v_matici(matrix, char):
    # Najde pozici znaku v matici ADFGVX a vrátí jeho odpovídající znaky z hlavičky matice (řádku a sloupce).
    for i in range(1, len(matrix)):
        for j in range(1, len(matrix[i])):
            if matrix[i][j] == char:
                return matrix[0][i], matrix[j][0]
    return None

def transpozice_sloupcu(text, key):
    # Provede transpozici textu na základě klíče
    col_count = len(key)  # Počet sloupců odpovídá délce klíče
    grid = ['' for _ in range(col_count)]
    for i in range(len(text)):
        grid[i % col_count] += text[i]
    key_index = sorted(range(len(key)), key=lambda k: key[k])  # Seřadí klíč podle abecedy
    return ''.join(grid[i] for i in key_index)

def zpetna_transpozice_sloupcu(text, key):
    # Provede zpětnou transpozici textu na základě klíče.
    col_count = len(key)
    row_count = len(text) // col_count
    extra_chars = len(text) % col_count
    key_index = sorted(range(len(key)), key=lambda k: key[k])
    col_lengths = [row_count + (1 if i < extra_chars else 0) for i in range(col_count)]
    grid = [''] * col_count
    index = 0
    for i in range(col_count):  # Naplní sloupce textem
        col_length = col_lengths[key_index[i]]
        grid[key_index[i]] = text[index:index + col_length]
        index += col_length
    original_text = ''
    for r in range(row_count + 1):  # Rekonstrukce textu z mřížky
        for c in range(col_count):
            if r < len(grid[c]):
                original_text += grid[c][r]
    return original_text

def adfgvx_sifrovat(text, key, matrix):
    # Provede šifrování textu pomocí matice ADFGVX a klíče.
    zasifrovany_text = ''
    for char in text:  # Najde pozice všech znaků v matici
        pozice = najit_pozici_v_matici(matrix, char)
        if pozice:
            zasifrovany_text += pozice[0] + pozice[1]
        else:
            raise ValueError(f"Znak '{char}' není v matici.")
    zasifrovany_text = transpozice_sloupcu(zasifrovany_text, key)
    return rozdel_do_skupin(zasifrovany_text, key)

def adfgvx_desifrovat(transposed_text, key, matrix):
    # Provede dešifrování textu pomocí matice ADFGVX a klíče.
    desifrovany_text = ''
    line = "ADFGVX"
    for i in range(0, len(transposed_text), 2):  # Zpracovává text po dvou znacích (odpovídajících řádku a sloupci)
        row_char = transposed_text[i]
        col_char = transposed_text[i + 1]
        try:
            row_index = line.index(row_char) + 1
            col_index = line.index(col_char) + 1
            decoded_char = matrix[row_index][col_index]  # Dekóduje znak na této pozici
            desifrovany_text += decoded_char
        except ValueError:
            desifrovany_text += '?'
    return obnovit_mezery(desifrovany_text)



'''
# Vstupy od uživatele
text = input("Zadejte text k zašifrování: ")
key = input("Zadejte klíč: ")

# Generování matice
matrix = vytvorit_adfgvx_matici()

# Šifrování a dešifrování
preprocessed_text = odstranit_diakritiku_a_spec_znaky(text)
zasifrovano = adfgvx_sifrovat(preprocessed_text, key, matrix)
desifrovano = adfgvx_desifrovat(zasifrovano, key, matrix)

print("Zašifrovaný text:", zasifrovano)
print("Dešifrovaný text:", desifrovano)'''


class ADFGVXApp(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.ui = Ui_ADFGVX()
        self.ui.setupUi(self)

        # Inicializace proměnné pro šifrovací matici (zatím prázdná)
        self.matrix = None  # Matice se nastaví ručně nebo tlačítkem

        # Připojení tlačítek k funkcím
        self.ui.Generace_Matice.clicked.connect(self.generovat_matici)
        self.ui.Zasifrovat_Button.clicked.connect(self.zasifrovat)
        self.ui.Desifrovat_Button.clicked.connect(self.desifrovat)
        self.ui.stahnout_matici.clicked.connect(self.stahnout_matici)
        self.ui.nahrat_matici.clicked.connect(self.nahrat_matici)
        self.ui.Prevest_transpozici.clicked.connect(self.prevest_text)

        # Aktualizace tabulky
        self.ui.tabulka_matice.clearContents()

    def generovat_matici(self):
        """Generuje novou šifrovací matici a aktualizuje zobrazení."""
        self.matrix = vytvorit_adfgvx_matici()
        self.zobrazit_matici()
        QtWidgets.QMessageBox.information(self, "Úspěch", "Nová matice byla úspěšně vygenerována.")

    def zobrazit_matici(self):
        """Zobrazí aktuální šifrovací matici v tabulce a umožní její editaci."""
        self.ui.tabulka_matice.clearContents()
        for i in range(6):
            for j in range(6):
                item = QtWidgets.QTableWidgetItem(self.matrix[i + 1][j + 1])  # +1 pro přeskočení hlaviček v matici
                item.setForeground(QtGui.QColor(255, 255, 255))  # Nastavení bílé barvy textu
                item.setTextAlignment(QtCore.Qt.AlignCenter)  # Zarovnání textu na střed
                item.setFlags(
                    QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsEditable)  # Povolit editaci
                self.ui.tabulka_matice.setItem(i, j, item)

        # Přizpůsobení velikosti buněk pro rovnoměrné rozložení
        self.ui.tabulka_matice.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.ui.tabulka_matice.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        # Připojení signálu pro zpracování změn
        self.ui.tabulka_matice.itemChanged.connect(self.aktualizovat_matici)

    def aktualizovat_matici(self, item):
        """
        Aktualizuje interní šifrovací matici na základě změny v tabulce.
        Automaticky převádí zadávané znaky na velká písmena a nastavuje jejich barvu na bílou.
        """
        try:
            # Zjistíme řádek a sloupec, kde byla změna provedena
            i, j = item.row() + 1, item.column() + 1  # +1 kvůli hlavičkám v matici
            new_value = item.text().strip().upper()  # Načtení nového textu a převod na velká písmena

            # Validace nového textu (pouze jedno písmeno nebo číslo)
            if len(new_value) == 1 and new_value in (string.ascii_uppercase + string.digits):
                self.matrix[i][j] = new_value  # Aktualizace matice
                item.setText(new_value)  # Přepsání do tabulky (pro případ, že byl zadaný malý znak)

            else:
                QtWidgets.QMessageBox.warning(self, "Chyba", "Zadejte pouze jedno písmeno nebo číslo.")
                item.setText(self.matrix[i][j])  # Vrátí starou hodnotu
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Chyba", f"Nastala chyba při aktualizaci matice: {e}")

    def stahnout_matici(self):
        """Uloží aktuální šifrovací matici do souboru JSON."""
        options = QtWidgets.QFileDialog.Options()
        file_path, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Uložit matici", "", "JSON Files (*.json)",
                                                             options=options)

        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as file:
                    json.dump(self.matrix, file, ensure_ascii=False, indent=4)
                QtWidgets.QMessageBox.information(self, "Úspěch", "Matice byla úspěšně uložena.")
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "Chyba", f"Chyba při ukládání matice: {e}")

    def nahrat_matici(self):
        """Načte šifrovací matici ze souboru JSON."""
        options = QtWidgets.QFileDialog.Options()
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Načíst matici", "", "JSON Files (*.json)",
                                                             options=options)

        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    loaded_matrix = json.load(file)

                # Ověření, že matice má správný formát
                if len(loaded_matrix) == 7 and all(len(row) == 7 for row in loaded_matrix):
                    self.matrix = loaded_matrix
                    self.zobrazit_matici()
                    QtWidgets.QMessageBox.information(self, "Úspěch", "Matice byla úspěšně načtena.")
                else:
                    raise ValueError("Načtená matice má neplatný formát.")
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "Chyba", f"Chyba při načítání matice: {e}")

    def prevest_text(self):
        """Provádí zpětnou transpozici a výsledek ukládá do pole 'text pro dešifrování'."""
        try:
            # Získání vstupů
            encrypted_text = self.ui.text_zasifrovany.toPlainText()
            key = self.ui.klic.text()

            # Kontrola vstupů
            if not encrypted_text or not key:
                raise ValueError("Musíte zadat zašifrovaný text a klíč.")

            # Odebrání mezer a zpětná transpozice
            encrypted_text_cleaned = encrypted_text.replace(" ", "")
            reversed_text = zpetna_transpozice_sloupcu(encrypted_text_cleaned, key)

            # Uložení výsledku do pole 'text pro dešifrování'
            self.ui.text_pro_desifrovani.setPlainText(reversed_text)

            # Výpis do konzole
            print(f"Zpětná transpozice provedena: {reversed_text}")
            print("Text nastaven do pole 'text pro dešifrování'.")
        except Exception as e:
            print(f"Chyba při zpětné transpozici: {e}")
            QtWidgets.QMessageBox.critical(self, "Chyba", str(e))

    def zasifrovat(self):
        try:
            if self.matrix is None:
                raise ValueError("Matice není nastavena. Nejprve ji vygenerujte nebo zadejte ručně.")

            # Získání textu pro šifrování a klíče z GUI
            text = self.ui.text_pro_sifrovani.toPlainText()
            key = self.ui.klic.text()

            if not text or not key:
                raise ValueError("Musíte zadat text i klíč.")

            # Předzpracování textu
            preprocessed_text = odstranit_diakritiku_a_spec_znaky(text)

            # Šifrování
            zasifrovany_text = adfgvx_sifrovat(preprocessed_text, key, self.matrix)
            rozdeleny_text = rozdel_do_skupin(zasifrovany_text, key)

            self.ui.text_zasifrovany.setPlainText(rozdeleny_text)

        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Chyba", str(e))

    def desifrovat(self):
        try:
            if self.matrix is None:
                raise ValueError("Matice není nastavena. Nejprve ji vygenerujte nebo zadejte ručně.")

            text_pro_desifrovani = self.ui.text_pro_desifrovani.toPlainText()
            key = self.ui.klic.text()

            if not text_pro_desifrovani or not key:
                raise ValueError("Musíte zadat text pro dešifrování a klíč.")

            desifrovany_text = adfgvx_desifrovat(text_pro_desifrovani, key, self.matrix)
            self.ui.text_desifrovany.setPlainText(desifrovany_text)

        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Chyba", str(e))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_window = ADFGVXApp()
    main_window.show()
    sys.exit(app.exec_())