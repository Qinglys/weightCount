from weight_count.src.exts import db
from weight_count.src.models import User, Weight
import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator


def gen_chart(userid, limit=15):
    """
    生成最近十五天的体重曲线图
    :param userid:
    :param limit:
    :return:
    """
    weight_data = Weight.query.filter_by(userid=userid).limit(15)
    username = User.query.filter_by(id=userid).first().username

    weight_list = []
    date_list = []
    for _ in weight_data:
        weight_list.append(_.weight)
        date_list.append(_.date.strftime('%m-%d'))
    print(weight_list)
    print(date_list)
    plt.plot(date_list, weight_list, 'o-', color='r', label=username)

    plt.ylim(min(weight_list) - 1, max(weight_list) + 1)
    plt.xlabel("日期")  # 横坐标名字
    plt.ylabel("体重/KG")  # 纵坐标名字
    plt.legend(loc="best")  # 设置图例一般用best就行
    # 把x轴的刻度间隔设置为1，并存在变量里
    x_major_locator = MultipleLocator(1)
    # ax为两条坐标轴的实例
    ax = plt.gca()
    # 把x轴的主刻度设置为1的倍数
    ax.xaxis.set_major_locator(x_major_locator)

    plt.savefig('./test.png')


if __name__ == '__main__':
    gen_chart(1)