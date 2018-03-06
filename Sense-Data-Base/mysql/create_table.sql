CREATE TABLE `sensor` (
	`id` varchar(255) NOT NULL,
	`deploy_id` int NOT NULL,
	`register_date` DATE NOT NULL,
	`last_update` DATE NOT NULL,
	`model` varchar(255),
	`version` FLOAT,
	PRIMARY KEY (`id`)
);

CREATE TABLE `company` (
	`id` int NOT NULL AUTO_INCREMENT,
	`name` varchar(255) NOT NULL UNIQUE,
	`type` varchar(255) NOT NULL,
	PRIMARY KEY (`id`)
);

CREATE TABLE `deploy` (
	`id` int NOT NULL AUTO_INCREMENT,
	`company_id` int NOT NULL,
	`name` varchar(255) NOT NULL UNIQUE,
	`date_time_start` DATETIME NOT NULL,
	`date_time_end` DATETIME,
	`street_address` varchar(255),
	`zip` varchar(8),
	`city` varchar(255),
	`state` varchar(2),
	`internal_id` varchar(255),
	`tel` int(255),
	`photo` varchar(255),
	PRIMARY KEY (`id`)
);

CREATE TABLE `whitelist_sense` (
	`id` bigint NOT NULL AUTO_INCREMENT,
	`mac_address` varchar(255) NOT NULL,
	`deploy_id` int NOT NULL,
	PRIMARY KEY (`id`)
);

CREATE TABLE `gateway` (
	`id` int NOT NULL AUTO_INCREMENT,
	`deploy_id` int NOT NULL,
	`mac_address` varchar(17) NOT NULL UNIQUE,
	`date_time` DATE NOT NULL,
	PRIMARY KEY (`id`)
);

CREATE TABLE `manager` (
	`id` varchar(255) NOT NULL,
	`deploy_id` int NOT NULL,
	`name` varchar(255) NOT NULL,
	`tel` int(255) NOT NULL,
	`role` varchar(255) NOT NULL,
	`photo` varchar(255),
	PRIMARY KEY (`id`)
);

CREATE TABLE `training_parameters_sense` (
	`id` varchar(255) NOT NULL,
	`deploy_id` int NOT NULL,
	`gbm` bool NOT NULL,
	`id_owner` int NOT NULL,
	`rf` bool NOT NULL,
	PRIMARY KEY (`id`)
);

CREATE TABLE `training_data_sense` (
	`id` int NOT NULL AUTO_INCREMENT,
	`training_id` varchar(255) NOT NULL,
	`area_name` varchar(255) NOT NULL,
	PRIMARY KEY (`id`)
);

CREATE TABLE `training_whitelist_sense` (
	`training_id` int NOT NULL,
	`mac_address` varchar(255) NOT NULL
);

CREATE TABLE `sensor_position_log_sense` (
	`deploy_id` int NOT NULL,
	`sensor_id` varchar(255) NOT NULL,
	`date_time` DATETIME NOT NULL,
	`area_name` varchar(255),
	`sensor_name` varchar(255),
	`x` FLOAT NOT NULL,
	`y` FLOAT NOT NULL,
	`z` FLOAT NOT NULL
);

CREATE TABLE `training_data_timestamp_sense` (
	`training_data_id` int NOT NULL,
	`date_time_start` DATETIME NOT NULL,
	`date_time_end` DATETIME NOT NULL
);

CREATE TABLE `whitelist_person_data_sense` (
	`whitelist_id` bigint NOT NULL,
	`keyword` varchar(255) NOT NULL,
	`content` varchar(255) NOT NULL
);

CREATE TABLE `deploy_data_sense` (
	`deploy_id` int NOT NULL,
	`sense_time` varchar(11) NOT NULL,
	`week_days` varchar(13) NOT NULL,
	`holiday` bool NOT NULL DEFAULT FALSE,
	PRIMARY KEY (`deploy_id`)
);

CREATE TABLE `sensor_data_sense` (
	`sensor_id` varchar(255) NOT NULL,
	`name` varchar(255),
	`x` varchar(255),
	`y` varchar(255),
	`z` varchar(255),
	`area_name` varchar(255),
	PRIMARY KEY (`sensor_id`)
);

ALTER TABLE `sensor` ADD CONSTRAINT `sensor_fk0` FOREIGN KEY (`deploy_id`) REFERENCES `deploy`(`id`);

ALTER TABLE `deploy` ADD CONSTRAINT `deploy_fk0` FOREIGN KEY (`company_id`) REFERENCES `company`(`id`);

ALTER TABLE `whitelist_sense` ADD CONSTRAINT `whitelist_sense_fk0` FOREIGN KEY (`deploy_id`) REFERENCES `deploy`(`id`);

ALTER TABLE `gateway` ADD CONSTRAINT `gateway_fk0` FOREIGN KEY (`deploy_id`) REFERENCES `deploy`(`id`);

ALTER TABLE `manager` ADD CONSTRAINT `manager_fk0` FOREIGN KEY (`deploy_id`) REFERENCES `deploy`(`id`);

ALTER TABLE `training_parameters_sense` ADD CONSTRAINT `training_parameters_sense_fk0` FOREIGN KEY (`deploy_id`) REFERENCES `deploy`(`id`);

ALTER TABLE `training_data_sense` ADD CONSTRAINT `training_data_sense_fk0` FOREIGN KEY (`training_id`) REFERENCES `training_parameters_sense`(`id`) ON DELETE CASCADE ;

ALTER TABLE `training_whitelist_sense` ADD CONSTRAINT `training_whitelist_sense_fk0` FOREIGN KEY (`training_id`) REFERENCES `training_data_sense`(`id`) ON DELETE CASCADE ;

ALTER TABLE `sensor_position_log_sense` ADD CONSTRAINT `sensor_position_log_sense_fk0` FOREIGN KEY (`deploy_id`) REFERENCES `deploy`(`id`);

ALTER TABLE `sensor_position_log_sense` ADD CONSTRAINT `sensor_position_log_sense_fk1` FOREIGN KEY (`sensor_id`) REFERENCES `sensor`(`id`);

ALTER TABLE `training_data_timestamp_sense` ADD CONSTRAINT `training_data_timestamp_sense_fk0` FOREIGN KEY (`training_data_id`) REFERENCES `training_data_sense`(`id`) ON DELETE CASCADE ;

ALTER TABLE `whitelist_person_data_sense` ADD CONSTRAINT `whitelist_person_data_sense_fk0` FOREIGN KEY (`whitelist_id`) REFERENCES `whitelist_sense`(`id`) ON DELETE CASCADE;

ALTER TABLE `deploy_data_sense` ADD CONSTRAINT `deploy_data_sense_fk0` FOREIGN KEY (`deploy_id`) REFERENCES `deploy`(`id`) ON DELETE CASCADE ;

ALTER TABLE `sensor_data_sense` ADD CONSTRAINT `sensor_data_sense_fk0` FOREIGN KEY (`sensor_id`) REFERENCES `sensor`(`id`) ON DELETE CASCADE ;

ALTER TABLE whitelist_person_data_sense ADD UNIQUE wkc ( whitelist_id, keyword) ;
ALTER TABLE whitelist_sense ADD UNIQUE md (mac_address, deploy_id);

CREATE VIEW view_whitelist_sense AS  SELECT w.id, w.mac_address, w.deploy_id, wp1.content as sentiment, wp2.content as score, wp3.content as person FROM whitelist_sense as w INNER JOIN whitelist_person_data_sense as wp1 ON w.id = wp1.whitelist_id AND wp1.keyword = 'SENTIMENT' INNER JOIN whitelist_person_data_sense as wp2 ON w.id = wp2.whitelist_id AND wp2.keyword = 'SCORE' INNER JOIN whitelist_person_data_sense as wp3 ON w.id = wp3.whitelist_id AND wp3.keyword = 'PERSON';

CREATE VIEW view_sensor_sense AS SELECT s.id as sensor_id, c.name as company, c.id as company_id, d.id as deploy_id FROM sensor as s JOIN deploy as d ON s.deploy_id = d.id JOIN company as c ON d.company_id = c.id;


