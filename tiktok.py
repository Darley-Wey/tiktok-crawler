import requests
import json
import re
from lxml import etree
requests.packages.urllib3.disable_warnings()


class Sessions(requests.Session):
    #重写部分request
    def request(self, *args, **kwargs):
        # 此处修改代理
        # proxies = {
        #     'https': 'socks5://127.0.0.1:10808',
        #     'http': 'socks5://127.0.0.1:10808'
        # }
        proxies = {
            "http": "http://127.0.0.1:8866",
            "https": "http://127.0.0.1:8866",
        }
        kwargs.setdefault('proxies', proxies)
        kwargs.setdefault('verify', False)
        return super(Sessions, self).request(*args, **kwargs)

#初始化session
def init(Session):
    session = Session()
    session.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.66'
    index_url = 'https://www.tiktok.com/?lang=en'
    response = session.get(index_url)
    return session
 

def get_user_info(session):
    #要爬取的用户主页地址
    user_url = 'https://www.tiktok.com/@sophie.seddon?lang=en'
    response = session.get(user_url).text
    following = re.search(
        r'title="Following">(.*?)</strong>', response).group(1)
    followers = re.search(
        r'title="Followers">(.*?)</strong>', response).group(1)
    likes = re.search(r'title="Likes">(.*?)</strong>', response).group(1)
    html = etree.HTML(response)
    js = html.xpath('//*[@id="__NEXT_DATA__"]/text()')
    json_data = json.loads(js[0])
    max_cursor = json_data['props']['pageProps']['videoListMaxCursor']
    user_id = json_data['props']['pageProps']['feedConfig']['id']
    videos = json_data['props']['pageProps']['items']
    videos_data = []
    for video in videos:
        videos_data.append((video['desc'], video['stats']))
    print(following, followers, likes)
    return following, followers, likes, videos_data, max_cursor, user_id


def get_recommend(session):
    discover_url = 'https://m.tiktok.com/node/share/discover'
    discover = session.get(discover_url).json()
    recommend = discover['body'][0]["exploreList"]
    recommend_list = []
    for account in recommend:
        recommend_list.append((account['cardItem']['subTitle'].replace(
            '@', ''), account['cardItem']['title']))
    for recommend in recommend_list:
        print(recommend)
    return recommend_list


def get_video_list(session, max_cursor, videos_data, user_id):
    video_url = 'https://t.tiktok.com/api/item_list/'
    params = {
        'count': '50',
        'maxCursor': max_cursor,
        'minCursor': '0',
        'sourceType': '8',
        'id': user_id
    }
    response = session.get(video_url, params=params).json()
    is_has_more = response['hasMore']
    max_cursor = response['maxCursor']
    videos = response['items']
    for video in videos:
        videos_data.append((video['desc'], video['stats']))
    if is_has_more == True:
        get_video_list(session, max_cursor, videos_data, user_id)
    for video in videos_data:
        print(video)
    return videos_data


if __name__ == "__main__":
    session = init(Sessions)
    user_info = get_user_info(session)
    videos_data = user_info[3]
    max_cursor = user_info[4]
    user_id = user_info[5]
    recommend = get_recommend(session)
    videos = get_video_list(session, max_cursor, videos_data, user_id)
    pass


#测试输出
'''
189 132.9K 2.5M
('bts_official_bighit', 'BTS')
('twice_tiktok_official', 'TWICE')
('gemdzq', 'GEM鄧紫棋')
('selina_1031', '任家萱Selina')
('jamhsiao_0330', '蕭敬騰')
('showlo', '羅志祥')
('willpan_23', '潘瑋柏 Will Pan')
('jolin_cai', '蔡依林')
('nana__ouyang', '歐陽娜娜Nana Ouyang')
('amit_feat_amei', 'aMEI')
('arashi_5_official', 'ARASHI')
('xinya_an', '安心亞')
('sunnyboyyyyy', '王陽明 Sunny Wang')
('sharon_hsu', '許維恩')
('cyndiwang905', '王心凌')
('official_bii', 'Bii畢書盡')
('davidbeckham', 'David Beckham')
('920alin', 'A-Lin')
('diegodtk09', '陳零九Nine Chen')
('eric.chou0622', 'Eric周興哲')
('butterfly092288', 'Butterfly愷樂')
('fafa19871115', '蔡黃汝 FLO.')
('nickthereal4sho', '周湯豪NICKTHEREAL')
('tialeeleelee', '李毓芬Tia Lee')
('blackie93', '黑人陳建州')
('rain.xix', 'RAIN')
('got7official', 'got7official')
('lockingjack', '許凱皓')
('by2girl', 'By2Girl')
('dansontang7', 'D.T. 唐禹哲')
('luv this trend #fyp #fairy 🧚🏼\u200d♀️', {'diggCount': 612, 'shareCount': 11, 'commentCount': 18, 'playCount': 3476})
('tip of the day: carry a film camera with u at all times !! you’ll thank me later xxx #film #fyp', {'diggCount': 6834, 'shareCount': 77, 'commentCount': 70, 'playCount': 23100})
('I ❤️ u all so much !! thank you for supporting me #fyp #sophieseddon', {'diggCount': 3063, 'shareCount': 26, 'commentCount': 26, 'playCount': 19400})
('1 month later .... #fyp #flat #2021', {'diggCount': 2109, 'shareCount': 19, 'commentCount': 25, 'playCount': 15000})
('that moment when @harrymorrismuso looks better in a skirt than i do 🌝 #fyp #boyfriend #outfit', {'diggCount': 8199, 'shareCount': 78, 'commentCount': 63, 'playCount': 44600})
('help me find this man \U0001f978 #fyp #soulmate 💘', {'diggCount': 13900, 'shareCount': 36, 'commentCount': 155, 'playCount': 173700})
('i am making bracelets and i will be uploading them to my website in January ! 💘 #fyp', {'diggCount': 1258, 'shareCount': 7, 'commentCount': 34, 'playCount': 14000})
('#stitch with @fashion_nissi', {'diggCount': 7730, 'shareCount': 71, 'commentCount': 110, 'playCount': 61600})
('this ain’t all but 🤩 #shoes #alt #fyp #sophieseddon', {'diggCount': 3696, 'shareCount': 41, 'commentCount': 70, 'playCount': 27700})
('guilty 😭 #cottagecore #alt #fyp', {'diggCount': 5363, 'shareCount': 36, 'commentCount': 36, 'playCount': 37100})
('ACCENT CHECK ! duet me #duet #accentcheck #accentchallenge #fyp', {'diggCount': 17700, 'shareCount': 528, 'commentCount': 1438, 'playCount': 116400})
('anyone else ??? 🥴 #fyp', {'diggCount': 4929, 'shareCount': 74, 'commentCount': 52, 'playCount': 3 0100})
('#AD - Here is my @gucci X @flannels wish list if anyone is struggling to find me a gift this Christmas #FLANNELSGucciWishlist #FLANNELS 🎄#fyp', {'diggCount': 1221, 'shareCount': 52, 'commentCount': 49, 'playCount': 32200})
('I struggled for years until I tried this technique #eyeliner #fyp', {'diggCount': 4632, 'shareCount': 63, 'commentCount': 32, 'playCount': 34500})
('Part 2 - moving into my flat 🔆💕🌀', {'diggCount': 3830, 'shareCount': 15, 'commentCount': 32, 'playCount': 35500})
('someone asked so here u go #curlyhair #sophieseddon #fyp', {'diggCount': 6080, 'shareCount': 49, 'commentCount': 72, 'playCount': 88500})
('Part 1 - showing u guys around my new flat !! ⚡️⭐️', {'diggCount': 14000, 'shareCount': 58, 'commentCount': 67, 'playCount': 89000})
('sorry @harrymorrismuso #hairgoals #boyfriend #fyp', {'diggCount': 3962, 'shareCount': 33, 'commentCount': 89, 'playCount': 30000})
('thrifted outfits every day of the week #vintage #sophieseddon #outfits #fyp', {'diggCount': 8228, 'shareCount': 71, 'commentCount': 55, 'playCount': 44000})
('#ad I love matching my outfits with the new Pret cups! What brings you joy? #JoyWithPret 💕✨ AD', {'diggCount': 2631, 'shareCount': 61, 'commentCount': 33, 'playCount': 46300})
('Song by Marcelo De La Vega - told you 🍭🧚🏼\u200d♀️🖤 #fyp #sophieseddon #outfitideas #fashion', {'diggCount': 1753, 'shareCount': 38, 'commentCount': 49, 'playCount': 15200})
('when I left school those boys were in my DMS 😂🥴 #fyp #sophieseddon #glowup', {'diggCount': 12600 , 'shareCount': 106, 'commentCount': 97, 'playCount': 76600})
('LINK IN BIO - 2nd vintage drop !! #sophieseddon #vintage #fyp', {'diggCount': 2836, 'shareCount': 44, 'commentCount': 25, 'playCount': 35700})
('hey #halloween #fyp #mycostume 😈 👼🏻', {'diggCount': 3783, 'shareCount': 16, 'commentCount': 49, 'playCount': 23300})
('#duet with @watchkittyshrink  HAHAHA i proper hate my accent', {'diggCount': 8432, 'shareCount': 32, 'commentCount': 82, 'playCount': 94900})
('this took me a while lmao 🤡🤡🤡 #fyp #sophieseddon #viral', {'diggCount': 5352, 'shareCount': 101, 'commentCount': 125, 'playCount': 33300})
("AD - #GOLDIERED25 making me feel #gucci 💄 let's see your best #guccibeauty look 💋 @gucci", {'diggCount': 1496, 'shareCount': 23, 'commentCount': 30, 'playCount': 34900})
('working super hard to get my website finished ✔️ #sophieseddon #fyp', {'diggCount': 3858, 'shareCount': 44, 'commentCount': 25, 'playCount': 23100})
('I do it for the girls and gays that’s it x #sophieseddon #fyp #viral', {'diggCount': 7655, 'shareCount': 14, 'commentCount': 43, 'playCount': 44600})
('i love events but sometimes they’re scary af #sophieseddon #fyp #viral #ukfashion', {'diggCount': 13200, 'shareCount': 40, 'commentCount': 80, 'playCount': 154300})
('#AD grooving to the jellyfish jam in my new #spongebob #pride t-shirt,\xa0available from George at Asda link in bio ❤️ @nickelodeonuk #wearegeorge', {'diggCount': 1324, 'shareCount': 22, 
'commentCount': 15, 'playCount': 17500})
('remove toxic ppl from ur life, you’ll thank me later #sophieseddon #fyp #viral', {'diggCount': 73700, 'shareCount': 144, 'commentCount': 160, 'playCount': 378200})
('⭐️✨ #stargazingchallenge', {'diggCount': 5163, 'shareCount': 27, 'commentCount': 58, 'playCount': 42300})
('we need to protect long haired men 🥰 @harrymorrismuso #boyfriend #sophieseddon #hairgoals', {'dig gCount': 33300, 'shareCount': 297, 'commentCount': 203, 'playCount': 211900})
('luv this song by @katyforkings ✌🏻#fyp #sophieseddon #viral #haircut', {'diggCount': 4233, 'shareCount': 7, 'commentCount': 40, 'playCount': 51500})
('it took me 15 mins dragging my mirror outside and 5 mins later it went cloudy omfg #sophieseddon #mirror #pinterest', {'diggCount': 8905, 'shareCount': 36, 'commentCount': 45, 'playCount': 62200})
('I saw a couple of ppl do this and i wanted to try it out ! #fakefreckles #sophieseddon #viral', {'diggCount': 3598, 'shareCount': 26, 'commentCount': 17, 'playCount': 44100})
('I can’t be the only one #viral #sophieseddon 🍓🐛🐜', {'diggCount': 18200, 'shareCount': 54, 'commentCount': 136, 'playCount': 156000})
('give me a new name #fyp #sophieseddon #viral 🍓', {'diggCount': 4663, 'shareCount': 21, 'commentCount': 1726, 'playCount': 39500})
('What did you do today for your future self ? Song by @bear  🐻 AD #viral #mountains #mentalhealthmatters', {'diggCount': 2762, 'shareCount': 10, 'commentCount': 30, 'playCount': 36500})  
('today #fyp #vintage #sophieseddon', {'diggCount': 4916, 'shareCount': 11, 'commentCount': 38, 'playCount': 46600})
('#duet with @livbehri #scoobydoo #scoobydoocosplay #fyp ❤️', {'diggCount': 17300, 'shareCount': 51, 'commentCount': 43, 'playCount': 138400})
('Reply to @sour_lemon_pie I hope this helps u find some cool clothes #sophieseddon #pinterest #ukfashion #vintage', {'diggCount': 3407, 'shareCount': 11, 'commentCount': 37, 'playCount': 40300})
('I ❤️ stranger things ! #strangerthings #80s #viral', {'diggCount': 8949, 'shareCount': 103, 'commentCount': 90, 'playCount': 69900})
('not true #fyp #curlyhair #viral', {'diggCount': 5273, 'shareCount': 6, 'commentCount': 41, 'playCount': 86600})
('millions of ppl have seen these photos on Pinterest but have no idea who it is , well it’s ME #fyp #pinterest #sophieseddon', {'diggCount': 24200, 'shareCount': 106, 'commentCount': 134, 
'playCount': 144100})
('3 thrifted outfits from @depop ! which one is ur fave? 1,2 or 3 #sophieseddon #outfitideas #fyp #ukfashion', {'diggCount': 5418, 'shareCount': 33, 'commentCount': 40, 'playCount': 49900})('depop haul , should i do more of these ? #depophaul #vintage #secondhand', {'diggCount': 8266, 'shareCount': 19, 'commentCount': 56, 'playCount': 64500})
('❤️🌞 #fyp #viral #positivity', {'diggCount': 13200, 'shareCount': 28, 'commentCount': 120, 'playCount': 79800})
('happy pride month everyone ! #pride #beyourselfchallenge #ally ❤️🧡💛💚💙💜', {'diggCount': 8558, 'shareCount': 34, 'commentCount': 36, 'playCount': 82700})
('u know when ur obsessed with scrunchies when .... #viral #sophieseddon #ukfashion', {'diggCount': 7844, 'shareCount': 84, 'commentCount': 42, 'playCount': 67100})
('hahahah I’ll cry at anything #foryoupage #viral #sophieseddon', {'diggCount': 4932, 'shareCount': 43, 'commentCount': 30, 'playCount': 54400})
('#tiktoktraditions  hA HA hA HA hA hA HAaaa #sophieseddon #fyp', {'diggCount': 4078, 'shareCount': 13, 'commentCount': 38, 'playCount': 56000})
('😭😭 #fyp #viral', {'diggCount': 23700, 'shareCount': 285, 'commentCount': 69, 'playCount': 222300})
('it’s the truth #UKfashion #sophieseddon #fyp', {'diggCount': 41000, 'shareCount': 253, 'commentCount': 61, 'playCount': 214100})
('why am i like this #viral #UKfashion #sophieseddon', {'diggCount': 5050, 'shareCount': 19, 'commentCount': 20, 'playCount': 42300})
('this is a joke 😭 #viral', {'diggCount': 14600, 'shareCount': 949, 'commentCount': 70, 'playCount': 188400})
('exposing myself big time 💀💀 thank GOD for puberty #fyp #viral', {'diggCount': 4571, 'shareCount': 17, 'commentCount': 39, 'playCount': 44600})
('i have a love/hate relationship with these sunglasses #fyp #viral', {'diggCount': 3787, 'shareCount': 6, 'commentCount': 13, 'playCount': 43600})
('I swear every British girl owned one #fyp #viral #ukfashion', {'diggCount': 16300, 'shareCount': 47, 'commentCount': 120, 'playCount': 382600})
('here are the answers to ur questions #fyp #sophieseddon #ukfashion', {'diggCount': 26600, 'shareCount': 411, 'commentCount': 56, 'playCount': 324500})
('story of my LIFE #fyp #sophieseddon', {'diggCount': 8714, 'shareCount': 176, 'commentCount': 81, 'playCount': 66100})
('long legs, short body = me 🌞 boat day with @harrymorrismuso #fyp #summer', {'diggCount': 4870, 'shareCount': 9, 'commentCount': 24, 'playCount': 50600})
('@harrymorrismuso  #relationship #couple #sophieseddon #fyp ❤️💓', {'diggCount': 4884, 'shareCount': 35, 'commentCount': 47, 'playCount': 109200})
('yikes thank god for rapidbrow #sophieseddon #fyp #pinterest', {'diggCount': 6143, 'shareCount': 1672, 'commentCount': 85, 'playCount': 97100})
('I secretly wanted the 80’s anyways.... #fyp #sophieseddon #ukfashion #aesthetic', {'diggCount': 247000, 'shareCount': 837, 'commentCount': 721, 'playCount': 1400000})
('i finally persuaded @harrymorrismuso to do this with me #fyp #sophieseddon #ukfashion ✨', {'diggCount': 56200, 'shareCount': 871, 'commentCount': 336, 'playCount': 736100})
('me every night #fyp #sophieseddon', {'diggCount': 6561, 'shareCount': 80, 'commentCount': 19, 'playCount': 64400})
('💀 #sophieseddon #UKfashion #pinterest', {'diggCount': 87700, 'shareCount': 160, 'commentCount': 438, 'playCount': 341200})
('this is all ur fault @tiktok_uk 💀😂 #sophieseddon #ukfashion #verified #fyp #speakyourmind', {'diggCount': 5719, 'shareCount': 3, 'commentCount': 56, 'playCount': 59500})
('when ur outfit goes viral #ukfashion #pinterest #sophieseddon', {'diggCount': 14900, 'shareCount': 37, 'commentCount': 63, 'playCount': 74700})
('i haven’t touched my brows since lockdown #fyp #lockdownlewks #secret #beautyhacks', {'diggCount': 16600, 'shareCount': 42, 'commentCount': 131, 'playCount': 301600})
('the last one is my fave #cartooncharacter 💀 #fyp', {'diggCount': 5731, 'shareCount': 26, 'commentCount': 38, 'playCount': 48200})
('I love my girlfriend @bass_ic ✨💓 #foryou #foryoupage #couplegoals', {'diggCount': 10500, 'shareCount': 228, 'commentCount': 98, 'playCount': 166800})
('im currently obsessed with this absolute BOP so i recreated moments from the video @yungblud  #weird #weareweird #ad ❤️💓', {'diggCount': 2582, 'shareCount': 5, 'commentCount': 31, 'playC
ount': 32000})
('I wanted to take my clothes off but apparently tiktok has guidelines against that 😂 #ifyouretooshy @the1975 #ad', {'diggCount': 4473, 'shareCount': 25, 'commentCount': 18, 'playCount': 61600})
('my favourite job so far ! #fyp #aesthetic #boyfriendcheck #goals', {'diggCount': 7559, 'shareCount': 49, 'commentCount': 43, 'playCount': 56600})
('sorry it took so long 🔆🍄 #Polaroid #vintage #fyp #aesthetic', {'diggCount': 2864, 'shareCount': 94, 'commentCount': 10, 'playCount': 37600})
('i cringed watching this lol #glowup #houseoftiktok #fyp #sophieseddon', {'diggCount': 4754, 'shareCount': 30, 'commentCount': 73, 'playCount': 43800})
('the daily brush @bass_ic #hairgoals #hairgrowth #aesthetic', {'diggCount': 23300, 'shareCount': 144, 'commentCount': 187, 'playCount': 220500})
('another day in paradise 🐌🌷#cottagecore #cottage #aesthetic #fyp', {'diggCount': 241300, 'shareCount': 5902, 'commentCount': 1757, 'playCount': 1000000})
('another day in the garden with my baby @bass_ic #cottagecore #cottagecorecheck #fyp #houseoftiktok', {'diggCount': 73200, 'shareCount': 825, 'commentCount': 170, 'playCount': 310000})    
('@bass_ic #fyp #boredvibes #houseoftiktok #foryoupage', {'diggCount': 52600, 'shareCount': 1482, 'commentCount': 276, 'playCount': 251300})
('!! 🌜✨  #houseoftiktok #foryoupage #viral #ukfashion', {'diggCount': 5783, 'shareCount': 69, 'commentCount': 26, 'playCount': 47700})
('space buns 🪐👽 ! #teachme #fyp #viral', {'diggCount': 4041, 'shareCount': 75, 'commentCount': 18,  'playCount': 49000})
('when ur 2 shy to use the underground because u know the coronavirus will b there #shychallenge #foryoupage #viral #shy', {'diggCount': 8914, 'shareCount': 79, 'commentCount': 44, 'playCount': 100200})
('2019, the year I started living ! 🔆 #fyp #viral #happiness #london', {'diggCount': 39300, 'shareCount': 368, 'commentCount': 150, 'playCount': 229500})
('I didn’t do a poo ! #coronavirus #papertowelchallenge #viral', {'diggCount': 9882, 'shareCount': 309, 'commentCount': 176, 'playCount': 104900})
('me styling @catfootweareu #ad #fyp #ukfashion', {'diggCount': 1966, 'shareCount': 25, 'commentCount': 13, 'playCount': 27200})
('ceo of ‘“it’s vintage” #fyp #london #ukfashion #vintagw #foryoupage', {'diggCount': 12500, 'shareCount': 160, 'commentCount': 53, 'playCount': 163400})
('Brick lane, London aka the best place for vintage fashion 🌈 #fyp #foryoupage #london #ukfashion', {'diggCount': 155300, 'shareCount': 14100, 'commentCount': 1279, 'playCount': 887300})  
('I really went from “no wait stop” to posing like that ????  #viral #fyp #foryoupge #london', {'diggCount': 30000, 'shareCount': 374, 'commentCount': 99, 'playCount': 202900})
('my boyfriend is the best 🥺❤️@harrymorrismuso #viral #fyp #foryoupage #boyfriend', {'diggCount': 3 8200, 'shareCount': 2544, 'commentCount': 88, 'playCount': 514200})
('me and @harrymorrismuso spent hours on this don’t let it flop ps who’s coming out with us on Saturday? 💀😂 #virał #foryoupage #foryou #ukfashion', {'diggCount': 17900, 'shareCount': 486, 'commentCount': 77, 'playCount': 155800})
('this vid is so cringe but my bf Tarzan is something else 🥺❤️ #foryou #foryoupage #viral #boyfrien dcheck', {'diggCount': 40300, 'shareCount': 1088, 'commentCount': 396, 'playCount': 658000})
('IT HAPPENS EVERY TIME !!! #foryoupage #foryou #viral #makeitviral', {'diggCount': 17000, 'shareCount': 53, 'commentCount': 30, 'playCount': 168400})
('lmao I was so grunge last year and now I’m a colourful af #foryoupage #foryou #virał #ukfashion', {'diggCount': 198900, 'shareCount': 2453, 'commentCount': 643, 'playCount': 1400000})    
('LA LA LAND #losangeles #foryoupage #foryou #viral', {'diggCount': 2377, 'shareCount': 44, 'commentCount': 10, 'playCount': 42100})
('👁 challenge #eyechallenge #foryou #foryoupage', {'diggCount': 5080, 'shareCount': 34, 'commentCou nt': 17, 'playCount': 86100})
('luv this trend #fyp #fairy 🧚🏼\u200d♀️', {'diggCount': 612, 'shareCount': 11, 'commentCount': 18, 'playCount': 3476})
('tip of the day: carry a film camera with u at all times !! you’ll thank me later xxx #film #fyp', {'diggCount': 6834, 'shareCount': 77, 'commentCount': 70, 'playCount': 23100})
('I ❤️ u all so much !! thank you for supporting me #fyp #sophieseddon', {'diggCount': 3063, 'shareCount': 26, 'commentCount': 26, 'playCount': 19400})
('1 month later .... #fyp #flat #2021', {'diggCount': 2109, 'shareCount': 19, 'commentCount': 25, 'playCount': 15000})
('that moment when @harrymorrismuso looks better in a skirt than i do 🌝 #fyp #boyfriend #outfit', {'diggCount': 8199, 'shareCount': 78, 'commentCount': 63, 'playCount': 44600})
('help me find this man \U0001f978 #fyp #soulmate 💘', {'diggCount': 13900, 'shareCount': 36, 'commentCount': 155, 'playCount': 173700})
('i am making bracelets and i will be uploading them to my website in January ! 💘 #fyp', {'diggCount': 1258, 'shareCount': 7, 'commentCount': 34, 'playCount': 14000})
('#stitch with @fashion_nissi', {'diggCount': 7730, 'shareCount': 71, 'commentCount': 110, 'playCount': 61600})
('this ain’t all but 🤩 #shoes #alt #fyp #sophieseddon', {'diggCount': 3696, 'shareCount': 41, 'commentCount': 70, 'playCount': 27700})
('guilty 😭 #cottagecore #alt #fyp', {'diggCount': 5363, 'shareCount': 36, 'commentCount': 36, 'playCount': 37100})
('ACCENT CHECK ! duet me #duet #accentcheck #accentchallenge #fyp', {'diggCount': 17700, 'shareCount': 528, 'commentCount': 1438, 'playCount': 116400})
('anyone else ??? 🥴 #fyp', {'diggCount': 4929, 'shareCount': 74, 'commentCount': 52, 'playCount': 3 0100})
('#AD - Here is my @gucci X @flannels wish list if anyone is struggling to find me a gift this Christmas #FLANNELSGucciWishlist #FLANNELS 🎄#fyp', {'diggCount': 1221, 'shareCount': 52, 'commentCount': 49, 'playCount': 32200})
('I struggled for years until I tried this technique #eyeliner #fyp', {'diggCount': 4632, 'shareCount': 63, 'commentCount': 32, 'playCount': 34500})
('Part 2 - moving into my flat 🔆💕🌀', {'diggCount': 3830, 'shareCount': 15, 'commentCount': 32, 'playCount': 35500})
('someone asked so here u go #curlyhair #sophieseddon #fyp', {'diggCount': 6080, 'shareCount': 49, 'commentCount': 72, 'playCount': 88500})
('Part 1 - showing u guys around my new flat !! ⚡️⭐️', {'diggCount': 14000, 'shareCount': 58, 'commentCount': 67, 'playCount': 89000})
('sorry @harrymorrismuso #hairgoals #boyfriend #fyp', {'diggCount': 3962, 'shareCount': 33, 'commentCount': 89, 'playCount': 30000})
('thrifted outfits every day of the week #vintage #sophieseddon #outfits #fyp', {'diggCount': 8228, 'shareCount': 71, 'commentCount': 55, 'playCount': 44000})
('#ad I love matching my outfits with the new Pret cups! What brings you joy? #JoyWithPret 💕✨ AD', {'diggCount': 2631, 'shareCount': 61, 'commentCount': 33, 'playCount': 46300})
('Song by Marcelo De La Vega - told you 🍭🧚🏼\u200d♀️🖤 #fyp #sophieseddon #outfitideas #fashion', {'diggCount': 1753, 'shareCount': 38, 'commentCount': 49, 'playCount': 15200})
('when I left school those boys were in my DMS 😂🥴 #fyp #sophieseddon #glowup', {'diggCount': 12600 , 'shareCount': 106, 'commentCount': 97, 'playCount': 76600})
('LINK IN BIO - 2nd vintage drop !! #sophieseddon #vintage #fyp', {'diggCount': 2836, 'shareCount': 44, 'commentCount': 25, 'playCount': 35700})
('hey #halloween #fyp #mycostume 😈 👼🏻', {'diggCount': 3783, 'shareCount': 16, 'commentCount': 49, 'playCount': 23300})
('#duet with @watchkittyshrink  HAHAHA i proper hate my accent', {'diggCount': 8432, 'shareCount': 32, 'commentCount': 82, 'playCount': 94900})
('this took me a while lmao 🤡🤡🤡 #fyp #sophieseddon #viral', {'diggCount': 5352, 'shareCount': 101, 'commentCount': 125, 'playCount': 33300})
("AD - #GOLDIERED25 making me feel #gucci 💄 let's see your best #guccibeauty look 💋 @gucci", {'diggCount': 1496, 'shareCount': 23, 'commentCount': 30, 'playCount': 34900})
('working super hard to get my website finished ✔️ #sophieseddon #fyp', {'diggCount': 3858, 'shareCount': 44, 'commentCount': 25, 'playCount': 23100})
('I do it for the girls and gays that’s it x #sophieseddon #fyp #viral', {'diggCount': 7655, 'shareCount': 14, 'commentCount': 43, 'playCount': 44600})
('i love events but sometimes they’re scary af #sophieseddon #fyp #viral #ukfashion', {'diggCount': 13200, 'shareCount': 40, 'commentCount': 80, 'playCount': 154300})
('#AD grooving to the jellyfish jam in my new #spongebob #pride t-shirt,\xa0available from George at Asda link in bio ❤️ @nickelodeonuk #wearegeorge', {'diggCount': 1324, 'shareCount': 22, 
'commentCount': 15, 'playCount': 17500})
('remove toxic ppl from ur life, you’ll thank me later #sophieseddon #fyp #viral', {'diggCount': 73700, 'shareCount': 144, 'commentCount': 160, 'playCount': 378200})
('⭐️✨ #stargazingchallenge', {'diggCount': 5163, 'shareCount': 27, 'commentCount': 58, 'playCount': 42300})
('we need to protect long haired men 🥰 @harrymorrismuso #boyfriend #sophieseddon #hairgoals', {'dig gCount': 33300, 'shareCount': 297, 'commentCount': 203, 'playCount': 211900})
('luv this song by @katyforkings ✌🏻#fyp #sophieseddon #viral #haircut', {'diggCount': 4233, 'shareCount': 7, 'commentCount': 40, 'playCount': 51500})
('it took me 15 mins dragging my mirror outside and 5 mins later it went cloudy omfg #sophieseddon #mirror #pinterest', {'diggCount': 8905, 'shareCount': 36, 'commentCount': 45, 'playCount': 62200})
('I saw a couple of ppl do this and i wanted to try it out ! #fakefreckles #sophieseddon #viral', {'diggCount': 3598, 'shareCount': 26, 'commentCount': 17, 'playCount': 44100})
('I can’t be the only one #viral #sophieseddon 🍓🐛🐜', {'diggCount': 18200, 'shareCount': 54, 'commentCount': 136, 'playCount': 156000})
('give me a new name #fyp #sophieseddon #viral 🍓', {'diggCount': 4663, 'shareCount': 21, 'commentCount': 1726, 'playCount': 39500})
('What did you do today for your future self ? Song by @bear  🐻 AD #viral #mountains #mentalhealthmatters', {'diggCount': 2762, 'shareCount': 10, 'commentCount': 30, 'playCount': 36500})  
('today #fyp #vintage #sophieseddon', {'diggCount': 4916, 'shareCount': 11, 'commentCount': 38, 'playCount': 46600})
('#duet with @livbehri #scoobydoo #scoobydoocosplay #fyp ❤️', {'diggCount': 17300, 'shareCount': 51, 'commentCount': 43, 'playCount': 138400})
('Reply to @sour_lemon_pie I hope this helps u find some cool clothes #sophieseddon #pinterest #ukfashion #vintage', {'diggCount': 3407, 'shareCount': 11, 'commentCount': 37, 'playCount': 40300})
('I ❤️ stranger things ! #strangerthings #80s #viral', {'diggCount': 8949, 'shareCount': 103, 'commentCount': 90, 'playCount': 69900})
('not true #fyp #curlyhair #viral', {'diggCount': 5273, 'shareCount': 6, 'commentCount': 41, 'playCount': 86600})
('millions of ppl have seen these photos on Pinterest but have no idea who it is , well it’s ME #fyp #pinterest #sophieseddon', {'diggCount': 24200, 'shareCount': 106, 'commentCount': 134, 
'playCount': 144100})
('3 thrifted outfits from @depop ! which one is ur fave? 1,2 or 3 #sophieseddon #outfitideas #fyp #ukfashion', {'diggCount': 5418, 'shareCount': 33, 'commentCount': 40, 'playCount': 49900})('depop haul , should i do more of these ? #depophaul #vintage #secondhand', {'diggCount': 8266, 'shareCount': 19, 'commentCount': 56, 'playCount': 64500})
('❤️🌞 #fyp #viral #positivity', {'diggCount': 13200, 'shareCount': 28, 'commentCount': 120, 'playCount': 79800})
('happy pride month everyone ! #pride #beyourselfchallenge #ally ❤️🧡💛💚💙💜', {'diggCount': 8558, 'shareCount': 34, 'commentCount': 36, 'playCount': 82700})
('u know when ur obsessed with scrunchies when .... #viral #sophieseddon #ukfashion', {'diggCount': 7844, 'shareCount': 84, 'commentCount': 42, 'playCount': 67100})
('hahahah I’ll cry at anything #foryoupage #viral #sophieseddon', {'diggCount': 4932, 'shareCount': 43, 'commentCount': 30, 'playCount': 54400})
('#tiktoktraditions  hA HA hA HA hA hA HAaaa #sophieseddon #fyp', {'diggCount': 4078, 'shareCount': 13, 'commentCount': 38, 'playCount': 56000})
('😭😭 #fyp #viral', {'diggCount': 23700, 'shareCount': 285, 'commentCount': 69, 'playCount': 222300})
('it’s the truth #UKfashion #sophieseddon #fyp', {'diggCount': 41000, 'shareCount': 253, 'commentCount': 61, 'playCount': 214100})
('why am i like this #viral #UKfashion #sophieseddon', {'diggCount': 5050, 'shareCount': 19, 'commentCount': 20, 'playCount': 42300})
('this is a joke 😭 #viral', {'diggCount': 14600, 'shareCount': 949, 'commentCount': 70, 'playCount': 188400})
('exposing myself big time 💀💀 thank GOD for puberty #fyp #viral', {'diggCount': 4571, 'shareCount': 17, 'commentCount': 39, 'playCount': 44600})
('i have a love/hate relationship with these sunglasses #fyp #viral', {'diggCount': 3787, 'shareCount': 6, 'commentCount': 13, 'playCount': 43600})
('I swear every British girl owned one #fyp #viral #ukfashion', {'diggCount': 16300, 'shareCount': 47, 'commentCount': 120, 'playCount': 382600})
('here are the answers to ur questions #fyp #sophieseddon #ukfashion', {'diggCount': 26600, 'shareCount': 411, 'commentCount': 56, 'playCount': 324500})
('story of my LIFE #fyp #sophieseddon', {'diggCount': 8714, 'shareCount': 176, 'commentCount': 81, 'playCount': 66100})
('long legs, short body = me 🌞 boat day with @harrymorrismuso #fyp #summer', {'diggCount': 4870, 'shareCount': 9, 'commentCount': 24, 'playCount': 50600})
('@harrymorrismuso  #relationship #couple #sophieseddon #fyp ❤️💓', {'diggCount': 4884, 'shareCount': 35, 'commentCount': 47, 'playCount': 109200})
('yikes thank god for rapidbrow #sophieseddon #fyp #pinterest', {'diggCount': 6143, 'shareCount': 1672, 'commentCount': 85, 'playCount': 97100})
('I secretly wanted the 80’s anyways.... #fyp #sophieseddon #ukfashion #aesthetic', {'diggCount': 247000, 'shareCount': 837, 'commentCount': 721, 'playCount': 1400000})
('i finally persuaded @harrymorrismuso to do this with me #fyp #sophieseddon #ukfashion ✨', {'diggCount': 56200, 'shareCount': 871, 'commentCount': 336, 'playCount': 736100})
('me every night #fyp #sophieseddon', {'diggCount': 6561, 'shareCount': 80, 'commentCount': 19, 'playCount': 64400})
('💀 #sophieseddon #UKfashion #pinterest', {'diggCount': 87700, 'shareCount': 160, 'commentCount': 438, 'playCount': 341200})
('this is all ur fault @tiktok_uk 💀😂 #sophieseddon #ukfashion #verified #fyp #speakyourmind', {'diggCount': 5719, 'shareCount': 3, 'commentCount': 56, 'playCount': 59500})
('when ur outfit goes viral #ukfashion #pinterest #sophieseddon', {'diggCount': 14900, 'shareCount': 37, 'commentCount': 63, 'playCount': 74700})
('i haven’t touched my brows since lockdown #fyp #lockdownlewks #secret #beautyhacks', {'diggCount': 16600, 'shareCount': 42, 'commentCount': 131, 'playCount': 301600})
('the last one is my fave #cartooncharacter 💀 #fyp', {'diggCount': 5731, 'shareCount': 26, 'commentCount': 38, 'playCount': 48200})
('I love my girlfriend @bass_ic ✨💓 #foryou #foryoupage #couplegoals', {'diggCount': 10500, 'shareCount': 228, 'commentCount': 98, 'playCount': 166800})
('im currently obsessed with this absolute BOP so i recreated moments from the video @yungblud  #weird #weareweird #ad ❤️💓', {'diggCount': 2582, 'shareCount': 5, 'commentCount': 31, 'playC
ount': 32000})
('I wanted to take my clothes off but apparently tiktok has guidelines against that 😂 #ifyouretooshy @the1975 #ad', {'diggCount': 4473, 'shareCount': 25, 'commentCount': 18, 'playCount': 61600})
('my favourite job so far ! #fyp #aesthetic #boyfriendcheck #goals', {'diggCount': 7559, 'shareCount': 49, 'commentCount': 43, 'playCount': 56600})
('sorry it took so long 🔆🍄 #Polaroid #vintage #fyp #aesthetic', {'diggCount': 2864, 'shareCount': 94, 'commentCount': 10, 'playCount': 37600})
('i cringed watching this lol #glowup #houseoftiktok #fyp #sophieseddon', {'diggCount': 4754, 'shareCount': 30, 'commentCount': 73, 'playCount': 43800})
('the daily brush @bass_ic #hairgoals #hairgrowth #aesthetic', {'diggCount': 23300, 'shareCount': 144, 'commentCount': 187, 'playCount': 220500})
('another day in paradise 🐌🌷#cottagecore #cottage #aesthetic #fyp', {'diggCount': 241300, 'shareCount': 5902, 'commentCount': 1757, 'playCount': 1000000})
('another day in the garden with my baby @bass_ic #cottagecore #cottagecorecheck #fyp #houseoftiktok', {'diggCount': 73200, 'shareCount': 825, 'commentCount': 170, 'playCount': 310000})    
('@bass_ic #fyp #boredvibes #houseoftiktok #foryoupage', {'diggCount': 52600, 'shareCount': 1482, 'commentCount': 276, 'playCount': 251300})
('!! 🌜✨  #houseoftiktok #foryoupage #viral #ukfashion', {'diggCount': 5783, 'shareCount': 69, 'commentCount': 26, 'playCount': 47700})
('space buns 🪐👽 ! #teachme #fyp #viral', {'diggCount': 4041, 'shareCount': 75, 'commentCount': 18,  'playCount': 49000})
('when ur 2 shy to use the underground because u know the coronavirus will b there #shychallenge #foryoupage #viral #shy', {'diggCount': 8914, 'shareCount': 79, 'commentCount': 44, 'playCount': 100200})
('2019, the year I started living ! 🔆 #fyp #viral #happiness #london', {'diggCount': 39300, 'shareCount': 368, 'commentCount': 150, 'playCount': 229500})
('I didn’t do a poo ! #coronavirus #papertowelchallenge #viral', {'diggCount': 9882, 'shareCount': 309, 'commentCount': 176, 'playCount': 104900})
('me styling @catfootweareu #ad #fyp #ukfashion', {'diggCount': 1966, 'shareCount': 25, 'commentCount': 13, 'playCount': 27200})
('ceo of ‘“it’s vintage” #fyp #london #ukfashion #vintagw #foryoupage', {'diggCount': 12500, 'shareCount': 160, 'commentCount': 53, 'playCount': 163400})
('Brick lane, London aka the best place for vintage fashion 🌈 #fyp #foryoupage #london #ukfashion', {'diggCount': 155300, 'shareCount': 14100, 'commentCount': 1279, 'playCount': 887300})  
('I really went from “no wait stop” to posing like that ????  #viral #fyp #foryoupge #london', {'diggCount': 30000, 'shareCount': 374, 'commentCount': 99, 'playCount': 202900})
('my boyfriend is the best 🥺❤️@harrymorrismuso #viral #fyp #foryoupage #boyfriend', {'diggCount': 3 8200, 'shareCount': 2544, 'commentCount': 88, 'playCount': 514200})
('me and @harrymorrismuso spent hours on this don’t let it flop ps who’s coming out with us on Saturday? 💀😂 #virał #foryoupage #foryou #ukfashion', {'diggCount': 17900, 'shareCount': 486, 'commentCount': 77, 'playCount': 155800})
('this vid is so cringe but my bf Tarzan is something else 🥺❤️ #foryou #foryoupage #viral #boyfrien dcheck', {'diggCount': 40300, 'shareCount': 1088, 'commentCount': 396, 'playCount': 658000})
('IT HAPPENS EVERY TIME !!! #foryoupage #foryou #viral #makeitviral', {'diggCount': 17000, 'shareCount': 53, 'commentCount': 30, 'playCount': 168400})
('lmao I was so grunge last year and now I’m a colourful af #foryoupage #foryou #virał #ukfashion', {'diggCount': 198900, 'shareCount': 2453, 'commentCount': 643, 'playCount': 1400000})    
('LA LA LAND #losangeles #foryoupage #foryou #viral', {'diggCount': 2377, 'shareCount': 44, 'commentCount': 10, 'playCount': 42100})
('👁 challenge #eyechallenge #foryou #foryoupage', {'diggCount': 5080, 'shareCount': 34, 'commentCou nt': 17, 'playCount': 86100})
('luv this trend #fyp #fairy 🧚🏼\u200d♀️', {'diggCount': 612, 'shareCount': 11, 'commentCount': 18, 'playCount': 3476})
('tip of the day: carry a film camera with u at all times !! you’ll thank me later xxx #film #fyp', {'diggCount': 6834, 'shareCount': 77, 'commentCount': 70, 'playCount': 23100})
('I ❤️ u all so much !! thank you for supporting me #fyp #sophieseddon', {'diggCount': 3063, 'shareCount': 26, 'commentCount': 26, 'playCount': 19400})
('1 month later .... #fyp #flat #2021', {'diggCount': 2109, 'shareCount': 19, 'commentCount': 25, 'playCount': 15000})
('that moment when @harrymorrismuso looks better in a skirt than i do 🌝 #fyp #boyfriend #outfit', {'diggCount': 8199, 'shareCount': 78, 'commentCount': 63, 'playCount': 44600})
('help me find this man \U0001f978 #fyp #soulmate 💘', {'diggCount': 13900, 'shareCount': 36, 'commentCount': 155, 'playCount': 173700})
('i am making bracelets and i will be uploading them to my website in January ! 💘 #fyp', {'diggCount': 1258, 'shareCount': 7, 'commentCount': 34, 'playCount': 14000})
('#stitch with @fashion_nissi', {'diggCount': 7730, 'shareCount': 71, 'commentCount': 110, 'playCount': 61600})
('this ain’t all but 🤩 #shoes #alt #fyp #sophieseddon', {'diggCount': 3696, 'shareCount': 41, 'commentCount': 70, 'playCount': 27700})
('guilty 😭 #cottagecore #alt #fyp', {'diggCount': 5363, 'shareCount': 36, 'commentCount': 36, 'playCount': 37100})
('ACCENT CHECK ! duet me #duet #accentcheck #accentchallenge #fyp', {'diggCount': 17700, 'shareCount': 528, 'commentCount': 1438, 'playCount': 116400})
('anyone else ??? 🥴 #fyp', {'diggCount': 4929, 'shareCount': 74, 'commentCount': 52, 'playCount': 3 0100})
('#AD - Here is my @gucci X @flannels wish list if anyone is struggling to find me a gift this Christmas #FLANNELSGucciWishlist #FLANNELS 🎄#fyp', {'diggCount': 1221, 'shareCount': 52, 'commentCount': 49, 'playCount': 32200})
('I struggled for years until I tried this technique #eyeliner #fyp', {'diggCount': 4632, 'shareCount': 63, 'commentCount': 32, 'playCount': 34500})
('Part 2 - moving into my flat 🔆💕🌀', {'diggCount': 3830, 'shareCount': 15, 'commentCount': 32, 'playCount': 35500})
('someone asked so here u go #curlyhair #sophieseddon #fyp', {'diggCount': 6080, 'shareCount': 49, 'commentCount': 72, 'playCount': 88500})
('Part 1 - showing u guys around my new flat !! ⚡️⭐️', {'diggCount': 14000, 'shareCount': 58, 'commentCount': 67, 'playCount': 89000})
('sorry @harrymorrismuso #hairgoals #boyfriend #fyp', {'diggCount': 3962, 'shareCount': 33, 'commentCount': 89, 'playCount': 30000})
('thrifted outfits every day of the week #vintage #sophieseddon #outfits #fyp', {'diggCount': 8228, 'shareCount': 71, 'commentCount': 55, 'playCount': 44000})
('#ad I love matching my outfits with the new Pret cups! What brings you joy? #JoyWithPret 💕✨ AD', {'diggCount': 2631, 'shareCount': 61, 'commentCount': 33, 'playCount': 46300})
('Song by Marcelo De La Vega - told you 🍭🧚🏼\u200d♀️🖤 #fyp #sophieseddon #outfitideas #fashion', {'diggCount': 1753, 'shareCount': 38, 'commentCount': 49, 'playCount': 15200})
('when I left school those boys were in my DMS 😂🥴 #fyp #sophieseddon #glowup', {'diggCount': 12600 , 'shareCount': 106, 'commentCount': 97, 'playCount': 76600})
('LINK IN BIO - 2nd vintage drop !! #sophieseddon #vintage #fyp', {'diggCount': 2836, 'shareCount': 44, 'commentCount': 25, 'playCount': 35700})
('hey #halloween #fyp #mycostume 😈 👼🏻', {'diggCount': 3783, 'shareCount': 16, 'commentCount': 49, 'playCount': 23300})
('#duet with @watchkittyshrink  HAHAHA i proper hate my accent', {'diggCount': 8432, 'shareCount': 32, 'commentCount': 82, 'playCount': 94900})
('this took me a while lmao 🤡🤡🤡 #fyp #sophieseddon #viral', {'diggCount': 5352, 'shareCount': 101, 'commentCount': 125, 'playCount': 33300})
("AD - #GOLDIERED25 making me feel #gucci 💄 let's see your best #guccibeauty look 💋 @gucci", {'diggCount': 1496, 'shareCount': 23, 'commentCount': 30, 'playCount': 34900})
('working super hard to get my website finished ✔️ #sophieseddon #fyp', {'diggCount': 3858, 'shareCount': 44, 'commentCount': 25, 'playCount': 23100})
('I do it for the girls and gays that’s it x #sophieseddon #fyp #viral', {'diggCount': 7655, 'shareCount': 14, 'commentCount': 43, 'playCount': 44600})
('i love events but sometimes they’re scary af #sophieseddon #fyp #viral #ukfashion', {'diggCount': 13200, 'shareCount': 40, 'commentCount': 80, 'playCount': 154300})
('#AD grooving to the jellyfish jam in my new #spongebob #pride t-shirt,\xa0available from George at Asda link in bio ❤️ @nickelodeonuk #wearegeorge', {'diggCount': 1324, 'shareCount': 22, 
'commentCount': 15, 'playCount': 17500})
('remove toxic ppl from ur life, you’ll thank me later #sophieseddon #fyp #viral', {'diggCount': 73700, 'shareCount': 144, 'commentCount': 160, 'playCount': 378200})
('⭐️✨ #stargazingchallenge', {'diggCount': 5163, 'shareCount': 27, 'commentCount': 58, 'playCount': 42300})
('we need to protect long haired men 🥰 @harrymorrismuso #boyfriend #sophieseddon #hairgoals', {'dig gCount': 33300, 'shareCount': 297, 'commentCount': 203, 'playCount': 211900})
('luv this song by @katyforkings ✌🏻#fyp #sophieseddon #viral #haircut', {'diggCount': 4233, 'shareCount': 7, 'commentCount': 40, 'playCount': 51500})
('it took me 15 mins dragging my mirror outside and 5 mins later it went cloudy omfg #sophieseddon #mirror #pinterest', {'diggCount': 8905, 'shareCount': 36, 'commentCount': 45, 'playCount': 62200})
('I saw a couple of ppl do this and i wanted to try it out ! #fakefreckles #sophieseddon #viral', {'diggCount': 3598, 'shareCount': 26, 'commentCount': 17, 'playCount': 44100})
('I can’t be the only one #viral #sophieseddon 🍓🐛🐜', {'diggCount': 18200, 'shareCount': 54, 'commentCount': 136, 'playCount': 156000})
('give me a new name #fyp #sophieseddon #viral 🍓', {'diggCount': 4663, 'shareCount': 21, 'commentCount': 1726, 'playCount': 39500})
('What did you do today for your future self ? Song by @bear  🐻 AD #viral #mountains #mentalhealthmatters', {'diggCount': 2762, 'shareCount': 10, 'commentCount': 30, 'playCount': 36500})  
('today #fyp #vintage #sophieseddon', {'diggCount': 4916, 'shareCount': 11, 'commentCount': 38, 'playCount': 46600})
('#duet with @livbehri #scoobydoo #scoobydoocosplay #fyp ❤️', {'diggCount': 17300, 'shareCount': 51, 'commentCount': 43, 'playCount': 138400})
('Reply to @sour_lemon_pie I hope this helps u find some cool clothes #sophieseddon #pinterest #ukfashion #vintage', {'diggCount': 3407, 'shareCount': 11, 'commentCount': 37, 'playCount': 40300})
('I ❤️ stranger things ! #strangerthings #80s #viral', {'diggCount': 8949, 'shareCount': 103, 'commentCount': 90, 'playCount': 69900})
('not true #fyp #curlyhair #viral', {'diggCount': 5273, 'shareCount': 6, 'commentCount': 41, 'playCount': 86600})
('millions of ppl have seen these photos on Pinterest but have no idea who it is , well it’s ME #fyp #pinterest #sophieseddon', {'diggCount': 24200, 'shareCount': 106, 'commentCount': 134, 
'playCount': 144100})
('3 thrifted outfits from @depop ! which one is ur fave? 1,2 or 3 #sophieseddon #outfitideas #fyp #ukfashion', {'diggCount': 5418, 'shareCount': 33, 'commentCount': 40, 'playCount': 49900})('depop haul , should i do more of these ? #depophaul #vintage #secondhand', {'diggCount': 8266, 'shareCount': 19, 'commentCount': 56, 'playCount': 64500})
('❤️🌞 #fyp #viral #positivity', {'diggCount': 13200, 'shareCount': 28, 'commentCount': 120, 'playCount': 79800})
('happy pride month everyone ! #pride #beyourselfchallenge #ally ❤️🧡💛💚💙💜', {'diggCount': 8558, 'shareCount': 34, 'commentCount': 36, 'playCount': 82700})
('u know when ur obsessed with scrunchies when .... #viral #sophieseddon #ukfashion', {'diggCount': 7844, 'shareCount': 84, 'commentCount': 42, 'playCount': 67100})
('hahahah I’ll cry at anything #foryoupage #viral #sophieseddon', {'diggCount': 4932, 'shareCount': 43, 'commentCount': 30, 'playCount': 54400})
('#tiktoktraditions  hA HA hA HA hA hA HAaaa #sophieseddon #fyp', {'diggCount': 4078, 'shareCount': 13, 'commentCount': 38, 'playCount': 56000})
('😭😭 #fyp #viral', {'diggCount': 23700, 'shareCount': 285, 'commentCount': 69, 'playCount': 222300})
('it’s the truth #UKfashion #sophieseddon #fyp', {'diggCount': 41000, 'shareCount': 253, 'commentCount': 61, 'playCount': 214100})
('why am i like this #viral #UKfashion #sophieseddon', {'diggCount': 5050, 'shareCount': 19, 'commentCount': 20, 'playCount': 42300})
('this is a joke 😭 #viral', {'diggCount': 14600, 'shareCount': 949, 'commentCount': 70, 'playCount': 188400})
('exposing myself big time 💀💀 thank GOD for puberty #fyp #viral', {'diggCount': 4571, 'shareCount': 17, 'commentCount': 39, 'playCount': 44600})
('i have a love/hate relationship with these sunglasses #fyp #viral', {'diggCount': 3787, 'shareCount': 6, 'commentCount': 13, 'playCount': 43600})
('I swear every British girl owned one #fyp #viral #ukfashion', {'diggCount': 16300, 'shareCount': 47, 'commentCount': 120, 'playCount': 382600})
('here are the answers to ur questions #fyp #sophieseddon #ukfashion', {'diggCount': 26600, 'shareCount': 411, 'commentCount': 56, 'playCount': 324500})
('story of my LIFE #fyp #sophieseddon', {'diggCount': 8714, 'shareCount': 176, 'commentCount': 81, 'playCount': 66100})
('long legs, short body = me 🌞 boat day with @harrymorrismuso #fyp #summer', {'diggCount': 4870, 'shareCount': 9, 'commentCount': 24, 'playCount': 50600})
('@harrymorrismuso  #relationship #couple #sophieseddon #fyp ❤️💓', {'diggCount': 4884, 'shareCount': 35, 'commentCount': 47, 'playCount': 109200})
('yikes thank god for rapidbrow #sophieseddon #fyp #pinterest', {'diggCount': 6143, 'shareCount': 1672, 'commentCount': 85, 'playCount': 97100})
('I secretly wanted the 80’s anyways.... #fyp #sophieseddon #ukfashion #aesthetic', {'diggCount': 247000, 'shareCount': 837, 'commentCount': 721, 'playCount': 1400000})
('i finally persuaded @harrymorrismuso to do this with me #fyp #sophieseddon #ukfashion ✨', {'diggCount': 56200, 'shareCount': 871, 'commentCount': 336, 'playCount': 736100})
('me every night #fyp #sophieseddon', {'diggCount': 6561, 'shareCount': 80, 'commentCount': 19, 'playCount': 64400})
('💀 #sophieseddon #UKfashion #pinterest', {'diggCount': 87700, 'shareCount': 160, 'commentCount': 438, 'playCount': 341200})
('this is all ur fault @tiktok_uk 💀😂 #sophieseddon #ukfashion #verified #fyp #speakyourmind', {'diggCount': 5719, 'shareCount': 3, 'commentCount': 56, 'playCount': 59500})
('when ur outfit goes viral #ukfashion #pinterest #sophieseddon', {'diggCount': 14900, 'shareCount': 37, 'commentCount': 63, 'playCount': 74700})
('i haven’t touched my brows since lockdown #fyp #lockdownlewks #secret #beautyhacks', {'diggCount': 16600, 'shareCount': 42, 'commentCount': 131, 'playCount': 301600})
('the last one is my fave #cartooncharacter 💀 #fyp', {'diggCount': 5731, 'shareCount': 26, 'commentCount': 38, 'playCount': 48200})
('I love my girlfriend @bass_ic ✨💓 #foryou #foryoupage #couplegoals', {'diggCount': 10500, 'shareCount': 228, 'commentCount': 98, 'playCount': 166800})
('im currently obsessed with this absolute BOP so i recreated moments from the video @yungblud  #weird #weareweird #ad ❤️💓', {'diggCount': 2582, 'shareCount': 5, 'commentCount': 31, 'playC
ount': 32000})
('I wanted to take my clothes off but apparently tiktok has guidelines against that 😂 #ifyouretooshy @the1975 #ad', {'diggCount': 4473, 'shareCount': 25, 'commentCount': 18, 'playCount': 61600})
('my favourite job so far ! #fyp #aesthetic #boyfriendcheck #goals', {'diggCount': 7559, 'shareCount': 49, 'commentCount': 43, 'playCount': 56600})
('sorry it took so long 🔆🍄 #Polaroid #vintage #fyp #aesthetic', {'diggCount': 2864, 'shareCount': 94, 'commentCount': 10, 'playCount': 37600})
('i cringed watching this lol #glowup #houseoftiktok #fyp #sophieseddon', {'diggCount': 4754, 'shareCount': 30, 'commentCount': 73, 'playCount': 43800})
('the daily brush @bass_ic #hairgoals #hairgrowth #aesthetic', {'diggCount': 23300, 'shareCount': 144, 'commentCount': 187, 'playCount': 220500})
('another day in paradise 🐌🌷#cottagecore #cottage #aesthetic #fyp', {'diggCount': 241300, 'shareCount': 5902, 'commentCount': 1757, 'playCount': 1000000})
('another day in the garden with my baby @bass_ic #cottagecore #cottagecorecheck #fyp #houseoftiktok', {'diggCount': 73200, 'shareCount': 825, 'commentCount': 170, 'playCount': 310000})    
('@bass_ic #fyp #boredvibes #houseoftiktok #foryoupage', {'diggCount': 52600, 'shareCount': 1482, 'commentCount': 276, 'playCount': 251300})
('!! 🌜✨  #houseoftiktok #foryoupage #viral #ukfashion', {'diggCount': 5783, 'shareCount': 69, 'commentCount': 26, 'playCount': 47700})
('space buns 🪐👽 ! #teachme #fyp #viral', {'diggCount': 4041, 'shareCount': 75, 'commentCount': 18,  'playCount': 49000})
('when ur 2 shy to use the underground because u know the coronavirus will b there #shychallenge #foryoupage #viral #shy', {'diggCount': 8914, 'shareCount': 79, 'commentCount': 44, 'playCount': 100200})
('2019, the year I started living ! 🔆 #fyp #viral #happiness #london', {'diggCount': 39300, 'shareCount': 368, 'commentCount': 150, 'playCount': 229500})
('I didn’t do a poo ! #coronavirus #papertowelchallenge #viral', {'diggCount': 9882, 'shareCount': 309, 'commentCount': 176, 'playCount': 104900})
('me styling @catfootweareu #ad #fyp #ukfashion', {'diggCount': 1966, 'shareCount': 25, 'commentCount': 13, 'playCount': 27200})
('ceo of ‘“it’s vintage” #fyp #london #ukfashion #vintagw #foryoupage', {'diggCount': 12500, 'shareCount': 160, 'commentCount': 53, 'playCount': 163400})
('Brick lane, London aka the best place for vintage fashion 🌈 #fyp #foryoupage #london #ukfashion', {'diggCount': 155300, 'shareCount': 14100, 'commentCount': 1279, 'playCount': 887300})  
('I really went from “no wait stop” to posing like that ????  #viral #fyp #foryoupge #london', {'diggCount': 30000, 'shareCount': 374, 'commentCount': 99, 'playCount': 202900})
('my boyfriend is the best 🥺❤️@harrymorrismuso #viral #fyp #foryoupage #boyfriend', {'diggCount': 3 8200, 'shareCount': 2544, 'commentCount': 88, 'playCount': 514200})
('me and @harrymorrismuso spent hours on this don’t let it flop ps who’s coming out with us on Saturday? 💀😂 #virał #foryoupage #foryou #ukfashion', {'diggCount': 17900, 'shareCount': 486, 'commentCount': 77, 'playCount': 155800})
('this vid is so cringe but my bf Tarzan is something else 🥺❤️ #foryou #foryoupage #viral #boyfrien dcheck', {'diggCount': 40300, 'shareCount': 1088, 'commentCount': 396, 'playCount': 658000})
('IT HAPPENS EVERY TIME !!! #foryoupage #foryou #viral #makeitviral', {'diggCount': 17000, 'shareCount': 53, 'commentCount': 30, 'playCount': 168400})
('lmao I was so grunge last year and now I’m a colourful af #foryoupage #foryou #virał #ukfashion', {'diggCount': 198900, 'shareCount': 2453, 'commentCount': 643, 'playCount': 1400000})
('LA LA LAND #losangeles #foryoupage #foryou #viral', {'diggCount': 2377, 'shareCount': 44, 'commentCount': 10, 'playCount': 42100})
('👁 challenge #eyechallenge #foryou #foryoupage', {'diggCount': 5080, 'shareCount': 34, 'commentCou nt': 17, 'playCount': 86100})
'''

