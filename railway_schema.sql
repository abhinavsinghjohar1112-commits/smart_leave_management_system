CREATE TABLE `signupdata` (
  `employeeid` varchar(50) NOT NULL,
  `position` enum('employee','manager','hr','supermanager') NOT NULL,
  `name` varchar(100) NOT NULL,
  `emailid` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `department` varchar(50) NOT NULL,
  `manager_id` varchar(50) DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL DEFAULT '1',
  PRIMARY KEY (`employeeid`),
  UNIQUE KEY `emailid` (`emailid`),
  KEY `fk_signupdata_manager` (`manager_id`),
  CONSTRAINT `fk_signupdata_manager` FOREIGN KEY (`manager_id`) REFERENCES `signupdata` (`employeeid`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `holidays` (
  `id` int NOT NULL AUTO_INCREMENT,
  `holiday_date` date NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `holiday_date` (`holiday_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `leave_policy` (
  `leave_type` varchar(20) NOT NULL,
  `total_leaves` int NOT NULL,
  `max_per_month` int DEFAULT NULL,
  `min_notice_days` int DEFAULT '0',
  `allow_half_day` tinyint(1) DEFAULT '1',
  PRIMARY KEY (`leave_type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `system_rules` (
  `id` int NOT NULL AUTO_INCREMENT,
  `max_department_leave_percent` int DEFAULT NULL,
  `exclude_weekends` tinyint(1) DEFAULT NULL,
  `exclude_holidays` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `leaves` (
  `id` int NOT NULL AUTO_INCREMENT,
  `employeeid` varchar(50) NOT NULL,
  `start_date` date NOT NULL,
  `end_date` date NOT NULL,
  `totaldays` decimal(4,1) NOT NULL,
  `leave_id` varchar(100) NOT NULL,
  `status` varchar(20) NOT NULL DEFAULT 'pending',
  `manager_comment` varchar(255) DEFAULT NULL,
  `manager_id` varchar(50) DEFAULT NULL,
  `halfofstart` varchar(50) DEFAULT NULL,
  `halfofend` varchar(50) DEFAULT NULL,
  `leave_type` varchar(50) DEFAULT NULL,
  `department` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `leave_id` (`leave_id`),
  KEY `fk_leaves_employee` (`employeeid`),
  KEY `fk_leaves_manager` (`manager_id`),
  CONSTRAINT `fk_leaves_employee` FOREIGN KEY (`employeeid`) REFERENCES `signupdata` (`employeeid`) ON DELETE CASCADE,
  CONSTRAINT `fk_leaves_manager` FOREIGN KEY (`manager_id`) REFERENCES `signupdata` (`employeeid`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Seed the system_rules row your app expects at id=1 (checked via "WHERE id=1" and "LIMIT 1" in app.py)
INSERT INTO system_rules (max_department_leave_percent, exclude_weekends, exclude_holidays)
VALUES (30, 1, 1);

-- Seed default leave policies so applyleave.html has something to validate against
INSERT INTO leave_policy (leave_type, total_leaves, max_per_month, min_notice_days, allow_half_day) VALUES
('casual leave', 12, 2, 1, 1),
('sick leave', 10, 3, 0, 1),
('earned leave', 15, 3, 3, 1);
