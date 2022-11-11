from bs4 import BeautifulSoup
import requests
import json
import time
import random
headers = {
     'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36'
 }
file = requests.get('https://rost.kh.ua/catalog/produktovaya_gruppa/',headers=headers)
soup = BeautifulSoup(file,'html.parser')
categories = soup.find_all('a',class_='display_all')
categories_for_json = {}
for item in categories:
    categories_for_json[item.text.strip()] = str('https://rost.kh.ua'+item['href'])
with open('links_group.json','w', encoding='utf-8') as link_group_file:
    json.dump(categories_for_json,link_group_file,indent=4,ensure_ascii=False)

with_categories_and_subcategories_for_json = {}
array_of_categories = []
count = 0
array_of_subcategories = []
count_for_goods = 0
with_subcategories_and_goods_for_json = {}
goods_info = []

for item in categories_for_json:
    array_of_categories.append(item)
try:
    while count < len(array_of_categories)-2:
        for item in categories_for_json.values():
            if item == "https://rost.kh.ua/catalog/produktovaya_gruppa-detskoe_pitanie/"  | item == 'https://rost.kh.ua/catalog/produktovaya_gruppa-sushi_i_syre_dlya_ix_prigotovleniya/':
                continue
            else:
                print('')
       
            res2 = requests.get(item,headers=headers)
            time.sleep(random.randint(2, 4))
            soup2 = BeautifulSoup(res2.text,'html.parser')
            subcategories = soup2.find_all('a',class_='display_all')
            for sub in subcategories:
                array_of_subcategories.append(sub.text.strip())
                print(sub['href'])
                res3 = requests.get('https://rost.kh.ua'+sub['href'],headers=headers)
                soup3 = BeautifulSoup(res3.text,'html.parser')
                body_card = soup3.find_all('div', class_ = 'item-card')
                for item in body_card:
                    title = item.find('h4', class_ = 'item-title')
                    price = item.find('span', class_ = 'big-price')
                    img = item.find('img')
                    print(img)
                    good = {'title':title.text.strip(),'price':price.text.strip(),'img':'https://rost.kh.ua'+img['src']}
                    goods_info.append(good.copy())
                with_subcategories_and_goods_for_json[sub.text.strip()]=goods_info.copy()
                goods_info.clear()
            with_categories_and_subcategories_for_json[array_of_categories[count]] = with_subcategories_and_goods_for_json.copy()
            time.sleep(random.randint(2, 4))
            array_of_subcategories.clear()
            count = count+1 
            with_subcategories_and_goods_for_json.clear()
finally:
    with open('links_group_with_subgroup.json' , 'w' ,encoding='utf-8') as links_group_with_subgroup:
        json.dump(with_categories_and_subcategories_for_json,links_group_with_subgroup,indent=4,ensure_ascii=False)
