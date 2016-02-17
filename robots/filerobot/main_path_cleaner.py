# coding=UTF-8

from robots.filerobot.class_filerobot import FileRobot

# 0. Initialization
FILE_POOL = 'E:\\room\\forawhile'
LIB_PATH = 'E:\\room\\libs'

# 1. Define a path Robot
path_robot = FileRobot(dirty_path=FILE_POOL, clean_path=LIB_PATH)

# 2. to scan file pool and copy files to lib path
path_robot.scan_and_copy()

# 3. to update database according to lib path
path_robot.update_database()
