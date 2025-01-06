-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jan 02, 2025 at 08:00 AM
-- Server version: 10.4.25-MariaDB
-- PHP Version: 7.4.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `education_schema`
--

-- --------------------------------------------------------

--
-- Table structure for table `aadhar_details`
--

CREATE TABLE `aadhar_details` (
  `aadhar_number` varchar(12) DEFAULT NULL,
  `gender` varchar(255) NOT NULL,
  `age_band` varchar(255) NOT NULL,
  `mobile_no` varchar(12) DEFAULT NULL,
  `state` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `aadhar_details`
--

INSERT INTO `aadhar_details` (`aadhar_number`, `gender`, `age_band`, `mobile_no`, `state`) VALUES
('756596069063', 'FEMALE', '20-30 years', '*******585', 'Maharashtra'),
('996311612023', 'MALE', '20-30 years', '*******852', 'Maharashtra');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
