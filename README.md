# 🛫 KELOMPOK 4: Sistem Pemesanan Tiket  
## ✈️ WingsJourney  
**WingsJourney** adalah aplikasi yang dirancang untuk mempermudah pengguna dalam mencari ataupun membeli tiket pesawat secara efisien dan aman. Aplikasi ini menyediakan berbagai fitur unggulan yang memungkinkan pengguna merencanakan perjalanan udara dengan lebih praktis, cepat, dan nyaman.  

---

## 🌟 Fitur Aplikasi  
- 🔑 **Menu Login dan Register**  
- ❓ **Fitur Lupa Password**  
- 🔍 **Searching Data Penerbangan (User)**  
- 🛠️ **Melihat, Menambah, dan Menghapus Data Penerbangan (Admin)**  
- 📝 **Form Pemesanan Tiket**  
- 📱 **Transaksi Tiket Menggunakan QR Code**  
- 📊 **Laporan Transaksi**  

---

## 🛠️ Tech  
Aplikasi ini dibangun dengan:  
- 🐍 **[Python]** - Bahasa pemrograman tingkat tinggi yang sederhana dan mudah dipahami, cocok untuk pengembangan web, analisis data, machine learning, dan lainnya.  
- 🗄️ **[SQL]** - Database SQL yang efisien untuk menyimpan data, sangat cocok untuk aplikasi berbasis web.  
- 🎨 **[PySide6 Framework]** - Framework untuk membangun antarmuka pengguna berbasis Python.  
- 🖌️ **[QSS]** - Style Sheets untuk menciptakan tampilan antarmuka yang menarik.  

---

## 🖥️ Requirement  
- 🧰 **Integrated Development Environment (IDE)**  
- 🐍 **Python**  
- 🛢️ **MySQL**  
- 🔧 **XAMPP**  

---

## 📥 Instalasi  
Langkah-langkah instalasi:  
1. Install **PySide6** dari library Python melalui terminal:  
    ```bash
    pip install PySide6
    ```  
2. Install library tambahan lainnya:  
    ```bash
    pip install flask
    pip install qrcode
    pip install mysql-connector-python
    pip install bcrypt
    ```  
3. Untuk menjalankan aplikasi ini, jalankan file bernama `main2.py`:  
    ```bash
    python main2.py
    ```  

---

## 📘 Cara Penggunaan Aplikasi  
1. **Install XAMPP sebagai Database**  
   - Unduh dan install aplikasi XAMPP melalui tautan berikut:  
     [Download XAMPP](https://www.apachefriends.org/download.html)  

2. **Jalankan XAMPP**  
   - Buka aplikasi XAMPP.  
   - Pada bagian modul **Apache** dan **MySQL**, klik tombol **Start** di kolom **Actions**.  

3. **Akses phpMyAdmin**  
   - Klik tombol **Admin** di modul **MySQL**. Anda akan diarahkan ke browser menuju halaman `localhost/phpMyAdmin/`.  

4. **Buat Database**  
   - Di halaman phpMyAdmin, tekan bagian **New**.  
   - Isi nama database dengan `penerbangan` dan ubah collation menjadi `utf8_general_ci`.  
   - Klik tombol **Create Database**.  

5. **Import File Database**  
   - Masuk ke database `penerbangan`.  
   - Pilih menu **Import**, lalu unggah file bernama `penerbangan-2.sql`.  
   - Gulir ke bawah dan tekan tombol **Import**.  

6. **Akses Folder Proyek**  
   - Salin alamat folder tempat Anda menyimpan file **GitHub kelompok4_ticketpesawat**.  
   - Buka terminal atau command prompt, lalu ketik:  
     ```bash
     cd [alamat_folder]
     ```  

7. **Jalankan Aplikasi**  
   - Ketik perintah berikut untuk menjalankan aplikasi:  
     ```bash
     python main2.py
     ```  

--- 

🎉 **Selamat menggunakan WingsJourney!** Semoga perjalanan Anda menyenangkan. 🌍  
