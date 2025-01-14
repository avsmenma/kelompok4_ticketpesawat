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
import mysql.connector
from mysql.connector import Error

import bcrypt
import hashlib

import string

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
        email = self.input_email.text().strip()
        password = self.input_password.text().strip()

        if not email and not password:
            QMessageBox.warning(self, "Perhatian", "Harap isi email dan password")
            return

        if not email:
            QMessageBox.warning(self, "Perhatian", "Email tidak boleh kosong!")
            return
        
        if not password:
            QMessageBox.warning(self, "Perhatian", "Password tidak boleh kosong!")
            return

        try:
            connect = mysql.connector.connect(
                host = "localhost",
                user="root",
                password="",
                database="penerbangan"
            )
            cursor = connect.cursor(dictionary=True)

            # Cari user berdasarkan email saja
            query = "SELECT id, nama, email, no_telp, password, role FROM akun WHERE email = %s"
            cursor.execute(query, (email,))
            user = cursor.fetchone()

            if user:
                # Cek apakah user adalah admin
                if user['role'] == 'admin':
                    # Untuk admin, langsung bandingkan password tanpa hashing
                    password_matches = (password == user['password'])

                    from dashboard_admin import Home_Page
                    self.close()
                    self.goToDashboardAdminPage = Home_Page()
                    app.setStyle("Fusion")
                    stylesheet_path = "style_admin.qss"
                    apply_stylesheet(app, stylesheet_path)
                    self.goToDashboardAdminPage.show()
                    return
                else:
                    # Untuk user biasa, gunakan verifikasi dengan bcrypt
                    password_matches = self.verify_password(password, user['password'])

                if password_matches:
                    verify_code = str(random.randint(100000, 999999))
                    update_query = "UPDATE akun SET verify_code = %s WHERE email = %s"
                    cursor.execute(update_query, (verify_code, email))
                    connect.commit()

                    # Store user data
                    self.user_data = {
                        'id': user['id'],
                        'nama': user['nama'],
                        'email': user['email'],
                        'no_telp': user['no_telp'],
                        'role': user['role']
                    }

                    try:
                        QMessageBox.information(self, "Notifikasi", "Tunggu Sebentar")
                        
                        # Kirim kode verifikasi ke email
                        server = smtplib.SMTP("smtp.gmail.com", 587)
                        server.starttls()
                        server.login("telegramstarsbusines@gmail.com", "swko ydjl dvou bhus")

                        # Isi pesan HTML
                        html_content = f"""
                        <html>
                        <head>
                            <style>
                                body {{
                                    font-family: Arial, sans-serif;
                                    background-color: #f9f9f9;
                                    color: #333;
                                    padding: 20px;
                                }}
                                .email-container {{
                                    background-color: #ffffff;
                                    padding: 20px;
                                    border: 1px solid #dddddd;
                                    border-radius: 8px;
                                    max-width: 600px;
                                    margin: auto;
                                }}
                                .header {{
                                    text-align: center;
                                    font-size: 24px;
                                    font-weight: bold;
                                    color: #0066CC;
                                }}
                                .content {{
                                    font-size: 16px;
                                    margin-top: 20px;
                                    line-height: 1.5;
                                }}
                                .footer {{
                                    text-align: center;
                                    font-size: 12px;
                                    color: #888888;
                                    margin-top: 20px;
                                }}
                            </style>
                        </head>
                        <body>
                            <div class="email-container">
                                <div class="header">Kode Verifikasi Anda</div>
                                <div class="content">
                                    <p>Halo,</p>
                                    <p>Selamat Datang Di WingsJourney. Berikut adalah kode verifikasi Anda:</p>
                                    <p style="font-size: 20px; font-weight: bold; text-align: center; color: #0066CC;">
                                        {verify_code}
                                    </p>
                                    <p>Silakan masukkan kode ini untuk memverifikasi akun Anda.</p>
                                </div>
                                <div class="footer">
                                    &copy; 2025 WingsJourney Business. Semua Hak Dilindungi.
                                </div>
                            </div>
                        </body>
                        </html>
                        """

                        # Buat pesan email
                        message = MIMEMultipart("alternative")
                        message['From'] = "telegramstarsbusines@gmail.com"
                        message['To'] = email
                        message['Subject'] = "Kode Verifikasi Anda"
                        message.attach(MIMEText(html_content, "html"))

                        server.send_message(message)
                        server.quit()

                        QMessageBox.information(self, "Notifikasi", "Kode Verifikasi Sudah dikirim...")
                        self.toWindowKonfirmasi()

                    except Exception as e:
                        QMessageBox.critical(self, "Kesalahan", f"Gagal mengirim email: {e}")
                else:
                    QMessageBox.warning(self, "Notifikasi", "Email atau password anda salah")

            else:
                QMessageBox.warning(self, "Notifikasi", "Email atau password anda salah")

            cursor.close()
            connect.close()

        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Kesalahan", f"Koneksi database gagal: {err}")

    def verify_password(self, password, hashed_password):
        return bcrypt.checkpw(password.encode(), hashed_password.encode())


    def toWindowKonfirmasi(self):
        self.close()
        self.changeWindow = konfirmasi_login(self.input_email.text().strip(), self.user_data)
        self.changeWindow.show()
                        
class konfirmasi_login(QWidget):

    def __init__(self, email, user_data):
        super().__init__()
        self.user_email = email
        self.user_data = user_data
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
        

        tombol_backToLoginPage = QPushButton("Back")
        tombol_backToLoginPage.setStyleSheet("""
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
        tombol_backToLoginPage.clicked.connect(self.fun_backToLoginPage)
        main_layout.addWidget(tombol_login)
        main_layout.addWidget(tombol_backToLoginPage)


        self.setLayout(main_layout)

    def fun_backToLoginPage(self):
        self.close()

        self.backToLoginPage = MainWindow()
        self.backToLoginPage.show()


    def fun_verify(self):  # Hapus parameter email karena sudah ada self.user_email
        verify_code = self.input_kode_verifikasi.text().strip()

        if not verify_code:
            QMessageBox.warning(self, "Perhatian", "Kode verifikasi tidak boleh kosong")
            return

        try:
            connect = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="penerbangan"
            )
            cursor = connect.cursor(dictionary=True)

            query = "SELECT verify_code, role FROM akun WHERE email = %s"
            cursor.execute(query, (self.user_email,))
            result = cursor.fetchone()

            if result is None:
                QMessageBox.warning(self, "gagal", "Email tidak ditemukan di database")
                return

            db_verify_code = result['verify_code']
            user_role = result['role']

            if str(verify_code) == str(db_verify_code):
                QMessageBox.information(self, "Notifikasi", "Berhasil, Anda akan diarahkan ke Dashboard")

                update_query = "UPDATE akun SET verify_code = '0' WHERE email = %s"
                cursor.execute(update_query, (self.user_email,))
                connect.commit()

                from WingsJourney import Home_Page
                self.close()
                self.dashboard = Home_Page(self.user_data)  # Pass user_data to Home_Page
                app.setStyle("Fusion")
                stylesheet_path = "style.qss"
                apply_stylesheet(app, stylesheet_path)
                self.dashboard.show()
            else:
                QMessageBox.warning(self, "gagal", "kode verifikasi tidak valid")

        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Kesalahan", f"Koneksi database gagal: {err}")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Terjadi kesalahan: {str(e)}")

    def center_window(self):
        qr = self.frameGeometry()
        screen_center = QApplication.primaryScreen().availableGeometry().center()
        qr.moveCenter(screen_center)
        self.move(qr.topLeft())

class windowResetPass(QWidget):

    def __init__(self):
        super().__init__()
        
        # self.kirimPasswordEmail()
        self.IU()
        
    def IU(self):
        
            self.setWindowTitle("WingJourney")

            self.resize(400, 210)

            self.center_window()
            self.connect = mysql.connector.connect(
            host="localhost", 
            user="root",  
            password="",  
            database="penerbangan"  
            )
            self.cursor = self.connect.cursor()

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

        if not email:
            QMessageBox.warning(self, "Perhatian", "Email tidak boleh kosong!")
            return

        try:
            # Cek apakah email terdaftar
            self.cursor.execute("SELECT id FROM akun WHERE email = %s", (email,))
            user = self.cursor.fetchone()

            if not user:
                QMessageBox.warning(self, "Notifikasi", "Email tidak terdaftar")
                return

            # Generate password baru secara random
            new_password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
            
            # Hash password baru
            salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), salt)
            
            # Update password di database
            self.cursor.execute("UPDATE akun SET password = %s WHERE email = %s", 
                            (hashed_password.decode('utf-8'), email))
            self.connect.commit()

            html_content = f"""
            <html>
            <head>
                <style>
                    body {{
                        font-family: Arial, sans-serif;
                        background-color: #f9f9f9;
                        color: #333;
                        padding: 20px;
                    }}
                    .email-container {{
                        background-color: #ffffff;
                        padding: 20px;
                        border: 1px solid #dddddd;
                        border-radius: 8px;
                        max-width: 600px;
                        margin: auto;
                    }}
                    .header {{
                        text-align: center;
                        font-size: 24px;
                        font-weight: bold;
                        color: #0066CC;
                    }}
                    .content {{
                        font-size: 16px;
                        margin-top: 20px;
                        line-height: 1.5;
                    }}
                    .footer {{
                        text-align: center;
                        font-size: 12px;
                        color: #888888;
                        margin-top: 20px;
                    }}
                </style>
            </head>
            <body>
                <div class="email-container">
                    <div class="header">Password Baru WingsJourney</div>
                    <div class="content">
                        <p>Halo,</p>
                        <p>Berikut adalah Password Baru untuk Akun WingsJourney Anda:</p>
                        <p style="font-size: 20px; font-weight: bold; text-align: center; color: #0066CC;">
                            {new_password}
                        </p>
                        <p>Silakan login dengan password ini dan segera ganti password Anda untuk keamanan akun.</p>
                    </div>
                    <div class="footer">
                        &copy; 2025 WingsJourney Business. Semua Hak Dilindungi.
                    </div>
                </div>
            </body>
            </html>
            """
            
            try:
                QMessageBox.information(self, "Notifikasi", "Tunggu Sebentar")

                server = smtplib.SMTP("smtp.gmail.com", 587)
                server.starttls()

                # Login ke akun pengirim
                server.login("telegramstarsbusines@gmail.com", "swko ydjl dvou bhus")

                # Membuat email
                message = MIMEMultipart()
                message['From'] = "telegramstarsbusines@gmail.com"
                message['To'] = email
                message['Subject'] = "Password Baru WingJourney"
                message.attach(MIMEText(html_content, "html"))

                # Mengirim email
                server.send_message(message)
                server.quit()

                QMessageBox.information(self, "Notifikasi", 
                                    "Password baru telah dikirim ke email Anda. Silakan cek email Anda.")

            except Exception as e:
                print(f"Terjadi kesalahan: {e}")
                QMessageBox.critical(self, "Kesalahan", f"Gagal mengirim email: {e}")
                return

        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Kesalahan", f"Error database: {err}")
            return


    def kirimPasswordHp(self):
        QMessageBox.information(self, "Notifikasi", "Fitur ini akan segera tersedia")
        return



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
        
        self.cursor.execute("SELECT * FROM akun WHERE email = %s",(email,))
        cari_email = self.cursor.fetchone()

        if not cari_email:
            verify_code = str(random.randint(100000, 999999))
            data = {
                "email" : email,
                "verify_code" : verify_code
            }

            self.cursor.execute("INSERT INTO akun (email, verify_code) VALUES (%s, %s)", (email, verify_code))
            self.conn.commit()

        else:
            verify_code = str(random.randint(100000, 999999))
            filter_email = {"email": email}

            self.cursor.execute("UPDATE akun SET verify_code = %s WHERE email = %s", (verify_code, email))
            self.conn.commit()

            QMessageBox.information(self, "Sukses", f"Tunggu Sebentar.....")


class register(QWidget):
    def __init__(self):
        super().__init__()
        self.connect = mysql.connector.connect(
            host="localhost", 
            user="root",  
            password="",  
            database="penerbangan"  
        )
        self.cursor = self.connect.cursor()
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

     

    def fun_regist(self, password):
        nama = self.input_nama.text().strip()
        email = self.input_regist_email.text().strip()
        nohp = self.input_regist_nohp.text().strip()
        password = self.input_regist_password.text().strip()
        konfirmasi_password = self.input_regist_konfirmasi_password.text().strip()
        verify_code = random.randint(100000, 999999)


        if not nama or not email or not nohp or not password or not konfirmasi_password:
            QMessageBox.warning(self, "Peringatan", "Harap isi semua data")
            return

        if not self.is_valid_email(email):
            QMessageBox.warning(self, "Peringatan", "Masukkan email yang valid")
            self.clear_email()
            return

        if password != konfirmasi_password:
            QMessageBox.warning(self, "Peringatan", "Password dan Konfirmasi Password tidak cocok")
            return

        try:
            # Cek email yang sudah terdaftar
            self.cursor.execute("SELECT * FROM akun WHERE nama = %s", (nama,))
            cari_email = self.cursor.fetchone()

            # Cek nama yang sudah terdaftar
            self.cursor.execute("SELECT * FROM akun WHERE email = %s", (email,))
            cari_nama = self.cursor.fetchone()

            # Cek nomor telepon yang sudah terdaftar
            self.cursor.execute("SELECT * FROM akun WHERE no_telp = %s", (nohp,))
            cari_nohp = self.cursor.fetchone()

            if cari_email:
                QMessageBox.warning(self, "Peringatan", "Email sudah terdaftar")
                self.clear_email()
                return

            if cari_nama:
                QMessageBox.warning(self, "Peringatan", "Nama sudah terdaftar")
                self.clear_nama()
                return

            if cari_nohp:
                QMessageBox.warning(self, "Peringatan", "Nomor HP sudah terdaftar")
                self.clear_nohp()
                return

            if not nohp.isdigit():
                QMessageBox.warning(self, "Peringatan", "Nomor HP tidak valid")
                self.clear_nohp()
                return
            
            password = self.hash_password(password)

            # Insert data baru
            query = """
            INSERT INTO akun (nama, email, no_telp, password, verify_code, saldo, role) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """

            values = (nama, email, nohp, password, verify_code, 0, 'penumpang')
            
            self.cursor.execute(query, values)
            self.connect.commit()

            QMessageBox.information(self, "Sukses", "Pendaftaran Berhasil, Silahkan Login")
            self.clear_text()
            self.back_login()

        except mysql.connector.Error as err:
            print(f"Error: {err}")
            QMessageBox.critical(self, "Error", f"Terjadi kesalahan database: {err}")
            self.connect.rollback()

        except Exception as e:
            print(f"Error: {e}")
            QMessageBox.critical(self, "Error", f"Terjadi kesalahan: {e}")
            self.connect.rollback()
            
    
    
    def hash_password(self, password):
        # Langsung menggunakan bcrypt untuk password
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    

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
