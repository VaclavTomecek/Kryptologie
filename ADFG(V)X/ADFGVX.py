import string
import random
import sys
from unidecode import unidecode
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication
from ADFGVX_ADFGX_ui import Ui_ADFGVX
import json

SPACE_HOLDER = "XMEZERAX"

# Funkce pro odstranění diakritiky a speciálních znaků
def remove_diacritics_and_special_chars(text):
    text = unidecode(text)
    text = text.upper()
    # Nahrazení mezer zástupným textem a odstranění nepovolených znaků
    return ''.join(SPACE_HOLDER if c == ' ' else c for c in text if c in (string.ascii_uppercase + string.digits + ' '))

# Funkce pro obnovení původních mezer v textu
def restore_spaces(text):
    return text.replace(SPACE_HOLDER, ' ')

# Funkce pro rozdělení textu do skupin podle klíče
def split_into_groups(text, key):
    size = len(key)
    if size == 0:
        raise ValueError("Klíč pro rozdělení skupin nesmí být prázdný.")
    text = text.replace(" ", "").strip()
    groups = [text[i:i + size] for i in range(0, len(text), size)]
    return ' '.join(groups)

# Funkce pro generování šifrovací matice ADFGVX
def create_adfgvx_matrix():
    alphabet = list(string.ascii_uppercase) + list(string.digits)
    random.seed()
    random.shuffle(alphabet)
    # Inicializace prázdné matice 7x7
    adfgvx_matrix = [["X" for _ in range(7)] for _ in range(7)]
    characters = 'ADFGVX'
    for i in range(6):
        adfgvx_matrix[0][i + 1] = characters[i]
        adfgvx_matrix[i + 1][0] = characters[i]
    # Vyplnění zbývající části matice náhodnými znaky
    for i in range(1, 7):
        for j in range(1, 7):
            if alphabet:
                adfgvx_matrix[i][j] = alphabet.pop(0)
    return adfgvx_matrix

# Funkce pro hledání pozice znaku v matici
def find_position_in_matrix(matrix, char):
    for i in range(1, len(matrix)):
        for j in range(1, len(matrix[i])):
            if matrix[i][j] == char:
                return matrix[0][i], matrix[j][0]
    return None

# Funkce pro sloupcovou transpozici textu
def columnar_transposition(text, key):
    col_count = len(key)
    grid = ['' for _ in range(col_count)]
    # Rozdělení textu do sloupců
    for i in range(len(text)):
        grid[i % col_count] += text[i]

    key_index = sorted(range(len(key)), key=lambda k: key[k])
    return ''.join(grid[i] for i in key_index)

# Funkce pro zpětnou sloupcovou transpozici
def reverse_columnar_transposition(text, key):
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
    # Rekonstrukce původního textu
    original_text = ''
    for r in range(row_count + 1):
        for c in range(col_count):
            if r < len(grid[c]):
                original_text += grid[c][r]
    return original_text

# Funkce pro šifrování textu pomocí ADFGVX
def adfgvx_encrypt(text, key, matrix):

    encrypted_text = ''
    for char in text:
        position = find_position_in_matrix(matrix, char)
        if position:
            encrypted_text += position[0] + position[1]
        else:
            raise ValueError(f"Znak '{char}' nebyl nalezen v matici.")

    encrypted_text = columnar_transposition(encrypted_text, key)
    return split_into_groups(encrypted_text, key)

# Funkce pro dešifrování textu pomocí ADFGVX
def adfgvx_decrypt(transposed_text, key, matrix):
    decrypted_text = ''
    line = "ADFGVX"

    # Převod textu zpět na znaky podle matice
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
    return restore_spaces(decrypted_text)


class ADFGVXApp(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.ui = Ui_ADFGVX()
        self.ui.setupUi(self)

        # Inicializace proměnné pro šifrovací matici (zatím prázdná)
        self.matrix = None  # Matice se nastaví ručně nebo tlačítkem

        # Připojení tlačítek k funkcím
        self.ui.Generace_Matice.clicked.connect(self.generate_matrix)
        self.ui.Zasifrovat_Button.clicked.connect(self.encrypt)
        self.ui.Desifrovat_Button.clicked.connect(self.decrypt)
        self.ui.stahnout_matici.clicked.connect(self.download_matrix)
        self.ui.nahrat_matici.clicked.connect(self.update_matrix)
        self.ui.Prevest_transpozici.clicked.connect(self.convert_text)

        # Aktualizace tabulky
        self.ui.tabulka_matice.clearContents()

    def generate_matrix(self):
        """Generuje novou šifrovací matici a aktualizuje zobrazení."""
        self.matrix = create_adfgvx_matrix()
        self.show_matrix()
        QtWidgets.QMessageBox.information(self, "Úspěch", "Nová matice byla úspěšně vygenerována.")

    def show_matrix(self):
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
        self.ui.tabulka_matice.itemChanged.connect(self.update_matrix)

    def update_matrix(self, item):
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

    def download_matrix(self):
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

    def upload_matrix(self):
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

    def convert_text(self):
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
            reversed_text = reverse_columnar_transposition(encrypted_text_cleaned, key)

            # Uložení výsledku do pole 'text pro dešifrování'
            self.ui.text_pro_desifrovani.setPlainText(reversed_text)

            # Výpis do konzole
            print(f"Zpětná transpozice provedena: {reversed_text}")
            print("Text nastaven do pole 'text pro dešifrování'.")
        except Exception as e:
            print(f"Chyba při zpětné transpozici: {e}")
            QtWidgets.QMessageBox.critical(self, "Chyba", str(e))

    def encrypt(self):
        try:
            if self.matrix is None:
                raise ValueError("Matice není nastavena. Nejprve ji vygenerujte nebo zadejte ručně.")

            # Získání textu pro šifrování a klíče z GUI
            text = self.ui.text_pro_sifrovani.toPlainText()
            key = self.ui.klic.text()

            if not text or not key:
                raise ValueError("Musíte zadat text i klíč.")

            # Předzpracování textu
            preprocessed_text = remove_diacritics_and_special_chars(text)

            # Šifrování
            zasifrovany_text = adfgvx_encrypt(preprocessed_text, key, self.matrix)
            rozdeleny_text = split_into_groups(zasifrovany_text, key)

            self.ui.text_zasifrovany.setPlainText(rozdeleny_text)

        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Chyba", str(e))

    def decrypt(self):
        try:
            if self.matrix is None:
                raise ValueError("Matice není nastavena. Nejprve ji vygenerujte nebo zadejte ručně.")

            text_pro_desifrovani = self.ui.text_pro_desifrovani.toPlainText()
            key = self.ui.klic.text()

            if not text_pro_desifrovani or not key:
                raise ValueError("Musíte zadat text pro dešifrování a klíč.")

            desifrovany_text = adfgvx_decrypt(text_pro_desifrovani, key, self.matrix)
            self.ui.text_desifrovany.setPlainText(desifrovany_text)

        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Chyba", str(e))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_window = ADFGVXApp()
    main_window.show()
    sys.exit(app.exec_())