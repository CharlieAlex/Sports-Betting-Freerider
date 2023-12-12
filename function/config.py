rawdata_path = '/Users/alexlo/Desktop/Project/Sport_Lottery/rawdata'
workdata_path = '/Users/alexlo/Desktop/Project/Sport_Lottery/workdata'

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