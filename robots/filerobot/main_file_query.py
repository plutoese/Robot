# coding=UTF-8

from datetime import datetime
from robots.filerobot.class_filerobot import FileRobot

# 0. Initialization
FILE_POOL = 'E:\\room\\forawhile'
LIB_PATH = 'E:\\room\\libs'
OPEN_PATH = 'E:\\temp'

# 1. to define a path Robot
path_robot = FileRobot(dirty_path=FILE_POOL, clean_path=LIB_PATH)

# 2. to do a query
path_robot.find(open_path=OPEN_PATH,last_modified={'$gt':datetime(2016,2,8)})


