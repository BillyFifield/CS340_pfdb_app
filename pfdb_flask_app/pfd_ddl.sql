-- MariaDB dump 10.19  Distrib 10.4.25-MariaDB, for Linux (x86_64)
--
-- Host: classmysql.engr.oregonstate.edu    Database: cs340_fifieldb
-- ------------------------------------------------------
-- Server version 10.6.8-MariaDB-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `Games`
--
SET FOREIGN_KEY_CHECKS=0;
SET AUTOCOMMIT = 0;

DROP TABLE IF EXISTS `Games`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Games` (
  `game_id` int(11) NOT NULL AUTO_INCREMENT,
  `home_team_id` int(11) NOT NULL,
  `away_team_id` int(11) NOT NULL,
  `home_score` int(11) NOT NULL,
  `away_score` int(11) NOT NULL,
  `date` date NOT NULL,
  `season_year` int(11) NOT NULL,
  PRIMARY KEY (`game_id`),
  UNIQUE KEY `game_id` (`game_id`),
  KEY `season_year` (`season_year`),
  KEY `home_team_id` (`home_team_id`),
  KEY `away_team_id` (`away_team_id`),
  CONSTRAINT `Games_ibfk_1` FOREIGN KEY (`season_year`) REFERENCES `Seasons` (`season_year`) ON DELETE CASCADE,
  CONSTRAINT `Games_ibfk_2` FOREIGN KEY (`home_team_id`) REFERENCES `Teams` (`team_id`) ON DELETE CASCADE,
  CONSTRAINT `Games_ibfk_3` FOREIGN KEY (`away_team_id`) REFERENCES `Teams` (`team_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Games`
--

LOCK TABLES `Games` WRITE;
/*!40000 ALTER TABLE `Games` DISABLE KEYS */;
INSERT INTO `Games` VALUES (1,1,2,24,10,'2015-02-05',2015),(2,4,2,35,10,'2023-02-06',2023),(3,2,3,2,53,'2022-10-15',2022);
/*!40000 ALTER TABLE `Games` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Players`
--

DROP TABLE IF EXISTS `Players`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Players` (
  `player_id` int(11) NOT NULL AUTO_INCREMENT,
  `fname` varchar(50) NOT NULL,
  `lname` varchar(50) NOT NULL,
  `team_id` int(11) DEFAULT NULL,
  `primary_position` varchar(25) NOT NULL,
  UNIQUE KEY `player_id` (`player_id`),
  UNIQUE KEY `team_id` (`team_id`),
  CONSTRAINT `Players_ibfk_1` FOREIGN KEY (`team_id`) REFERENCES `Teams` (`team_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Players`
--

LOCK TABLES `Players` WRITE;
/*!40000 ALTER TABLE `Players` DISABLE KEYS */;
INSERT INTO `Players` VALUES (1,'Russell','Wilson',1,'QB'),(2,'Najee','Harris',3,'RB'),(3,'Derrick','Henry',2,'RB'),(4,'Devonta','Smith',5,'WR');
/*!40000 ALTER TABLE `Players` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Players_Games_Stats`
--

DROP TABLE IF EXISTS `Players_Games_Stats`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Players_Games_Stats` (
  `player_stats_id` int(11) NOT NULL AUTO_INCREMENT,
  `player_id` int(11) NOT NULL,
  `game_id` int(11) NOT NULL,
  `passing_yard_total` int(11) DEFAULT NULL,
  `passing_td_total` int(11) DEFAULT NULL,
  `rushing_yard_total` int(11) DEFAULT NULL,
  `rushing_td_total` int(11) DEFAULT NULL,
  `receiving_yard_total` int(11) DEFAULT NULL,
  `receiving_td_total` int(11) DEFAULT NULL,
  PRIMARY KEY (`player_stats_id`),
  UNIQUE KEY `player_stats_id` (`player_stats_id`),
  KEY `player_id` (`player_id`),
  KEY `game_id` (`game_id`),
  CONSTRAINT `Players_Games_Stats_ibfk_1` FOREIGN KEY (`player_id`) REFERENCES `Players` (`player_id`) ON DELETE CASCADE,
  CONSTRAINT `Players_Games_Stats_ibfk_2` FOREIGN KEY (`game_id`) REFERENCES `Games` (`game_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Players_Games_Stats`
--

LOCK TABLES `Players_Games_Stats` WRITE;
/*!40000 ALTER TABLE `Players_Games_Stats` DISABLE KEYS */;
INSERT INTO `Players_Games_Stats` VALUES (1,1,1,350,4,50,1,0,0),(2,3,1,0,0,275,3,25,1),(3,2,3,10,1,150,2,50,1);
/*!40000 ALTER TABLE `Players_Games_Stats` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Seasons`
--

DROP TABLE IF EXISTS `Seasons`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Seasons` (
  `season_year` int(11) NOT NULL,
  `super_bowl_champ` int(11) DEFAULT NULL,
  `super_bowl_runner_up` int(11) DEFAULT NULL,
  PRIMARY KEY (`season_year`),
  KEY `super_bowl_champ` (`super_bowl_champ`),
  KEY `super_bowl_runner_up` (`super_bowl_runner_up`),
  CONSTRAINT `Seasons_ibfk_1` FOREIGN KEY (`super_bowl_champ`) REFERENCES `Teams` (`team_id`) ON DELETE CASCADE,
  CONSTRAINT `Seasons_ibfk_2` FOREIGN KEY (`super_bowl_runner_up`) REFERENCES `Teams` (`team_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Seasons`
--

LOCK TABLES `Seasons` WRITE;
/*!40000 ALTER TABLE `Seasons` DISABLE KEYS */;
INSERT INTO `Seasons` VALUES (2023,4,2), (2015,1,4),(2022,3,4);
/*!40000 ALTER TABLE `Seasons` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Teams`
--

DROP TABLE IF EXISTS `Teams`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Teams` (
  `team_id` int(11) NOT NULL AUTO_INCREMENT,
  `team_city` varchar(25) NOT NULL,
  `team_name` varchar(25) NOT NULL,
  `conference` varchar(25) NOT NULL,
  PRIMARY KEY (`team_id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Teams`
--

LOCK TABLES `Teams` WRITE;
/*!40000 ALTER TABLE `Teams` DISABLE KEYS */;
INSERT INTO `Teams` VALUES (1,'Denver','Broncos','AFC'),(2,'Tennessee','Titans','AFC'),(3,'Pittsburgh','Steelers','AFC'),(4,'Detroit','Lions','NFC'),(5,'Philadelphia','Eagles','NFC');
/*!40000 ALTER TABLE `Teams` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

SET FOREIGN_KEY_CHECKS=1;
COMMIT;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-07-11 17:38:46
