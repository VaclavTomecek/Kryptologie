import sys
from unidecode import unidecode
from PyQt5.QtWidgets import QApplication, QMainWindow
from playfair_cipher_ui import Ui_Playfair_cipher


def prepare_text(text):
    # Převede text na velká písmena a nahradí "W" písmenem "V"
    text = unidecode(text).upper().replace("W", "V")

    # Pokud se jedná o šifrování, nahradí čísla odpovídajícim textem

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

    for digit, word in number_mapping.items():
        text = text.replace(digit, word)

    # Odstraní všechny znaky, které nejsou písmena nebo čísla
    text = ''.join(filter(str.isalnum, text))

    # Pokud je délka textu lichá, přidejte na jeho konec písmeno "Q"
    if len(text) % 2 != 0:
        text += "Q"

    # Rozdělí text na dvojice písmen (bigramy)
    pairs = [text[i:i + 2] for i in range(0, len(text), 2)]
    return pairs


def create_playfair_matrix(key):
    # Vytvoří Playfair matici na základě klíče
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVXYZ0123456789"  # Bez "W" s "V"
    key = key.upper().replace("W", "V")
    matrix = []
    for char in key + alphabet:
        if char not in matrix:
            matrix.append(char)

    # Pokud je matice menší než 25, doplní ji chybějícími znaky
    while len(matrix) < 25:
        for char in alphabet:
            if char not in matrix:
                matrix.append(char)

    playfair_matrix = [matrix[i:i+5] for i in range(0, 25, 5)]
    return playfair_matrix


def find_position(matrix, char):
    # Zjistí pozici písmen v matici
    for i in range(5):
        for j in range(5):
            if matrix[i][j] == char:
                return i, j
    return None


def playfair_encrypt(plain_text, key):
    # Vloží mezery na stejné pozice jako v původním textu
    get_user_key(key)

    for i in range(len(plain_text)):
        if plain_text[i] == " ":
            plain_text = plain_text[:i] + "X" + plain_text[i+1:]

    text = prepare_text(plain_text)
    playfair_matrix = create_playfair_matrix(key)
    cipher_text = ""
    intermediate_results = []

    for pair in text:
        row1, col1 = find_position(playfair_matrix, pair[0])
        row2, col2 = find_position(playfair_matrix, pair[1])
        if row1 == row2:
            # Písmena ve stejném řádku
            result1 = playfair_matrix[row1][(col1 + 1) % 5]
            result2 = playfair_matrix[row2][(col2 + 1) % 5]
            cipher_text += result1 + result2
            intermediate_results.append(f"Šifrování ({pair}): {result1}{result2}")
        elif col1 == col2:
            # Písmena ve stejném sloupci
            result1 = playfair_matrix[(row1 + 1) % 5][col1]
            result2 = playfair_matrix[(row2 + 1) % 5][col2]
            cipher_text += result1 + result2
            intermediate_results.append(f"Šifrování ({pair}): {result1}{result2}")
        else:
            # Písmena v různých řádcích a sloupcích
            result1 = playfair_matrix[row1][col2]
            result2 = playfair_matrix[row2][col1]
            cipher_text += result1 + result2

            cipher_text = cipher_text.replace(" ", "")
            temp = ""
            a = 0
            for i in cipher_text:
                if a < 5:
                    temp += i
                elif a == 5:
                    temp += " "
                    temp += i
                    a = 0
                a += 1
            cipher_text = temp

            intermediate_results.append(f"Šifrování ({pair}): {result1}{result2}")

    return cipher_text, intermediate_results


def playfair_decrypt(cipher_text, key):
    get_user_key(key)
    playfair_matrix = create_playfair_matrix(key)
    cipher_text = cipher_text.replace(" ", "")
    plain_text = ""
    intermediate_results = []

    for pair in prepare_text(cipher_text):
        row1, col1 = find_position(playfair_matrix, pair[0])
        row2, col2 = find_position(playfair_matrix, pair[1])
        if row1 == row2:
            # Písmena ve stejném řádku
            result1 = playfair_matrix[row1][(col1 - 1) % 5]
            result2 = playfair_matrix[row2][(col2 - 1) % 5]
            plain_text += result1 + result2
            intermediate_results.append(f"Dešifrování ({pair}): {result1}{result2}")
        elif col1 == col2:
            # Písmena ve stejném sloupci
            result1 = playfair_matrix[(row1 - 1) % 5][col1]
            result2 = playfair_matrix[(row2 - 1) % 5][col2]
            plain_text += result1 + result2
            intermediate_results.append(f"Dešifrování ({pair}): {result1}{result2}")
        else:
            # Písmena v různých řádcích a sloupcích
            result1 = playfair_matrix[row1][col2]
            result2 = playfair_matrix[row2][col1]
            plain_text += result1 + result2
            intermediate_results.append(f"Dešifrování ({pair}): {result1}{result2}")

            number_mapping = {
                "NULA": "0",
                "JEDNA": "1",
                "DVA": "2",
                "TRI": "3",
                "CTYRI": "4",
                "PET": "5",
                "SEST": "6",
                "SEDM": "7",
                "OSM": "8",
                "DEVET": "9"
            }

            for word, digit in number_mapping.items():
                plain_text = plain_text.replace(word, digit)

            # Převede `plain_text` na seznam znaků
            plain_text = list(plain_text)

            if len(plain_text) % 2 == 0 and plain_text[-1] == "Q":

                # Pokud je délka lichá a poslední znak je "Q", odstraní se
                plain_text.pop()

            # Převeďte seznam znaků zpět na řetězec
            plain_text = ''.join(plain_text)

    return plain_text, intermediate_results


def get_user_key(user_key):
    # Získá klíč od uživatele
    # user_key = input()
    user_key = unidecode(user_key).replace(" ", "").upper().replace("W", "V")
    return user_key


"""def get_user_text():
    # Získá text od uživatele
    user_text = input("Zadejte text k zašifrování: ")
    return user_text"""


def display_playfair_matrix(matrix):
    # Zobrazí Playfair šifrovací matici
    for row in matrix:
        print(" ".join(row))


def display_intermediate_results(results):
    # Zobrazí mezivýsledky
    for result in results:
        print(result)


class PlayfairApp(QMainWindow, Ui_Playfair_cipher):

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.Zasifrovat_button.clicked.connect(self.encrypt_text)
        self.Desifrovat_button.clicked.connect(self.decrypt_text)
        self.Zasifrovat_button.clicked.connect(self.set_operation_to_encrypt)
        self.Desifrovat_button.clicked.connect(self.set_operation_to_decrypt)
        self.Zasifrovat_button.clicked.connect(self.bad_key)
        self.Desifrovat_button.clicked.connect(self.bad_key)
        self.Zobrazeni_tabulky.clicked.connect(self.display_playfair_matrix)
        self.Mezivysledky.clicked.connect(self.display_intermediate_results)

    def bad_key(self):
        user_key = self.Klic_k_sifrovani.text()
        key = get_user_key(user_key)
        if len(key) < 8:
            self.key_size.setText("Klíč musí obsahovat alespoň 8 unikátních znaků")
        else:
            self.key_size.clear()
            self.key_size.setText("")

    # Zjišťování operace (šif/dešif) pro zobrazení mezivýsledků
    def set_operation(self, mode):
        global operation
        operation = mode

    def set_operation_to_encrypt(self):
        self.set_operation("Šifrování")

    def set_operation_to_decrypt(self):
        self.set_operation("Dešifrování")

    def encrypt_text(self):
        user_key = self.Klic_k_sifrovani.text()
        if len(user_key) < 8:
            return
        user_text = self.Text_pro_sifrovani.toPlainText()
        encrypted_text, intermediate_results = playfair_encrypt(user_text, user_key)
        self.Zasifrovany_text.setPlainText(encrypted_text)

    def decrypt_text(self):
        user_key = self.Klic_k_desifrovani.text()
        if len(user_key) < 8:
            return
        user_text = self.Text_pro_desifrovani.toPlainText()
        decrypted_text, intermediate_results = playfair_decrypt(user_text, user_key)

        decrypted_text = decrypted_text.replace("X", " ")

        self.Desifrovany_text_3.setPlainText(decrypted_text)

    # Zobrazemí mezivýsledků
    def display_intermediate_results(self):
        user_key = self.Klic_k_sifrovani.text()
        user_text = self.Text_pro_sifrovani.toPlainText()

        intermediate_results = []

        if operation == "Šifrování":
            intermediate_results = playfair_encrypt(user_text, user_key)[1]
        elif operation == "Dešifrování":
            intermediate_results = playfair_decrypt(user_text, user_key)[1]

        self.mezivysledky_vypis.setPlainText("\n".join(intermediate_results))

    # Zobrazení šifrovací tabulky
    def display_playfair_matrix(self):
        playfair_matrix = create_playfair_matrix(self.Klic_k_sifrovani.text())
        self.matice_vypis.setPlainText("\n".join([" ".join(row) for row in playfair_matrix]))


def main():
    app = QApplication(sys.argv)
    window = PlayfairApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
