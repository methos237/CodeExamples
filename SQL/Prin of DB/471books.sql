-- -----------------------------------------------------
-- Schema 471books
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `471books` DEFAULT CHARACTER SET utf8 ;
USE `471books` ;

-- -----------------------------------------------------
-- Table `471books`.`publishers`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `471books`.`publishers` (
  `publisher_id` INT NOT NULL AUTO_INCREMENT,
  `publisher_name` VARCHAR(255) NULL,
  `city` VARCHAR(45) NULL,
  `country` VARCHAR(45) NULL,
  PRIMARY KEY (`publisher_id`))
ENGINE = InnoDB;

INSERT INTO `471books`.`publishers` (`publisher_id`, `publisher_name`, `city`, `country`) VALUES
(1, 'Hachette Livre', 'Paris', 'France'),
(2, 'Random House', 'New York City', 'USA'),
(3, 'Penguin Books', 'London', 'England'),
(4, 'HarperCollins', 'New York City', 'USA'),
(5, 'Pan Macmillan', 'London', 'England'),
(6, 'Pearson Education', 'London', 'England'),
(7, 'Bloomsbury', 'London', 'England'),
(8, 'Oxford University Press', 'Oxford', 'England'),
(9, 'Simon & Schuster', 'New York CIty', 'USA'),
(10, 'John Wiley & Sons', 'Hoboken', 'USA'),
(11, 'Egmont', 'Copenhagen', 'Denmark'),
(12, 'Elsevier', 'Amsterdam', 'Netherlands');
COMMIT;
-- -----------------------------------------------------
-- Table `471books`.`genres`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `471books`.`genres` (
  `genre_id` INT NOT NULL AUTO_INCREMENT,
  `genre_name` VARCHAR(45) NULL,
  PRIMARY KEY (`genre_id`))
ENGINE = InnoDB;

INSERT INTO `471books`.`genres` (`genre_id`, `genre_name`) VALUES
(1, 'Action and adventure'),
(2, 'Alternate history'),
(3, 'Anthology'),
(4, 'Chick lit'),
(5, 'Children\'s literature'),
(6, 'Comic book'),
(7, 'Coming-of-age'),
(8, 'Crime'),
(9, 'Drama'),
(10, 'Fairytale'),
(11, 'Fantasy'),
(12, 'Graphic novel'),
(13, 'Historical fiction'),
(14, 'Horror'),
(15, 'Mystery'),
(16, 'Paranormal romance'),
(17, 'Picture book'),
(18, 'Poetry'),
(19, 'Political thriller'),
(20, 'Romance'),
(21, 'Satire'),
(22, 'Science fiction'),
(23, 'Short story'),
(24, 'Suspense'),
(25, 'Thriller'),
(26, 'Young adult'),
(27, 'Art'),
(28, 'Autobiography'),
(29, 'Biography'),
(30, 'Book review'),
(31, 'Cookbook'),
(32, 'Diary'),
(33, 'Dictionary'),
(34, 'Encyclopedia'),
(35, 'Guide'),
(36, 'Health'),
(37, 'History'),
(38, 'Journal'),
(39, 'Math'),
(40, 'Memoir'),
(41, 'Prayer'),
(42, 'Religion, spirituality, and new age'),
(43, 'Textbook'),
(44, 'Review'),
(45, 'Science'),
(46, 'Self help'),
(47, 'Travel'),
(48, 'True crime');
COMMIT;

-- -----------------------------------------------------
-- Table `471books`.`book`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `471books`.`book` (
  `ISBN` BIGINT(13) NOT NULL,
  `publisher_id` INT NULL,
  `genre_id` INT NULL,
  `year` INT(4) NULL,
  `title` VARCHAR(255) NULL,
  `price` DECIMAL(19,2) NULL,
  PRIMARY KEY (`ISBN`),
  CONSTRAINT `publisher_id`
    FOREIGN KEY (`publisher_id`)
    REFERENCES `471books`.`publishers` (`publisher_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `genre_id`
    FOREIGN KEY (`genre_id`)
    REFERENCES `471books`.`genres` (`genre_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;

CREATE INDEX `publisher_id_idx` ON `471books`.`book` (`publisher_id` ASC) VISIBLE;

CREATE INDEX `genre_id_idx` ON `471books`.`book` (`genre_id` ASC) VISIBLE;


-- -----------------------------------------------------
-- Table `471books`.`authors`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `471books`.`authors` (
  `author_id` INT NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(45) NULL,
  `last_name` VARCHAR(45) NULL,
  PRIMARY KEY (`author_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `471books`.`book_authors`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `471books`.`book_authors` (
  `book_ISBN` BIGINT(13) NOT NULL,
  `author_author_id` INT NOT NULL,
  PRIMARY KEY (`book_ISBN`, `author_author_id`),
  CONSTRAINT `books_authors_ISBN`
    FOREIGN KEY (`book_ISBN`)
    REFERENCES `471books`.`book` (`ISBN`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `books_authors_author_id`
    FOREIGN KEY (`author_author_id`)
    REFERENCES `471books`.`authors` (`author_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

CREATE INDEX `author_id_idx` ON `471books`.`book_authors` (`author_author_id` ASC) VISIBLE;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
