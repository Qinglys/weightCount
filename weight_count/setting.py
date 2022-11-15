import os

DEBUG_MODE = False
DATABASE_URL = 'sqlite:///' + os.path.join(os.path.abspath('.'), 'weight_count/src/weightDB.sqlite')

# 首次创建需要初始化数据库
INIT_DB = False
if 'weightDB.sqlite' not in os.listdir(os.path.join(os.path.abspath('.'), 'weight_count/src/')):
    INIT_DB = True
