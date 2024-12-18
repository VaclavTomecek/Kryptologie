import string
import random
import sys
from unidecode import unidecode
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication
from ADFGVX_ADFGX_ui import Ui_ADFGVX
import json

SPACE_HOLDER = "YMEZERAY"


def remove_diacritics_and_special_chars(text):
    # Odstraňuje diakritiku a speciální znaky z textu.
    text = unidecode(text)
    text = text.upper().replace("W", "V")
    text = replace_numbers(text)
    processed_text = ''.join(SPACE_HOLDER if c == ' ' else c for c in text if c in (string.ascii_uppercase + 'X '))
    return processed_text


def replace_numbers(text):
    # Nahrazuje číslice v textu specifickými řetězci, např. '0' → 'XNULAX'.
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


def restore_numbers(text):
    # Obnovuje původní číslice z jejich specifických reprezentací, např. 'XNULAX' → '0'.
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


def split_into_groups(text, key):
    # Rozděluje text na skupiny o délce odpovídající délce klíče.

    size = len(key)
    if size == 0:
        raise ValueError("Key for splitting groups cannot be empty.")
    text = text.replace(" ", "").strip()
    groups = [text[i:i + size] for i in range(0, len(text), size)]
    return ' '.join(groups)


def create_adfgx_matrix():
    # Generuje náhodnou ADFGX matici obsahující písmena abecedy bez W.

    alphabet = list(string.ascii_uppercase)
    alphabet.remove('W')
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


def find_position_in_matrix(matrix, char):
    # Hledá pozici znaku v ADFGX matici.
    # Vrací odpovídající řádek a sloupec znaku jako písmena ADFGX.

    for i in range(1, len(matrix)):
        for j in range(1, len(matrix[i])):
            if matrix[i][j] == char:
                return matrix[0][i], matrix[j][0]
    return None


def columnar_transposition(text, key):
    # Provádí transpozici textu podle klíče (sloupcová transpozice).

    col_count = len(key)
    grid = ['' for _ in range(col_count)]
    for i in range(len(text)):
        grid[i % col_count] += text[i]
    key_index = sorted(range(len(key)), key=lambda k: key[k])
    transposed_text = ''.join(grid[i] for i in key_index)
    return transposed_text


def reverse_columnar_transposition(text, key):
    # Obrací sloupcovou transpozici a vrací původní text.

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


def adfgx_encrypt(text, key, matrix):
    # Šifruje text pomocí ADFGX matice a sloupcové transpozice.

    encrypted_text = ''
    for char in text:
        position = find_position_in_matrix(matrix, char)
        if position:
            encrypted_text += position[0] + position[1]
        else:
            raise ValueError(f"Character '{char}' not found in the matrix.")
    encrypted_text = columnar_transposition(encrypted_text, key)
    return split_into_groups(encrypted_text, key)


def restore_spaces(text):
    # Obnovuje mezery v textu nahrazené konstantou SPACE_HOLDER.

    text = text.replace(SPACE_HOLDER, " ")
    return text


def adfgx_decrypt(transposed_text, key, matrix):
    # Dešifruje text pomocí obrácené transpozice a ADFGX matice.

    decrypted_text = ''
    line = "ADFGX"
    for i in range(0, len(transposed_text), 2):
        row_char = transposed_text[i]
        col_char = transposed_text[i + 1]
        try:
            row_index = line.index(row_char) + 1
            col_index = line.index(col_char) + 1
            decoded_char = matrix[row_index][col_index]
            decrypted_text += decoded_char
        except ValueError:
            decrypted_text += '?'
    decrypted_text = restore_numbers(decrypted_text)
    decrypted_text = restore_spaces(decrypted_text)
    return decrypted_text


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
        self.ui.ENGLISH_BUTTON_ADFGX.clicked.connect(lambda: self.zmena_jazyka("ENG"))
        self.ui.CZECH_BUTTON_ADFGX.clicked.connect(lambda: self.zmena_jazyka("CZE"))

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
            reversed_text = reverse_columnar_transposition(encrypted_text_cleaned, key)

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

            preprocessed_text = remove_diacritics_and_special_chars(text)

            zasifrovany_text = adfgx_encrypt(preprocessed_text, key, self.matrix)
            rozdeleny_text = split_into_groups(zasifrovany_text, key)

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

            desifrovany_text = adfgx_decrypt(text_pro_desifrovani, key, self.matrix)
            self.ui.text_desifrovany_ADFGX.setPlainText(desifrovany_text)

        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Chyba", str(e))

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_window = ADFGXApp()
    main_window.show()
    sys.exit(app.exec_())



