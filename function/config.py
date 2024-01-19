rawdata_path = '/Users/alexlo/Desktop/Project/Sport_Lottery/rawdata'
workdata_path = '/Users/alexlo/Desktop/Project/Sport_Lottery/workdata'
database_url = 'https://docs.google.com/spreadsheets/d/1IcTCgwnIk_EKnqRdBYK7-MGfxiTrxbTnm3-89Fc76X4/edit?usp=sharing'

back_links = [
    '','','','','','',
    'https://www.cakeresume.com/companies/playsport-cc',
    'https://mypaper.pchome.com.tw/slk_1320',
    'https://sites.ipaddress.com/playsport.cc/',
    'https://decoratoradvice.com/our-favorite-site-list/',
    'https://ro.wikipedia.org/wiki/Calific%C4%83rile_pentru_Campionatul_Mondial_de_Fotbal_2018_(AFC)_%E2%80%93_prima_rund%C4%83',
    'https://www.juksy.com/article/98898',
    'https://www.jkforum.net/home.php?mod=space&uid=3545071',
    'https://tw.pycon.org/2018/zh-hant/events/talk/596319992962613435/',
]

alliance_dict = {
    'NBA': '3',
    '歐洲職籃': '8',
    '韓國職籃': '92',
    '中國職籃': '94',
    '日本職籃': '97',
    '澳洲職籃': '12',
    '澳洲職棒': '83',
    '足球': '4',
    'NHL冰球': '91',
    '俄羅斯冰球': '87',
    '賽馬': '90',
    '美式足球': '93',
}

during_list = [
    'lastmonth',
    'thismonth',
    'lastweek',
    'thisweek',
    'season',
]

img_url_dict = {
    'NBA':'https://media.cnn.com/api/v1/images/stellar/prod/160204121559-nba-slam-dunk-23.jpg?q=x_4,y_0,h_1934,w_3437,c_crop/w_800',
    '歐洲職籃': 'https://cdn.britannica.com/44/193844-131-1E4A9F84/ball-net-basketball-game-arena.jpg',
    '韓國職籃': 'https://www.rappler.com/tachyon/2022/12/rhenz-abando-december-18-20222.jpeg',
    '中國職籃': 'https://news.cgtn.com/news/3d3d514f7a51444e34457a6333566d54/img/93a0a0eb0d2b491882b87983bd22919a/93a0a0eb0d2b491882b87983bd22919a.jpg',
    '日本職籃': 'https://cdn.britannica.com/44/193844-131-1E4A9F84/ball-net-basketball-game-arena.jpg',
    '澳洲職籃': 'https://cdn.britannica.com/44/193844-131-1E4A9F84/ball-net-basketball-game-arena.jpg',
    '澳洲職棒': 'https://m.thepeninsulaqatar.com/get/maximage/20230309_1678356344-391.jpeg?1678356344',
    '足球':'https://img1.wsimg.com/isteam/ip/062f8e95-2657-40ed-a40a-acb450331c62/8-20200926-IMG_5064.jpg/:/cr=t:26.49%25,l:33.91%25,w:64.94%25,h:48.72%25/rs=w:1240,h:620,cg:true,m',
    'NHL冰球':'https://help.viaplay.com/wp-content/uploads/capture-3-1024x576.png',
    '俄羅斯冰球': 'https://static01.nyt.com/images/2016/11/08/sports/08KUNLUNWEB3/08KUNLUNWEB3-articleLarge.jpg',
    '賽馬': 'https://flameracing.files.wordpress.com/2023/07/20230723_invisible_self.jpg?w=1200',
    '美式足球': 'https://news-data.pts.org.tw/news_images/512396/1612749030t.jpg',
}

help_text = '''請輸入以下格式進行爬蟲: 目標 資料範圍 爬取數量 郵件帳號1 郵件帳號2...
e.g. NBA thismonth 15 aaa@gmail.com bbb@gmail.com

目標包含: NBA, 歐洲職籃, 韓國職籃, 中國職籃, 日本職籃, 澳洲職籃, 澳洲職棒, 足球, NHL冰球, 俄羅斯冰球, 賽馬, 美式足球。

資料範圍包含: lastmonth, thismonth, lastweek, thisweek, season。

爬取數量範圍: 1~30，如果有開放預測的人不足，則會爬取所有開放預測的人。'''

NBA_team = [
    "底特律活塞", "休士頓火箭", "猶他爵士", "明尼蘇達灰狼", "達拉斯獨行俠", "洛杉磯湖人", "曼斐斯灰熊",
    "紐約尼克", "沙加緬度國王", "芝加哥公牛", "丹佛金塊", "波士頓塞爾提克", "費城76人", "印第安那溜馬",
    "紐奧良鵜鶘", "鳳凰城太陽", "金州勇士", "布魯克林籃網", "邁阿密熱火", "密爾瓦基公鹿", "洛杉磯快艇",
    "亞特蘭大老鷹", "奧克拉荷馬雷霆", "聖安東尼奧馬刺", "華盛頓巫師", "多倫多暴龍", "奧蘭多魔術",
    "夏洛特黃蜂", "波特蘭拓荒者", "克里夫蘭騎士",
]
CBA_team = [
    "新疆廣匯飛虎", "青島國信海天雄鷹", "寧波富邦火箭", "福建鱘潯興", "吉林東北虎", "深圳新世紀烈豹", "山東高速", "山西汾酒猛龍",
    "天津榮鋼先行者", "浙江廣廈猛獅", "廣東宏遠華南虎", "上海久事大鯊魚", "浙江稠州金牛", "遼寧瀋陽三生飛豹", "北京北汽", "江蘇龍",
    "廣州龍獅", "北京控股紫禁勇士", "四川金強藍鯨", "南京大聖"
]
NHL_team = [
    "大都會分區", "紐澤西魔鬼", "紐約島人", "紐約遊騎兵", "費城飛人", "匹茲堡企鵝", "卡羅萊納颶風", "華盛頓首都",
    "哥倫布藍衣", "大西洋分區", "波士頓棕熊", "水牛城軍刀", "蒙特婁加拿大人", "渥太華參議員", "多倫多楓葉",
    "佛羅里達美洲豹", "坦帕灣閃電", "底特律紅翼", "中央分區", "溫尼伯噴射機", "芝加哥黑鷹", "納許維爾掠奪者",
    "聖路易藍調", "科羅拉多雪崩", "明尼蘇達荒野", "達拉斯星辰", "亞歷桑那土狼", "太平洋分區", "卡加利火焰",
    "愛德蒙頓油人", "溫哥華加人", "安納罕鴨", "洛杉磯國王", "聖荷西鯊魚", "維加斯黃金騎士", "西雅圖海怪",
]
Korea_team = [
    "首爾三星迅雷", "蔚山現代太陽神", "釜山KCC宙斯盾", "昌原LG獵隼", "首爾SK騎士",
    "高陽索諾天空槍手", "安陽正官庄赤紅火箭", "水原KT爆音", "韓國石油公社", "原州東浦新世代",
]
Aus_team = [
    "布里斯本子彈", "墨爾本聯隊", "伯斯野貓", "紐西蘭破壞者", "肯因斯太攀蛇", "阿德雷德36人",
    "雪梨國王", "東南墨爾本鳳凰", "伊拉瓦拉老鷹", "塔斯馬尼亞跳蟻",
]
team_pattern = '|'.join(NBA_team+CBA_team+NHL_team+Korea_team+Aus_team)