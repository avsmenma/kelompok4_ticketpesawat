import mysql.connector
import sys
from PySide6.QtGui import QIcon
from PySide6.QtCore import QSize
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QPushButton,
    QLineEdit,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QTableWidget,
    QHeaderView,
    QTableWidgetItem,
    QDialog,
    QFormLayout,
    QDialogButtonBox,
    QMessageBox
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
        self.label_judul = QLabel("WingsAdmin")
        self.label_judul.setObjectName("judul")
        layout_bar.addWidget(self.label_judul)

        # Tombol logout
        self.logout = QPushButton("Logout")
        self.logout.setObjectName("out")
        self.logout.clicked.connect(self.close)
        layout_bar.addWidget(self.logout)

        main_layout.addLayout(layout_bar)

        # Label sub judul
        self.label_subjudul = QLabel("Your Wings to Dream Destinations.")
        self.label_subjudul.setObjectName("subjudul")
        main_layout.addWidget(self.label_subjudul)

        # Input rute dan jadwal keberangkatan
        self.line_id = QLineEdit()
        self.line_id.setPlaceholderText("Cari ID penerbangan")
        self.line_id.setFixedWidth(300)
        layout_content.addWidget(self.line_id)

        # Tombol tambah data
        self.button_tambah = QPushButton("Tambah Data")
        self.button_tambah.setObjectName("tambah")
        self.button_tambah.clicked.connect(self.add_data)
        layout_content.addWidget(self.button_tambah)

        # Tombol hapus data
        self.button_hapus = QPushButton("Hapus data")
        self.button_hapus.setObjectName("hapus")
        self.button_hapus.clicked.connect(self.delete_data)
        layout_content.addWidget(self.button_hapus)

        # Tombol Pencarian Tiket 
        self.button_search = QPushButton("Cari")
        self.button_search.setIcon(QIcon("search.png"))
        self.button_search.setIconSize(QSize(12, 12))
        self.button_search.setObjectName("cari")
        self.button_search.clicked.connect(self.search_database)
        layout_content.addWidget(self.button_search)

        main_layout.addLayout(layout_content)

        # Label Hasil Pencarian
        self.label_data = QLabel("Data penerbangan")
        self.label_data.setObjectName("hasil_pencarian")
        main_layout.addWidget(self.label_data)

        # Scroll area untuk pencarian
        self.table = QTableWidget()
        self.table.setColumnCount(9)
        self.table.setHorizontalHeaderLabels([
            "ID Penerbangan","Maskapai","Asal","Tujuan","Tanggal","Jam Berangkat","Jam Sampai","Harga","Jumlah kursi"
        ])

        header = self.table.horizontalHeader()
        for i in range(10):
            header.setSectionResizeMode(i, QHeaderView.Stretch)

        main_layout.addWidget(self.table)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # memuat semua data pada saat aplikasi dibuka
        self.load_data()

# Fungsi untuk memuat semua data ke tabel
    def load_data(self):
        connect = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="penerbangan"
        )
        cursor = connect.cursor()

        query = '''
        SELECT info_penerbangan.id_penerbangan,
               maskapai.nama_maskapai AS maskapai,
               info_penerbangan.asal,
               info_penerbangan.tujuan,
               jadwal_penerbangan.tgl_keberangkatan,
               jadwal_penerbangan.jam_berangkat,
               jadwal_penerbangan.jam_sampai,
               info_penerbangan.harga_tiket,
               info_penerbangan.jumlah_kursi_tersedia
        FROM info_penerbangan
        JOIN jadwal_penerbangan ON info_penerbangan.id_penerbangan = jadwal_penerbangan.id_penerbangan
        JOIN maskapai ON info_penerbangan.id_maskapai = maskapai.id_maskapai
        '''
        cursor.execute(query)
        hasil = cursor.fetchall()
        connect.close()

        self.table.setRowCount(0)
        for row_number, row_data in enumerate(hasil):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                if column_number == 7:  # Kolom harga tiket
                    data = f"{data:,}".replace(",", ".")  # Format angka dengan titik
                self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))

# Fungsi untuk menambah data penerbangan
    def add_data(self):
        dialog = QDialog(self)

        layout = QFormLayout()

        # input data penerbangan
        id_penerbangan = QLineEdit()
        layout.addRow(QLabel("ID Penerbangan:"),id_penerbangan)

        id_maskapai = QLineEdit()
        layout.addRow(QLabel("ID Maskapai:"),id_maskapai)

        asal = QLineEdit()
        layout.addRow(QLabel("Asal:"),asal)

        tujuan = QLineEdit()
        layout.addRow(QLabel("Tujuan:"),tujuan)

        tanggal = QLineEdit()
        layout.addRow(QLabel("Tanggal (YYYY-MM-DD):"),tanggal)

        jam_berangkat = QLineEdit()
        layout.addRow(QLabel("Jam Berangkat:"),jam_berangkat)

        jam_sampai = QLineEdit()
        layout.addRow(QLabel("Jam Sampai:"),jam_sampai)

        harga = QLineEdit()
        layout.addRow(QLabel("Harga:"),harga)

        kursi = QLineEdit()
        layout.addRow(QLabel("Jumlah Kursi:"),kursi)

        # Tombol untuk menyimpan
        button_box = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        layout.addRow(button_box)


        def save_data():
            # Validasi input
            if not (id_penerbangan.text().strip() and id_maskapai.text().strip() and asal.text().strip() and 
                tujuan.text().strip() and tanggal.text().strip() and jam_berangkat.text().strip() 
                and jam_sampai.text().strip and harga.text().strip() and kursi.text().strip()):
                QMessageBox.warning(self, "Peringatan", "Semua kolom harus diisi.")
                return

            try:
                connect = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="",
                    database="penerbangan"
                )
                cursor = connect.cursor()

                query = """
                    INSERT INTO info_penerbangan (id_penerbangan, id_maskapai, asal, tujuan, harga_tiket, jumlah_kursi_tersedia)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """
                cursor.execute(query, (id_penerbangan.text(), id_maskapai.text(), asal.text(), tujuan.text(), harga.text(), kursi.text()))

                # Menambahkan jadwal penerbangan
                query_jadwal = """
                    INSERT INTO jadwal_penerbangan (id_penerbangan, tgl_keberangkatan, jam_berangkat, jam_sampai)
                    VALUES (%s, %s, %s, %s)
                    """
                cursor.execute(query_jadwal, (id_penerbangan.text(), tanggal.text(), jam_berangkat.text(), jam_sampai.text()))

                connect.commit()

                QMessageBox.information(self, "Sukses", "Data berhasil ditambahkan.")
                dialog.accept()
                
                # memuat data yang baru ditambahkan
                self.load_data()

            except Exception as e:
                QMessageBox.critical(self, "Error", f"Gagal menambahkan data:\n{e}")
                dialog.reject()
            finally:
                connect.close()

        # Koneksi tombol
        button_box.accepted.connect(save_data)
        button_box.rejected.connect(dialog.reject)

        dialog.setLayout(layout)
        dialog.exec()

# Fungsi untuk menghapus data penerbangan
    def delete_data(self):
        selected_row = self.table.currentRow()

        if selected_row == -1:
            QMessageBox.warning(self, "Peringatan", "Pilih baris data yang ingin dihapus terlebih dahulu.")
            return
        
        id_penerbangan = self.table.item(selected_row,0).text()

        confirm = QMessageBox.question(
            self,
            "Konfirmasi",
            f"Apakah Anda yakin ingin menghapus data dengan ID Penerbangan {id_penerbangan}?",
            QMessageBox.Yes | QMessageBox.No,
        )

        if confirm == QMessageBox.Yes:
            try:
                connect = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="penerbangan"
                )
                cursor = connect.cursor()

                # Hapus data dari tabel `jadwal_penerbangan` terlebih dahulu karena ada hubungan dengan tabel `info_penerbangan`
                query_jadwal = "DELETE FROM jadwal_penerbangan WHERE id_penerbangan = %s"
                cursor.execute(query_jadwal, (id_penerbangan,))

                # Hapus data dari tabel `info_penerbangan`
                query_info = "DELETE FROM info_penerbangan WHERE id_penerbangan = %s"
                cursor.execute(query_info, (id_penerbangan,))

                connect.commit()

                QMessageBox.information(self, "Sukses", f"Data dengan ID Penerbangan {id_penerbangan} berhasil dihapus.")
                self.load_data()

            except Exception as e:
                QMessageBox.critical(self, "Error", f"Gagal menghapus data:\n{e}")

            finally:
                connect.close()

# Fungsi untuk mencari data penerbangan
    def search_database(self):
        id_penerbangan = self.line_id.text()

        # Menghubungkan ke database SQLite
        connect = mysql.connector.connect(
            host = "localhost",
            user="root",
            password="",
            database="penerbangan"
        )
        cursor = connect.cursor()

        # Query data berdasarkan input pengguna
        query = '''
        SELECT info_penerbangan.id_penerbangan,
               maskapai.nama_maskapai AS maskapai,
               info_penerbangan.asal,
               info_penerbangan.tujuan,
               jadwal_penerbangan.tgl_keberangkatan,
               jadwal_penerbangan.jam_berangkat,
               jadwal_penerbangan.jam_sampai,
               info_penerbangan.harga_tiket,
               info_penerbangan.jumlah_kursi_tersedia
        FROM info_penerbangan
        JOIN jadwal_penerbangan ON info_penerbangan.id_penerbangan = jadwal_penerbangan.id_penerbangan
        JOIN maskapai ON info_penerbangan.id_maskapai = maskapai.id_maskapai
        WHERE info_penerbangan.id_penerbangan LIKE %s
        '''
        cursor.execute(query, (f"%{id_penerbangan}%",))

        hasil = cursor.fetchall()
        connect.close()

        # Membersihkan tabel sebelum menambahkan data baru
        self.table.setRowCount(0)

        # Menambahkan data ke tabel
        if hasil:
            for row_number, row_data in enumerate(hasil):
                self.table.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    if column_number == 7:  # Kolom harga tiket
                        data = f"{data:,}".replace(",", ".")  # Format angka dengan titik
                    self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))

        else:
            # Jika tidak ada hasil, tambahkan baris dengan pesan "Tidak ada hasil yang ditemukan"
            self.table.setRowCount(1)
            self.table.setItem(0, 0, QTableWidgetItem("Tidak ada hasil yang ditemukan."))
            for col in range(1, self.table.columnCount()):
                self.table.setItem(0, col, QTableWidgetItem(""))


def apply_stylesheet(app, path):
    with open(path, "r") as file:
        qss = file.read()
        app.setStyleSheet(qss)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    stylesheet_path = "style_admin.qss"
    apply_stylesheet(app, stylesheet_path)

    window = Home_Page()
    window.show()
    sys.exit(app.exec())