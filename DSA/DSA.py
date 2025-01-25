import hashlib
import random
import os
import base64
import datetime
import math
import zipfile
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QFileDialog
from DSA_GUI_ui import Ui_DSA


def fix_base64_padding(b64_string):
    # Opraví zarovnání Base64 řetězce přidáním chybějících znaků =.
    return b64_string + "=" * ((4 - len(b64_string) % 4) % 4)


class DSAApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_DSA()
        self.ui.setupUi(self)

        self.ui.generovat_klice.clicked.connect(self.generate_keys)
        self.ui.podepsat_soubor_button.clicked.connect(self.sign_file)
        self.ui.overit.clicked.connect(self.verify_signature)
        self.ui.nacist_soubor_button.clicked.connect(self.select_and_load_file)
        self.ui.nacist_zip.clicked.connect(self.load_zip_file)
        self.ui.nacist_klice.clicked.connect(self.load_keys)

        self.extracted_files = {}  # Ukládá extrahované soubory z ZIP

    def generate_keys(self):
        # Dialog pro výběr cílové složky
        directory = QFileDialog.getExistingDirectory(self, "Vyberte složku pro uložení klíčů", "")
        if not directory:
            self.ui.stav_je.setText("Generování klíčů zrušeno.")
            print("Generování klíčů zrušeno.")
            return

        # Generuje veřejný a soukromý klíč pro RSA a ukládá je do souborů.
        self.p = self.generate_large_prime(128, 256)
        self.q = self.generate_large_prime(128, 256)
        self.n = self.p * self.q
        self.phi = (self.p - 1) * (self.q - 1)
        self.e = self.find_public_exponent(self.phi)
        self.d = pow(self.e, -1, self.phi)

        print(f"Generované klíče: p={self.p}, q={self.q}, n={self.n}, e={self.e}, d={self.d}")

        # Konverze klíčů do Base64
        private_key = base64.b64encode(f"{self.d},{self.n}".encode()).decode()
        public_key = base64.b64encode(f"{self.e},{self.n}".encode()).decode()

        # Uložení klíčů do vybrané složky
        priv_key_path = os.path.join(directory, "rsa_key.priv")
        pub_key_path = os.path.join(directory, "rsa_key.pub")

        with open(priv_key_path, "w") as priv_file:
            priv_file.write(f"RSA {private_key}")
        with open(pub_key_path, "w") as pub_file:
            pub_file.write(f"RSA {public_key}")

        print(f"Klíče uloženy: {priv_key_path}, {pub_key_path}")

        self.ui.verejny_klic.setPlainText(f"e={self.e}, n={self.n}")
        self.ui.soukromy_klic.setPlainText(f"d={self.d}, n={self.n}")
        self.ui.stav_je.setText(f"Klíče uloženy do: {directory}")

    def generate_large_prime(self, min_digits, max_digits):
        iterations = 5  # Počet iterací pro testování
        while True:
            candidate = self.random_large_number(min_digits, max_digits)
            if self.is_prime(candidate, iterations):
                return candidate

    def random_large_number(self, min_digits, max_digits):
        return random.randint(10 ** (min_digits - 1), 10 ** max_digits - 1)

    def is_prime(self, number, iterations):
        # Používá Miller-Rabinův test na určení prvočíselnosti.
        if number < 2 or number % 2 == 0:
            return number == 2

            # Rozložení čísla na (n - 1) = d * 2^r
        r, d = 0, number - 1
        while d % 2 == 0:
            r += 1
            d //= 2

        for _ in range(iterations):
            a = random.randint(2, number - 2)
            x = pow(a, d, number)
            if x == 1 or x == number - 1:
                continue
            for _ in range(r - 1):
                x = pow(x, 2, number)
                if x == number - 1:
                    break
            else:
                return False
        return True

    def find_public_exponent(self, phi):
        # Najde vhodný veřejný exponent e.
        e = 65537  # Standardní hodnota
        if math.gcd(e, phi) == 1:
            return e
        raise ValueError("Nelze najít vhodný exponent.")

    def select_and_load_file(self):
        # Otevře dialog pro výběr souboru a načte jeho informace.
        file_path, _ = QFileDialog.getOpenFileName(self, "Vyberte soubor", "", "All Files (*.*)")
        if file_path:
            print(f"Vybraný soubor: {file_path}")
            self.ui.cesta_k_souboru.setText(file_path)
            self.load_file(file_path)

    def load_file(self, file_path):
        # Načte soubor a zobrazí jeho informace v odpovídajících polích.
        try:
            if not os.path.exists(file_path):
                self.ui.stav_je.setText("Soubor nenalezen.")
                print("Soubor nenalezen.")
                return

            file_info = os.stat(file_path)
            file_name = os.path.basename(file_path)
            file_size = file_info.st_size  # Velikost v B
            modification_date = datetime.datetime.fromtimestamp(file_info.st_mtime)

            print(f"Načtený soubor: {file_name}, velikost: {file_size}, upraveno: {modification_date}")

            self.ui.nazev_souboru.setText(file_name)
            self.ui.velikost_souboru.setText(f"{file_size} B")
            self.ui.datum_vytvoreni.setText(modification_date.strftime("%Y-%m-%d %H:%M:%S"))
            self.ui.cesta_k_souboru.setText(file_path)

            self.ui.stav_je.setText("Soubor načten.")
        except Exception as e:
            self.ui.stav_je.setText(f"Chyba: {str(e)}")
            print(f"Chyba při načítání souboru: {str(e)}")

    def load_zip_file(self):
        # Načte ZIP soubor a pouze uloží jeho cestu bez extrahování souborů.
        zip_path, _ = QFileDialog.getOpenFileName(self, "Vyberte ZIP soubor", "", "ZIP Files (*.zip)")
        if not zip_path:
            self.ui.stav_zip_souboru.setText("Soubor ZIP nebyl vybrán.")
            print("Soubor ZIP nebyl vybrán.")
            return

        try:
            # Kontrola, zda vybraný soubor je skutečně ZIP
            if not zipfile.is_zipfile(zip_path):
                self.ui.stav_zip_souboru.setText("Vybraný soubor není platný ZIP soubor.")
                print("Vybraný soubor není platný ZIP soubor.")
                return

            # Uložení cesty k ZIP souboru
            self.ui.cesta_k_zip_souboru.setText(zip_path)
            # Uložení názvu ZIP souboru
            zip_name = os.path.basename(zip_path)
            self.ui.nazev_zipu.setText(zip_name)

            self.ui.stav_zip_souboru.setText("ZIP soubor byl úspěšně načten.")
            print(f"ZIP soubor načten: {zip_path}")

        except Exception as e:
            self.ui.stav_zip_souboru.setText(f"Chyba při načítání ZIP souboru: {str(e)}")
            print(f"Chyba při načítání ZIP souboru: {str(e)}")

    def load_keys(self):
        # Načte veřejný a soukromý klíč ze souborů.
        try:
            priv_key_path, _ = QFileDialog.getOpenFileName(self, "Vyberte soukromý klíč", "", "Priv Files (*.priv)")
            pub_key_path, _ = QFileDialog.getOpenFileName(self, "Vyberte veřejný klíč", "", "Pub Files (*.pub)")

            if priv_key_path:
                with open(priv_key_path, "r") as priv_file:
                    priv_key = priv_file.read().replace("RSA ", "")
                    priv_key = fix_base64_padding(priv_key)  # Oprava paddingu
                    d, n = map(int, base64.b64decode(priv_key).decode().split(","))
                    self.d = d
                    self.n = n
                    self.ui.soukromy_klic.setPlainText(f"d={d}, n={n}")

            if pub_key_path:
                with open(pub_key_path, "r") as pub_file:
                    pub_key = pub_file.read().replace("RSA ", "")
                    pub_key = fix_base64_padding(pub_key)  # Oprava paddingu
                    e, n = map(int, base64.b64decode(pub_key).decode().split(","))
                    self.e = e
                    self.n = n
                    self.ui.verejny_klic.setPlainText(f"e={e}, n={n}")

            print(f"Klíč d: {self.d}")
            print(f"Klíč e: {self.e}")
            print(f"Klíč n: {self.n}\n")

            self.ui.stav_je.setText("Klíče načteny.")
        except Exception as e:
            self.ui.stav_je.setText(f"Chyba při načítání klíčů: {str(e)}")
            print(f"Chyba při načítání klíčů: {str(e)}")

    def sign_file(self):
        # Podepíše soubor pomocí RSA a SHA3-512, a uloží podepsaný soubor do ZIP.
        try:
            file_path = self.ui.cesta_k_souboru.text()
            if not os.path.exists(file_path):
                self.ui.stav_je.setText("Soubor pro podpis nebyl nalezen.")
                print("Soubor pro podpis nebyl nalezen.")
                return

            with open(file_path, 'rb') as file:
                data = file.read()

            # Výpočet hash hodnoty souboru
            hash_value = hashlib.sha3_512(data).digest()
            hash_hex = hash_value.hex()
            print(f"Hash souboru: {hash_hex}")

            # Vytvoření podpisu pomocí soukromého klíče
            signature = pow(int.from_bytes(hash_value, "big"), self.d, self.n)
            print(f"Generovaný podpis: {signature}")

            # Uložení podpisu do .sign souboru
            signature_base64 = base64.b64encode(signature.to_bytes((self.n.bit_length() + 7) // 8, "big")).decode()
            signature_file = file_path + '.sign'
            with open(signature_file, 'w') as sig_file:
                sig_file.write(signature_base64)

            # Uložení podepsaného souboru a podpisu do ZIP
            zip_file_path, _ = QFileDialog.getSaveFileName(self, "Uložte ZIP soubor", "", "ZIP Files (*.zip)")
            if not zip_file_path:
                self.ui.stav_je.setText("Ukládání ZIP souboru zrušeno.")
                print("Ukládání ZIP souboru zrušeno.")
                return

            with zipfile.ZipFile(zip_file_path, 'w') as zipf:
                zipf.write(file_path, os.path.basename(file_path))
                zipf.write(signature_file, os.path.basename(signature_file))

            # Odstranění dočasného .sign souboru
            os.remove(signature_file)

            print(f"Soubor a podpis uloženy do ZIP: {zip_file_path}\n")
            self.ui.stav_je.setText(f"Soubor a podpis uloženy do ZIP: {zip_file_path}")

        except Exception as e:
            self.ui.stav_je.setText(f"Chyba při podepisování: {str(e)}")
            print(f"Chyba při podepisování: {str(e)}\n")

    def verify_signature(self):
        try:
            # Načtení cesty k ZIP souboru z uživatelského rozhraní
            zip_file_path = self.ui.cesta_k_zip_souboru.text().strip()

            if not zip_file_path:
                raise ValueError("Cesta k ZIP souboru není nastavena.")

            if not os.path.exists(zip_file_path):
                raise ValueError("Zadaný ZIP soubor neexistuje.")

            signed_file_path = os.path.basename(zip_file_path).replace('.zip', '')

            with zipfile.ZipFile(zip_file_path, 'r') as zip_file:
                file_list = zip_file.namelist()

            print("Složky v ZIP:", file_list)

            # Získání cest k podpisovému a podepsanému souboru
            signature_file = None
            signed_file = None

            for file in file_list:
                if file.endswith('.sign'):
                    signature_file = file
                    print(f"Podpisový soubor: {signature_file}")
                elif not file.startswith('__MACOSX/') and not file.startswith('.') and not file.startswith(
                        '._') and not file.startswith('__'):
                    signed_file = file
                    print(f"Podepsaný soubor: {signed_file}")

            if not signature_file or not signed_file:
                print("Podpisový soubor nebo dokument nebyl nalezen v ZIP.")
                self.ui.stav_je.setText("Podpisový soubor nebo dokument nebyl nalezen v ZIP.")
                return

            with zipfile.ZipFile(zip_file_path, 'r') as zip_file:
                # Načtení obsahu podepsaného souboru
                with zip_file.open(signed_file, 'r') as file:
                    signed_file_data = file.read()
                    hashed_data = hashlib.sha3_512(signed_file_data).digest()
                    print(f"Hash podepsaného souboru: {hashed_data.hex()}")

                # Načtení obsahu podpisového souboru
                with zip_file.open(signature_file, 'r') as file:
                    signature_content = file.read().decode()
                    signature_content = signature_content.replace("RSA_SHA3-512\n", "")
                    signature_bytes = base64.b64decode(signature_content)
                    signature_int = int.from_bytes(signature_bytes, byteorder='big')
                    print(f"Dekódovaný podpis: {signature_int}")

            # Dešifrování podpisu pomocí veřejného klíče
            decrypted_hash = pow(signature_int, self.e, self.n)
            decrypted_hash_bytes = decrypted_hash.to_bytes((self.n.bit_length() + 7) // 8, byteorder='big')
            decrypted_hash_final = decrypted_hash_bytes[-64:]
            print(f"Dekódovaný hash z podpisu: {decrypted_hash_final.hex()}\n")

            # Porovnání hashe
            if decrypted_hash_final == hashed_data:
                print("Podpis je platný.")
                self.ui.stav_je.setText("Podpis je platný.")
            else:
                print("Podpis není platný.")
                self.ui.stav_je.setText("Podpis není platný.")

        except zipfile.BadZipFile:
            print("ZIP soubor je poškozen nebo není validní.")
            self.ui.stav_je.setText("ZIP soubor je poškozen nebo není validní.")
        except ValueError as ve:
            print(f"Validation error: {ve}")
            self.ui.stav_je.setText(str(ve))
        except Exception as e:
            print(f"Error during signature verification: {e}")
            self.ui.stav_je.setText(f"Chyba při ověřování podpisu: {e}")


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    dsa_window = DSAApp()
    dsa_window.show()
    sys.exit(app.exec_())