import requests
import json
import time
import csv
import os

CSV_BASE_PATH = os.getenv('CSV_PATH', './data')


def callback2dict(src_data: str, callback: str) -> dict:
    data_tmp = src_data.replace(callback, '', 1)
    if data_tmp.startswith('('):
        data_tmp = data_tmp[1:]
    if data_tmp.endswith(')'):
        data_tmp = data_tmp[:-1]

    return dict(json.loads(data_tmp))


def save_fund_list():
    CSV_PATH = os.path.join(CSV_BASE_PATH, )
    if not os.path.isdir(CSV_PATH):
        os.makedirs(CSV_PATH)

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"
    }
    url = "http://fund.eastmoney.com/js/fundcode_search.js"
    res = requests.get(url, headers=headers)
    
    fund_info_sets = []
    fund_info_src = res.text.replace('var r = [', '').replace('];', '').replace('],[', '@@').replace('"', '')[1:-1].split('@@')
    for item in fund_info_src:
        token = item.split(',')
        fund_info_sets.append({'基金代码':token[0], '拼音缩写': token[1], '基金名称': token[2], '基金类型':token[3], '拼音全称': token[4]})
    # print(fund_info_sets[0])
    
    data_frame = ['基金代码', '拼音缩写', '基金名称', '基金类型', '拼音全称']

    with open('./data/fund_list.csv', 'w') as f:
        writer = csv.DictWriter(f, fieldnames=data_frame)
        writer.writeheader()
        writer.writerows(fund_info_sets)

    
def save_fund_lsjz(code:str):
    CSV_PATH = os.path.join(CSV_BASE_PATH, 'lsjz')
    if not os.path.isdir(CSV_PATH):
        os.makedirs(CSV_PATH)

    url = "http://api.fund.eastmoney.com/f10/lsjz"
    callback = "jQuery18306461675574671744_1588245122574"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
        "Referer": f"http://fundf10.eastmoney.com/jjjz_{code}.html",
    }
    params = {
        "callback": callback,
        "fundCode": code,
        "pageIndex": "1",
        "pageSize": "10000",
        "startDate": "",
        "endDate": "",
        "_": round(time.time() * 1000),
    }
    r = requests.get(url, params=params, headers=headers)

    data = callback2dict(r.text, callback)
    
    if len(data['Data']['LSJZList']) > 0:
        file_name = os.path.join(CSV_PATH, f'{code}.csv')
        with open(file_name, 'w') as f:
            field_name = data['Data']['LSJZList'][0].keys()
            writer = csv.DictWriter(f=f, fieldnames=field_name)
            
            writer.writeheader()
            writer.writerows(data['Data']['LSJZList'])
    else:
        print(code)
        print(data['Data'])
        print('=====================')
        
def save_all_fund_lsjz():
    fund_list = []
    data_frame = ['基金代码', '拼音缩写', '基金名称', '基金类型', '拼音全称']
    with open('./data/fund_list.csv', 'r') as f:
        reader = csv.DictReader(f, fieldnames=data_frame)

        header_flag = True
        
        for row in reader:
            if not header_flag:
                fund_list.append(row['基金代码'])
            else:
                header_flag = False
                
    for code in fund_list:
        save_fund_lsjz(code)


if __name__ == '__main__':
    save_fund_list()
    save_all_fund_lsjz()