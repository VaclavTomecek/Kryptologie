import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
from Afinni_Sifra_ui import Ui_AfinniSifra


# Funkce pro odstranění diakritiky
def remove_diacritics(text):
    diacritics = {
        'á': 'a', 'č': 'c', 'ď': 'd', 'é': 'e', 'ě': 'e', 'í': 'i', 'ň': 'n',
        'ó': 'o', 'ř': 'r', 'š': 's', 'ť': 't', 'ú': 'u', 'ů': 'u', 'ý': 'y', 'ž': 'z',
        'Á': 'A', 'Č': 'C', 'Ď': 'D', 'É': 'E', 'Ě': 'E', 'Í': 'I', 'Ň': 'N',
        'Ó': 'O', 'Ř': 'R', 'Š': 'S', 'Ť': 'T', 'Ú': 'U', 'Ů': 'U', 'Ý': 'Y', 'Ž': 'Z'
    }
    # Nahrazení diakritiky
    text = ''.join(diacritics.get(char, char) for char in text)
    # Odstranění speciálních znaků
    text = ''.join(char for char in text if char.isalnum() or char.isspace())
    return text


alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"  # Change to uppercase
alphabet_length = len(alphabet)

SPACE_PLACEHOLDER = "XMEZERAX"

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


def gcd(a, b):
    while b:
        a, b = b, a % b
    return a


def map_numbers(text):
    mapped_text = ""
    for char in text:
        if char in number_mapping:
            mapped_text += f"#{number_mapping[char]}#"
        else:
            mapped_text += char
    return mapped_text


def unmap_numbers(text):
    for word, digit in reverse_number_mapping.items():
        text = text.replace(f"#{word}#", digit)
    return text


def encrypt(text, a, b):
    if gcd(a, alphabet_length) != 1:
        return "Neplatný klíč: 'a' musí být nesoudělné s délkou abecedy."
    # Remove diacritics, convert to uppercase, replace spaces
    text = remove_diacritics(text).upper().replace(" ", SPACE_PLACEHOLDER)
    text = map_numbers(text)  # Map numbers to words
    encrypted_text = ""
    for char in text:
        if char in alphabet:
            index = alphabet.index(char)
            encrypted_char_index = (a * index + b) % alphabet_length
            encrypted_text += alphabet[encrypted_char_index]
        else:
            encrypted_text += char

    # Insert spaces every five characters
    grouped_text = ' '.join([encrypted_text[i:i + 5] for i in range(0, len(encrypted_text), 5)])
    return grouped_text


def decrypt(text, a, b):
    if gcd(a, alphabet_length) != 1:
        return "Neplatný klíč: 'a' musí být nesoudělné s délkou abecedy."
    decrypted_text = ""
    a_inv = None

    # Hledáme inverzi a
    for i in range(alphabet_length):
        if (a * i) % alphabet_length == 1:
            a_inv = i
            break
    if a_inv is None:
        return "Neplatný klíč"

    temp_text = text.replace(" ", "")  # Remove spaces before processing

    for char in temp_text:
        if char in alphabet:
            index = alphabet.index(char)
            decrypted_char_index = (a_inv * (index - b)) % alphabet_length
            decrypted_text += alphabet[decrypted_char_index]
        else:
            decrypted_text += char  # Ostatní znaky zůstávají nezměněny

    # Restore placeholder spaces
    decrypted_text = decrypted_text.replace(SPACE_PLACEHOLDER, " ")

    # Unmap numbers back to digits
    decrypted_text = unmap_numbers(decrypted_text)

    return decrypted_text


class Afinni_Sifra_App(QMainWindow, Ui_AfinniSifra):

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.ZakodovatButton.clicked.connect(self.encrypt_text)
        self.DekodovatButton.clicked.connect(self.decrypt_text)

    def encrypt_text(self):
        try:
            plaintext = self.Vstup_1.toPlainText().strip()
            if not plaintext:
                QtWidgets.QMessageBox.warning(self, "Chyba", "Vstupní text nemůže být prázdný.")
                return
            a = int(self.klic_a.text())
            b = int(self.klic_b.text())
            if gcd(a, alphabet_length) != 1:
                QtWidgets.QMessageBox.warning(self, "Chyba", "Klíč 'a' musí být nesoudělný s délkou abecedy.")
                return
            ciphertext = encrypt(plaintext, a, b)
            self.Vystup_1.setPlainText(ciphertext)
        except ValueError:
            QtWidgets.QMessageBox.warning(self, "Chyba", "Zadejte platná čísla pro 'a' a 'b'.")

    def decrypt_text(self):
        try:
            ciphertext = self.Vstup_2.toPlainText().strip()
            if not ciphertext:
                QtWidgets.QMessageBox.warning(self, "Chyba", "Vstupní text nemůže být prázdný.")
                return
            a = int(self.klic_a.text())
            b = int(self.klic_b.text())
            if gcd(a, alphabet_length) != 1:
                QtWidgets.QMessageBox.warning(self, "Chyba", "Klíč 'a' musí být nesoudělný s délkou abecedy.")
                return
            plaintext = decrypt(ciphertext, a, b)
            self.Vystup_2.setPlainText(plaintext)
        except ValueError:
            QtWidgets.QMessageBox.warning(self, "Chyba", "Zadejte platná čísla pro 'a' a 'b'.")


def main():
    app = QApplication(sys.argv)
    window = Afinni_Sifra_App()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
