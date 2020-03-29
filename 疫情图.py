import requests
from lxml import etree
import json
from pyecharts import Map  # 0.1.9.4


class nCoV_2019:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1"
        }
        self.url = "https://ncov.dxy.cn/ncovh5/view/pneumonia_peopleapp"

    def parse_url(self):
        # 发送get请求网页
        r = requests.get(url=self.url, headers=self.headers)
        # 我们用断言来判断他的状态码手否为200，如果不是200则会报错
        assert r.status_code == 200
        # 这里是要用xpath 来提取我想要的信息
        html = etree.HTML(r.content.decode())
        # 获取id为getListByCountryTypeService1 script标签里的数据
        # 通过split函数以'}'分割成一个列表
        # html.xpath('//*[@id="getListByCountryTypeService1"]//text()')[0] 本身列表只有一个数据 类型为str 我只要取出来 我就能用字符串函数
        results = html.xpath('//*[@id="getListByCountryTypeService1"]//text()')[0].split('}')[:-3]
        return results

    # 拿到数据后观察数据
    # 1.我们要把无关的字符删除，
    # 2.我们用data_dict存取每个省份的数据 确诊 死亡 治愈 三个字段

    def getDataList(self, results):
        data_list = []
        for result in results:
            # 申明一个字典，存放数据，一个循环存放完，入data_list里，在清空，相当于一个临时存储变量
            data_dict = {}
            # 修改第一条数据
            if results.index(result) == 0:
                # replace(old,new)
                result = result.replace('try { window.getListByCountryTypeService1 = [', '')
            # 去除开头多的',' 并且将str类型的一个'字典'  转换成一个真正的字典
            result = json.loads(result.lstrip(',') + '}')
            # 省份
            data_dict['provinceShortName'] = result['provinceShortName']
            # 确诊人数
            data_dict['confirmedCount'] = result['confirmedCount']
            # 死亡人数
            data_dict['deadCount'] = result['deadCount']
            # 治愈人数
            data_dict['curedCount'] = result['curedCount']
            data_list.append(data_dict)
        return data_list

    def main(self):
        results = self.parse_url()
        data_list = self.getDataList(results)
        return data_list


nCoV_2019 = nCoV_2019()
data_list = nCoV_2019.main()
# 省份列表
provinceShortName_list = []
# 确诊人数列表
confirmedCount_list = []
# 死亡人数列表
deadCount_list = []
# 治愈人数列表
curedCount_list = []
# 列表赋值
for i in data_list:
    provinceShortName_list.append(i['provinceShortName'])
    confirmedCount_list.append(i['confirmedCount'])
    deadCount_list.append(i['deadCount'])
    curedCount_list.append(i['curedCount'])

# 画图
map = Map("中国疫情分布图", '', width=1980, height=1024, title_text_size=35)
# is_label_show 显示每个店 is_visualmap 显示颜色以及注释 maptype地区
map.add("", provinceShortName_list, confirmedCount_list, visual_range=[0, 1000], maptype='china', is_visualmap=True,
        visual_text_color='#000', is_label_show=True)
map.show_config()
map.render(path='./中国疫情图.html')
