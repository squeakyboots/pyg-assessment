CREATE TABLE IF NOT EXISTS `Coin` (
   `ID` int NOT NULL AUTO_INCREMENT,
   `CoinID` varchar(10) NOT NULL,
   `CoinSymbol` varchar(5) NOT NULL,
   `CoinName` varchar(45) NOT NULL,
   `CoinCurrentPrice` decimal(15,2) NOT NULL,
   `CoinMarketCap` bigint NOT NULL,
   PRIMARY KEY (`ID`),
   UNIQUE KEY `CoinID_UNIQUE` (`CoinID`),
   UNIQUE KEY `ID_UNIQUE` (`ID`),
   UNIQUE KEY `CoinSymbol_UNIQUE` (`CoinSymbol`),
   UNIQUE KEY `CoinName_UNIQUE` (`CoinName`)
 ) ENGINE=InnoDB AUTO_INCREMENT=73 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='Keeps details on coin entities.';
