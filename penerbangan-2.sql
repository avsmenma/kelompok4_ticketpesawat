-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jan 11, 2025 at 04:37 PM
-- Server version: 10.4.28-MariaDB
-- PHP Version: 8.0.28

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `penerbangan`
--

-- --------------------------------------------------------

--
-- Table structure for table `akun`
--

CREATE TABLE `akun` (
  `id` int(11) NOT NULL,
  `verify_code` varchar(100) NOT NULL,
  `nama` varchar(100) DEFAULT NULL,
  `password` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `no_telp` varchar(50) DEFAULT NULL,
  `saldo` int(50) DEFAULT NULL,
  `role` enum('penumpang','admin') DEFAULT 'penumpang'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `akun`
--

INSERT INTO `akun` (`id`, `verify_code`, `nama`, `password`, `email`, `no_telp`, `saldo`, `role`) VALUES
(1, '12345', 'Admin', 'wj_admin', 'admin@penerbangan.com', '2147483647', 0, 'admin');

-- --------------------------------------------------------

--
-- Table structure for table `info_penerbangan`
--

CREATE TABLE `info_penerbangan` (
  `id_penerbangan` varchar(10) NOT NULL,
  `id_maskapai` varchar(10) NOT NULL,
  `id` int(11) NOT NULL,
  `asal` varchar(50) DEFAULT NULL,
  `tujuan` varchar(50) DEFAULT NULL,
  `harga_tiket` int(10) NOT NULL,
  `jumlah_kursi_tersedia` int(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `info_penerbangan`
--

INSERT INTO `info_penerbangan` (`id_penerbangan`, `id_maskapai`, `id`, `asal`, `tujuan`, `harga_tiket`, `jumlah_kursi_tersedia`) VALUES
('P001', 'M001', 0, 'Pontianak', 'Jakarta', 1400000, 120),
('P002', 'M002', 0, 'Banda Aceh', 'Jakarta', 1800000, 140),
('P003', 'M003', 0, 'Bali', 'Medan', 2400000, 138),
('P004', 'M004', 0, 'Bali', 'Jakarta', 1500000, 156),
('P005', 'M005', 0, 'Pontianak', 'Padang', 1500000, 122),
('P006', 'M005', 0, 'Surabaya', 'Yogyakarta', 1200000, 150),
('P007', 'M007', 0, 'Medan', 'Bandung', 1800000, 140),
('P008', 'M001', 0, 'Surabaya', 'Medan', 1300000, 160),
('P009', 'M002', 0, 'Balikpapan', 'Jakarta', 1450000, 135),
('P010', 'M003', 0, 'Semarang', 'Makassar', 1700000, 125),
('P011', 'M004', 0, 'Surabaya', 'Yogyakarta', 1700000, 110),
('P012', 'M005', 0, 'Surabaya', 'Yogyakarta', 1500000, 140),
('P013', 'M006', 0, 'Lampung', 'Palembang', 900000, 130),
('P014', 'M007', 0, 'Lampung', 'Palembang', 1000000, 115),
('P015', 'M001', 0, 'Jayapura', 'Makassar', 2700000, 120),
('P016', 'M002', 0, 'Jakarta', 'Manado', 2300000, 125),
('P017', 'M003', 0, 'Jakarta', 'Manado', 1900000, 140),
('P018', 'M004', 0, 'Batam', 'Jakarta', 1500000, 150),
('P019', 'M005', 0, 'Batam', 'Jakarta', 2200000, 135),
('P020', 'M006', 0, 'Padang', 'Palembang', 1400000, 145),
('P021', 'M007', 0, 'Pekanbaru', 'Medan', 1100000, 140),
('P022', 'M001', 0, 'Banjarmasin', 'Bandung', 1550000, 160),
('P023', 'M002', 0, 'Solo', 'Jakarta', 1000000, 130),
('P024', 'M003', 0, 'Kupang', 'Surabaya', 2000000, 140),
('P025', 'M004', 0, 'Pontianak', 'Semarang', 1200000, 125),
('P026', 'M005', 0, 'Makassar', 'Banjarmasin', 1450000, 140),
('P027', 'M001', 0, 'Makassar', 'Banjarmasin', 2500000, 130),
('P028', 'M007', 0, 'Makassar', 'Banjarmasin', 1750000, 140),
('P029', 'M001', 0, 'Sorong', 'Makassar', 3000000, 110),
('P030', 'M002', 0, 'Jakarta', 'Balikpapan', 1350000, 145),
('P031', 'M003', 0, 'Bandung', 'Medan', 2000000, 130),
('P032', 'M004', 0, 'Bandung', 'Medan', 2400000, 115),
('P033', 'M005', 0, 'Makassar', 'Kupang', 1500000, 140),
('P034', 'M006', 0, 'Pontianak', 'Sorong', 3200000, 100),
('P035', 'M007', 0, 'Ambon', 'Jayapura', 2700000, 120);

-- --------------------------------------------------------

--
-- Table structure for table `jadwal_penerbangan`
--

CREATE TABLE `jadwal_penerbangan` (
  `id_penerbangan` varchar(10) DEFAULT NULL,
  `tgl_keberangkatan` date DEFAULT NULL,
  `jam_berangkat` time DEFAULT NULL,
  `jam_sampai` time DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `jadwal_penerbangan`
--

INSERT INTO `jadwal_penerbangan` (`id_penerbangan`, `tgl_keberangkatan`, `jam_berangkat`, `jam_sampai`) VALUES
('P001', '2025-01-01', '14:00:00', '15:30:00'),
('P002', '2025-01-02', '19:30:00', '21:30:00'),
('P003', '2025-01-03', '11:30:00', '14:00:00'),
('P004', '2025-01-03', '13:45:00', '15:15:00'),
('P005', '2025-01-04', '13:20:00', '15:45:00'),
('P006', '2025-01-05', '08:00:00', '09:15:00'),
('P007', '2025-01-05', '14:30:00', '16:30:00'),
('P008', '2025-01-05', '10:00:00', '11:30:00'),
('P009', '2025-01-05', '18:00:00', '19:45:00'),
('P010', '2025-01-05', '07:00:00', '09:30:00'),
('P011', '2025-01-06', '11:15:00', '13:45:00'),
('P012', '2025-01-06', '15:00:00', '16:45:00'),
('P013', '2025-01-06', '09:00:00', '10:00:00'),
('P014', '2025-01-07', '13:45:00', '16:15:00'),
('P015', '2025-01-07', '06:00:00', '09:00:00'),
('P016', '2025-01-08', '19:00:00', '22:00:00'),
('P017', '2025-01-08', '12:30:00', '14:15:00'),
('P018', '2025-01-08', '17:00:00', '18:45:00'),
('P019', '2025-01-08', '08:30:00', '11:30:00'),
('P020', '2025-01-08', '10:45:00', '12:15:00'),
('P021', '2025-01-09', '09:00:00', '10:15:00'),
('P022', '2025-01-09', '14:15:00', '16:00:00'),
('P023', '2025-01-09', '07:45:00', '08:45:00'),
('P024', '2025-01-10', '11:30:00', '14:00:00'),
('P025', '2025-01-10', '06:15:00', '08:00:00'),
('P026', '2025-01-10', '13:30:00', '15:15:00'),
('P027', '2025-01-10', '09:45:00', '12:30:00'),
('P028', '2025-01-10', '16:00:00', '18:00:00'),
('P029', '2025-01-10', '08:00:00', '11:00:00'),
('P030', '2025-01-11', '07:30:00', '09:15:00'),
('P031', '2025-01-11', '15:00:00', '17:30:00'),
('P032', '2025-01-11', '10:45:00', '13:30:00'),
('P033', '2025-01-11', '11:30:00', '13:30:00'),
('P034', '2025-01-12', '06:00:00', '08:30:00'),
('P035', '2000-01-01', '09:15:00', '12:15:00');

-- --------------------------------------------------------

--
-- Table structure for table `maskapai`
--

CREATE TABLE `maskapai` (
  `id_maskapai` varchar(10) NOT NULL,
  `nama_maskapai` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `maskapai`
--

INSERT INTO `maskapai` (`id_maskapai`, `nama_maskapai`) VALUES
('M001', 'Garuda Indonesia'),
('M002', 'Lion Air'),
('M003', 'Super Air Jet'),
('M004', 'Sriwijaya Air'),
('M005', 'Citilink'),
('M006', 'Batik Air'),
('M007', 'NAM Air');

-- --------------------------------------------------------

--
-- Table structure for table `transaksi`
--

CREATE TABLE `transaksi` (
  `id_transaksi` int(11) NOT NULL,
  `id_penerbangan` varchar(10) NOT NULL,
  `jumlah_tiket` int(10) DEFAULT NULL,
  `total_harga` int(10) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `akun`
--
ALTER TABLE `akun`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `info_penerbangan`
--
ALTER TABLE `info_penerbangan`
  ADD PRIMARY KEY (`id_penerbangan`);

--
-- Indexes for table `maskapai`
--
ALTER TABLE `maskapai`
  ADD PRIMARY KEY (`id_maskapai`);

--
-- Indexes for table `transaksi`
--
ALTER TABLE `transaksi`
  ADD PRIMARY KEY (`id_transaksi`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `akun`
--
ALTER TABLE `akun`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `transaksi`
--
ALTER TABLE `transaksi`
  MODIFY `id_transaksi` int(11) NOT NULL AUTO_INCREMENT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
