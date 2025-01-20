DROP DATABASE IF EXISTS `unitywassim`;
CREATE DATABASE IF NOT EXISTS `unitywassim` 
USE `unitywassim`;

-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Hôte : localhost:3306
-- Généré le : lun. 20 jan. 2025 à 00:02
-- Version du serveur : 5.7.39
-- Version de PHP : 8.1.31

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données : `unitywassim`
--

-- --------------------------------------------------------

--
-- Structure de la table `commentaire`
--


CREATE TABLE `commentaire` (
  `id_commentaire` int(11) NOT NULL,
  `id_user` int(11) NOT NULL,
  `commentaire` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Déchargement des données de la table `commentaire`
--

INSERT INTO `commentaire` (`id_commentaire`, `id_user`, `commentaire`) VALUES
(1, 1, 'WS'),
(2, 1, 'SALUT TEST depuis unity'),
(3, 1, 'test3'),
(13, 1, 'sasa');

-- --------------------------------------------------------

--
-- Structure de la table `user`
--

CREATE TABLE `user` (
  `id` int(11) NOT NULL,
  `login` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Déchargement des données de la table `user`
--

INSERT INTO `user` (`id`, `login`, `password`) VALUES
(1, 'WSM', 'scrypt:32768:8:1$DZ8ia8NZV7nbA7bN$763bd81128208c21bb594562124cd1cd09fe76b008aeb449eecaf23a49feba37bf0f519338c4de0524397159d350fc1adf832e81efbed1ec16e530e3bbe136a1'),
(2, 'WSM2', 'scrypt:32768:8:1$WSoMKmMB398fDOVg$9b79154bba1dc410137ac99f546e10fb70e05e817674e9e695465ecf8d5ac949bac197f3afba4f3f54e7defd6fbbc4fa83a237320d741e5787f10684c3c4097c'),
(3, 'WSM', 'scrypt:32768:8:1$528MhdXnc9O7JoWz$9a1fa43bbc7b2e3c8b8710ce0a18d914d877fe2624aa505f66a973da3efefc62b5c24e6be28835d025f25542845467af96b388269e6be146baae78312e13251b');

--
-- Index pour les tables déchargées
--

--
-- Index pour la table `commentaire`
--
ALTER TABLE `commentaire`
  ADD PRIMARY KEY (`id_commentaire`),
  ADD KEY `FK1_user_comment` (`id_user`);

--
-- Index pour la table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT pour les tables déchargées
--

--
-- AUTO_INCREMENT pour la table `commentaire`
--
ALTER TABLE `commentaire`
  MODIFY `id_commentaire` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT pour la table `user`
--
ALTER TABLE `user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- Contraintes pour les tables déchargées
--

--
-- Contraintes pour la table `commentaire`
--
ALTER TABLE `commentaire`
  ADD CONSTRAINT `FK1_user_comment` FOREIGN KEY (`id_user`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
