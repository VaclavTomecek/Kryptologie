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


def modular_exponentiation(base, exponent, modulus):
    # Tato funkce efektivně počítá (base^exponent) % modulus pomocí iterativního algoritmu.
    print(f"Modular exponentiation: base={base}, exponent={exponent}, modulus={modulus}")
    if modulus <= 0:
        raise ValueError("Modulus musí být kladné číslo.")

    result = 1

    while exponent > 0:
        if exponent % 2 == 1:
            result = (result * base) % modulus
        base = (base * base) % modulus
        exponent //= 2

    return result


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
        self.p = self.generate_large_prime()
        self.q = self.generate_large_prime()
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

    def generate_large_prime(self):
        # Generuje velké prvočíslo.
        while True:
            candidate = random.randint(10**9, 10**10)
            if self.is_prime(candidate):
                print(f"Generované prvočíslo: {candidate}")
                return candidate

    def is_prime(self, n):
        # Kontroluje, zda je číslo prvočíslo.
        if n <= 1:
            return False
        for i in range(2, int(n**0.5) + 1):
            if n % i == 0:
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
            file_extension = os.path.splitext(file_path)[1]
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
            self.ui.cesta_k_zip_souboru.setText(zip_path)  # Změněno pro správné pole v GUI
            # Uložení názvu ZIP souboru
            zip_name = os.path.basename(zip_path)
            self.ui.nazev_zipu.setText(zip_name)  # Přidáno pro název ZIP souboru

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

            print(f"Klíče načteny: d={self.d}, e={self.e}, n={self.n}")
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
            hash_value = int(hashlib.sha3_512(data).hexdigest(), 16)
            print(f"Hash hodnoty souboru: {hash_value}")

            # Vytvoření podpisu pomocí soukromého klíče
            signature = modular_exponentiation(hash_value, self.d, self.n)
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

            print(f"Soubor a podpis uloženy do ZIP: {zip_file_path}")
            self.ui.stav_je.setText(f"Soubor a podpis uloženy do ZIP: {zip_file_path}")
        except Exception as e:
            self.ui.stav_je.setText(f"Chyba při podepisování: {str(e)}")
            print(f"Chyba při podepisování: {str(e)}")

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

            print("Files in ZIP:", file_list)

            # Získání cest k podpisovému a podepsanému souboru
            signature_file = None
            signed_file = None

            for file in file_list:
                if file.endswith('.sign'):
                    signature_file = file
                    print(f"Signature file found: {signature_file}")
                elif not file.startswith('__MACOSX/') and not file.startswith('.') and not file.startswith(
                        '._') and not file.startswith('__'):
                    signed_file = file
                    print(f"Signed file found: {signed_file}")

            if not signature_file or not signed_file:
                print("Signature or signed file not found in ZIP.")
                self.ui.stav_je.setText("Podpisový soubor nebo dokument nebyl nalezen v ZIP.")
                return

            with zipfile.ZipFile(zip_file_path, 'r') as zip_file:
                # Načtení obsahu podepsaného souboru
                with zip_file.open(signed_file, 'r') as file:
                    signed_file_data = file.read()
                    hashed_data = hashlib.sha3_512(signed_file_data).digest()
                    print(f"Computed hash of signed file: {hashed_data.hex()}")

                # Načtení obsahu podpisového souboru
                with zip_file.open(signature_file, 'r') as file:
                    signature_content = file.read().decode()
                    signature_content = signature_content.replace("RSA_SHA3-512\n", "")
                    signature_bytes = base64.b64decode(signature_content)
                    signature_int = int.from_bytes(signature_bytes, byteorder='big')
                    print(f"Decoded signature: {signature_int}")

            # Dešifrování podpisu pomocí veřejného klíče
            decrypted_hash = pow(signature_int, self.e, self.n)
            decrypted_hash_bytes = decrypted_hash.to_bytes((self.n.bit_length() + 7) // 8, byteorder='big')
            print(f"Decrypted hash from signature: {decrypted_hash_bytes.hex()}")

            # Porovnání hashe
            if decrypted_hash_bytes == hashed_data:
                print("Signature is valid.")
                self.ui.stav_je.setText("Podpis je platný.")
            else:
                print("Signature is invalid.")
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
