import models.publisher as publisher_model
import models.book as book_model
import models.sqlalchemy_config as sqlalchemy_config
import models.supplier as supplier_model
import requests
from itertools import cycle
import time
import os
import json
import re
import models.shipping as shipping_model


def search_shipping_item_by_temp_member_name(shipping_item_id, member_info):
    shipping_item_id = shipping_item_id
    temp_member_name = member_info["temp_member_name"]
    change_member_id = member_info["member_id"]

    db = sqlalchemy_config.get_db()
    result_shipping_items = shipping_model.get_shipping_by_temp_member_name(db, temp_member_name)

    for result_shipping_item in result_shipping_items:
        if result_shipping_item:
            result_shipping_item_id = result_shipping_item.shipping_id
            result_temp_member_name = result_shipping_item.temp_member_name
            result_member_id = result_shipping_item.member_id
            if result_temp_member_name == temp_member_name:
                print(f"-----")
                print(
                    f"Shipping Item ID: {result_shipping_item_id} | Member: {result_temp_member_name} = {temp_member_name} Changed Member ID:{result_member_id} to {change_member_id}")
                shipping_model.update_shipping_by_id(db, result_shipping_item_id,
                                                                      {"member_id": change_member_id})

    db.close()


if __name__ == '__main__':
    member_names = {
        "som201504160001601": {"temp_member_name": "詹正德PC", "member_id": 16},
        "som201504200002801": {"temp_member_name": "曾建富", "member_id": 28},
        "som201504200003701": {"temp_member_name": "林新淵(轉讓汪世旭,不再使用此帳號)", "member_id": 37},
        "som201504230006501": {"temp_member_name": "林詩涵P", "member_id": 65},
        "som201504270002201": {"temp_member_name": "鍾尚樺PC", "member_id": 22},
        "som201505070006201": {"temp_member_name": "黃淑貞C", "member_id": 62},
        "som201505140002901": {"temp_member_name": "廖珮璇C", "member_id": 29},
        "som201506040001001": {"temp_member_name": "蘇紋雯P", "member_id": 10},
        "som201506050006801": {"temp_member_name": "林世傑P", "member_id": 68},
        "som201507090008201": {"temp_member_name": "陳秀蘭PC", "member_id": 82},
        "som201507140007501": {"temp_member_name": "洪存", "member_id": 75},
        "som201507290005501": {"temp_member_name": "張文彬P", "member_id": 55},
        "som201508120008501": {"temp_member_name": "陳瑋駿P", "member_id": 85},
        "som201508280008601": {"temp_member_name": "陳詠安C", "member_id": 86},
        "som201509150008301": {"temp_member_name": "財團法人人智學教育基金會", "member_id": 83},
        "som201511240010201": {"temp_member_name": "林佑鍶", "member_id": 102},
        "som201512150010301": {"temp_member_name": "廖妙卿C", "member_id": 103},
        "som201512210009301": {"temp_member_name": "邱月亭C", "member_id": 93},
        "som201605100011301": {"temp_member_name": "吳佳靜P", "member_id": 113},
        "som201606010012801": {"temp_member_name": "周奕成(1920)P++C", "member_id": 128},
        "som201606170013301": {"temp_member_name": "王逸夫C", "member_id": 133},
        "som201606200012901": {"temp_member_name": "趙瑜玲C", "member_id": 129},
        "som201608290013701": {"temp_member_name": "張慧如C", "member_id": 137},
        "som201609120013801": {"temp_member_name": "蔡瑞珊(華山)PC", "member_id": 138},
        "som201705170015901": {"temp_member_name": "唐曼凌C", "member_id": 159},
        "som201706140016301": {"temp_member_name": "張翰文C", "member_id": 163},
        "som201707030016401": {"temp_member_name": "吳易臨C", "member_id": 164},
        "som201708300016801": {"temp_member_name": "蔡瑞珊(北藝)PC", "member_id": 168},
        "som201709060017101": {"temp_member_name": "陳巍仁C", "member_id": 171},
        "som201711010017401": {"temp_member_name": "鄧雅文P", "member_id": 174},
        "som201711130017901": {"temp_member_name": "其它銷售", "member_id": 179},
        "som201711170017701": {"temp_member_name": "許菁珊C", "member_id": 177},
        "som201712050017601": {"temp_member_name": "林彥廷C", "member_id": 176},
        "som201712220016901": {"temp_member_name": "陳芃諭P", "member_id": 169},
        "som201806120019701": {"temp_member_name": "財團法人文心藝術基金會(藝所)P", "member_id": 197},
        "som201808100020101": {"temp_member_name": "(退社)吳亭儀C", "member_id": 201},
        "som201808100020601": {"temp_member_name": "何新松", "member_id": 206},
        "som201808170020501": {"temp_member_name": "劉育育C", "member_id": 205},
        "som201809180020701": {"temp_member_name": "范立穎C", "member_id": 207},
        "som201810110020801": {"temp_member_name": "陳脩平C", "member_id": 208},
        "som201810250021001": {"temp_member_name": "蒲錦洪C", "member_id": 210},
        "som201811260021101": {"temp_member_name": "龔心怡P", "member_id": 211},
        "som201901220021401": {"temp_member_name": "廖子鈞C", "member_id": 214},
        "som201903070022801": {"temp_member_name": "徐孝晴P", "member_id": 228},
        "som201903190021501": {"temp_member_name": "(寄售)書局", "member_id": 215},
        "som201904250022001": {"temp_member_name": "張沛榛PC", "member_id": 220},
        "som201904250023301": {"temp_member_name": "陳官廷P", "member_id": 233},
        "som201905080023001": {"temp_member_name": "總裁青鳥(蔡瑞珊)", "member_id": 230},
        "som201905090022501": {"temp_member_name": "陳柏諺", "member_id": 225},
        "som201908070024201": {"temp_member_name": "蔡瑞珊(太平)PC+", "member_id": 242},
        "som201912020025001": {"temp_member_name": "張嘉倪P", "member_id": 250},
        "som202001020025201": {"temp_member_name": "陳添順(風旅)", "member_id": 252},
        "som202002260025401": {"temp_member_name": "林榮基P", "member_id": 254},
        "som202003110026001": {"temp_member_name": "蔡瑞珊(南村)", "member_id": 260},
        "som202005270026301": {"temp_member_name": "翁禎霞PC", "member_id": 263},
        "som202006090026501": {"temp_member_name": "鍾添涵", "member_id": 265},
        "som202007210027501": {"temp_member_name": "林欣穎P", "member_id": 275},
        "som202007290027401": {"temp_member_name": "顏惠珠C", "member_id": 274},
        "som202008050027801": {"temp_member_name": "(寄售)書店", "member_id": 278},
        "som202008130028101": {"temp_member_name": "沙彥羲P", "member_id": 281},
        "som202008180027101": {"temp_member_name": "林彥汝C", "member_id": 271},
        "som202008280028301": {"temp_member_name": "夏淑儀P", "member_id": 283},
        "som202103120029601": {"temp_member_name": "甘庭嘉P", "member_id": 296},
        "som202103260030301": {"temp_member_name": "鄭煜彬(臺灣代表)", "member_id": 303},
        "som202104290030601": {"temp_member_name": "(員工)田芳羽", "member_id": 306},
        "som202105030030401": {"temp_member_name": "辦公室體驗3", "member_id": 304},
        "som202106240030901": {"temp_member_name": "(員工)高嘉瑀", "member_id": 309},
        "som202108020031001": {"temp_member_name": "(員工)邱泳涵", "member_id": 310},
        "som202108120031201": {"temp_member_name": "王茜茜(逃逸線)", "member_id": 312},
        "som202108270032401": {"temp_member_name": "謝正川C", "member_id": 324},
        "som202109150032501": {"temp_member_name": "李雅靖P", "member_id": 325},
        "som202110050032801": {"temp_member_name": "陳威豪P+", "member_id": 328},
        "som202111150031601": {"temp_member_name": "曾琮彥P+", "member_id": 316},
        "som202111240033301": {"temp_member_name": "張文彬(台文館)P", "member_id": 333},
        "som202112080033501": {"temp_member_name": "趙偉仁P", "member_id": 335},
        "som202201060032601": {"temp_member_name": "(員工)鍾菀勻", "member_id": 326},
        "som202201120033901": {"temp_member_name": "辦公室體驗2", "member_id": 339},
        "som202202210033801": {"temp_member_name": "高世澤P", "member_id": 338},
        "som202202250031401": {"temp_member_name": "(前員工)借使用驚喜包", "member_id": 314},
        "som202203040034101": {"temp_member_name": "羅健福P", "member_id": 341},
        "som202203070034301": {"temp_member_name": "林世傑(文學館)P", "member_id": 343},
        "som202204110034401": {"temp_member_name": "楊宗翰P", "member_id": 344},
        "som202204250034801": {"temp_member_name": "陳虹吟P+", "member_id": 348},
        "som202207290034901": {"temp_member_name": "(員工)蔡佩珊", "member_id": 349},
        "som202208160035701": {"temp_member_name": "友善書業", "member_id": 357},
        "som202211240036201": {"temp_member_name": "(員工)陳孟涵", "member_id": 362},
        "som202212160037101": {"temp_member_name": "陳常智_奎府聚(基地書店2)", "member_id": 371},
        "som202303100036801": {"temp_member_name": "（非社員買斷）萬卷樓", "member_id": 368},
        "som202305250038601": {"temp_member_name": "(員工)葉澄羽", "member_id": 386},
        "som202306290038701": {"temp_member_name": "(員工)莊中辰", "member_id": 387},
        "som202309260038501": {"temp_member_name": "(員工)温君梅", "member_id": 385},
        "som202311200020201": {"temp_member_name": "", "member_id": 202},
        "som202312290024201": {"temp_member_name": "蔡瑞珊(太平)", "member_id": 242},
        "som202404180013801": {"temp_member_name": "蔡瑞珊(華山)", "member_id": 138},
        "som202404180016801": {"temp_member_name": "(退社)蔡瑞珊(北藝)", "member_id": 168},
    }
    for shipping_item_id, member_info in member_names.items():
        search_shipping_item_by_temp_member_name(shipping_item_id, member_info)
