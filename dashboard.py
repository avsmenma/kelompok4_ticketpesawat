import sqlite3
import sys
from PySide6.QtGui import QIcon
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
)


class Home_Page(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("WingsJourney")
        self.setGeometry(300, 200, 700, 400)

        main_layout = QVBoxLayout()
        layout_bar = QHBoxLayout()
        layout_content = QHBoxLayout()

        # Label judul
        self.label_judul = QLabel("WingsJourney")
        self.label_judul.setObjectName("judul")
        layout_bar.addWidget(self.label_judul)

        # Logout button
        self.button_out = QPushButton("Logout")
        self.button_out.setFixedWidth(55)
        self.button_out.setObjectName("out")
        self.button_out.clicked.connect(self.close)
        layout_bar.addWidget(self.button_out)

        main_layout.addLayout(layout_bar)

        # Label sub judul
        self.label_subjudul = QLabel("Your Wings to Dream Destinations.")
        self.label_subjudul.setObjectName("subjudul")
        main_layout.addWidget(self.label_subjudul)

        # Label pertanyaan
        self.question = QLabel("Mau Kemana Hari Ini?")
        self.question.setObjectName("ask")
        main_layout.addWidget(self.question)

        # Input rute dan jadwal keberangkatan
        self.line_from = QLineEdit()
        self.line_from.setPlaceholderText("Berangkat dari")
        layout_content.addWidget(self.line_from)

        self.line_to = QLineEdit()
        self.line_to.setPlaceholderText("Pergi ke")
        layout_content.addWidget(self.line_to)

        self.date = QDateEdit()
        self.date.setCalendarPopup(True)
        self.date.setDisplayFormat("dd-MM-yyyy")
        self.date.setFixedWidth(150)
        layout_content.addWidget(self.date)

        # Tombol Pencarian Tiket 
        self.button_search = QPushButton("Cari")
        self.button_search.setIcon(QIcon("search.png"))
        self.button_search.setIconSize(QSize(12, 12))
        self.button_search.setObjectName("cari")
        self.button_search.clicked.connect(self.search_database)
        layout_content.addWidget(self.button_search)

        main_layout.addLayout(layout_content)

        # Label Hasil Pencarian
        self.label_pencarian = QLabel("Hasil Pencarian")
        self.label_pencarian.setObjectName("hasil_pencarian")
        main_layout.addWidget(self.label_pencarian)

        # Scroll area untuk pencarian
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)

        # Layout hasil pencarian
        self.hasil_widget = QWidget()
        self.hasil_widget.setObjectName("pencarian")
        self.hasil_layout = QVBoxLayout()

        self.hasil_widget.setLayout(self.hasil_layout)
        self.scroll.setWidget(self.hasil_widget)
        main_layout.addWidget(self.scroll)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

# Fungsi untuk mencari database
    def search_database(self):
        kotaAsal = self.line_from.text()
        kotaTujuan = self.line_to.text()
        tanggal = self.date.text() 

        # Menghubungkan ke database SQLite
        connect = sqlite3.connect("penerbangan.sqlite")
        cursor = connect.cursor()

        # Query data berdasarkan input pengguna
        cursor.execute('''
            SELECT kota_asal,
            kota_tujuan, 
            tanggal_keberangkatan,
            nama_maskapai,
            harga_tiket,
            jumlah_kursi_tersedia   
            FROM penerbangan
            WHERE kota_asal LIKE ? AND kota_tujuan LIKE ? AND tanggal_keberangkatan LIKE ?
        ''', (f"%{kotaAsal}%", f"%{kotaTujuan}%", f"%{tanggal}%"))

        hasil = cursor.fetchall()
        connect.close()

        # Menghapus hasil data sebelumnya
        for i in reversed(range(self.hasil_layout.count())):
            widget = self.hasil_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

        # Menampilkan hasil data yang baru
        if hasil:
            for kota_asal, kota_tujuan, tanggal, nama_maskapai, harga_tiket, jumlah_kursi_tersedia in hasil:
                harga_format = f"{harga_tiket:,}".replace(",",".") # Format angka dengan titik
                hasil_pencarian = QPushButton(f"{nama_maskapai} : {kota_asal} → {kota_tujuan} IDR {harga_format}/pax")
                hasil_pencarian.setObjectName("hasil")
                hasil_pencarian.clicked.connect(
                    lambda checked, 
                    asal=kota_asal, 
                    tujuan=kota_tujuan, 
                    tgl=tanggal,
                    maskapai=nama_maskapai,
                    kursi=jumlah_kursi_tersedia,
                    harga=harga_tiket: self.searched(asal,tujuan,tgl,maskapai,harga,kursi)
                    )
                self.hasil_layout.addWidget(hasil_pencarian)
        else:
            self.tidak_ditemukan = QLabel("Tidak ada hasil yang ditemukan.")
            self.tidak_ditemukan.setAlignment(Qt.AlignCenter)
            self.tidak_ditemukan.setObjectName("nofind")
            self.hasil_layout.addWidget(self.tidak_ditemukan)
           

    def searched(self, asal, tujuan, tgl, maskapai, harga, kursi):
        self.transaksi = Transaksi_tiket(asal, tujuan, tgl, maskapai, harga, kursi)
        self.transaksi.show()


class Transaksi_tiket(QWidget):
    def __init__(self, asal, tujuan, tgl, maskapai, harga, kursi):
        super().__init__()
        self.setObjectName("widget")
        self.setWindowTitle("WingsJourney")
        self.setGeometry(300, 200, 700, 400)

        # Menyimpan data untuk bukti pembayaran
        self.asal = asal
        self.tujuan = tujuan
        self.tgl = tgl
        self.maskapai = maskapai
        self.harga = harga
        self.kursi = kursi

        layout = QVBoxLayout()

        # Label mengenai informasi tiket
        self.label_maskapai = QLabel(maskapai)
        self.label_maskapai.setObjectName("maskapai")

        self.label_asal = QLabel(f"Kota Asal: {asal}")
        self.label_asal.setObjectName("info")

        self.label_tujuan = QLabel(f"Kota Tujuan: {tujuan}")
        self.label_tujuan.setObjectName("info")

        self.label_tgl = QLabel(f"Tanggal Keberangkatan: {tgl}")
        self.label_tgl.setObjectName("info")

        self.label_kursi = QLabel(f"Jumlah kursi yang tersedia: {kursi}")
        self.label_kursi.setObjectName("info")

        layout.addWidget(self.label_maskapai)
        layout.addWidget(self.label_asal)
        layout.addWidget(self.label_tujuan)
        layout.addWidget(self.label_tgl)
        layout.addWidget(self.label_kursi)

        # Label jumlah kursi yang ingin dipesan
        self.label_slider = QLabel("Jumlah kursi yang ingin dipesan (Maks 10): 1")
        self.label_slider.setObjectName("jumlah")
        layout.addWidget(self.label_slider)

        # Slider untuk menentukan jumlah tiket
        self.slider_tiket = QSlider(Qt.Horizontal)
        self.slider_tiket.setRange(1,10)
        self.slider_tiket.setPageStep(1)
        self.slider_tiket.setValue(1)
        self.slider_tiket.valueChanged.connect(self.total_harga)
        layout.addWidget(self.slider_tiket)

        # Label total harga tiket
        self.harga_tiket = harga
        self.label_harga = QLabel(f"IDR {self.harga_tiket:,}".replace(",","."))
        self.label_harga.setObjectName("harga")
        self.label_harga.setAlignment(Qt.AlignRight)
        layout.addWidget(self.label_harga)

        # Tombol untuk konfirmasi
        self.button_ok = QDialogButtonBox(QDialogButtonBox.Ok)
        self.button_ok.clicked.connect(self.konfirmasi_pembayaran)
        layout.addWidget(self.button_ok)

        self.setLayout(layout)
    
    def total_harga(self):
        jumlah = self.slider_tiket.value()
        total = jumlah * self.harga_tiket
        self.label_slider.setText(f"Jumlah kursi yang ingin dipesan (Maks 10): {jumlah}")
        self.label_harga.setText(f"IDR {total:,}".replace(",","."))
        

    def konfirmasi_pembayaran(self):
        jumlah = self.slider_tiket.value()
        total_harga = jumlah * self.harga_tiket
        self.konfirmasi = DialogKonfirmasi(self.asal, self.tujuan, self.tgl, self.maskapai, total_harga, jumlah)
        self.konfirmasi.show()
        

class DialogKonfirmasi(QDialog):
    def __init__(self, asal, tujuan, tgl, maskapai, total_harga, jumlah):
        super().__init__()
        self.setWindowTitle("WingsJourney")
        self.setGeometry(450, 200, 400, 300)

        # Menyimpan data untuk bukti pembayaran
        self.asal = asal
        self.tujuan = tujuan
        self.tgl = tgl
        self.maskapai = maskapai
        self.harga = total_harga
        self.kursi = jumlah

        layout = QVBoxLayout()

        # Label konfirmasi pembayaran
        self.label_konfirmasi = QLabel("Apakah Anda yakin \n untuk melanjutkan pembayaran?")
        self.label_konfirmasi.setObjectName("konfirmasi")
        self.label_konfirmasi.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label_konfirmasi)

        # Tombol opsi 
        buttons = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        self.button_opsi = QDialogButtonBox(buttons)
        self.button_opsi.accepted.connect(self.confirm_ok)
        self.button_opsi.rejected.connect(self.reject)
        layout.addWidget(self.button_opsi)

        self.setLayout(layout)

    def confirm_ok(self):
        self.konfirmasi_pembayaran = Pembayaran_Sukses(self.asal, self.tujuan, self.tgl, self.maskapai, self.harga, self.kursi)
        self.konfirmasi_pembayaran.show()

class Pembayaran_Sukses(QWidget):
    def __init__(self, asal, tujuan, tgl, maskapai, harga, kursi):
        super().__init__()
        self.setObjectName("widget")
        self.setGeometry(300, 200, 700, 400)

        # Menyimpan data untuk bukti pembayaran
        self.asal = asal
        self.tujuan = tujuan
        self.tgl = tgl
        self.maskapai = maskapai
        self.harga = harga
        self.kursi = kursi

        layout = QVBoxLayout()
        layout_button = QHBoxLayout()

        # Membuat label untuk icon
        self.label_gambar = QLabel(self)

        # Memuat gambar di QPixmap
        self.label_gambar.setObjectName("mark")
        self.label_gambar.setAlignment(Qt.AlignCenter)

        layout.addWidget(self.label_gambar)

        # Label pembayaran telah sukses
        self.label_sukses = QLabel("Pembayaran telah sukses!")
        self.label_sukses.setObjectName("sukses")
        self.label_sukses.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label_sukses)

        # Tombol untuk konfirmasi dan melihat bukti pembayaran
        self.button_kembali = QPushButton("Kembali")
        self.button_kembali.setMinimumWidth(120)
        self.button_kembali.clicked.connect(self.close)
        layout_button.addWidget(self.button_kembali)

        self.button_bukti = QPushButton("Lihat bukti pembayaran")
        self.button_bukti.setMinimumWidth(200)
        self.button_bukti.clicked.connect(self.bukti)
        layout_button.addWidget(self.button_bukti)

        layout.addLayout(layout_button)

        self.setLayout(layout)

    def bukti(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Bukti pembayaran")
        dialog.setGeometry(450, 100, 400, 500)

        layout = QVBoxLayout()

        # Label judul aplikasi
        label_judul = QLabel("WingsJourney")
        label_judul.setObjectName("judul")
        layout.addWidget(label_judul)

        # Label informasi transaksi
        label_maskapai = QLabel(f"Maskapai: {self.maskapai}")
        label_maskapai.setObjectName("bukti")

        label_rute = QLabel(f"Rute: {self.asal} → {self.tujuan}")
        label_rute.setObjectName("bukti")

        label_tgl = QLabel(f"Tanggal Keberangkatan: {self.tgl}")
        label_tgl.setObjectName("bukti")

        label_kursi = QLabel(f"Jumlah kursi: {self.kursi}")
        label_kursi.setObjectName("bukti")

        label_total = QLabel(f"Total harga: IDR {self.harga:,}".replace(",","."))
        label_total.setObjectName("bukti")

        label_sukses = QLabel("Transaksi Berhasil")
        label_sukses.setObjectName("berhasil")

        layout.addWidget(label_maskapai)
        layout.addWidget(label_rute)
        layout.addWidget(label_tgl)
        layout.addWidget(label_kursi)
        layout.addWidget(label_total)
        layout.addWidget(label_sukses)

        # Tombol konfirmasi
        button_ok = QDialogButtonBox(QDialogButtonBox.Ok)
        button_ok.accepted.connect(dialog.accept)
        layout.addWidget(button_ok)

        dialog.setLayout(layout)
        dialog.exec()

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
