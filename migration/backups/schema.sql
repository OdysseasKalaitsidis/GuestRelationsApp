CREATE TABLE `cases` (
  `id` int NOT NULL AUTO_INCREMENT,
  `room` varchar(50) DEFAULT NULL,
  `status` varchar(50) DEFAULT NULL,
  `importance` varchar(50) DEFAULT NULL,
  `type` varchar(50) DEFAULT NULL,
  `title` text,
  `action` text,
  `owner_id` int DEFAULT NULL,
  `guest` varchar(255) DEFAULT NULL,
  `created` varchar(100) DEFAULT NULL,
  `created_by` varchar(255) DEFAULT NULL,
  `modified` varchar(100) DEFAULT NULL,
  `modified_by` varchar(255) DEFAULT NULL,
  `source` varchar(255) DEFAULT NULL,
  `membership` varchar(255) DEFAULT NULL,
  `case_description` text,
  `in_out` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `owner_id` (`owner_id`),
  KEY `ix_cases_id` (`id`),
  CONSTRAINT `cases_ibfk_1` FOREIGN KEY (`owner_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=630 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `documents` (
  `id` int NOT NULL AUTO_INCREMENT,
  `filename` varchar(255) NOT NULL,
  `file_type` varchar(50) NOT NULL,
  `content` text NOT NULL,
  `uploaded_by` int NOT NULL,
  `uploaded_at` varchar(50) NOT NULL,
  `file_size` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `uploaded_by` (`uploaded_by`),
  KEY `ix_documents_id` (`id`),
  CONSTRAINT `documents_ibfk_1` FOREIGN KEY (`uploaded_by`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `followups` (
  `id` int NOT NULL AUTO_INCREMENT,
  `case_id` int DEFAULT NULL,
  `suggestion_text` text NOT NULL,
  `assigned_to` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `case_id` (`case_id`),
  KEY `assigned_to` (`assigned_to`),
  KEY `ix_followups_id` (`id`),
  CONSTRAINT `followups_ibfk_1` FOREIGN KEY (`case_id`) REFERENCES `cases` (`id`),
  CONSTRAINT `followups_ibfk_2` FOREIGN KEY (`assigned_to`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=602 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `tasks` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `description` text,
  `task_type` varchar(50) NOT NULL,
  `assigned_to` int DEFAULT NULL,
  `assigned_by` int NOT NULL,
  `due_date` varchar(50) NOT NULL,
  `status` varchar(50) DEFAULT NULL,
  `created_at` varchar(50) NOT NULL,
  `completed_at` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `assigned_to` (`assigned_to`),
  KEY `assigned_by` (`assigned_by`),
  KEY `ix_tasks_id` (`id`),
  CONSTRAINT `tasks_ibfk_1` FOREIGN KEY (`assigned_to`) REFERENCES `users` (`id`),
  CONSTRAINT `tasks_ibfk_2` FOREIGN KEY (`assigned_by`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `hashed_password` varchar(255) NOT NULL,
  `is_admin` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_users_email` (`email`),
  UNIQUE KEY `ix_users_username` (`username`),
  KEY `ix_users_id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

