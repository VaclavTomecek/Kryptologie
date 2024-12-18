import math
import random
import unidecode
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem
from RSA_GUI_ui import Ui_RSA
from PyQt5.QtGui import QColor, QBrush


def is_prime_number(n):
    # Kontroluje, zda je číslo prvočíslo
    if n <= 1 or (n % 2 == 0 and n > 2):
        return False
    return all(n % i != 0 for i in range(3, int(n ** 0.5) + 1, 2))


def generate_random_prime():
    # Generuje náhodné velké prvočíslo (10místné)
    while True:
        candidate = random.randint(10 ** 9, 10 ** 10)
        if is_prime_number(candidate):
            return candidate


def calculate_totient(p, q):
    # Vypočítá Eulerovu funkci (totient) jako (p - 1) * (q - 1)
    return (p - 1) * (q - 1)


def find_public_exponent(totient):
    # Hledá veřejný exponent 'e', který je nesoudělný s totientem
    while True:
        candidate = random.randint(2, totient)
        if math.gcd(candidate, totient) == 1:
            return candidate


def modular_exponentiation(base, exponent, modulus):
    # Provádí modulární umocňování (base^exponent mod modulus) pomocí binární exponentace
    result = 1
    binary_exponent = bin(exponent)[2:]
    for bit in binary_exponent:
        result = (result ** 2) % modulus
        if bit == '1':
            result = (result * base) % modulus
    return result


def split_binary_string(binary_string):
    # Rozděluje binární řetězec na bloky po 8 bitech
    return [''.join(binary_string[i:i + 8]) for i in range(0, len(binary_string), 8)]


class RSAApp(QtWidgets.QMainWindow):
    # Hlavní třída pro aplikaci RSA, která implementuje generování klíčů, šifrování a dešifrování textu

    def __init__(self):
        super().__init__()
        self.ui = Ui_RSA()
        self.ui.setupUi(self)

        # Připojení tlačítek a změn textu k funkcím
        self.ui.Generovat_Button.clicked.connect(self.generate_keys)
        self.ui.Text_pro_sifrovani.textChanged.connect(self.encrypt_text)
        self.ui.Text_pro_desifrovani.textChanged.connect(self.check_and_decrypt)

    def generate_keys(self):
        # Generuje RSA klíče: prvočísla p, q; modul n; veřejný exponent e a privátní exponent d
        # Klíče se zobrazí v odpovídajících polích GUI
        self.p = generate_random_prime()
        self.q = generate_random_prime()
        self.n = self.p * self.q
        self.totient = calculate_totient(self.p, self.q)
        self.e = find_public_exponent(self.totient)
        self.d = pow(self.e, -1, self.totient)

        # Zobrazení klíčů v GUI
        self.ui.P.setText(str(self.p))
        self.ui.Q.setText(str(self.q))
        self.ui.FI.setText(str(self.totient))
        self.ui.E.setText(str(self.e))
        self.ui.D.setText(str(self.d))
        self.ui.N.setText(str(self.n))

    def encrypt_text(self):
        # Šifruje text zadaný uživatelem pomocí veřejného klíče (e, n)
        # Zašifrovaný text a jeho binární podoba se zobrazí v GUI
        if not hasattr(self, 'e') or not hasattr(self, 'd') or not hasattr(self, 'n'):
            self.ui.Zasifrovany_text.setPlainText("Klíče nejsou vygenerovány.")
            return

        plaintext = self.ui.Text_pro_sifrovani.toPlainText()
        if not plaintext.strip():  # Kontrola na prázdný text
            self.ui.Zasifrovany_text.clear()
            self.ui.Binarni_zobrazeni_sifrovani.clear()
            self.ui.Text_pro_desifrovani.clear()
            self.ui.Desifrovany_text.clear()
            return

        # Odstranění diakritiky a příprava textu
        sanitized_text = unidecode.unidecode(plaintext.replace("\n", ""))
        binary_data = ""
        data_blocks = []

        try:
            # Rozdělení textu na bloky
            for index, character in enumerate(sanitized_text):
                ascii_value = ord(character)
                binary_value = bin(ascii_value)[2:].zfill(8)  # ASCII na binární hodnotu
                binary_data += binary_value
                if (index + 1) % 8 == 0:  # Každých 8 znaků tvoří blok
                    data_blocks.append(int(binary_data, 2))
                    binary_data = ""
            if binary_data:  # Zbývající data v posledním bloku doplněná nulami
                while len(binary_data) < 64:
                    binary_data += "0"
                data_blocks.append(int(binary_data, 2))
        except Exception as e:
            self.ui.Zasifrovany_text.setPlainText(f"Chyba při šifrování: {str(e)}")
            return

        # Šifrování bloků
        encrypted_blocks = [modular_exponentiation(block, self.e, self.n) for block in data_blocks]
        self.ui.Zasifrovany_text.setPlainText(" ".join(map(str, encrypted_blocks)))
        self.ui.Binarni_zobrazeni_sifrovani.setPlainText("\n".join(bin(block)[2:].zfill(64) for block in data_blocks))

        # Aktualizace tabulky v GUI
        self.update_table(data_blocks, sanitized_text)

        # Automatická aktualizace pole pro dešifrování
        self.ui.Text_pro_desifrovani.setPlainText(" ".join(map(str, encrypted_blocks)))
        self.check_and_decrypt()

    def decrypt_text(self):
        # Dešifruje text zadaný uživatelem pomocí privátního klíče (d, n)
        # Dešifrovaný text a jeho binární podoba se zobrazí v GUI
        ciphertext = self.ui.Text_pro_desifrovani.toPlainText()
        if not ciphertext:
            return
        encrypted_numbers = map(int, ciphertext.split())
        decrypted_blocks = [modular_exponentiation(number, self.d, self.n) for number in encrypted_numbers]

        # Dekódování znaků z dešifrovaných bloků
        decoded_characters = []
        for block in decrypted_blocks:
            binary_value = bin(block)[2:].zfill(64)
            binary_chunks = split_binary_string(binary_value)
            for chunk in binary_chunks:
                if chunk != "00000000":  # Přeskakuje prázdné znaky
                    decoded_characters.append(chr(int(chunk, 2)))

        # Zobrazení dešifrovaného textu a binární podoby v GUI
        self.ui.Desifrovany_text.setPlainText("".join(decoded_characters))
        self.ui.Binarni_zobrazeni_desifrovani.setPlainText("\n".join(bin(block)[2:].zfill(64) for block in decrypted_blocks))

    def check_and_decrypt(self):
        # Kontroluje, zda jsou klíče a šifrovaný text vyplněny, a pokud ano, provádí dešifrování
        ciphertext = self.ui.Text_pro_desifrovani.toPlainText()
        if not ciphertext.strip():  # Kontrola na prázdný text
            self.ui.Desifrovany_text.clear()
            self.ui.Binarni_zobrazeni_desifrovani.clear()
            return

        # Kontrola, zda jsou všechny klíče vyplněny
        if not all([
            self.ui.P.text().strip(), self.ui.Q.text().strip(), self.ui.FI.text().strip(),
            self.ui.E.text().strip(), self.ui.D.text().strip(), self.ui.N.text().strip()
        ]):
            self.ui.Desifrovany_text.setPlainText("Klíče nejsou kompletní.")
            return

        try:
            self.decrypt_text()
        except Exception as e:
            self.ui.Desifrovany_text.setPlainText(f"Chyba při dešifrování: {str(e)}")

    def update_table(self, data_blocks, text):
        # Aktualizuje tabulku v GUI zobrazením bloků, ASCII hodnot a binárních reprezentací textu
        self.ui.tabulka.setRowCount(len(data_blocks))
        for row_index, (block, character) in enumerate(zip(data_blocks, text)):
            table_data = [
                str(row_index),               # Index bloku
                character,                    # Původní znak
                str(ord(character)),          # ASCII hodnota
                bin(ord(character))[2:].zfill(8),  # Binární hodnota ASCII
                str(block),                   # Šifrovaný blok
                bin(block)[2:].zfill(64)      # Binární hodnota bloku
            ]
            for column_index, value in enumerate(table_data):
                cell = QTableWidgetItem(value)
                cell.setForeground(QBrush(QColor("white")))  # Nastavení barvy textu na bílou
                self.ui.tabulka.setItem(row_index, column_index, cell)


if __name__ == "__main__":
    # Hlavní část programu: spuštění aplikace
    import sys
    app = QtWidgets.QApplication(sys.argv)
    rsa_window = RSAApp()
    rsa_window.show()
    sys.exit(app.exec_())
