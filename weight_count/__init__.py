from flask import Flask
from weight_count.api.views import my_app
from logging.handlers import TimedRotatingFileHandler
from weight_count.src.exts import db
import logging
import weight_count.setting
import os

app = Flask(__name__)

# 调试模式
app.debug = setting.DEBUG_MODE

# 初始化日志
formatter = logging.Formatter(
    "[%(asctime)s][%(filename)s:%(lineno)d][%(levelname)s] - %(message)s")
if not os.path.isdir("./log"):
    os.mkdir("./log")
handler = TimedRotatingFileHandler(
    "./log/weight_count.log", when="D", interval=1, backupCount=15,
    encoding="UTF-8", delay=False, utc=True)
app.logger.addHandler(handler)
handler.setFormatter(formatter)
app.logger.setLevel(logging.DEBUG if setting.DEBUG_MODE else logging.INFO)

# 注册数据库

app.config['SQLALCHEMY_DATABASE_URI'] = setting.DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db.init_app(app)

# 注册蓝图
app.register_blueprint(my_app, url_prefix='/')


if __name__ == '__main__':
    app.run()