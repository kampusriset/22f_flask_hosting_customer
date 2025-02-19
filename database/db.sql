-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Waktu pembuatan: 19 Feb 2025 pada 11.25
-- Versi server: 8.0.30
-- Versi PHP: 8.3.3

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `hosting_db`
--

-- --------------------------------------------------------

--
-- Struktur dari tabel `hosting`
--

CREATE TABLE `hosting` (
  `id` int NOT NULL,
  `user_id` int DEFAULT NULL,
  `domain` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `expiry_date` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data untuk tabel `hosting`
--

INSERT INTO `hosting` (`id`, `user_id`, `domain`, `expiry_date`) VALUES
(1, 2, 'Testing 123', '2025-03-12'),
(2, 2, 'Paket Gento', '2025-03-20'),
(3, 2, 'Ryzen Cikidaw', '2025-04-11'),
(4, 2, 'Aku Lelah', '2025-04-01'),
(5, 2, 'Aselole', '2025-06-25'),
(6, 2, 'Hokyahokya', '2025-04-02'),
(7, 2, 'Fufufafa', '2025-02-19');

-- --------------------------------------------------------

--
-- Struktur dari tabel `users`
--

CREATE TABLE `users` (
  `id` int NOT NULL,
  `username` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `password` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `role` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'user'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data untuk tabel `users`
--

INSERT INTO `users` (`id`, `username`, `password`, `role`) VALUES
(1, 'dio', '$2b$12$Ll6CTFIEHdifNS2Sme1muOPCbfIr32aPhqc.3D8NcIu27NLBh79Xi', 'user'),
(2, 'admin', '$2b$12$.PMKeZQHscOui0Z2WEPiRODRKphG9z3DaO5V2uJIM5My75.edzUi6', 'user'),
(3, 'mbelo', '$2b$12$IWOIw7FdVZjTIPTx.u6y2.PZfrIeqQ4AOhoqeOSJOBoV4rIYv8.O.', 'user');

--
-- Indexes for dumped tables
--

--
-- Indeks untuk tabel `hosting`
--
ALTER TABLE `hosting`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indeks untuk tabel `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT untuk tabel yang dibuang
--

--
-- AUTO_INCREMENT untuk tabel `hosting`
--
ALTER TABLE `hosting`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT untuk tabel `users`
--
ALTER TABLE `users`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- Ketidakleluasaan untuk tabel pelimpahan (Dumped Tables)
--

--
-- Ketidakleluasaan untuk tabel `hosting`
--
ALTER TABLE `hosting`
  ADD CONSTRAINT `hosting_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
