/*
 Navicat MySQL Data Transfer

 Source Server         : 笔记本的数据库
 Source Server Type    : MySQL
 Source Server Version : 50646
 Source Host           : localhost:3306
 Source Schema         : login

 Target Server Type    : MySQL
 Target Server Version : 50646
 File Encoding         : 65001

 Date: 11/08/2020 14:04:50
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for loginre
-- ----------------------------
DROP TABLE IF EXISTS `loginre`;
CREATE TABLE `loginre`  (
  `loginid` int(11) NULL DEFAULT NULL,
  `type` varchar(255) CHARACTER SET latin1 COLLATE latin1_swedish_ci NULL DEFAULT NULL,
  `callback` varchar(255) CHARACTER SET latin1 COLLATE latin1_swedish_ci NULL DEFAULT NULL,
  `return` varchar(255) CHARACTER SET latin1 COLLATE latin1_swedish_ci NULL DEFAULT NULL
) ENGINE = InnoDB CHARACTER SET = latin1 COLLATE = latin1_swedish_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user`  (
  `AD` varchar(255) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL,
  `AK` varchar(255) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL,
  PRIMARY KEY (`AD`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = latin1 COLLATE = latin1_swedish_ci ROW_FORMAT = Compact;

SET FOREIGN_KEY_CHECKS = 1;
