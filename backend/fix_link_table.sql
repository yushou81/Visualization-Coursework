-- 创建 department 表（如果不存在）
CREATE TABLE IF NOT EXISTS `department` (
  `id` varchar(4) NOT NULL,
  `department` varchar(255) DEFAULT NULL,
  `position` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- 创建 link 表（如果不存在）
CREATE TABLE IF NOT EXISTS `link` (
  `id` varchar(4) NOT NULL,
  `ip` varchar(255) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `level` int DEFAULT NULL,
  `depart` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

