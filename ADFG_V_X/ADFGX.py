import string
import random
import sys
from unidecode import unidecode
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication
from ADFGVX_ADFGX_ui import Ui_ADFGVX
import json

SPACE_HOLDER = "YMEZERAY"

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

'''
def log_step(step_description):
    print(f"[LOG] {step_description}")
'''


def odstranit_diakritiku_a_spec_znaky(text):

    # Použít unidecode pro odstranění diakritiky
    text = unidecode(text)

    # Velká písmena a nahrazení 'W' za 'V'
    text = text.upper().replace("W", "V")

    # Nahrazení čísel speciálním formátem
    text = nahrazeni_cisel(text)

    # Nahrazení mezer SPACE_HOLDER
    processed_text = ''.join(SPACE_HOLDER if c == ' ' else c for c in text if c in (string.ascii_uppercase + 'X '))

    return processed_text


def nahrazeni_cisel(text: str) -> str:
    text = text.upper()

    text = text.replace('0', "XNULAX")
    text = text.replace('1', "XJEDNAX")
    text = text.replace('2', "XDVAX")
    text = text.replace('3', "XTRIX")
    text = text.replace('4', "XCTYRIX")
    text = text.replace('5', "XPETX")
    text = text.replace('6', "XSESTX")
    text = text.replace('7', "XSEDMX")
    text = text.replace('8', "XOSMX")
    text = text.replace('9', "XDEVETX")

    return text


def obnoveni_cisel(text: str) -> str:
    text = text.replace("XNULAX", '0')
    text = text.replace("XJEDNAX", '1')
    text = text.replace("XDVAX", '2')
    text = text.replace("XTRIX", '3')
    text = text.replace("XCTYRIX", '4')
    text = text.replace("XPETX", '5')
    text = text.replace("XSESTX", '6')
    text = text.replace("XSEDMX", '7')
    text = text.replace("XOSMX", '8')
    text = text.replace("XDEVETX", '9')

    return text


def rozdel_do_skupin(text, key):
    # Rozdělení textu na skupiny podle délky klíče
    velikost = len(key)
    if velikost == 0:
        raise ValueError("Klíč pro rozdělení skupin nesmí být prázdný.")
    text = text.replace(" ", "").strip()
    skupiny = [text[i:i + velikost] for i in range(0, len(text), velikost)]
    return ' '.join(skupiny)


def vytvorit_adfgx_matici():
    # Vytvoření šifrovací matice pro ADFGX
    alphabet = list(string.ascii_uppercase)
    alphabet.remove('W')  # W a V jsou sdruženy
    random.seed()
    random.shuffle(alphabet)

    adfgx_matrix = [["X" for _ in range(6)] for _ in range(6)]
    characters = 'ADFGX'
    for i in range(5):
        adfgx_matrix[0][i + 1] = characters[i]
        adfgx_matrix[i + 1][0] = characters[i]

    for i in range(1, 6):
        for j in range(1, 6):
            if alphabet:
                adfgx_matrix[i][j] = alphabet.pop(0)

    return adfgx_matrix


def najit_pozici_v_matici(matrix, char):
    # Vyhledání pozice znaku v šifrovací matici
    for i in range(1, len(matrix)):
        for j in range(1, len(matrix[i])):
            if matrix[i][j] == char:
                return matrix[0][i], matrix[j][0]
    return None


def transpozice_sloupcu(text, key):
    # Transpozice textu podle klíče
    col_count = len(key)
    grid = ['' for _ in range(col_count)]
    for i in range(len(text)):
        grid[i % col_count] += text[i]
    key_index = sorted(range(len(key)), key=lambda k: key[k])
    transposed_text = ''.join(grid[i] for i in key_index)
    return transposed_text


def zpetna_transpozice_sloupcu(text, key):
    # Obrácená transpozice textu podle klíče
    col_count = len(key)
    row_count = len(text) // col_count
    extra_chars = len(text) % col_count
    key_index = sorted(range(len(key)), key=lambda k: key[k])
    col_lengths = [row_count + (1 if i < extra_chars else 0) for i in range(col_count)]
    grid = [''] * col_count
    index = 0
    for i in range(col_count):
        col_length = col_lengths[key_index[i]]
        grid[key_index[i]] = text[index:index + col_length]
        index += col_length
    original_text = ''
    for r in range(row_count + 1):
        for c in range(col_count):
            if r < len(grid[c]):
                original_text += grid[c][r]
    return original_text


def adfgx_sifrovat(text, key, matrix):
    zasifrovany_text = ''
    for char in text:
        pozice = najit_pozici_v_matici(matrix, char)
        if pozice:
            zasifrovany_text += pozice[0] + pozice[1]
        else:
            raise ValueError(f"Znak '{char}' není v matici.")
    zasifrovany_text = transpozice_sloupcu(zasifrovany_text, key)
    return rozdel_do_skupin(zasifrovany_text, key)


def vratit_mezery(text):

    text = text.replace(SPACE_HOLDER, " ")

    return text


def adfgx_desifrovat(transposed_text, key, matrix):
    desifrovany_text = ''
    line = "ADFGX"
    for i in range(0, len(transposed_text), 2):
        row_char = transposed_text[i]
        col_char = transposed_text[i + 1]
        try:
            row_index = line.index(row_char) + 1
            col_index = line.index(col_char) + 1
            decoded_char = matrix[row_index][col_index]
            desifrovany_text += decoded_char
        except ValueError:
            desifrovany_text += '?'

    # Převést speciální formát zpět na čísla
    desifrovany_text = obnoveni_cisel(desifrovany_text)
    desifrovany_text = vratit_mezery(desifrovany_text)

    return desifrovany_text


class ADFGXApp(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.ui = Ui_ADFGVX()
        self.ui.setupUi(self)

        # Nastavení výchozí matice a abeced
        self.matrix = None
        self.current_language = "ENG"  # Výchozí jazyk je anglický
        self.english_alphabet = "ABCDEFGHIJKLMNOPRSTUVWXYZ"  # Anglická abeceda bez Q
        self.czech_alphabet = "ABCDEFGHIJKLMNOPQRSTUVXYZ"   # Česká abeceda bez W

        # Připojení tlačítek k funkcím
        self.ui.Generace_Matice_ADFGX.clicked.connect(self.generovat_matici)
        self.ui.Zasifrovat_Button_ADFGX.clicked.connect(self.zasifrovat)
        self.ui.Desifrovat_Button_ADFGX.clicked.connect(self.desifrovat)
        self.ui.stahnout_matici_ADFGX.clicked.connect(self.stahnout_matici)
        self.ui.nahrat_matici_ADFGX.clicked.connect(self.nahrat_matici)
        self.ui.Prevest_transpozici_ADFGX.clicked.connect(self.prevest_text)

        # Přepínače jazyků
        self.ui.ENGLISH_BUTTON_ADFGX.clicked.connect(lambda: self.switch_language("ENG"))
        self.ui.CZECH_BUTTON_ADFGX.clicked.connect(lambda: self.switch_language("CZE"))

        # Aktualizace tabulky
        self.ui.tabulka_matice_ADFGX.clearContents()

    def zmena_jazyka(self, language):
        """Přepne aktuální jazyk a vygeneruje novou matici."""
        if language == "ENG":
            self.current_language = "ENG"
            QtWidgets.QMessageBox.information(self, "Jazyk", "Přepnuto na anglickou abecedu.")
        elif language == "CZE":
            self.current_language = "CZE"
            QtWidgets.QMessageBox.information(self, "Jazyk", "Přepnuto na českou abecedu.")
        else:
            QtWidgets.QMessageBox.warning(self, "Chyba", "Neznámý jazyk.")
            return

        self.generovat_matici()

    def generovat_matici(self):
        """Generuje novou šifrovací matici podle aktuálního jazyka."""
        alphabet = self.english_alphabet if self.current_language == "ENG" else self.czech_alphabet
        alphabet = list(alphabet)
        random.seed()
        random.shuffle(alphabet)

        self.matrix = [["" for _ in range(6)] for _ in range(6)]
        characters = 'ADFGX'

        for i in range(5):
            self.matrix[0][i + 1] = characters[i]
            self.matrix[i + 1][0] = characters[i]

        for i in range(1, 6):
            for j in range(1, 6):
                if alphabet:
                    self.matrix[i][j] = alphabet.pop(0)

        self.zobrazit_matici()
        QtWidgets.QMessageBox.information(self, "Úspěch", "Nová matice byla úspěšně vygenerována.")

    def zobrazit_matici(self):
        """Zobrazí aktuální šifrovací matici v tabulce."""
        self.ui.tabulka_matice_ADFGX.clearContents()
        for i in range(5):
            for j in range(5):
                item = QtWidgets.QTableWidgetItem(self.matrix[i + 1][j + 1])  # +1 pro hlavičky matice
                item.setForeground(QtGui.QColor(255, 255, 255))  # Nastavení bílé barvy textu
                item.setTextAlignment(QtCore.Qt.AlignCenter)  # Zarovnání na střed
                self.ui.tabulka_matice_ADFGX.setItem(i, j, item)

        # Přizpůsobení velikosti buněk
        self.ui.tabulka_matice_ADFGX.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.ui.tabulka_matice_ADFGX.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

    def aktualizovat_matici(self, item):
        """
        Aktualizuje interní šifrovací matici na základě změny v tabulce.
        Automaticky převádí zadávané znaky na velká písmena a nastavuje jejich barvu na bílou.
        """
        try:
            i, j = item.row() + 1, item.column() + 1  # +1 kvůli hlavičkám v matici
            new_value = item.text().strip().upper()  # Načtení nového textu a převod na velká písmena

            if len(new_value) == 1 and new_value in string.ascii_uppercase.replace('W', ''):
                self.matrix[i][j] = new_value  # Aktualizace matice
                item.setText(new_value)  # Přepsání do tabulky (pro případ, že byl zadaný malý znak)

            else:
                QtWidgets.QMessageBox.warning(self, "Chyba", "Zadejte pouze jedno písmeno bez 'W'.")
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

                if len(loaded_matrix) == 6 and all(len(row) == 6 for row in loaded_matrix):
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
            encrypted_text = self.ui.text_zasifrovany_ADFGX.toPlainText()
            key = self.ui.klic_ADFGX.text()

            if not encrypted_text or not key:
                raise ValueError("Musíte zadat zašifrovaný text a klíč.")

            encrypted_text_cleaned = encrypted_text.replace(" ", "")
            reversed_text = zpetna_transpozice_sloupcu(encrypted_text_cleaned, key)

            self.ui.text_pro_desifrovani_ADFGX.setPlainText(reversed_text)

        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Chyba", str(e))

    def zasifrovat(self):
        try:
            if self.matrix is None:
                raise ValueError("Matice není nastavena. Nejprve ji vygenerujte nebo zadejte ručně.")

            text = self.ui.text_pro_sifrovani_ADFGX.toPlainText()
            key = self.ui.klic_ADFGX.text()

            if not text or not key:
                raise ValueError("Musíte zadat text i klíč.")

            preprocessed_text = odstranit_diakritiku_a_spec_znaky(text)

            zasifrovany_text = adfgx_sifrovat(preprocessed_text, key, self.matrix)
            rozdeleny_text = rozdel_do_skupin(zasifrovany_text, key)

            self.ui.text_zasifrovany_ADFGX.setPlainText(rozdeleny_text)

        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Chyba", str(e))

    def desifrovat(self):
        try:
            if self.matrix is None:
                raise ValueError("Matice není nastavena. Nejprve ji vygenerujte nebo zadejte ručně.")

            text_pro_desifrovani = self.ui.text_pro_desifrovani_ADFGX.toPlainText()
            key = self.ui.klic_ADFGX.text()

            if not text_pro_desifrovani or not key:
                raise ValueError("Musíte zadat text pro dešifrování a klíč.")

            desifrovany_text = adfgx_desifrovat(text_pro_desifrovani, key, self.matrix)
            self.ui.text_desifrovany_ADFGX.setPlainText(desifrovany_text)

        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Chyba", str(e))

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_window = ADFGXApp()
    main_window.show()
    sys.exit(app.exec_())



