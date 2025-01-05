from PySide6.QtWidgets import (QApplication, 
QMainWindow, 
QPushButton,
QLabel,
QLineEdit,
QVBoxLayout,
QWidget,
QHBoxLayout,
QMessageBox,
QFormLayout,
)
from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QPixmap, QFont, QScreen
import sys

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

import random



MONGO_URL = "mongodb+srv://admin:admin@cluster0.sleh9.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(MONGO_URL)
db = client['avsmenma']
users = db['posts']

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.UI()

    def center_window(self):
        qr = self.frameGeometry()
        screen_center = QApplication.primaryScreen().availableGeometry().center()
        qr.moveCenter(screen_center)
        self.move(qr.topLeft())

    def UI(self):
        self.setWindowTitle("WingJourney")
        self.resize(400, 350)
        self.center_window()

        main_layout = QVBoxLayout()

        title_label = QLabel("Welcome Back")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setFont(QFont('Arial', 18, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #2c3e50; margin-bottom: 20px;")
        main_layout.addWidget(title_label)

        from_layout = QFormLayout()

        self.input_email = QLineEdit()
        self.input_email.setStyleSheet("padding: 5px; border: 1px solid #bdc3c7; border-radius: 3px;")
        self.input_email.setPlaceholderText("Email or Phone Number")
        from_layout.addRow(self.input_email)

        self.input_password = QLineEdit()
        self.input_password.setStyleSheet("padding: 5px; border: 1px solid #bdc3c7; border-radius: 3px;")
        self.input_password.setPlaceholderText("Password")
        self.input_password.setEchoMode(QLineEdit.Password)
        from_layout.addRow(self.input_password)

        main_layout.addLayout(from_layout)

        tombol_login = QPushButton("Login")
        tombol_login.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                padding: 10px;
                border: none;
                border-radius: 5px;
                font-weight: bold;
            } QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        tombol_login.clicked.connect(self.fun_login)
        main_layout.addWidget(tombol_login)

        tombol_lupa_pass = QPushButton("Lupa Password")
        tombol_lupa_pass.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                padding: 10px;
                border: none;
                border-radius: 5px;
                font-weight: bold;
            } QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        tombol_lupa_pass.clicked.connect(self.open_window_reset_pw_password)
        main_layout.addWidget(tombol_lupa_pass)

        self.link_regist = QLabel()
        self.link_regist.setText('<a href="window_regist">No have account? Register!</a>')
        self.link_regist.setOpenExternalLinks(False)
        self.link_regist.linkActivated.connect(self.open_window_regist)
        self.link_regist.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.link_regist)

        self.setLayout(main_layout)

    def open_window_regist(self):
        self.close()

        self.window_register = register()
        self.window_register.show()

    def open_window_reset_pw_password(self):
        self.close()

        self.window_reset_pw = windowResetPass()
        self.window_reset_pw.show()

    def lupa_pass(self):
        return

    def fun_login(self):
        # Mengambil input email dan memvalidasi
        email = self.input_email.text().strip()
        password = self.input_password.text().strip()

        # cari_email = users.find_one({"email": email})
        # cari_password = users.find_one({"password": password})

        if not email and not password:
            QMessageBox.warning(self, "Perhatian", "Harap isi email dan password")

        if not email:
            QMessageBox.warning(self, "Perhatian", "Email tidak boleh kosong!")
            return
        
        if not password:
            QMessageBox.warning(self, "Perhatian", "Password tidak boleh kosong!")
            return

        cek_emailDanPassword = users.find_one({"email": email, "password": password})

        if cek_emailDanPassword:

            verify_code = str(random.randint(100000, 999999))
            filter_email = {"email": email}

            new_code = {"$set": {"verify_code": verify_code}}

            users.update_one(filter_email, new_code)
            QMessageBox.information(self, "Notifikasi","Tunggu Sebentar")

            

            

        
            try:
                server = smtplib.SMTP("smtp.gmail.com", 587)
                server.starttls()

                # Login ke akun pengirim
                server.login("telegramstarsbusines@gmail.com", "swko ydjl dvou bhus")

                # Membuat email
                message = MIMEMultipart()
                message['From'] = "telegramstarsbusines@gmail.com"
                message['To'] = email  # Gunakan input_email untuk email tujuan
                message['Subject'] = "Kode Verifikasi"
                message.attach(MIMEText(f'Kode Verifikasi anda adalah : {verify_code}'))  # Isi dengan teks

                # Mengirim email
                server.send_message(message)

                server.quit()

                # Tampilkan notifikasi setelah email bercari_email dikirim
                QMessageBox.information(self, "Notifikasi", f"Kode Verifikasi Sudah dikirim...")
                self.toWindowKonfirmasi()

            except Exception as e:
                print(f"Terjadi kesalahan: {e}")
                QMessageBox.critical(self, "Kesalahan", f"Gagal mengirim email: {e}")
                return


        else:
            QMessageBox.warning(self, "Notifikasi", "Email atau password anda salah")

    def toWindowKonfirmasi(self):
        email = self.input_email.text().strip()  # Ambil email sebelum menutup window
        self.close()
        self.changeWindow = konfirmasi_login(email)  # Pass email ke window konfirmasi
        self.changeWindow.show()
                        
class konfirmasi_login(QWidget):

    def __init__(self, email):  # Tambah parameter email
        super().__init__()
        self.user_email = email  # Simpan email sebagai instance variable
        self.window_konfirmasiLogin()

    def window_konfirmasiLogin(self):
        self.setWindowTitle("WingJourney")
        self.resize(400, 350)
        self.center_window()

        main_layout = QVBoxLayout()

        title_label = QLabel("Konfirmasi Login")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setFont(QFont('Arial', 18, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #2c3e50; margin-bottom: 20px;")
        main_layout.addWidget(title_label)

        from_layout = QFormLayout()

        self.input_kode_verifikasi = QLineEdit()
        self.input_kode_verifikasi.setStyleSheet("padding: 5px; border: 1px solid #bdc3c7; border-radius: 3px;")
        self.input_kode_verifikasi.setPlaceholderText("Masukkan Kode Verifikasi")
        from_layout.addRow(self.input_kode_verifikasi)

        main_layout.addLayout(from_layout)

        tombol_login = QPushButton("Login")
        tombol_login.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                padding: 10px;
                border: none;
                border-radius: 5px;
                font-weight: bold;
            } QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        tombol_login.clicked.connect(self.fun_verify)
        main_layout.addWidget(tombol_login)

        self.setLayout(main_layout)


    def fun_verify(self):  # Hapus parameter email karena sudah ada self.user_email
        verify_code = self.input_kode_verifikasi.text().strip()

        if not verify_code:
            QMessageBox.warning(self, "Perhatian", "Kode verifikasi tidak boleh kosong")
            return

        try:
            konfirmasi_verifyCode = users.find_one(
                {"email": self.user_email},  # Gunakan self.user_email
                {"email": 1, "verify_code": 1}
            )

            if konfirmasi_verifyCode is None:
                QMessageBox.warning(self, "gagal", "Email tidak ditemukan di database")
                return

            db_verify_code = konfirmasi_verifyCode.get('verify_code')

            if str(verify_code) == str(db_verify_code):
                QMessageBox.information(self, "Notifikasi", "Berhasil, Anda akan diarahkan ke Dashboard")
                from WingsJourney import Home_Page
                self.close()  # Tutup window konfirmasi
                self.dashboard = Home_Page()
                app.setStyle("Fusion")
                stylesheet_path = "style.qss"
                apply_stylesheet(app, stylesheet_path)
                self.dashboard.show()
            else:
                QMessageBox.warning(self, "gagal", "kode verifikasi tidak valid")

        except Exception as e:
            print(f"Error: {str(e)}")
            QMessageBox.critical(self, "Error", f"Terjadi kesalahan: {str(e)}")

    def center_window(self):
        qr = self.frameGeometry()
        screen_center = QApplication.primaryScreen().availableGeometry().center()
        qr.moveCenter(screen_center)
        self.move(qr.topLeft())

class windowResetPass(QWidget):

    def __init__(self):
        super().__init__()
        self.IU()
        
    def IU(self):
            self.setWindowTitle("WingJourney")

            self.resize(400, 210)

            self.center_window()

            main_layout = QVBoxLayout()

            title_label = QLabel("Kirim Password")
            title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            title_label.setFont(QFont('Arial', 18, QFont.Weight.Bold))
            title_label.setStyleSheet("color: #2c3e50; margin-bottom: 20px;")
            main_layout.addWidget(title_label)


            from_layout = QFormLayout()

            # Input email/nohp untuk reset password
            self.input_lupa_email = QLineEdit()
            self.input_lupa_email.setStyleSheet("padding: 5px; border: 1px solid #bdc3c7; border-radius: 3px;")
            self.input_lupa_email.setPlaceholderText("Masukkan Email or Phone Number untuk menerima email")
            from_layout.addRow(self.input_lupa_email)

            main_layout.addLayout(from_layout)

            # tombol login
            tombol_kode_email = QPushButton("Kirim Password Melalui Email")
            tombol_kode_email.setStyleSheet("""
                QPushButton {
                    background-color: #3498db;
                    color: white;
                    padding: 10px;
                    border: none;
                    border-radius: 5px;
                    font-weight: bold;
                } QPushButton:hover {
                background-color: #2980b9;
            }
            """)

            button_layout = QHBoxLayout()
            
            tombol_kode_email.clicked.connect(self.kirimPasswordEmail)
            button_layout.addWidget(tombol_kode_email)

            # tombol lupa password
            tombol_kode_hp = QPushButton("Kirim Password Melalui No Hp")
            tombol_kode_hp.setStyleSheet("""
                QPushButton {
                    background-color: #3498db;
                    color: white;
                    padding: 10px;
                    border: none;
                    border-radius: 5px;
                    font-weight: bold;
                } QPushButton:hover {
                background-color: #2980b9;
            }
            """)

            tombol_kode_hp.clicked.connect(self.kirimPasswordHp)
            button_layout.addWidget(tombol_kode_hp)
            main_layout.addLayout(button_layout)


            self.link_back = QLabel()
            self.link_back.setText('<a href="window_regist">Already have account? Login</a>')
            self.link_back.setOpenExternalLinks(False)
            self.link_back.linkActivated.connect(self.back_login)
            self.link_back.setAlignment(Qt.AlignmentFlag.AlignCenter)
            main_layout.addWidget(self.link_back)
            

            
            main_layout.addWidget(self.link_back)
            self.setLayout(main_layout)

    def back_login(self):
        self.close()

        self.window_login = MainWindow()
        self.window_login.show()

    def kirimPasswordEmail(self):
        email = self.input_lupa_email.text().strip()

        cari_password = users.find_one({"email": email})
        if cari_password:
            password = cari_password.get("password")

            if password:
                pesan_email = f"{password}"
            else:
                QMessageBox.warning(self, "Notifikasi", "Password tidak ada didatabase")

        else:
            QMessageBox.warning(self, "Notifikasi", "Email tidak terdaftar")

        QMessageBox.information(self, "Notifikasi", "Tunggu Sebentar...")

        try:
                server = smtplib.SMTP("smtp.gmail.com", 587)
                server.starttls()

                # Login ke akun pengirim
                server.login("telegramstarsbusines@gmail.com", "swko ydjl dvou bhus")

                # Membuat email
                message = MIMEMultipart()
                message['From'] = "telegramstarsbusines@gmail.com"
                message['To'] = email  # Gunakan input_email untuk email tujuan
                message['Subject'] = "Password WingJourney"
                message.attach(MIMEText(f'Password anda adalah : {pesan_email}'))  # Isi dengan teks

                # Mengirim email
                server.send_message(message)

                server.quit()

                # Tampilkan notifikasi setelah email bercari_email dikirim
                QMessageBox.information(self, "Notifikasi", f"Password anda Sudah dikirim...")

        except Exception as e:
                print(f"Terjadi kesalahan: {e}")
                QMessageBox.critical(self, "Kesalahan", f"Gagal mengirim email: {e}")
                return

    def kirimPasswordHp(self):
        QMessageBox.information(self, "Notifikasi", "Fitur ini akan segera tersedia")

    def center_window(self):
        qr = self.frameGeometry()

        screen_center = QApplication.primaryScreen().availableGeometry().center()

        qr.moveCenter(screen_center)

        self.move(qr.topLeft())

    def fun_login(self):
        # Mengambil input email dan memvalidasi
        email = self.input_email.text().strip()

        if not email:
            QMessageBox.warning(self, "Perhatian", "Email tidak boleh kosong!")
            return
        
        cari_email = users.find_one({"email": email})

        if not cari_email:
            verify_code = str(random.randint(100000, 999999))
            data = {
                "email" : email,
                "verify_code" : verify_code
            }

            users.insert_one(data)

        else:
            verify_code = str(random.randint(100000, 999999))
            filter_email = {"email": email}

            new_code = {"$set": {"verify_code": verify_code}}

            users.update_one(filter_email, new_code)

            QMessageBox.information(self, "Sukses", f"Tunggu Sebentar.....")


class register(QWidget):
    def __init__(self):
        super().__init__()
        self.regist()

    def regist(self):
            self.setWindowTitle("WingJourney")

            self.resize(400, 350)

            self.center_window()

            main_layout = QVBoxLayout()

            title_label = QLabel("Register WingsJourney")
            title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            title_label.setFont(QFont('Arial', 18, QFont.Weight.Bold))
            title_label.setStyleSheet("color: #2c3e50; margin-bottom: 20px;")
            main_layout.addWidget(title_label)


            from_layout = QFormLayout()

            # Input nama untuk regist
            self.input_nama = QLineEdit()
            self.input_nama.setStyleSheet("padding: 5px; border: 1px solid #bdc3c7; border-radius: 3px;")
            self.input_nama.setPlaceholderText("Name")
            from_layout.addRow(self.input_nama)

            #input email untuk regist
            self.input_regist_email = QLineEdit()
            self.input_regist_email.setStyleSheet("padding: 5px; border: 1px solid #bdc3c7; border-radius: 3px;")
            self.input_regist_email.setPlaceholderText("Email")
            from_layout.addRow(self.input_regist_email)

            #input no hp untuk regist
            self.input_regist_nohp = QLineEdit()
            self.input_regist_nohp.setStyleSheet("padding: 5px; border: 1px solid #bdc3c7; border-radius: 3px;")
            self.input_regist_nohp.setPlaceholderText("Phone Number")
            from_layout.addRow(self.input_regist_nohp)

            #input input password reigst
            self.input_regist_password = QLineEdit()
            self.input_regist_password.setStyleSheet("padding: 5px; border: 1px solid #bdc3c7; border-radius: 3px;")
            self.input_regist_password.setPlaceholderText("Password")
            from_layout.addRow(self.input_regist_password)

            #input input konfirmasi password reigst
            self.input_regist_konfirmasi_password = QLineEdit()
            self.input_regist_konfirmasi_password.setStyleSheet("padding: 5px; border: 1px solid #bdc3c7; border-radius: 3px;")
            self.input_regist_konfirmasi_password.setPlaceholderText("Confirm Password")
            from_layout.addRow(self.input_regist_konfirmasi_password)

            main_layout.addLayout(from_layout)

            # tombol login
            tombol_regist = QPushButton("Register")
            tombol_regist.setStyleSheet("""
                QPushButton {
                    background-color: #3498db;
                    color: white;
                    padding: 10px;
                    border: none;
                    border-radius: 5px;
                    font-weight: bold;
                } QPushButton:hover {
                background-color: #2980b9;
            }
            """)

            tombol_regist.clicked.connect(self.fun_regist)

            main_layout.addWidget(tombol_regist)

            self.link_back = QLabel()
            self.link_back.setText('<a href="window_regist">Already have account? Login</a>')
            self.link_back.setOpenExternalLinks(False)
            self.link_back.linkActivated.connect(self.back_login)
            self.link_back.setAlignment(Qt.AlignmentFlag.AlignCenter)
            main_layout.addWidget(self.link_back)
            

            
            main_layout.addWidget(self.link_back)

            self.setLayout(main_layout)  

    def back_login(self):
        self.close()

        self.window_login = MainWindow()
        self.window_login.show() 

    def fun_regist(self):
        nama = self.input_nama.text().strip()
        email = self.input_regist_email.text().strip()
        nohp = self.input_regist_nohp.text().strip()
        password = self.input_regist_password.text().strip()
        konfirmasi_password = self.input_regist_konfirmasi_password.text().strip()
        verify_code = 000000

        cari_nama = users.find_one({"nama": nama})
        cari_email = users.find_one({"email": email})
        cari_nohp = users.find_one({"phone_number": nohp})

        if not nama or not email or not nohp or not password or not konfirmasi_password:
            QMessageBox.warning(self, "Peringatan", "Harap isi semua data")
            return
        
        if not self.is_valid_email(email):
            QMessageBox.warning(self, "Peringatan", "Masukkan email yang valid")
            self.clear_email()
            return

        if password == konfirmasi_password:
                if not cari_email:
                    if not cari_nama:
                        if not cari_nohp:
                                if nohp.isdigit():
                                    data_regist = {
                                            "nama" : nama,
                                            "email" : email,
                                            "phone_number": nohp,
                                            "password": password,
                                            "saldo": 0,
                                            "verify_code": verify_code,
                                        }

                                    users.insert_one(data_regist)
                                    QMessageBox.information(self, "Sukses", "Pendafataran Berhasil, Silahkan Login")
                                    self.clear_text()

                                else:
                                    QMessageBox.warning(self, "Peringatan", "Nomor Hp tidak valid")
                                    self.clear_nohp()
                        else:
                            QMessageBox.warning(self, "Peringatan", "Nomor Hp sudah terdaftar")
                            self.clear_nohp()

                    else:
                        QMessageBox.warning(self, "Peringatan", "Nama sudah terdaftar")
                        self.clear_nama()
                
                else:
                    QMessageBox.warning(self, "Peringatan", "Email sudah terdaftar")
                    self.clear_email()
        else:
            QMessageBox.warning(self, "Peringatan", "Password harus sama")
            
    

    def clear_text(self):
        # Membersihkan teks di QLineEdit
            self.input_regist_konfirmasi_password.clear()
            self.input_regist_password.clear()
            self.input_regist_nohp.clear()
            self.input_regist_email.clear()
            self.input_nama.clear()
    
    def clear_nohp(self):
        self.input_regist_nohp.clear()

    def clear_email(self):
        self.input_regist_email.clear()

    def clear_nama(self):
        self.input_nama.clear()

    def is_valid_email(self, email):
        # Regex untuk validasi email
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None


    
    def center_window(self):
        qr = self.frameGeometry()
        screen_center = QApplication.primaryScreen().availableGeometry().center()
        qr.moveCenter(screen_center)
        self.move(qr.topLeft())

    

    





def apply_stylesheet(app, path):
    with open(path, "r") as file:
        qss = file.read()
        app.setStyleSheet(qss)



app = QApplication(sys.argv)


window = MainWindow()
window.show()
sys.exit(app.exec())
