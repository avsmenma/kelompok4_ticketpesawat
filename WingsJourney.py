import mysql.connector

import sys
from PySide6.QtGui import QIcon, QPixmap, QFont
from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QPushButton,
    QLineEdit,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QDateEdit,
    QScrollArea,
    QSlider,
    QDialog,
    QDialogButtonBox,
    QToolBar,
    QFrame,
    QStackedWidget,
    QFormLayout,
    QMessageBox,
)

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import bcrypt

class Home_Page(QMainWindow):
    def __init__(self, user_data):
        super().__init__()
        self.user_data = user_data
        self.setWindowTitle("WingsJourney")
        self.setGeometry(300, 200, 1000, 500)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #e8f4fc;
            }
            QLabel#judul {
                font-family: 'Segoe UI', Arial;
                font-size: 24px;
                font-weight: bold;
                color: #2c3e50;
                padding: 5px;
            }
            QLabel#subjudul {
                font-family: 'Segoe UI', Arial;
                font-size: 14px;
                color: #7f8c8d;
                margin-bottom: 5px;
            }
            QLabel#ask {
                font-family: 'Segoe UI', Arial;
                font-size: 18px;
                font-weight: bold;
                color: #2c3e50;
                margin: 5px 0;
            }
            QLabel#hasil_pencarian {
                font-family: 'Segoe UI', Arial;
                font-size: 16px;
                font-weight: bold;
                color: #2c3e50;
                margin: 10px 0;
                padding-left: 5px;
            }
            QPushButton#hasil {
                background-color: white;
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                padding: 10px;
                font-size: 14px;
                color: #2c3e50;
                text-align: left;
                margin: 3px 0;
            }
            QPushButton#hasil:hover {
                background-color: #f8f9fa;
                border: 1px solid #3498db;
            }
            QLabel#nofind {
                font-family: 'Segoe UI', Arial;
                font-size: 14px;
                color: #95a5a6;
                padding: 10px;
            }
        """)

        self.center_window()

        # Main container with smaller margins
        main_widget = QWidget()
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 10, 20, 10)
        main_layout.setSpacing(10)

        # Header container with gradient background
        header_widget = QWidget()
        header_widget.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #3498db, stop:1 #2980b9);
                border-radius: 10px;
            }
        """)
        header_layout = QVBoxLayout()
        header_layout.setContentsMargins(15, 10, 15, 15)
        header_layout.setSpacing(5)

        # Top bar with logo and profile
        top_bar = QHBoxLayout()
        
        logo_layout = QHBoxLayout()
        self.label_judul = QLabel("WingsJourney")
        self.label_judul.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 22px;
                font-weight: bold;
                padding: 0;
            }
        """)
        logo_layout.addWidget(self.label_judul)
        
        self.button_out = QPushButton("Profile")
        self.button_out.setFixedSize(50, 50)
        self.button_out.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 255, 255, 0.2);
                border-radius: 1px;
                border: none;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.3);
            }
        """)
        self.button_out.clicked.connect(self.changePage_to_Profile)
        
        top_bar.addLayout(logo_layout)
        top_bar.addStretch()
        top_bar.addWidget(self.button_out)
        
        header_layout.addLayout(top_bar)
        
        # Subtitle and search section
        self.label_subjudul = QLabel("Your Wings to Dream Destinations.")
        self.label_subjudul.setStyleSheet("color: rgba(255, 255, 255, 0.8); font-size: 13px;")
        header_layout.addWidget(self.label_subjudul)
        
        self.question = QLabel("Mau Kemana Hari Ini?")
        self.question.setStyleSheet("color: white; font-size: 16px; font-weight: bold;")
        header_layout.addWidget(self.question)
        
        # Search container with smaller padding
        search_layout = QHBoxLayout()
        search_layout.setSpacing(10)
        
        # Styled input fields
        input_style = """
            QLineEdit {
                background-color: rgba(255, 255, 255, 0.9);
                border: none;
                border-radius: 8px;
                padding: 8px;
                font-size: 13px;
                color: #2c3e50;
            }
            QLineEdit:focus {
                background-color: white;
            }
        """
        
        self.line_from = QLineEdit()
        self.line_from.setPlaceholderText("🛫 Berangkat dari")
        self.line_from.setStyleSheet(input_style)
        search_layout.addWidget(self.line_from)
        
        self.line_to = QLineEdit()
        self.line_to.setPlaceholderText("🛬 Pergi ke")
        self.line_to.setStyleSheet(input_style)
        search_layout.addWidget(self.line_to)
        
        self.date = QDateEdit()
        self.date.setCalendarPopup(True)
        self.date.setDisplayFormat("yyyy-MM-dd")
        self.date.setStyleSheet("""
            QDateEdit {
                background-color: rgba(255, 255, 255, 0.9);
                border: none;
                border-radius: 8px;
                padding: 8px;
                font-size: 13px;
                color: #2c3e50;
            }
            QDateEdit:focus {
                background-color: white;
            }
        """)
        search_layout.addWidget(self.date)
        
        self.button_search = QPushButton("Cari")
        self.button_search.setStyleSheet("""
            QPushButton {
                background-color: #2ecc71;
                color: white;
                padding: 8px 20px;
                border: none;
                border-radius: 8px;
                font-size: 13px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
        """)
        self.button_search.clicked.connect(self.search_database)
        search_layout.addWidget(self.button_search)
        
        header_layout.addLayout(search_layout)
        header_widget.setLayout(header_layout)
        main_layout.addWidget(header_widget)

        # Results section
        results_widget = QWidget()
        results_widget.setStyleSheet("""
            QWidget {
                background-color: rgba(255, 255, 255, 0.7);
                border-radius: 10px;
            }
        """)
        results_layout = QVBoxLayout()
        results_layout.setContentsMargins(10, 5, 10, 5)
        
        self.label_pencarian = QLabel("Hasil Pencarian")
        self.label_pencarian.setObjectName("hasil_pencarian")
        results_layout.addWidget(self.label_pencarian)
        
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar:vertical {
                border: none;
                background-color: #f0f2f5;
                width: 8px;
                margin: 0;
            }
            QScrollBar::handle:vertical {
                background-color: #3498db;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #2980b9;
            }
        """)
        
        self.hasil_widget = QWidget()
        self.hasil_layout = QVBoxLayout()
        self.hasil_layout.setSpacing(5)
        self.hasil_widget.setLayout(self.hasil_layout)
        self.scroll.setWidget(self.hasil_widget)
        results_layout.addWidget(self.scroll)
        
        results_widget.setLayout(results_layout)
        main_layout.addWidget(results_widget)
        
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

    # Keep existing methods (search_database, searched, center_window, etc.)
    def search_database(self):
        kotaAsal = self.line_from.text()
        kotaTujuan = self.line_to.text()
        tanggal = self.date.text() 

        # Menghubungkan ke database
        connect = mysql.connector.connect(
            host = "localhost",
            user="root",
            password="",
            database="penerbangan"
        )
        cursor = connect.cursor()

        # Updated query to include departure and arrival times
        query = '''
        SELECT 
            asal,
            tujuan, 
            tgl_keberangkatan,
            jam_berangkat,
            jam_sampai,
            nama_maskapai,
            harga_tiket,
            jumlah_kursi_tersedia   
        FROM info_penerbangan
        JOIN jadwal_penerbangan ON info_penerbangan.id_penerbangan = jadwal_penerbangan.id_penerbangan
        JOIN maskapai ON info_penerbangan.id_maskapai = maskapai.id_maskapai
        WHERE asal LIKE %s AND tujuan LIKE %s AND tgl_keberangkatan LIKE %s
        '''
        cursor.execute(query, (f"%{kotaAsal}%",f"%{kotaTujuan}%", f"%{tanggal}%"))

        hasil = cursor.fetchall()
        connect.close()

        # Menghapus hasil pencarian sebelumnya
        for i in reversed(range(self.hasil_layout.count())):
            widget = self.hasil_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

        if hasil:
            for kota_asal, kota_tujuan, tanggal, jam_berangkat, jam_sampai, nama_maskapai, harga_tiket, jumlah_kursi_tersedia in hasil:
                # Create flight result card
                result_card = QWidget()
                result_card.setStyleSheet("""
                    QWidget {
                        background-color: white;
                        border-radius: 8px;
                        padding: 5px;
                    }
                    QWidget:hover {
                        border: 1px solid #3498db;
                    }
                """)
                card_layout = QHBoxLayout()
                card_layout.setContentsMargins(10, 10, 10, 10)

                # Left section - Airline info
                left_section = QVBoxLayout()
                airline_label = QLabel(nama_maskapai)
                airline_label.setStyleSheet("font-weight: bold; color: #2c3e50; font-size: 14px;")
                left_section.addWidget(airline_label)
                
                seats_label = QLabel(f"Tersedia: {jumlah_kursi_tersedia} kursi")
                seats_label.setStyleSheet("color: #7f8c8d; font-size: 12px;")
                left_section.addWidget(seats_label)
                card_layout.addLayout(left_section)

                # Middle section - Flight schedule
                middle_section = QVBoxLayout()
                
                # Route
                route_layout = QHBoxLayout()
                from_label = QLabel(kota_asal)
                from_label.setStyleSheet("font-weight: bold; color: #2c3e50; font-size: 13px;")
                
                arrow_label = QLabel("→")
                arrow_label.setStyleSheet("color: #3498db; font-weight: bold; margin: 0 10px;")
                
                to_label = QLabel(kota_tujuan)
                to_label.setStyleSheet("font-weight: bold; color: #2c3e50; font-size: 13px;")
                
                route_layout.addWidget(from_label)
                route_layout.addWidget(arrow_label)
                route_layout.addWidget(to_label)
                middle_section.addLayout(route_layout)

                # Time schedule
                time_layout = QHBoxLayout()
                departure_time = QLabel(f"🛫 {jam_berangkat}")
                departure_time.setStyleSheet("color: #2c3e50; font-size: 12px;")
                
                duration_arrow = QLabel("→")
                duration_arrow.setStyleSheet("color: #95a5a6; margin: 0 10px;")
                
                arrival_time = QLabel(f"🛬 {jam_sampai}")
                arrival_time.setStyleSheet("color: #2c3e50; font-size: 12px;")
                
                time_layout.addWidget(departure_time)
                time_layout.addWidget(duration_arrow)
                time_layout.addWidget(arrival_time)
                middle_section.addLayout(time_layout)
                
                card_layout.addLayout(middle_section)

                # Right section - Price and button
                right_section = QVBoxLayout()
                right_section.setAlignment(Qt.AlignRight)
                
                harga_format = f"IDR {harga_tiket:,}".replace(",", ".")
                price_label = QLabel(harga_format)
                price_label.setStyleSheet("font-weight: bold; color: #2c3e50; font-size: 14px;")
                right_section.addWidget(price_label)
                
                per_pax_label = QLabel("/pax")
                per_pax_label.setStyleSheet("color: #7f8c8d; font-size: 12px;")
                right_section.addWidget(per_pax_label)
                
                book_button = QPushButton("Pilih")
                book_button.setStyleSheet("""
                    QPushButton {
                        background-color: #3498db;
                        color: white;
                        border: none;
                        border-radius: 4px;
                        padding: 5px 15px;
                        font-size: 12px;
                        font-weight: bold;
                    }
                    QPushButton:hover {
                        background-color: #2980b9;
                    }
                """)
                book_button.clicked.connect(
                    lambda checked, 
                    asal=kota_asal, 
                    tujuan=kota_tujuan, 
                    tgl=tanggal,
                    maskapai=nama_maskapai,
                    harga=harga_tiket,
                    kursi=jumlah_kursi_tersedia: 
                        self.searched(asal, tujuan, tgl, maskapai, harga, kursi)
                )
                right_section.addWidget(book_button)
                
                card_layout.addLayout(right_section)

                # Set layout for result card
                result_card.setLayout(card_layout)
                self.hasil_layout.addWidget(result_card)
        else:
            self.tidak_ditemukan = QLabel("Tidak ada hasil yang ditemukan.")
            self.tidak_ditemukan.setAlignment(Qt.AlignCenter)
            self.tidak_ditemukan.setObjectName("nofind")
            self.hasil_layout.addWidget(self.tidak_ditemukan)

    def searched(self, asal, tujuan, tgl, maskapai, harga, kursi):
        self.transaksi = Transaksi_tiket(
            user_data=self.user_data,  # Tambahkan user_data
            asal=asal,
            tujuan=tujuan,
            tgl=tgl,
            maskapai=maskapai,
            harga=harga,
            kursi=kursi
        )
        self.transaksi.show()

    def center_window(self):
        qr = self.frameGeometry()
        screen_center = QApplication.primaryScreen().availableGeometry().center()
        qr.moveCenter(screen_center)
        self.move(qr.topLeft())

    def changePage_to_Profile(self):
        self.close()

        self.page_profile = ProfileApp(self.user_data)
        self.page_profile.show()
        
        

class MenuButton(QPushButton):
    def __init__(self, text, icon_path=None, parent=None):
        super().__init__(text, parent)
        self.setMinimumHeight(40)
        self.setCursor(Qt.PointingHandCursor)
        if icon_path:
            self.setIcon(QIcon(icon_path))
        self.setStyleSheet("""
            QPushButton {
                text-align: left;
                padding-left: 15px;
                border: none;
                background: transparent;
                color: #444;
            }
            QPushButton:hover {
                background: #f0f0f0;
            }
            QPushButton:checked {
                background: #e0e0e0;
                border-left: 3px solid #0066CC;
            }
        """)
        self.setCheckable(True)

class PageWidget(QFrame):
    def __init__(self, title, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QFrame {
                background-color: #f5f5f5;
                padding: 20px;
            }
        """)
        layout = QVBoxLayout(self)

        header = QLabel(title)
        header.setFont(QFont("Arial", 18, QFont.Bold))

        self.content = QFrame()
        self.content.setStyleSheet("""
            QFrame {
                background-color:rgb(238, 238, 238);
                border-radius: 10px;
                padding: 20px;
            }
        """)
        self.content_layout = QVBoxLayout(self.content)

        content_label = QLabel(f"This is the {title} page content")
        self.content_layout.addWidget(content_label)

        layout.addWidget(header)
        layout.addWidget(self.content)
        layout.addStretch()

class ProfilePage(PageWidget):
    def __init__(self, user_data, parent=None):
        super().__init__("Pusat Akun", parent)
        self.user_data = user_data

        while self.content_layout.count():
            item = self.content_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        name_label = QLabel(f"Nama : {self.user_data['nama']}")
        email_label = QLabel(f"Email : {self.user_data['email']}")
        phone_label = QLabel(f"Nomor HP : {self.user_data['no_telp']}")


        self.content_layout.addWidget(name_label)
        self.content_layout.addWidget(phone_label)
        self.content_layout.addWidget(email_label)
        self.content_layout.addSpacing(20)


class ProfileApp(QMainWindow):
    def __init__(self, user_data):
        super().__init__()
        self.user_data = user_data
        self.setWindowTitle("Profile Page")
        self.setMinimumSize(800, 600)

        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)

        sidebar = QFrame()
        sidebar.setMaximumWidth(250)
        sidebar.setStyleSheet("background-color: white;")
        sidebar_layout = QVBoxLayout(sidebar)

        profile_frame = QFrame()
        profile_frame.setStyleSheet("""
            QFrame {
                background: #0052A3;
                border-radius: 10px;
                margin: 10px;
                padding: 20px;
            }
        """)
        profile_layout = QVBoxLayout(profile_frame)

        # Tambahkan QLabel untuk foto profil
        profile_photo = QLabel()
        profile_pixmap = QPixmap("profilecarton.jpg")
        scaled_pixmap = profile_pixmap.scaled(150, 400, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        profile_photo.setPixmap(scaled_pixmap)
        profile_photo.setAlignment(Qt.AlignCenter)
        profile_photo.setStyleSheet("""
            QLabel {
                border-radius: 60;
                background-color: transparent;
            }
        """)

        self.button_backToDashboard = QPushButton("Back Dashboard")
        self.button_backToDashboard.setStyleSheet("""
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
        self.button_backToDashboard.move(100, 100)
        self.button_backToDashboard.clicked.connect(self.fun_button_backToDashboard)

        profile_layout.addWidget(profile_photo)
        sidebar_layout.addWidget(profile_frame)

        self.stacked_widget = QStackedWidget()

        self.menu_buttons = []
        menu_items = [
            ("Akun", "aditt.png", ProfilePage(self.user_data)),  # Pass user_data here
            ("Ganti Password", "save.png", ChangePasswordPage(self.user_data)),
        ]

        for i, (text, icon, page) in enumerate(menu_items):
            btn = MenuButton(text, icon)
            btn.setChecked(i == 0)
            btn.clicked.connect(lambda checked, idx=i: self.switch_page(idx))
            self.menu_buttons.append(btn)
            sidebar_layout.addWidget(btn)
            self.stacked_widget.addWidget(page)

        sidebar_layout.addStretch()
        sidebar_layout.addWidget(self.button_backToDashboard)
        main_layout.addWidget(sidebar)
        main_layout.addWidget(self.stacked_widget)

        main_layout.setStretch(0, 1)
        main_layout.setStretch(1, 3)

        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
        """)

    def switch_page(self, index):
        for i, btn in enumerate(self.menu_buttons):
            btn.setChecked(i == index)
        self.stacked_widget.setCurrentIndex(index)

    def fun_button_backToDashboard(self):
        self.close()

        self.backToDashboardPage = Home_Page(self.user_data)
        self.backToDashboardPage.show()

    def fun_button_historyOrder(self):
        return

    

    def fun_button_ChangePasswordUser(self):
        self.changePageToChangePassword = ChangePasswordPage(self.user_data)
        self.changePageToChangePassword.show()

    def center_window(self):
        qr = self.frameGeometry()
        screen_center = QApplication.primaryScreen().availableGeometry().center()
        qr.moveCenter(screen_center)
        self.move(qr.topLeft())

class ChangePasswordPage(PageWidget):
    def __init__(self, user_data, parent=None):
        self.user_data = user_data
        super().__init__("Ganti Password", parent)

        while self.content_layout.count():
            item = self.content_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        form_layout = QFormLayout()

        self.inputPasswordLama = QLineEdit()
        self.inputPasswordLama.setPlaceholderText("Password Lama")
        self.inputPasswordLama.setStyleSheet("""
            QLineEdit {
                background-color: white;
                color: black;
                padding: 10px;
                border-radius: 5px;
                font-weight: bold;
            }
        """)
        form_layout.addRow("Password Lama:", self.inputPasswordLama)

        self.inputPasswordBaru = QLineEdit()
        self.inputPasswordBaru.setPlaceholderText("Password Baru")
        self.inputPasswordBaru.setStyleSheet("""
            QLineEdit {
                background-color: white;
                color: black;
                padding: 10px;
                border-radius: 5px;
                font-weight: bold;
            }
        """)
        form_layout.addRow("Password Baru:", self.inputPasswordBaru)

        self.inputKonfirmasiPasswordBaru = QLineEdit()
        self.inputKonfirmasiPasswordBaru.setPlaceholderText("Konfirmasi Password Baru")
        self.inputKonfirmasiPasswordBaru.setEchoMode(QLineEdit.Password)
        self.inputKonfirmasiPasswordBaru.setStyleSheet("""
            QLineEdit {
                background-color: white;
                color: black;
                padding: 10px;
                border-radius: 5px;
                font-weight: bold;
            }
        """)
        form_layout.addRow("Konfirmasi Password:", self.inputKonfirmasiPasswordBaru)

        submit_button = QPushButton("Ganti Password")
        submit_button.clicked.connect(self.gantiPassword)
        submit_button.setStyleSheet("""
            QPushButton {
                background-color: #0066CC;
                color: white;
                padding: 8px 16px;
                border-radius: 5px;
                border: none;
            }
            QPushButton:hover {
                background-color: #0052A3;
            }
        """)

        self.content_layout.addLayout(form_layout)
        self.content_layout.addSpacing(20)
        self.content_layout.addWidget(submit_button)

    def gantiPassword(self):
        passwordLama = self.inputPasswordLama.text().strip()
        passwordBaru = self.inputPasswordBaru.text().strip()
        konfirmasiPasswordBaru = self.inputKonfirmasiPasswordBaru.text().strip()

        # Validasi input kosong
        if not passwordLama:
            QMessageBox.warning(self, "Perhatian", "Harap isi password lama Anda")
            return

        if not passwordBaru:
            QMessageBox.warning(self, "Perhatian", "Harap isi password baru")
            return

        if not konfirmasiPasswordBaru:
            QMessageBox.warning(self, "Perhatian", "Harap isi konfirmasi password baru")
            return

        # Validasi kesamaan password baru
        if passwordBaru != konfirmasiPasswordBaru:
            QMessageBox.warning(self, "Perhatian", "Password baru harus sama dengan konfirmasi password")
            return

        try:
            # Buat koneksi ke database
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="penerbangan"
            )
            cursor = connection.cursor()

            # Ambil password terenkripsi dari database
            select_query = "SELECT password FROM akun WHERE id = %s"
            cursor.execute(select_query, (self.user_data['id'],))
            result = cursor.fetchone()

            if not result:
                QMessageBox.warning(self, "Error", "User tidak ditemukan")
                return

            stored_hashed_password = result[0]

            # Verifikasi password lama menggunakan bcrypt
            if not bcrypt.checkpw(passwordLama.encode('utf-8'), stored_hashed_password.encode('utf-8')):
                QMessageBox.warning(self, "Error", "Password lama tidak sesuai")
                return

            # Generate salt dan hash password baru
            salt = bcrypt.gensalt()
            hashed_new_password = bcrypt.hashpw(passwordBaru.encode('utf-8'), salt)

            # Update password terenkripsi di database
            update_query = "UPDATE akun SET password = %s WHERE id = %s"
            cursor.execute(update_query, (hashed_new_password.decode('utf-8'), self.user_data['id']))
            connection.commit()

            QMessageBox.information(self, "Sukses", "Password berhasil diganti")

        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Error", f"Terjadi kesalahan: {err}")
            return
        
        finally:
            if 'connection' in locals() and connection.is_connected():
                cursor.close()
                connection.close()

        # Clear input fields after successful password change
        self.inputPasswordLama.clear()
        self.inputPasswordBaru.clear()
        self.inputKonfirmasiPasswordBaru.clear()

class Transaksi_tiket(QWidget):
    def __init__(self, user_data, asal, tujuan, tgl, maskapai, harga, kursi):
        super().__init__()
        self.user_data = user_data
        

        self.asal = asal
        self.tujuan = tujuan
        self.tgl = tgl
        self.maskapai = maskapai
        self.harga_tiket = harga
        self.kursi = kursi

        self.setObjectName("widget")
        self.setWindowTitle("WingsJourney")
        self.setGeometry(300, 200, 1000, 500)

        self.center_window()
        
        # Set window style
        self.setStyleSheet("""
            QWidget#widget {
                background-color: #f5f6fa;
            }
            QLabel#maskapai {
                font-family: 'Segoe UI', Arial;
                font-size: 24px;
                font-weight: bold;
                color: #2c3e50;
                padding: 5px 0;
            }
            QLabel#info {
                color: #7f8c8d;
                font-size: 14px;
                padding: 3px 0;
            }
            QLabel#jumlah {
                font-size: 14px;
                color: #2c3e50;
                padding: 5px 0;
            }
            QLabel#harga {
                font-size: 28px;
                font-weight: bold;
                color: #2c3e50;
            }
        """)

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(30, 10, 30, 20)
        main_layout.setSpacing(10)

        # Header card
        header_card = QWidget()
        header_card.setStyleSheet("""
            QWidget {
                background-color: #3498db;
                border-radius: 10px;
                padding: 15px;
            }
            QLabel {
                color: white;
            }
        """)
        header_layout = QVBoxLayout()
        header_layout.setSpacing(4)  # Reduced spacing between rows
        header_layout.setContentsMargins(10, 8, 10, 8)  # Reduced margins inside header

        # Maskapai name with icon
        maskapai_layout = QHBoxLayout()
        maskapai_layout.setSpacing(5)
        self.label_maskapai = QLabel(maskapai)
        self.label_maskapai.setStyleSheet("font-size: 20px; font-weight: bold;")
        plane_icon = QLabel("✈")
        plane_icon.setStyleSheet("font-size: 24px;")
        maskapai_layout.addWidget(plane_icon)
        maskapai_layout.addWidget(self.label_maskapai)
        maskapai_layout.addStretch()
        header_layout.addLayout(maskapai_layout)

        # Route information
        route_layout = QHBoxLayout()
        route_layout.setSpacing(8)
        from_layout = QVBoxLayout()
        from_label = QLabel(f"Dari {asal}")
        from_label.setStyleSheet("font-size: 12px; color: rgba(255,255,255,0.8);")
        from_layout.addWidget(from_label)

        arrow_label = QLabel("→")
        arrow_label.setStyleSheet("font-size: 20px; padding: 0 15px;")

        to_layout = QVBoxLayout()
        to_label = QLabel(f"Ke {tujuan}")
        to_label.setStyleSheet("font-size: 12px; color: rgba(255,255,255,0.8);")
        to_layout.addWidget(to_label)

        route_layout.addLayout(from_layout)
        route_layout.addWidget(arrow_label)
        route_layout.addLayout(to_layout)
        route_layout.addStretch()
        header_layout.addLayout(route_layout)

        # Date and seats info
        date_seat_layout = QHBoxLayout()
        date_seat_layout.setSpacing(10)
        self.label_tgl = QLabel(f"🗓 {tgl}")
        self.label_tgl.setStyleSheet("font-size: 14px;")
        self.label_kursi = QLabel(f"💺 {kursi} kursi tersedia")
        self.label_kursi.setStyleSheet("font-size: 14px;")
        date_seat_layout.addWidget(self.label_tgl)
        date_seat_layout.addWidget(self.label_kursi)
        date_seat_layout.addStretch()
        header_layout.addLayout(date_seat_layout)

        header_card.setLayout(header_layout)
        main_layout.addWidget(header_card)

        # Ticket selection card
        selection_card = QWidget()
        selection_card.setStyleSheet("""
            QWidget {
                background-color: white;
                border-radius: 10px;
                padding: 20px;
            }
        """)
        selection_layout = QVBoxLayout()

        # Seats selection
        self.label_slider = QLabel("Jumlah kursi yang ingin dipesan")
        self.label_slider.setStyleSheet("""
            font-size: 16px;
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 5px;
        """)
        selection_layout.addWidget(self.label_slider)

        seats_layout = QHBoxLayout()
        self.seats_number = QLabel("1")
        self.seats_number.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #3498db;
            padding: 0 15px;
        """)

        self.slider_tiket = QSlider(Qt.Horizontal)
        self.slider_tiket.setRange(1, 10)
        self.slider_tiket.setPageStep(1)
        self.slider_tiket.setValue(1)
        self.slider_tiket.valueChanged.connect(self.total_harga)
        self.slider_tiket.setStyleSheet("""
            QSlider::groove:horizontal {
                height: 8px;
                background: #e0e0e0;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: #3498db;
                border: none;
                width: 18px;
                margin: -5px 0;
                border-radius: 9px;
            }
            QSlider::sub-page:horizontal {
                background: #3498db;
                border-radius: 4px;
            }
        """)

        max_label = QLabel("(Maks. 10)")
        max_label.setStyleSheet("color: #95a5a6; font-size: 14px;")

        seats_layout.addWidget(self.seats_number)
        seats_layout.addWidget(self.slider_tiket)
        seats_layout.addWidget(max_label)
        selection_layout.addLayout(seats_layout)

        # Price section
        price_layout = QHBoxLayout()
        price_layout.addStretch()
        price_info = QVBoxLayout()
        price_info.setAlignment(Qt.AlignRight)
        
        total_label = QLabel("Total Pembayaran")
        total_label.setStyleSheet("color: #7f8c8d; font-size: 14px;")
        price_info.addWidget(total_label)
        
        self.harga_tiket = harga
        self.label_harga = QLabel(f"IDR {self.harga_tiket:,}".replace(",", "."))
        self.label_harga.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #2c3e50;
        """)
        price_info.addWidget(self.label_harga)
        price_layout.addLayout(price_info)
        selection_layout.addLayout(price_layout)

        selection_card.setLayout(selection_layout)
        main_layout.addWidget(selection_card)

        # Confirmation button
        self.button_ok = QPushButton("Lanjutkan Pembayaran")
        self.button_ok.setStyleSheet("""
            QPushButton {
                background-color: #2ecc71;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
        """)
        self.button_ok.clicked.connect(self.konfirmasi_pembayaran)
        main_layout.addWidget(self.button_ok)

        self.setLayout(main_layout)

    def total_harga(self):
        jumlah = self.slider_tiket.value()
        total = jumlah * self.harga_tiket
        self.seats_number.setText(str(jumlah))
        self.label_harga.setText(f"IDR {total:,}".replace(",", "."))

    def konfirmasi_pembayaran(self):
        self.close()
        jumlah = self.slider_tiket.value()
        total_harga = jumlah * self.harga_tiket
        
        # Pass user_data dan parameter lainnya
        self.konfirmasi = DialogKonfirmasi(
            user_data=self.user_data,  # Tambahkan user_data
            asal=self.asal,
            tujuan=self.tujuan,
            tgl=self.tgl,
            maskapai=self.maskapai,
            total_harga=total_harga,
            jumlah=jumlah
        )
        self.konfirmasi.show()

    def center_window(self):
        qr = self.frameGeometry()
        screen_center = QApplication.primaryScreen().availableGeometry().center()
        qr.moveCenter(screen_center)
        self.move(qr.topLeft())
        
class DialogKonfirmasi(QDialog):
    def __init__(self, user_data, asal, tujuan, tgl, maskapai, total_harga, jumlah):
        super().__init__()
        self.user_data = user_data
        self.setWindowTitle("Konfirmasi Pembayaran - WingsJourney")
        self.setGeometry(450, 200, 500, 400)
        self.setStyleSheet("""
            QDialog {
                background-color: #f5f6fa;
            }
            QLabel {
                color: #2c3e50;
            }
            QLabel#title {
                font-size: 22px;
                font-weight: bold;
                color: #2c3e50;
                margin: 10px 0;
            }
            QLabel#detail {
                font-size: 14px;
                color: #7f8c8d;
            }
            QLabel#price {
                font-size: 24px;
                font-weight: bold;
                color: #2c3e50;
                margin: 10px 0;
            }
            QPushButton {
                padding: 12px 25px;
                border-radius: 6px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton#confirm {
                background-color: #2ecc71;
                color: white;
                border: none;
            }
            QPushButton#confirm:hover {
                background-color: #27ae60;
            }
            QPushButton#cancel {
                background-color: #e74c3c;
                color: white;
                border: none;
            }
            QPushButton#cancel:hover {
                background-color: #c0392b;
            }
            QFrame#card {
                background-color: white;
                border-radius: 10px;
                padding: 20px;
            }
        """)

        # Menyimpan data untuk bukti pembayaran
        self.asal = asal
        self.tujuan = tujuan
        self.tgl = tgl
        self.maskapai = maskapai
        self.harga = total_harga
        self.kursi = jumlah

        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 30, 30, 30)

        # Card container
        card = QFrame()
        card.setObjectName("card")
        card_layout = QVBoxLayout()
        card_layout.setSpacing(15)

        # Title
        title = QLabel("Konfirmasi Pembayaran")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(title)

        # Flight details
        details_widget = QWidget()
        details_layout = QVBoxLayout()
        details_layout.setSpacing(8)

        # Maskapai info
        maskapai_label = QLabel(f"✈ {self.maskapai}")
        maskapai_label.setObjectName("detail")
        details_layout.addWidget(maskapai_label)

        # Route info
        route_label = QLabel(f"📍 {self.asal} → {self.tujuan}")
        route_label.setObjectName("detail")
        details_layout.addWidget(route_label)

        # Date and seats
        date_seat_label = QLabel(f"🗓 {self.tgl} • 💺 {self.kursi} kursi")
        date_seat_label.setObjectName("detail")
        details_layout.addWidget(date_seat_label)

        details_widget.setLayout(details_layout)
        card_layout.addWidget(details_widget)

        # Separator
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setStyleSheet("background-color: #e0e0e0;")
        card_layout.addWidget(line)

        # Total price
        price_label = QLabel(f"Total Pembayaran:\nIDR {self.harga:,}".replace(",", "."))
        price_label.setObjectName("price")
        price_label.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(price_label)

        card.setLayout(card_layout)
        main_layout.addWidget(card)

        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)

        cancel_btn = QPushButton("Batal")
        cancel_btn.setObjectName("cancel")
        cancel_btn.clicked.connect(self.reject)
        
        confirm_btn = QPushButton("Konfirmasi Pembayaran")
        confirm_btn.setObjectName("confirm")
        confirm_btn.clicked.connect(self.confirm_ok)
        
        button_layout.addWidget(cancel_btn)
        button_layout.addWidget(confirm_btn)
        
        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)
        
        self.center_window()


    # def scanbayar(self):
    #     from qr_code2 import PaymentWindow
    #     self.pageScan = PaymentWindow(self.asal, self.tujuan, self.tgl, self.maskapai, self.harga, self.kursi)
    #     self.pageScan.show()
    #     self.accept()

    def confirm_ok(self):

        QMessageBox.information(self, 'Informasi', 'Pembayaran sedang diproses')
        # Asumsikan self.user_data sudah tersedia dari proses login
        self.konfirmasi_pembayaran = Pembayaran_Sukses(
            user_data=self.user_data,  # Tambahkan user_data
            asal=self.asal,
            tujuan=self.tujuan,
            tgl=self.tgl,
            maskapai=self.maskapai,
            harga=self.harga,
            kursi=self.kursi
        )
        self.konfirmasi_pembayaran.show()
        self.accept()

    def center_window(self):
        qr = self.frameGeometry()
        screen_center = QApplication.primaryScreen().availableGeometry().center()
        qr.moveCenter(screen_center)
        self.move(qr.topLeft())



class Pembayaran_Sukses(QWidget):
    def __init__(self, user_data, asal, tujuan, tgl, maskapai, harga, kursi):
        super().__init__()

        self.user_data = user_data

        # Store data tiket yang sudah ada
        self.asal = asal
        self.tujuan = tujuan
        self.tgl = tgl
        self.maskapai = maskapai
        self.harga = harga
        self.kursi = kursi

        status = self.kirim_email_tiket(
            user_data=self.user_data,
            asal=self.asal,
            tujuan=self.tujuan,
            tgl=self.tgl,
            maskapai=self.maskapai,
            harga=self.harga,
            kursi=self.kursi,
            email=self.user_data['email']  # Mengambil email dari user_data
        )

        if not status:
            # Tampilkan pesan error jika gagal mengirim email
            QMessageBox.warning(self, "Error", "Gagal mengirim email tiket")
            return
        

        self.setObjectName("widget")
        self.setWindowTitle("Pembayaran Sukses - WingsJourney")
        self.setGeometry(300, 200, 600, 500)
        self.setStyleSheet("""
            QWidget#widget {
                background-color: #f5f6fa;
            }
            QLabel#success-icon {
                font-size: 64px;
                color: #2ecc71;
            }
            QLabel#success-title {
                font-size: 24px;
                font-weight: bold;
                color: #2c3e50;
            }
            QLabel#success-message {
                font-size: 16px;
                color: #7f8c8d;
            }
            QPushButton {
                padding: 12px 25px;
                border-radius: 6px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton#primary {
                background-color: #3498db;
                color: white;
                border: none;
            }
            QPushButton#primary:hover {
                background-color: #2980b9;
            }
            QPushButton#secondary {
                background-color: #95a5a6;
                color: white;
                border: none;
            }
            QPushButton#secondary:hover {
                background-color: #7f8c8d;
            }
            QFrame#card {
                background-color: white;
                border-radius: 10px;
                padding: 20px;
            }
        """)


        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 30, 30, 30)

        # Success card
        success_card = QFrame()
        success_card.setObjectName("card")
        success_layout = QVBoxLayout()
        success_layout.setSpacing(15)
        success_layout.setAlignment(Qt.AlignCenter)

        # Success icon
        success_icon = QLabel("✓")
        success_icon.setObjectName("success-icon")
        success_icon.setAlignment(Qt.AlignCenter)
        success_layout.addWidget(success_icon)

        # Success message
        success_title = QLabel("Pembayaran Berhasil!")
        success_title.setObjectName("success-title")
        success_title.setAlignment(Qt.AlignCenter)
        success_layout.addWidget(success_title)

        success_message = QLabel("Tiket Anda telah berhasil dipesan\nBukti Transaksi Dikirim Melalui Email")
        success_message.setObjectName("success-message")
        success_message.setAlignment(Qt.AlignCenter)
        success_layout.addWidget(success_message)

        success_card.setLayout(success_layout)
        main_layout.addWidget(success_card)

        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)

        back_btn = QPushButton("Kembali")
        back_btn.setObjectName("secondary")
        back_btn.clicked.connect(self.close)
        
        receipt_btn = QPushButton("Lihat Bukti Pembayaran")
        receipt_btn.setObjectName("primary")
        receipt_btn.setMinimumWidth(200)
        receipt_btn.clicked.connect(self.toBuktiPembayaranPage)
        
        button_layout.addWidget(back_btn)
        button_layout.addWidget(receipt_btn)
        
        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)
        
        self.center_window()

    def toBuktiPembayaranPage(self):
        self.close()

        

        # Show bukti pembayaran dialog
        dialog = QDialog(self)
        dialog.setWindowTitle("Bukti Pembayaran - WingsJourney")
        dialog.setGeometry(450, 100, 400, 500)

        def centerdialog():
            qr = dialog.frameGeometry()
            screen_center = QApplication.primaryScreen().availableGeometry().center()
            qr.moveCenter(screen_center)
            dialog.move(qr.topLeft())

        centerdialog()

        dialog.setStyleSheet("""
            QDialog {
                background-color: #f5f6fa;
            }
            QLabel#title {
                font-size: 24px;
                font-weight: bold;
                color: #2c3e50;
                margin-bottom: 20px;
            }
            QLabel#detail {
                font-size: 14px;
                color: #7f8c8d;
                padding: 8px 0;
            }
            QLabel#success {
                font-size: 16px;
                font-weight: bold;
                color: #2ecc71;
                padding: 10px 0;
            }
            QPushButton {
                padding: 12px 25px;
                border-radius: 6px;
                font-size: 14px;
                font-weight: bold;
                background-color: #3498db;
                color: white;
                border: none;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QFrame#card {
                background-color: white;
                border-radius: 10px;
                padding: 20px;
            }
        """)

        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 30, 30, 30)

        # Receipt card
        receipt_card = QFrame()
        receipt_card.setObjectName("card")
        card_layout = QVBoxLayout()

        # Title
        title = QLabel("WingsJourney")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(title)

        # Flight details
        maskapai_label = QLabel(f"Maskapai: {self.maskapai}")
        maskapai_label.setObjectName("detail")
        card_layout.addWidget(maskapai_label)

        route_label = QLabel(f"Rute: {self.asal} → {self.tujuan}")
        route_label.setObjectName("detail")
        card_layout.addWidget(route_label)

        date_label = QLabel(f"Tanggal Keberangkatan: {self.tgl}")
        date_label.setObjectName("detail")
        card_layout.addWidget(date_label)

        seats_label = QLabel(f"Jumlah kursi: {self.kursi}")
        seats_label.setObjectName("detail")
        card_layout.addWidget(seats_label)

        price_label = QLabel(f"Total harga: IDR {self.harga:,}".replace(",",".")) 
        price_label.setObjectName("detail")
        card_layout.addWidget(price_label)

        # Separator
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setStyleSheet("background-color: #e0e0e0;")
        card_layout.addWidget(line)

        # Success status
        status_label = QLabel("✓ Transaksi Berhasil")
        status_label.setObjectName("success")
        status_label.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(status_label)

        receipt_card.setLayout(card_layout)
        main_layout.addWidget(receipt_card)

        # Button
        close_btn = QPushButton("Tutup")
        close_btn.clicked.connect(dialog.accept)
        main_layout.addWidget(close_btn)

        dialog.setLayout(main_layout)
        if dialog.exec() == QDialog.Accepted:  # Menunggu dialog ditutup
            # Buat instance baru Transaksi_tiket dengan parameter yang diperlukan
            self.pagePemesanan = Transaksi_tiket(
                user_data=self.user_data,
                asal=self.asal,
                tujuan=self.tujuan,
                tgl=self.tgl,
                maskapai=self.maskapai,
                harga=self.harga,
                kursi=self.kursi
            )
            self.pagePemesanan.close()

    def kirim_email_tiket(self, user_data, asal, tujuan, tgl, maskapai, harga, kursi, email):
        self.user_data = user_data

        try:
            connect = mysql.connector.connect(
                host = "localhost",
                user="root",
                password="",
                database="penerbangan"
            )
            cursor = connect.cursor(dictionary=True)

            # Cari user berdasarkan email
            query = "SELECT id, nama, email, no_telp, password, role FROM akun WHERE email = %s"
            cursor.execute(query, (email,))
            user = cursor.fetchone()

            # Store user data
            self.user_data = {
                'id': user['id'],
                'nama': user['nama'],
                'email': user['email'],
                'no_telp': user['no_telp'],
                'role': user['role']
            }
        except Exception as e:
            print(f"Error: {e}")
            return False

        # Store tiket data
        tiket_data = {
            'asal': asal,
            'tujuan': tujuan,
            'tgl': tgl,
            'maskapai': maskapai,
            'harga': harga,
            'kursi': kursi
        }

        try:
            # Konfigurasi server email
            sender_email = "telegramstarsbusines@gmail.com"
            sender_password = "swko ydjl dvou bhus"
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(sender_email, sender_password)

            # Buat isi email
            subject = "Tiket Penerbangan Anda - WingsJourney"
            html_content = f"""
            <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #2c3e50;">
                <h2 style="color: #3498db;">Halo, {self.user_data['nama']}!</h2>
                <p>Pesanan tiket Anda telah berhasil dikonfirmasi. Berikut detailnya:</p>
                <ul style="list-style-type: none; padding: 0;">
                    <li><strong>Maskapai:</strong> {tiket_data['maskapai']}</li>
                    <li><strong>Rute:</strong> {tiket_data['asal']} → {tiket_data['tujuan']}</li>
                    <li><strong>Tanggal Keberangkatan:</strong> {tiket_data['tgl']}</li>
                    <li><strong>Jumlah Kursi:</strong> {tiket_data['kursi']}</li>
                    <li><strong>Total Harga:</strong> IDR {tiket_data['harga']:,}</li>
                </ul>
                <p>Selamat menikmati perjalanan Anda!</p>
                <p>Salam hangat,<br><strong>WingsJourney Team</strong></p>
            </body>
            </html>
            """

            # Susun email
            msg = MIMEMultipart()
            msg["From"] = sender_email
            msg["To"] = self.user_data['email']  # Gunakan email dari user_data
            msg["Subject"] = subject
            msg.attach(MIMEText(html_content, "html"))

            # Kirim email
            server.send_message(msg)
            print("Email berhasil dikirim!")
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False
        finally:
            server.quit()


    def center_window(self):
        qr = self.frameGeometry()
        screen_center = QApplication.primaryScreen().availableGeometry().center()
        qr.moveCenter(screen_center)
        self.move(qr.topLeft())


def apply_stylesheet(app, path):
    with open(path, "r") as file:
        qss = file.read()
        app.setStyleSheet(qss)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    stylesheet_path = "style.qss"
    apply_stylesheet(app, stylesheet_path)

    window = Home_Page()
    window.show()
    sys.exit(app.exec())
