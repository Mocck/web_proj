-- 设置字符集
SET NAMES utf8mb4;
SET CHARACTER SET utf8mb4;

-- 创建数据库（指定字符集）
CREATE DATABASE IF NOT EXISTS agent_db 
DEFAULT CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

USE agent_db;

CREATE TABLE `t_user` (
    `id` BIGINT AUTO_INCREMENT PRIMARY KEY COMMENT '主键',
    `username` VARCHAR(100) NOT NULL UNIQUE COMMENT '用户名',
    `email` VARCHAR(128) NOT NULL UNIQUE COMMENT '邮箱',
    `phone_number` VARCHAR(15) UNIQUE COMMENT '手机号',
    `password` VARCHAR(256) NOT NULL COMMENT '密码',
    `confirmpassword` VARCHAR(256) NOT NULL COMMENT '确认密码',
    `nickname` VARCHAR(64) DEFAULT NULL COMMENT '昵称',
    `avatar` VARCHAR(255) DEFAULT NULL COMMENT '头像路径',
    `bio` TEXT DEFAULT NULL COMMENT '个人简介',
    `is_active` BOOLEAN DEFAULT TRUE COMMENT '是否激活',
    `is_locked` BOOLEAN DEFAULT FALSE COMMENT '是否锁定',
    `failed_login_attempts` INT DEFAULT 0 COMMENT '登录失败次数',
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    `locked_at` DATETIME DEFAULT NULL COMMENT '锁定时间',
    INDEX `idx_username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户';

CREATE TABLE `t_login_history` (
    `id` BIGINT AUTO_INCREMENT PRIMARY KEY,
    `user_id` BIGINT NOT NULL COMMENT '用户 ID',
    `login_time` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '登录时间',
    `ip_address` VARCHAR(45) NOT NULL COMMENT 'IP 地址',
    `device_info` VARCHAR(256) NOT NULL COMMENT '设备信息',
    INDEX `idx_user` (`user_id`),
    CONSTRAINT `fk_login_user` FOREIGN KEY (`user_id`) REFERENCES `t_user`(`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='登录历史';

CREATE TABLE `t_team` (
    `id` BIGINT AUTO_INCREMENT PRIMARY KEY COMMENT '团队ID',
    `name` VARCHAR(100) NOT NULL UNIQUE COMMENT '团队名称',
    `description` TEXT DEFAULT NULL COMMENT '团队描述',
    `avatar` VARCHAR(500) DEFAULT NULL COMMENT '团队头像URL',
    `is_public` VARCHAR(20) DEFAULT 'private' COMMENT '可见性',
    `join_policy` VARCHAR(20) DEFAULT 'approval' COMMENT '加入策略',
    `max_members` INT DEFAULT NULL COMMENT '最大成员数',
    `owner_id` BIGINT NOT NULL COMMENT '团队负责人',
    `status` SMALLINT DEFAULT 1 COMMENT '状态',
    `settings` JSON DEFAULT NULL COMMENT '团队设置',
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    `deleted_at` DATETIME DEFAULT NULL COMMENT '删除时间',
    INDEX `idx_owner_id` (`owner_id`),
    INDEX `idx_visibility` (`is_public`),
    INDEX `idx_status` (`status`),
    INDEX `idx_created_at` (`created_at`),
    INDEX `idx_deleted_at` (`deleted_at`),
    CONSTRAINT `fk_team_owner` FOREIGN KEY (`owner_id`) REFERENCES `t_user`(`id`) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='团队';

CREATE TABLE `t_role` (
    `id` BIGINT AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(64) NOT NULL UNIQUE COMMENT '角色名称',
    `description` VARCHAR(256) DEFAULT NULL COMMENT '角色描述',
    `scope` VARCHAR(32) NOT NULL COMMENT '作用域',
    `sort_order` INT DEFAULT 0 COMMENT '排序等级'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='角色';

CREATE TABLE `t_permission` (
    `id` BIGINT AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(64) NOT NULL UNIQUE COMMENT '权限名称',
    `code` VARCHAR(64) NOT NULL UNIQUE COMMENT '权限编码',
    `description` VARCHAR(256) DEFAULT NULL COMMENT '权限描述',
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='权限';

CREATE TABLE `t_user_role` (
    `id` BIGINT AUTO_INCREMENT PRIMARY KEY,
    `user_id` BIGINT NOT NULL COMMENT '用户',
    `role_id` BIGINT NOT NULL COMMENT '角色',
    `team_id` BIGINT DEFAULT NULL COMMENT '团队',
    CONSTRAINT `fk_user_role_user` FOREIGN KEY (`user_id`) REFERENCES `t_user`(`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_user_role_role` FOREIGN KEY (`role_id`) REFERENCES `t_role`(`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_user_role_team` FOREIGN KEY (`team_id`) REFERENCES `t_team`(`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户角色关联';

CREATE TABLE `t_role_permission` (
    `id` BIGINT AUTO_INCREMENT PRIMARY KEY,
    `role_id` BIGINT NOT NULL COMMENT '角色',
    `permission_id` BIGINT NOT NULL COMMENT '权限',
    CONSTRAINT `fk_role_perm_role` FOREIGN KEY (`role_id`) REFERENCES `t_role`(`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_role_perm_perm` FOREIGN KEY (`permission_id`) REFERENCES `t_permission`(`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='角色权限关联';

CREATE TABLE `chat_session` (
    `id` BIGINT AUTO_INCREMENT PRIMARY KEY,
    `user_id` BIGINT NOT NULL COMMENT '所属用户',
    `title` VARCHAR(100) DEFAULT NULL COMMENT '会话标题',
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    `is_deleted` BOOLEAN DEFAULT FALSE COMMENT '是否删除',
    CONSTRAINT `fk_session_user` FOREIGN KEY (`user_id`) REFERENCES `t_user`(`id`) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='聊天会话';

CREATE TABLE `chat_message` (
    `id` BIGINT AUTO_INCREMENT PRIMARY KEY,
    `session_id` BIGINT NOT NULL COMMENT '会话ID',
    `role` VARCHAR(20) NOT NULL COMMENT '角色',
    `content` TEXT NOT NULL COMMENT '消息内容',
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '发送时间',
    CONSTRAINT `fk_message_session` FOREIGN KEY (`session_id`) REFERENCES `chat_session`(`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='聊天消息';


-- 插入初始数据
INSERT INTO t_user (username, password, confirmpassword, nickname, email) VALUES
('admin', 'pass123', 'pass123', '管理员', 'admin@example.com'),
('test', 'pass123', 'pass123', '测试用户', 'test@example.com')
ON DUPLICATE KEY UPDATE password=VALUES(password), confirmpassword=VALUES(confirmpassword), nickname=VALUES(nickname), email=VALUES(email);

-- 转存表中的数据 `t_role`
INSERT INTO `t_role` (`id`, `name`, `description`, `scope`, `sort_order`) VALUES
(1, 'super_admin', '系统最高权限管理员，拥有所有权限', 'system', 1),
(2, 'admin', '系统管理员，可管理用户、角色、团队等', 'system', 2),
(3, 'team_owner', '团队创建者', 'team', 3),
(4, 'team_admin', '团队管理员', 'team', 4),
(5, 'user', '普通注册用户', 'user', 5);

INSERT INTO `t_user_role` (`id`, `user_id`, `role_id`, `team_id`) VALUES
(1, 1, 1, NULL),
(2, 2, 2, NULL);

-- 转存表中的数据 `t_team`
INSERT INTO `t_team` (`id`, `name`, `description`, `avatar`, `is_public`, `join_policy`, `max_members`, `owner_id`, `status`, `settings`, `created_at`, `updated_at`, `deleted_at`) VALUES
(1, 'abc', '', NULL, 'true', 'open', 10, 1, 1, NULL, '2025-10-29 18:12:25', '2025-10-29 18:12:25', NULL),
(2, 'qwe', '', NULL, 'true', 'open', 10, 1, 1, NULL, '2025-10-29 18:14:50', '2025-10-29 18:14:50', NULL);
