-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Mar 01, 2024 at 07:16 PM
-- Server version: 10.4.24-MariaDB
-- PHP Version: 8.1.6

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `4cite`
--

-- --------------------------------------------------------

--
-- Table structure for table `alembic_version`
--

CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `alembic_version`
--

INSERT INTO `alembic_version` (`version_num`) VALUES
('99ff3cdc1bc5');

-- --------------------------------------------------------

--
-- Table structure for table `booking`
--

CREATE TABLE `booking` (
  `id` int(11) NOT NULL,
  `chambre_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `datein` date NOT NULL,
  `dateout` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `chambre`
--

CREATE TABLE `chambre` (
  `id` int(11) NOT NULL,
  `numero` varchar(20) NOT NULL,
  `nb_personne` int(11) NOT NULL,
  `description` varchar(255) NOT NULL,
  `hotel_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `chambres`
--

CREATE TABLE `chambres` (
  `id` int(11) NOT NULL,
  `numero` varchar(20) NOT NULL,
  `nb_personne` int(11) NOT NULL,
  `hotel_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `hotel`
--

CREATE TABLE `hotel` (
  `id` int(11) NOT NULL,
  `location` varchar(255) NOT NULL,
  `description` varchar(255) NOT NULL,
  `create_at` datetime DEFAULT NULL,
  `name` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `image`
--

CREATE TABLE `image` (
  `id` int(11) NOT NULL,
  `name` varchar(100) DEFAULT NULL,
  `data` blob DEFAULT NULL,
  `hotel_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `id` int(11) NOT NULL,
  `pseudo` varchar(30) NOT NULL,
  `email` varchar(30) NOT NULL,
  `role` varchar(30) NOT NULL,
  `password` varchar(256) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`id`, `pseudo`, `email`, `role`, `password`) VALUES
(17, 'TestUser', 'user.user@user.fr', 'user', 'scrypt:32768:8:1$ubx97RmqdD9l6hbd$44f9795a8a9444e531fdf889e4d7260d0ca36d88384c3b0436321e7145ce5ea84b5b6a414b4d711c80a3fb3e3704f30abd3b4ef45ea96d8a94be0d5a6c1d1829'),
(18, 'TestAdmin', 'admin.admin@admin.fr', 'admin', 'scrypt:32768:8:1$bJCjUSYP6enCZsmx$2043a14c510eac7052a7e93abae846ab69536542bbe39937d886a3c7c59813267055ad1936837ee9c31652e07bdbc4dfa149ee036781b72fee5913b1f6ee9c63'),
(19, 'TestEmployee', 'employee.employee@employee.fr', 'employee', 'scrypt:32768:8:1$71A4KGjub5gnLUEN$b8a86149eb88a01ec6ec0977641dacda966934bd6f15bc55b519189228e2c0104e12d6e993625d932ed405f5fd43a5ab7727dcd9ad6121375f3b86f5eb9c8617');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `alembic_version`
--
ALTER TABLE `alembic_version`
  ADD PRIMARY KEY (`version_num`);

--
-- Indexes for table `booking`
--
ALTER TABLE `booking`
  ADD PRIMARY KEY (`id`),
  ADD KEY `chambre_id` (`chambre_id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `chambre`
--
ALTER TABLE `chambre`
  ADD PRIMARY KEY (`id`),
  ADD KEY `hotel_id` (`hotel_id`);

--
-- Indexes for table `chambres`
--
ALTER TABLE `chambres`
  ADD PRIMARY KEY (`id`),
  ADD KEY `hotel_id` (`hotel_id`);

--
-- Indexes for table `hotel`
--
ALTER TABLE `hotel`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `image`
--
ALTER TABLE `image`
  ADD PRIMARY KEY (`id`),
  ADD KEY `hotel_id` (`hotel_id`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `booking`
--
ALTER TABLE `booking`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT for table `chambre`
--
ALTER TABLE `chambre`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `chambres`
--
ALTER TABLE `chambres`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `hotel`
--
ALTER TABLE `hotel`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `image`
--
ALTER TABLE `image`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=32;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `booking`
--
ALTER TABLE `booking`
  ADD CONSTRAINT `booking_ibfk_1` FOREIGN KEY (`chambre_id`) REFERENCES `chambres` (`id`),
  ADD CONSTRAINT `booking_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`);

--
-- Constraints for table `chambre`
--
ALTER TABLE `chambre`
  ADD CONSTRAINT `chambre_ibfk_1` FOREIGN KEY (`hotel_id`) REFERENCES `hotel` (`id`);

--
-- Constraints for table `chambres`
--
ALTER TABLE `chambres`
  ADD CONSTRAINT `chambres_ibfk_1` FOREIGN KEY (`hotel_id`) REFERENCES `hotel` (`id`);

--
-- Constraints for table `image`
--
ALTER TABLE `image`
  ADD CONSTRAINT `image_ibfk_1` FOREIGN KEY (`hotel_id`) REFERENCES `hotel` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
