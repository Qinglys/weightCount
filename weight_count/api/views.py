from flask import Blueprint, request, current_app, render_template
import datetime
from weight_count.src.exts import db
from weight_count.src.models import User, Weight
from weight_count.api import common
from weight_count import setting
from pytz import timezone

my_app = Blueprint('index', __name__)


@my_app.route('/')
def index(msg='\"\"'):
    # 初始化数据库 创建表
    if setting.INIT_DB:
        db.create_all()
    
    # 构造 chart_div
    all_data = get_weight()
    user_number = len(all_data['users'])
    chars = ""
    for i in range(user_number):
        chars += f'<div id="chart{i}" style="width: 100%;height: 200px;"></div> '


    # 判断hello_world
    now_time = datetime.datetime.now(tz=timezone('Asia/Shanghai')).strftime('%H:%M:%S')
    print(now_time)
    if '06:00:00' <= now_time <= '11:00:00':
        hello_world = '早上好！'
    elif '11:00:00' < now_time < "14:00:00":
        hello_world = '中午好！'
    elif '14:00:00' <= now_time <= "18:00:00":
        hello_world = '下午好！'
    elif '18:00:00' < now_time < "24:00:00":
        hello_world = '晚上好！'
    else:
        hello_world = '还不睡觉？'
    # print(hello_world)
    # 构造user_select
    user_select = ''
    users = User.query.order_by(User.id).all()
    for user in users:
        user_select += f'<option value="{user.id}">{user.username}</option> '
    
    return render_template("index.html", all_data = dict(all_data), chart_div=chars, hello_world=hello_world, user_select=user_select, msg='\"'+msg+'\"' if msg!='\"\"' else '\"\"')


@my_app.route('/add_user', methods=['post'])
def add_user():

    data = common.get_request_json(request)
    if not data:
        current_app.logger.warning('add_user 存在异常请求！')
        return common.make_error('请求参数错误！')

    username = data.get('user', '')
    init_weight = data.get('weight', '')
    try:
        init_weight = float(init_weight)
    except ValueError:
        current_app.logger.warning('add_user 请求weight非数字类型！')
        init_weight = ''

    if not all([username, init_weight]):
        return common.make_error('参数不完整, 或参数格式错误！')

    # 数据库username不可重复
    if User.query.filter_by(username=username).first() is not None:
        return common.make_error('用户已存在！')

    user = User(username=username)
    db.session.add(user)
    db.session.flush()
    current_app.logger.info(datetime.datetime.utcnow())
    weight = Weight(userid=user.id, weight=init_weight, date=datetime.datetime.utcnow())
    db.session.add(weight)
    db.session.commit()
    return common.make_success('添加成功！')


@my_app.route('/add_weight', methods=['POST'])
def add_weight():

    if request.method == 'POST':
        data = common.get_request_json(request)
        if not data:
            current_app.logger.warning('add_weight 存在异常请求！')
            return common.make_error('请求参数错误！')
        userid = data.get('userid', '')
        new_weight = data.get('weight', '')
    else:
        userid = request.args.get('userid', default='')
        new_weight = request.args.get('weight', default='')
    try:
        new_weight = float(new_weight)
    except ValueError:
        new_weight = ''
    if not all([userid, new_weight]):
        return common.make_error('参数不完整, 或参数格式错误！')
    # 用户ID校验
    if not User.query.filter_by(id=userid):
        return common.make_error('用户不存在！')

    # 用户今日添加校验
    last_date = Weight.query.filter_by(userid=userid).order_by(Weight.date.desc()).first()
    print(last_date.date, datetime.datetime.today().date())
    if last_date and last_date.date == datetime.datetime.today().date():
        # 更新今日体重
        last_date.weight = new_weight
        db.session.commit()
        if request.method == 'GET':
            return index(msg='更新成功！')
        return common.make_success('更新成功！')
    else:
        # 记录新体重信息
        weight = Weight(userid=userid, weight=new_weight, date=datetime.datetime.today().date())
        db.session.add(weight)
        db.session.commit()
        if request.method == 'GET':
            return index(msg='添加成功！')
        return common.make_success('添加成功！')


@my_app.route('/get_weight', methods=['get'])
def get_weight():
    result = {
        'users':{},
        'chart_date': []
    }
    SHOW_DATE = 14
    # 先处理chart_date
    today = datetime.datetime.today().date()
    for i in range(SHOW_DATE):
        result['chart_date'].append((today - datetime.timedelta(days=SHOW_DATE - 1 - i)).strftime('%m-%d'))

    # 处理体重
    # 日期 - 下标对照表
    day_index = {}
    for index, day in enumerate(result['chart_date']):
        day_index[day] = index

    # 查询最近的体重记录
    data = db.session.query(User, Weight).join(Weight).filter(Weight.date>=(today-datetime.timedelta(days=SHOW_DATE - 1 ))).all()
    for d in data:
        if not d.User.username in result['users']:
            result['users'][d.User.username] = ['_'] * 15
        if d.Weight.date.strftime('%m-%d') in day_index:
            result['users'][d.User.username][day_index[d.Weight.date.strftime('%m-%d')]] = d.Weight.weight
        else:
            current_app.logger.error(f'get_weight 查询语法有误！查询到日期：{d.Weight.date.strftime("%m-%d")}的记录。')
    return result


