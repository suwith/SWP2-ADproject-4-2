import sys
from PyQt5.QtWidgets import (QWidget, QPushButton,
    QGridLayout, QApplication, QLabel, QTextBrowser, QSizePolicy)
from bs4 import BeautifulSoup
from urllib.request import urlopen
import requests



class Button(QToolButton):

    def __init__(self, img, callback):
        super().__init__()
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.setStyleSheet(img)
        self.clicked.connect(callback)
        self.setMaximumSize(100, 100)

class Trender(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()


    def initUI(self):

        self.video = Button('border-image:url(netflix.PNG);', self.videorank)
        self.music = Button('border-image:url(사본 -001.PNG);', self.musicrank)
        self.search = Button('border-image:url(google.PNG);', self.searchrank)
        self.headline = Button('border-image:url(사본 -news.PNG);', self.Headline)

        self.resultText = QTextBrowser()
        self.resultText.setReadOnly(True)
        self.resultText.setOpenExternalLinks(True)
        self.resultText.setMaximumSize(650, 700)
        self.resultText.setStyleSheet('background-color: lightgrey')

        self.trendIs = QLabel("What is Today Trend?", self)
        self.trendIs.setStyleSheet('font-size: 30pt;')

        gridBox = QGridLayout()

        gridBox.addWidget(self.trendIs, 0, 0, 1, 2)
        gridBox.addWidget(self.video, 1, 0, 1, 1)
        gridBox.addWidget(self.music, 2, 0, 1, 1)
        gridBox.addWidget(self.search, 3, 0, 1, 1)
        gridBox.addWidget(self.headline, 4, 0, 1, 1)
        gridBox.addWidget(self.resultText, 1, 1, 5, 1)

        self.setLayout(gridBox)
        self.setGeometry(300, 150, 850, 650)
        self.setWindowTitle('트렌드 분석기')
        self.show()


    def videorank(self):
        self.resultText.clear()
        self.resultText.setStyleSheet('font-size: 18pt')
        self.trendIs.setText("Today Netflix Trend")
        n = 1
        with urlopen('https://flixpatrol.com/top10/netflix/south-korea/') as response:
            soup = BeautifulSoup(response, 'html.parser')
            for anchor in soup.find('tbody', {'class': 'tabular-nums'}).find_all('tr'):
                v = anchor.find("a")["href"]
                VRank = str(n) + ". " + str(anchor.find('a').get_text()) + '\t <a href=\"https://flixpatrol.com' + str(v) + '\">'+ '■' + "</a>"
                n += 1
                self.resultText.append(VRank)

    def musicrank(self):
        self.trendIs.setText("Today Music Trend")
        header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko'}
        req = requests.get('https://www.melon.com/chart/week/index.htm', headers=header)
        html = req.text
        parse = BeautifulSoup(html, 'html.parser')


        self.resultText.clear()
        title = []
        singer = []

        titles = parse.find_all("div", {"class": "ellipsis rank01"})
        singers = parse.find_all("div", {"class": "ellipsis rank02"})

        for t in titles:
            title.append(t.find('a').text)

        for s in singers:
            singer.append(s.find('span', {"class": "checkEllipsis"}).text)

        for i in range(20):
            m = title[i]
            m_ = m.replace(" ", "+")
            MRank = str(i + 1) + ". " + str(title[i]) + " - " + str(singer[i]) +\
                '\t <a href=\"https://www.melon.com/search/total/index.htm?q=' + str(m_) + '\">'+ '■' + "</a>"
            self.resultText.append(MRank)
        self.resultText.setStyleSheet('font-size: 10pt')

    def searchrank(self):
        self.resultText.clear()
        self.resultText.setStyleSheet('font-size: 14pt')
        self.trendIs.setText("Today Popular Search")
        n = 1
        with urlopen("https://trends.google.com/trends/trendingsearches/daily/rss?geo=KR") as response:
            soup = BeautifulSoup(response, 'html.parser')
            for anchor in soup.find('channel').find_all('item'):
                s = str(anchor.find('title').get_text())
                s_ = s.replace(" ", "+")
                SRank = str(n) + ". " + str(anchor.find('title').get_text()) + '\t <a href=\"https://www.google.com/search?q=' + str(s_) + '\">'+ '■'  + "</a>"
                self.resultText.append(SRank)
                n += 1

    def Headline(self):
        self.resultText.clear()
        self.resultText.setStyleSheet('font-size: 10pt')
        self.trendIs.setText("Today Headline News")
        n = 1
        with urlopen('https://news.naver.com') as response:
            self.resultText.append('<헤드라인 뉴스>')
            soup = BeautifulSoup(response, 'html.parser')
            for anchor in soup.find('ul', {'class': 'hdline_article_list'}).find_all('li'):
                Link = anchor.find("a")["href"]
                h = anchor.find('a').get_text()
                H = h.split()
                H_ = str(" ".join(H))
                News = str(n) + ". " + str(H_) + '\t <a href=\"https://news.naver.com' + str(Link) + '\">'+ '■'  + "</a>"
                self.resultText.append(News)
                n += 1

            self.resultText.append('\n <정치>')
            n = 1
            for anchor in soup.find('div', {'class': 'main_component droppable', 'id': 'section_politics'}).find_all('li'):
                Link = anchor.find("a")["href"]
                h = anchor.find('a').get_text()
                H = h.split()
                H_ = str(" ".join(H))
                News = str(n) + ". " + str(H_) + '\t <a href=\"' + str(Link) + '\">'+ '■'  + "</a>"
                self.resultText.append(News)
                n += 1

            self.resultText.append('\n <경제>')
            n = 1
            for anchor in soup.find('div', {'class': 'main_component droppable', 'id': 'section_economy'}).find_all('li'):
                Link = anchor.find("a")["href"]
                h = anchor.find('a').get_text()
                H = h.split()
                H_ = str(" ".join(H))
                News = str(n) + ". " + str(H_) + '\t <a href=\"' + str(Link) + '\">' + '■' + "</a>"
                self.resultText.append(News)
                n += 1

            self.resultText.append('\n <사회>')
            n = 1
            for anchor in soup.find('div', {'class': 'main_component droppable', 'id': 'section_society'}).find_all('li'):
                Link = anchor.find("a")["href"]
                h = anchor.find('a').get_text()
                H = h.split()
                H_ = str(" ".join(H))
                News = str(n) + ". " + str(H_) + '\t <a href=\"' + str(Link) + '\">' + '■' + "</a>"
                self.resultText.append(News)
                n += 1

            self.resultText.append('\n <생활/문화>')
            n = 1
            for anchor in soup.find('div', {'class': 'main_component droppable', 'id': 'section_life'}).find_all('li'):
                Link = anchor.find("a")["href"]
                h = anchor.find('a').get_text()
                H = h.split()
                H_ = str(" ".join(H))
                News = str(n) + ". " + str(H_) + '\t <a href=\"' + str(Link) + '\">' + '■' + "</a>"
                self.resultText.append(News)
                n += 1

            self.resultText.append('\n <세계>')
            n = 1
            for anchor in soup.find('div', {'class': 'main_component droppable', 'id': 'section_world'}).find_all('li'):
                Link = anchor.find("a")["href"]
                h = anchor.find('a').get_text()
                H = h.split()
                H_ = str(" ".join(H))
                News = str(n) + ". " + str(H_) + '\t <a href=\"' + str(Link) + '\">' + '■' + "</a>"
                self.resultText.append(News)
                n += 1

            self.resultText.append('\n <IT/과학>')
            n = 1
            for anchor in soup.find('div', {'class': 'main_component droppable', 'id': 'section_it'}).find_all('li'):
                Link = anchor.find("a")["href"]
                h = anchor.find('a').get_text()
                H = h.split()
                H_ = str(" ".join(H))
                News = str(n) + ". " + str(H_) + '\t <a href=\"' + str(Link) + '\">' + '■' + "</a>"
                self.resultText.append(News)
                n += 1


if __name__ == '__main__':
    app = QApplication(sys.argv)
    trend = Trender()
    sys.exit(app.exec_())
