import csv
import datetime
import time
import pandas as pd
from bs4 import BeautifulSoup as Soup
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
from random import randint

# 你的資訊
url = "https://www.facebook.com/"
email = ""
password = ""

# 防止跳出通知
chrome_options = Options()
prefs = {
    "profile.default_content_setting_values.notifications": 2
}
chrome_options.add_experimental_option("prefs", prefs)

# 使用ChromeDriverManager自動下載chromedriver
driver = webdriver.Chrome(options=chrome_options)

# 最大化視窗
driver.maximize_window()
# 進入Facebook登入畫面
driver.get(url)

# 填入帳號密碼，並送出
elem = driver.find_element(By.ID, "email")
elem.send_keys(email)

elem = driver.find_element(By.ID, ("pass"))
elem.send_keys(password)

elem.send_keys(Keys.RETURN)
time.sleep(1)

# 進入專頁
driver.get("https://www.facebook.com/groups/cyberkage")

time.sleep(1)

# 暫存資料的容器
iconUrlList = [str]
nameList = [str]
articleList = [str]
picUrlList = [str]
likeCountList = [str]
commentCountList = [str]

counter = 0
while counter < 1:

    # 往下滑3次，讓Facebook載入文章內容
    for x in range(100):
        # 模擬滑動頁面行為
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        time.sleep(5)

    # 擷取網頁內容
    pageContent = Soup(driver.page_source, "html.parser")

    '''
    ------------------------------------------------------------------------------------------------------------------------
    '''

    postTag = "x1yztbdb x1n2onr6 xh8yej3 x1ja2u2z"
    posts = pageContent.find_all("div", class_=postTag)
    for post in posts:

        '''處理頭像照片'''
        try:
            iconBlock = post.find('image')
            iconUrl = str()
            iconUrl = iconUrl + iconBlock['xlink:href']
            iconUrlList.append(iconUrl)

        except():
            iconUrlList.append("")

        '''處理名字'''
        try:
            nameTag = 'strong'
            nameElement = post.select(nameTag)
            name = nameElement[0].text
            nameList.append(name)

        except():
            nameList.append("")

        '''處理文章內容'''
        try:
            # 文章有內容或無內容的case
            articleTag1 = "xdj266r x11i5rnm xat24cr x1mh8g0r x1vvkbs x126k92a"
            articleTag2 = "x11i5rnm xat24cr x1mh8g0r x1vvkbs xtlvy1s x126k92a"
            articleElements = post.find_all("div", {"class": {articleTag1, articleTag2}})
            articles = str()

            # Usual Case / 特殊case:
            if len(articleElements) != 0:
                for articleElement in articleElements:

                    articleLines = articleElement.find_all("div", style="text-align: start;")

                    for articleLine in articleLines:
                        articles += articleLine.text
                        articles += "\t"
            else:
                articleSpecialTag = "x1iorvi4 x1pi30zi x1l90r2v x1swvt13"
                articleElements = post.find_all("div", {"class": {articleSpecialTag}})
                for index in range(len(articleElements)):
                    articles += articleElements[index].text
                    articles += "\t"

            # 單句文配單色背景case
            contentLine = str()
            lineElements = post.find_all("div", class_="x1cy8zhl x78zum5 x1nhvcw1 x1n2onr6 xh8yej3")

            for lineSet in lineElements:
                lines = lineSet.find_all("div", class_="xdj266r x11i5rnm xat24cr x1mh8g0r x1vvkbs")

                contentLine = contentLine + lines[0].text
                contentLine = contentLine + "\t"

            if len(articles) != 0 or len(contentLine) != 0:
                if len(articles) != 0:
                    articles = articles
                    articleList.append(articles)
                else:
                    contentLine = contentLine
                    articleList.append(contentLine)
            else:
                articleList.append("")

        except():
            articleList.append("")

        '''處理內文照片'''
        try:
            # 無照片或單張照片的case
            photoTage = 'x1i10hfl x1qjc9v5 xjbqb8w xjqpnuy xa49m3k xqeqjp1 x2hbi6w x13fuv20 xu3j5b3 x1q0q8m5 x26u7qi x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xdl72j9 x2lah0s xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r x2lwn1j xeuugli xexx8yu x4uap5 x18d9i69 xkhd6sd x1n2onr6 x16tdsg8 x1hl2dhg xggy1nq x1ja2u2z x1t137rt x1o1ewxj x3x9cwd x1e5q0jg x13rtm0m x1q0g3np x87ps6o x1lku1pv x1a2a7pz x1lliihq x1pdlv7q'
            photoElements = post.find_all('a', class_=photoTage)
            if len(photoElements) != 0:
                index = 0
                photoUrl = photoElements[index].get('href')
                photoUrl = photoUrl
                picUrlList.append(photoUrl)


            # 多張照片的case
            picSetTag = "x1ey2m1c xds687c x5yr21d x10l6tqk x17qophe x13vifvy xh8yej3"
            picSetElements = post.find_all("img", class_=picSetTag)
            picUrls = str()
            if len(picSetElements) != 0:
                for pic in picSetElements:
                    picUrls = picUrls + (pic.get('src') + '\t')

                picUrls = picUrls
                picUrlList.append(picUrls)

            if len(photoElements) == 0 and len(picSetElements) == 0:
                picUrlList.append("")

        except():
            picUrlList.append("")

        '''處理按讚數'''
        try:
            likeTag = "xt0b8zv x1jx94hy xrbpyxo xl423tq"
            like = post.find("span", class_=likeTag)
            if like:
                likeCount = like.find("span", class_="x1e558r4").text
                likeCountList.append(likeCount)
            else:
                likeCountList.append("")

        except():
            likeCountList.append("")

        '''處理留言數'''
        try:
            commentTag = 'x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x3x7a5m x6prxxf xvq8zen xo1l8bm xi81zsa'
            commentBlock = post.find("span", class_=commentTag)
            if commentBlock:

                # commentCountMsg = commentBlock.find("span", class_="")
                commentCount = commentBlock.text
                commentCountList.append(commentCount)
            else:
                commentCountList.append("")

        except():
            commentCountList.append("")
    '''
    ------------------------------------------------------------------------------------------------------------------------
    '''
    # 存檔
    counter += 1
    if counter % 2 == 1:
        df = pd.DataFrame()
        columns = ['IconLink', 'Name', 'Article', 'PicLinks', 'LikeCounts', 'CommentCounts']
        cols = [iconUrlList, nameList, articleList, picUrlList, likeCountList, commentCountList]
        for i, j in zip(columns, cols):
            df[i] = j
        versionNum = counter
        filePath = f'C:\\Users\\heyhe\\Desktop\\FBCrawler\\20230617\\{datetime.date.today()}_v{versionNum}.csv'
        df.to_csv(filePath, quoting=csv.QUOTE_NONNUMERIC, index=False)

