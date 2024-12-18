import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
from Afinni_Sifra_ui import Ui_AfinniSifra


# Funkce pro odstranění diakritiky
def remove_diacritics(text):
    # Mapa diakritických znaků a jejich náhrad
    diacritics = {
        'á': 'a', 'č': 'c', 'ď': 'd', 'é': 'e', 'ě': 'e', 'í': 'i', 'ň': 'n',
        'ó': 'o', 'ř': 'r', 'š': 's', 'ť': 't', 'ú': 'u', 'ů': 'u', 'ý': 'y', 'ž': 'z',
        'Á': 'A', 'Č': 'C', 'Ď': 'D', 'É': 'E', 'Ě': 'E', 'Í': 'I', 'Ň': 'N',
        'Ó': 'O', 'Ř': 'R', 'Š': 'S', 'Ť': 'T', 'Ú': 'U', 'Ů': 'U', 'Ý': 'Y', 'Ž': 'Z'
    }
    # Nahrazení znaků s diakritikou odpovídajícími znaky bez diakritiky
    text = ''.join(diacritics.get(char, char) for char in text)
    # Odstranění speciálních znaků a ponechání pouze alfanumerických znaků a mezer
    text = ''.join(char for char in text if char.isalnum() or char.isspace())
    return text


# Abeceda použitá v šifře
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"  # Změna na velká písmena
alphabet_length = len(alphabet)  # Délka abecedy

# Znaková náhrada pro mezery
SPACE_PLACEHOLDER = "XMEZERAX"

# Mapa pro převod čísel na slova
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

# Obrácená mapa pro převod slov zpět na čísla
reverse_number_mapping = {v: k for k, v in number_mapping.items()}


# Funkce pro výpočet největšího společného dělitele (GCD)
def gcd(a, b):
    # Iterativní algoritmus pro výpočet GCD pomocí Eukleidova algoritmu
    while b:
        a, b = b, a % b
    return a


# Funkce pro mapování čísel na odpovídající slova
def map_numbers(text):
    mapped_text = ""
    for char in text:
        if char in number_mapping:
            # Nahrazení čísla odpovídajícím slovem, obaleným značkami '#'
            mapped_text += f"#{number_mapping[char]}#"
        else:
            # Zachování ostatních znaků
            mapped_text += char
    return mapped_text


# Funkce pro zpětné mapování slov na čísla
def unmap_numbers(text):
    for word, digit in reverse_number_mapping.items():
        # Nahrazení slov odpovídajícími čísly
        text = text.replace(f"#{word}#", digit)
    return text


# Funkce pro šifrování textu
def encrypt(text, a, b):
    # Kontrola, zda je 'a' nesoudělné s délkou abecedy
    if gcd(a, alphabet_length) != 1:
        return "Neplatný klíč: 'a' musí být nesoudělné s délkou abecedy."
    # Odstranění diakritiky, převod na velká písmena a nahrazení mezer
    text = remove_diacritics(text).upper().replace(" ", SPACE_PLACEHOLDER)
    text = map_numbers(text)  # Převod čísel na slova
    encrypted_text = ""
    for char in text:
        if char in alphabet:
            # Výpočet šifrovaného znaku pomocí affine transformace
            index = alphabet.index(char)
            encrypted_char_index = (a * index + b) % alphabet_length
            encrypted_text += alphabet[encrypted_char_index]
        else:
            # Zachování ostatních znaků
            encrypted_text += char

    # Vložení mezer po každých pěti znacích
    grouped_text = ' '.join([encrypted_text[i:i + 5] for i in range(0, len(encrypted_text), 5)])
    return grouped_text


# Funkce pro dešifrování textu
def decrypt(text, a, b):
    # Kontrola, zda je 'a' nesoudělné s délkou abecedy
    if gcd(a, alphabet_length) != 1:
        return "Neplatný klíč: 'a' musí být nesoudělné s délkou abecedy."
    decrypted_text = ""
    a_inv = None

    # Hledání multiplikativní inverze 'a'
    for i in range(alphabet_length):
        if (a * i) % alphabet_length == 1:
            a_inv = i
            break
    if a_inv is None:
        return "Neplatný klíč"

    # Odstranění mezer před zpracováním textu
    temp_text = text.replace(" ", "")

    for char in temp_text:
        if char in alphabet:
            # Výpočet dešifrovaného znaku pomocí inverzní affine transformace
            index = alphabet.index(char)
            decrypted_char_index = (a_inv * (index - b)) % alphabet_length
            decrypted_text += alphabet[decrypted_char_index]
        else:
            # Zachování ostatních znaků
            decrypted_text += char

    # Obnova nahrazených mezer
    decrypted_text = decrypted_text.replace(SPACE_PLACEHOLDER, " ")

    # Zpětné mapování slov na čísla
    decrypted_text = unmap_numbers(decrypted_text)

    return decrypted_text


# Třída reprezentující GUI aplikace
class Afinni_Sifra_App(QMainWindow, Ui_AfinniSifra):

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # Přiřazení funkcí k tlačítkům
        self.ZakodovatButton.clicked.connect(self.encrypt_text)
        self.DekodovatButton.clicked.connect(self.decrypt_text)

    def encrypt_text(self):
        try:
            # Načtení vstupního textu
            plaintext = self.Vstup_1.toPlainText().strip()
            if not plaintext:
                QtWidgets.QMessageBox.warning(self, "Chyba", "Vstupní text nemůže být prázdný.")
                return
            # Načtení klíčů
            a = int(self.klic_a.text())
            b = int(self.klic_b.text())
            if gcd(a, alphabet_length) != 1:
                QtWidgets.QMessageBox.warning(self, "Chyba", "Klíč 'a' musí být nesoudělný s délkou abecedy.")
                return
            # Šifrování textu
            ciphertext = encrypt(plaintext, a, b)
            self.Vystup_1.setPlainText(ciphertext)
        except ValueError:
            # Chyba při neplatném vstupu klíčů
            QtWidgets.QMessageBox.warning(self, "Chyba", "Zadejte platná čísla pro 'a' a 'b'.")

    def decrypt_text(self):
        try:
            # Načtení vstupního textu
            ciphertext = self.Vstup_2.toPlainText().strip()
            if not ciphertext:
                QtWidgets.QMessageBox.warning(self, "Chyba", "Vstupní text nemůže být prázdný.")
                return
            # Načtení klíčů
            a = int(self.klic_a.text())
            b = int(self.klic_b.text())
            if gcd(a, alphabet_length) != 1:
                QtWidgets.QMessageBox.warning(self, "Chyba", "Klíč 'a' musí být nesoudělný s délkou abecedy.")
                return
            # Dešifrování textu
            plaintext = decrypt(ciphertext, a, b)
            self.Vystup_2.setPlainText(plaintext)
        except ValueError:
            # Chyba při neplatném vstupu klíčů
            QtWidgets.QMessageBox.warning(self, "Chyba", "Zadejte platná čísla pro 'a' a 'b'.")


# Funkce hlavního programu
def main():
    app = QApplication(sys.argv)
    window = Afinni_Sifra_App()
    window.show()
    sys.exit(app.exec_())


# Spuštění programu
if __name__ == "__main__":
    main()
