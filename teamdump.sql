-- MySQL dump 10.13  Distrib 5.1.62, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: jtaddei_tecmo
-- ------------------------------------------------------
-- Server version	5.1.62-0ubuntu0.11.10.1-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `players_pro_team`
--

DROP TABLE IF EXISTS `players_pro_team`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `players_pro_team` (
  `short` varchar(3) NOT NULL,
  `long` varchar(45) NOT NULL,
  `bye` int(11) NOT NULL,
  `wins` int(11) NOT NULL,
  `loss` int(11) NOT NULL,
  `tie` int(11) NOT NULL,
  PRIMARY KEY (`short`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `players_pro_team`
--

LOCK TABLES `players_pro_team` WRITE;
/*!40000 ALTER TABLE `players_pro_team` DISABLE KEYS */;
INSERT INTO `players_pro_team` VALUES ('ARZ','Arizona Cardinals',6,1,0,0),('ATL','Atlanta Falcons',8,1,0,0),('BAL','Baltimore Ravens',5,0,1,0),('BUF','Buffalo Bills',7,1,0,0),('CAR','Carolina Panthers',9,0,1,0),('CHI','Chicago Bears',8,0,1,0),('CIN','Cincinnati Bengals',7,1,0,0),('CLE','Cleveland Browns',5,0,1,0),('DAL','Dallas Cowboys',5,0,1,0),('DEN','Denver Broncos',6,1,0,0),('DET','Detroit Lions',9,0,1,0),('GB','Green Bay Packers',8,0,1,0),('HOU','Houston Texans',11,1,0,0),('IND','Indianapolis Colts',11,0,1,0),('JAC','Jacksonville Jaguars',9,1,0,0),('KC','Kansas City Chiefs',6,0,1,0),('MIA','Miami Dolphins',5,0,1,0),('MIN','Minnesota Vikings',9,1,0,0),('NE','New England Patriots',7,1,0,0),('NO','New Orleans Saints',11,1,0,0),('NYG','New York Giants',7,1,0,0),('NYJ','New York Jets',8,1,0,0),('OAK','Oakland Raiders',8,0,1,0),('PHI','Philadelphia Eagles',7,0,1,0),('PIT','Pittsburgh Steelers',11,1,0,0),('SD','San Diego Chargers',6,0,1,0),('SEA','Seattle Seahawks',6,1,0,0),('SF','San Francisco 49ers',7,0,1,0),('STL','St. Louis Rams',5,1,0,0),('TB','Tampa Bay Buccaneers',8,1,0,0),('TEN','Tennessee Titans',6,0,1,0),('WAS','Washington Redskins',5,0,1,0);
/*!40000 ALTER TABLE `players_pro_team` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2012-06-07 20:11:53
