CREATE TABLE IF NOT EXISTS `Portfolio` (
   `ID` int NOT NULL AUTO_INCREMENT,
   `CoinID` int NOT NULL,
   `PortfolioQuantity` int NOT NULL,
   `PortfolioPaid` decimal(15,2) NOT NULL,
   `PortfolioGain` decimal(5,2) NOT NULL,
   PRIMARY KEY (`ID`),
   UNIQUE KEY `ID_UNIQUE` (`ID`),
   UNIQUE KEY `CoinID_UNIQUE` (`CoinID`)
 ) ENGINE=InnoDB AUTO_INCREMENT=54 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='Keeps cryptocurrency coin portfolio details.';
