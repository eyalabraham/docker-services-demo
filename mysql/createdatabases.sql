/*
    borrowing.sql

    Create a database 'borrowdb'
    Create a table 'borrowed' in the 'borrowdb' database to hold the list of library borrowing transactions
    Grant a user 'rest', and grant SELECT, INSERT, UPDATE and DELETE privileges on the 'borrowed' table
    The table 'borrowed' will be empty
    
    11/12/19    Created
    
*/

CREATE DATABASE borrowdb;
USE borrowdb;

CREATE TABLE IF NOT EXISTS borrowed
(
  id           INT      NOT NULL AUTO_INCREMENT PRIMARY KEY,
  bookId       INT      NOT NULL,
  patronId     INT      NOT NULL,
  dateOut      DATE     NOT NULL, 
  dateDue      DATE     NOT NULL,
  INDEX (dateDue)
);

/*
    catalog.sql

    Create a database 'catalogdb'
    Create a table 'catalog' in the 'catalogdb' database to hold the book library catalog
    Grant a user 'rest' and grant only SELECT priviliges
    Pupulate the 'catalog' table with demo data from local CSV file 'catalog_demo.csv'
    
    11/12/19    Created
    
*/
CREATE DATABASE catalogdb;
USE catalogdb;

CREATE TABLE IF NOT EXISTS catalog
(
  id           INT          NOT NULL AUTO_INCREMENT PRIMARY KEY,
  title        VARCHAR(256) NOT NULL,
  author       VARCHAR(128) NOT NULL,
  count        INT          NOT NULL DEFAULT 0,
  thumbnailUrl TEXT,
  FULLTEXT(title),
  INDEX (author)
);

LOAD DATA LOCAL INFILE '/docker-entrypoint-initdb.d/catalog_demo.csv' 
INTO TABLE catalogdb.catalog 
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

/*
    patrons.sql

    Create a database 'patronsdb'
    Create a table 'patrons' in the 'patronsdb' database to hold the list of library patrons
    Grant a user 'rest' and grant only SELECT priviliges
    Pupulate the 'patrons' table with demo data from local CSV file 'patrons_demo.csv'
    
    11/12/19    Created
    
*/
CREATE DATABASE patronsdb;
USE patronsdb;

CREATE TABLE IF NOT EXISTS patrons
(
  id           INT         NOT NULL AUTO_INCREMENT PRIMARY KEY,
  firstName    VARCHAR(64) NOT NULL,
  lastName     VARCHAR(64) NOT NULL,
  patronNum    CHAR(12)    NOT NULL UNIQUE,
  INDEX (patronNum)
);

LOAD DATA LOCAL INFILE '/docker-entrypoint-initdb.d/patrons_demo.csv' 
INTO TABLE patronsdb.patrons 
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

/*
    Grant 'rest' user access to data tables.
*/
CREATE USER 'rest'@'%' IDENTIFIED BY 'password';
GRANT SELECT ON catalogdb.* TO 'rest'@'%';
GRANT SELECT, UPDATE, INSERT, DELETE ON borrowdb.borrowed TO 'rest'@'%';
GRANT SELECT ON patronsdb.* TO 'rest'@'%';

FLUSH PRIVILEGES;
