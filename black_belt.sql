-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema black_belt
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema black_belt
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `black_belt` DEFAULT CHARACTER SET utf8 ;
USE `black_belt` ;

-- -----------------------------------------------------
-- Table `black_belt`.`user`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `black_belt`.`user` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(255) NOT NULL,
  `last_name` VARCHAR(255) NOT NULL,
  `email` VARCHAR(255) NOT NULL,
  `password` VARCHAR(255) NOT NULL,
  `created_at` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `black_belt`.`show`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `black_belt`.`show` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `title` VARCHAR(255) NOT NULL,
  `network` VARCHAR(255) NOT NULL,
  `release_date` DATETIME NOT NULL,
  `description` VARCHAR(255) NOT NULL,
  `created_at` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
  `posted_by` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_show_user_idx` (`posted_by` ASC) VISIBLE,
  CONSTRAINT `fk_show_user`
    FOREIGN KEY (`posted_by`)
    REFERENCES `black_belt`.`user` (`id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `black_belt`.`like`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `black_belt`.`like` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `show_id` INT NOT NULL,
  `liked_by` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_like_show1_idx` (`show_id` ASC) VISIBLE,
  INDEX `fk_like_user1_idx` (`liked_by` ASC) VISIBLE,
  CONSTRAINT `fk_like_show1`
    FOREIGN KEY (`show_id`)
    REFERENCES `black_belt`.`show` (`id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_like_user1`
    FOREIGN KEY (`liked_by`)
    REFERENCES `black_belt`.`user` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
