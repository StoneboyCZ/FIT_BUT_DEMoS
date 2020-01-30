-- phpMyAdmin SQL Dump
-- version 4.8.0.1
-- https://www.phpmyadmin.net/
--
-- Hostiteľ: 127.0.0.1
-- Čas generovania: Št 16.Máj 2019, 01:28
-- Verzia serveru: 10.1.32-MariaDB
-- Verzia PHP: 5.6.36

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Databáza: `dev_ruian`
--

-- --------------------------------------------------------

--
-- Štruktúra tabuľky pre tabuľku `cadastral_coordinates`
--

CREATE TABLE `cadastral_coordinates` (
  `id` int(11) NOT NULL,
  `coordinate` double NOT NULL,
  `id_cadastral_territory` int(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Štruktúra tabuľky pre tabuľku `cadastral_territory`
--

CREATE TABLE `cadastral_territory` (
  `id` int(6) NOT NULL,
  `name` varchar(48) NOT NULL,
  `from_date` datetime NOT NULL,
  `creation_date` datetime DEFAULT NULL,
  `digital_map` tinyint(1) NOT NULL,
  `id_village` int(6) NOT NULL,
  `id_fall` int(11) NOT NULL,
  `id_geometry` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Štruktúra tabuľky pre tabuľku `district`
--

CREATE TABLE `district` (
  `id` int(4) NOT NULL,
  `name` varchar(32) NOT NULL,
  `from_date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `creation_date` datetime NOT NULL,
  `nuts_lau` varchar(6) NOT NULL,
  `id_vusc` int(3) NOT NULL,
  `id_region_1960` int(3) NOT NULL,
  `id_geometry` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Štruktúra tabuľky pre tabuľku `district_administrative`
--

CREATE TABLE `district_administrative` (
  `id` int(3) NOT NULL,
  `name` varchar(32) NOT NULL,
  `from_date` datetime NOT NULL,
  `creation_date` datetime NOT NULL,
  `nuts_lau` varchar(6) NOT NULL,
  `id_momc` int(6) NOT NULL,
  `id_village` int(6) NOT NULL,
  `id_geometry` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Štruktúra tabuľky pre tabuľku `fall`
--

CREATE TABLE `fall` (
  `id` int(11) NOT NULL,
  `id_main` int(11) NOT NULL,
  `name` varchar(48) NOT NULL,
  `no_of_fall` int(2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Štruktúra tabuľky pre tabuľku `geometry`
--

CREATE TABLE `geometry` (
  `id` int(11) NOT NULL,
  `x_axis` double NOT NULL,
  `y_axis` double NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Štruktúra tabuľky pre tabuľku `logs`
--

CREATE TABLE `logs` (
  `id` int(11) NOT NULL,
  `date` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Štruktúra tabuľky pre tabuľku `momc`
--

CREATE TABLE `momc` (
  `id` int(6) NOT NULL,
  `name` varchar(32) NOT NULL,
  `from_date` datetime NOT NULL,
  `creation_date` datetime NOT NULL,
  `flag_text` text,
  `sign_text` text,
  `id_fall` int(11) NOT NULL,
  `id_mop` int(3) DEFAULT NULL,
  `id_village` int(6) NOT NULL,
  `id_district_administrative` int(6) DEFAULT NULL,
  `id_geometry` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Štruktúra tabuľky pre tabuľku `mop`
--

CREATE TABLE `mop` (
  `id` int(3) NOT NULL,
  `name` varchar(32) NOT NULL,
  `from_date` datetime NOT NULL,
  `creation_date` datetime NOT NULL,
  `id_village` int(6) NOT NULL,
  `id_geometry` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Štruktúra tabuľky pre tabuľku `orp`
--

CREATE TABLE `orp` (
  `id` int(4) NOT NULL,
  `name` varchar(48) NOT NULL,
  `from_date` datetime NOT NULL,
  `creation_date` datetime NOT NULL,
  `id_geometry` int(11) NOT NULL,
  `id_vusc` int(3) NOT NULL,
  `id_village` int(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Štruktúra tabuľky pre tabuľku `pou`
--

CREATE TABLE `pou` (
  `id` int(4) NOT NULL,
  `name` varchar(48) NOT NULL,
  `from_date` datetime NOT NULL,
  `creation_date` datetime NOT NULL,
  `id_geometry` int(11) NOT NULL,
  `id_orp` int(4) NOT NULL,
  `id_village` int(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Štruktúra tabuľky pre tabuľku `region`
--

CREATE TABLE `region` (
  `id` int(3) NOT NULL,
  `name` varchar(32) NOT NULL,
  `from_date` datetime NOT NULL,
  `creation_date` datetime NOT NULL,
  `nuts_lau` varchar(6) NOT NULL,
  `id_geometry` int(11) NOT NULL,
  `id_state` int(2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Štruktúra tabuľky pre tabuľku `region_1960`
--

CREATE TABLE `region_1960` (
  `id` int(3) NOT NULL,
  `name` varchar(32) NOT NULL,
  `from_date` datetime NOT NULL,
  `creation_date` datetime NOT NULL,
  `id_geometry` int(11) NOT NULL,
  `id_state` int(2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Štruktúra tabuľky pre tabuľku `state`
--

CREATE TABLE `state` (
  `id` int(2) NOT NULL,
  `name` varchar(32) NOT NULL,
  `from_date` datetime NOT NULL,
  `creation_date` datetime NOT NULL,
  `nuts_lau` varchar(6) NOT NULL,
  `id_geometry` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Štruktúra tabuľky pre tabuľku `status`
--

CREATE TABLE `status` (
  `id` int(11) NOT NULL,
  `name` varchar(32) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Štruktúra tabuľky pre tabuľku `village`
--

CREATE TABLE `village` (
  `id` int(6) NOT NULL,
  `name` varchar(48) NOT NULL,
  `from_date` datetime NOT NULL,
  `creation_date` datetime DEFAULT NULL,
  `nuts_lau` varchar(6) NOT NULL,
  `flag_text` text,
  `sign_text` text,
  `id_fall` int(11) NOT NULL,
  `id_pou` int(4) NOT NULL,
  `id_status` int(11) NOT NULL,
  `id_district` int(4) NOT NULL,
  `id_geometry` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Štruktúra tabuľky pre tabuľku `village_coordinates`
--

CREATE TABLE `village_coordinates` (
  `id` int(11) NOT NULL,
  `coordinate` double NOT NULL,
  `id_village` int(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Štruktúra tabuľky pre tabuľku `village_parts`
--

CREATE TABLE `village_parts` (
  `id` int(6) NOT NULL,
  `name` varchar(48) NOT NULL,
  `from_date` datetime NOT NULL,
  `id_fall` int(11) NOT NULL,
  `id_village` int(6) NOT NULL,
  `id_geometry` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Štruktúra tabuľky pre tabuľku `village_streets`
--

CREATE TABLE `village_streets` (
  `id` int(7) NOT NULL,
  `name` varchar(255) NOT NULL,
  `from_date` datetime NOT NULL,
  `id_village` int(6) NOT NULL,
  `id_geometry` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Štruktúra tabuľky pre tabuľku `village_type`
--

CREATE TABLE `village_type` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `shortcut` varchar(255) NOT NULL,
  `description` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Štruktúra tabuľky pre tabuľku `vusc`
--

CREATE TABLE `vusc` (
  `id` int(3) NOT NULL,
  `name` varchar(32) NOT NULL,
  `from_date` datetime NOT NULL,
  `creation_date` datetime NOT NULL,
  `nuts_lau` varchar(6) NOT NULL,
  `id_geometry` int(11) NOT NULL,
  `id_region` int(3) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Štruktúra tabuľky pre tabuľku `zsj`
--

CREATE TABLE `zsj` (
  `id` int(6) NOT NULL,
  `name` int(48) NOT NULL,
  `from_date` datetime NOT NULL,
  `creation_date` datetime DEFAULT NULL,
  `acreage` mediumint(18) NOT NULL,
  `id_cadastral_territory` int(6) NOT NULL,
  `id_geometry` int(11) DEFAULT NULL,
  `id_zsj_character` int(4) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Štruktúra tabuľky pre tabuľku `zsj_character`
--

CREATE TABLE `zsj_character` (
  `id` int(11) NOT NULL,
  `name` varchar(70) NOT NULL,
  `validity_start_date` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Kľúče pre exportované tabuľky
--

--
-- Indexy pre tabuľku `cadastral_coordinates`
--
ALTER TABLE `cadastral_coordinates`
  ADD PRIMARY KEY (`id`);

--
-- Indexy pre tabuľku `cadastral_territory`
--
ALTER TABLE `cadastral_territory`
  ADD PRIMARY KEY (`id`);

--
-- Indexy pre tabuľku `district`
--
ALTER TABLE `district`
  ADD PRIMARY KEY (`id`);

--
-- Indexy pre tabuľku `district_administrative`
--
ALTER TABLE `district_administrative`
  ADD PRIMARY KEY (`id`);

--
-- Indexy pre tabuľku `fall`
--
ALTER TABLE `fall`
  ADD PRIMARY KEY (`id`);

--
-- Indexy pre tabuľku `geometry`
--
ALTER TABLE `geometry`
  ADD PRIMARY KEY (`id`);

--
-- Indexy pre tabuľku `logs`
--
ALTER TABLE `logs`
  ADD PRIMARY KEY (`id`);

--
-- Indexy pre tabuľku `momc`
--
ALTER TABLE `momc`
  ADD PRIMARY KEY (`id`);

--
-- Indexy pre tabuľku `mop`
--
ALTER TABLE `mop`
  ADD PRIMARY KEY (`id`);

--
-- Indexy pre tabuľku `orp`
--
ALTER TABLE `orp`
  ADD PRIMARY KEY (`id`);

--
-- Indexy pre tabuľku `pou`
--
ALTER TABLE `pou`
  ADD PRIMARY KEY (`id`);

--
-- Indexy pre tabuľku `region`
--
ALTER TABLE `region`
  ADD PRIMARY KEY (`id`);

--
-- Indexy pre tabuľku `region_1960`
--
ALTER TABLE `region_1960`
  ADD PRIMARY KEY (`id`);

--
-- Indexy pre tabuľku `state`
--
ALTER TABLE `state`
  ADD PRIMARY KEY (`id`);

--
-- Indexy pre tabuľku `status`
--
ALTER TABLE `status`
  ADD PRIMARY KEY (`id`);

--
-- Indexy pre tabuľku `village`
--
ALTER TABLE `village`
  ADD PRIMARY KEY (`id`);

--
-- Indexy pre tabuľku `village_coordinates`
--
ALTER TABLE `village_coordinates`
  ADD PRIMARY KEY (`id`);

--
-- Indexy pre tabuľku `village_parts`
--
ALTER TABLE `village_parts`
  ADD PRIMARY KEY (`id`);

--
-- Indexy pre tabuľku `village_streets`
--
ALTER TABLE `village_streets`
  ADD PRIMARY KEY (`id`);

--
-- Indexy pre tabuľku `village_type`
--
ALTER TABLE `village_type`
  ADD PRIMARY KEY (`id`);

--
-- Indexy pre tabuľku `vusc`
--
ALTER TABLE `vusc`
  ADD PRIMARY KEY (`id`);

--
-- Indexy pre tabuľku `zsj`
--
ALTER TABLE `zsj`
  ADD PRIMARY KEY (`id`);

--
-- Indexy pre tabuľku `zsj_character`
--
ALTER TABLE `zsj_character`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT pre exportované tabuľky
--

--
-- AUTO_INCREMENT pre tabuľku `cadastral_coordinates`
--
ALTER TABLE `cadastral_coordinates`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pre tabuľku `fall`
--
ALTER TABLE `fall`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=29921;

--
-- AUTO_INCREMENT pre tabuľku `geometry`
--
ALTER TABLE `geometry`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6692;

--
-- AUTO_INCREMENT pre tabuľku `logs`
--
ALTER TABLE `logs`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pre tabuľku `village_coordinates`
--
ALTER TABLE `village_coordinates`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1980800;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
