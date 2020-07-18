import requests
import json
from pyecharts import options as opts
from pyecharts.charts import Map
from pyecharts.faker import Faker
from pyecharts.commons.utils import JsCode

class nCov_2019:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
        }
        self.url = 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5'

    def parse_url(self):
        response = requests.get("https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5")
        list_json = json.loads(response.text)
        return list_json

    def getDateList(self, list_json):
        # 将data数据类型str 转成dict类型 方便操作数据
        global false, null, true
        false = null = true = ''
        jo = list_json['data']
        data = eval(jo)
        return data;

    def main(self):
        list_json = self.parse_url()
        data = self.getDateList(list_json)
        return data

nCov_2019 = nCov_2019()
data = nCov_2019.main()

# 地区
area = []
# 现存确诊
nowConfirm = []
# 累计确诊
confirm = []
# 死亡人数
dead = []
# 治愈人数
heal = []
for i in range(34):
    area.append(data['areaTree'][0]['children'][i]['name'])
    nowConfirm.append(data['areaTree'][0]['children'][i]['total']['nowConfirm'])
    confirm.append(data['areaTree'][0]['children'][i]['total']['confirm'])
    dead.append(data['areaTree'][0]['children'][i]['total']['dead'])
    heal.append(data['areaTree'][0]['children'][i]['total']['heal'])

# 将数据封装成 ['北京', [325, 923, 9, 589]] 这样的形式方便于数据可视化
data_pair = []
for i in range(34):
    x = []
    x.append(confirm[i])
    x.append(dead[i])
    x.append(heal[i])
    x.append(nowConfirm[i])
    data_pair.append(x)

testv = []
for i in range(34):
    testMap = [area[i], data_pair[i]]
    testv.append(testMap)

tools_js = """
    function (params){
        console.log(params.data);
        return params.name + ' - ' + '<br/>'
               + '现存确诊:' +  params.data.value[3]
               + '累计确诊:' +  params.data.value[0] + '<br/>'
               + '死亡人数:' +  params.data.value[1]
               + '治愈人数:' +  params.data.value[2];
    }
"""
c = (
    Map()
    .add(
        series_name="",data_pair=testv,maptype="china", label_opts=opts.LabelOpts(
            is_show=True),is_map_symbol_show=False
        )
    .set_series_opts(label_opts=opts.LabelOpts(
                    formatter="{b|{b}}",
                    rich={
                        'b': {
                            'fontSize': 14,
                            'color': '#fff',
                            'textBorderColor': 'black',
                            'textBorderWidth': '0.5'
                        }
                    }
                    ))
    .set_global_opts(title_opts=opts.TitleOpts(title="2020中国疫情地图",subtitle='Ramelon'),
                     visualmap_opts=opts.VisualMapOpts(is_piecewise=True, pieces=[
                                                         {"max": 0, "label": "0", "color": "#ffffff"},
                                                         {"min": 1, "max": 10, "color": "#ebb4a8"},
                                                         {"min": 10, "max": 100, "color": "#e09694"},
                                                         {"min": 100, "max": 500, "color": "#cb8382"},
                                                         {"min": 500, "max": 1000, "color": "#b27372"},
                                                         {"min": 1000, "color": "#976461"},
                                                       ],is_inverse=True, pos_right=10,
                                                       ),
                     tooltip_opts=opts.TooltipOpts(axis_pointer_type='shadow',background_color='white',
                                                    border_width=1, textstyle_opts=opts.TextStyleOpts(color='black'),
                                                    formatter=(JsCode(tools_js))
                                                   )

                     )
    .render("China_2019-nCov_map.html")
    )
