--
-- Table structure for table `books`
--

DROP TABLE IF EXISTS `books`;
CREATE TABLE `books` (
  `isbn` int(11) NOT NULL COMMENT 'uniquely identifies a book',
  `title` varchar(45) NOT NULL COMMENT 'Title of book',
  `author` varchar(45) NOT NULL COMMENT 'Writer of the book',
  `genre` varchar(45) NOT NULL COMMENT 'category or subject matter',
  `price` varchar(45) NOT NULL COMMENT 'cost of the book',
  PRIMARY KEY (`isbn`),
  UNIQUE KEY `id_UNIQUE` (`isbn`)
)

LOCK TABLES `books` WRITE;
INSERT INTO `books` VALUES (13,'EEqq','123','234','2'),(104,'qwe','yuiiuy','qwqwioio','23'),(121,'TTqq','123','234','2'),(122,'RRqq','123','234','2'),(144,'KKqq','123','234','2'),(155,'GGqq','123','234','2'),(1041,'qwe','yuiiuy','qwqwioio','23'),(1441,'1441','aitwpi','qwqwioio','23'),(10400,'qwe','yuiiuy','qwqwioio','23'),(13341,'weqrewq','aitwpi','qwqwioio','23'),(14444,'qwe','yuiiuy','qwqwioio','23');
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'unique Id of every user of the application',
  `user_name` varchar(45) NOT NULL COMMENT 'the name of the user',
  `password` varchar(45) DEFAULT NULL COMMENT 'password required for the User with Delete access',
  `access` int(11) NOT NULL COMMENT 'user with access code==0 can only view and give ratings, where as user with access code==1 can delete the book',
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) 
--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
INSERT INTO `users` VALUES (1,'john','john12',1),(2,'betty','betty14',0);
UNLOCK TABLES;