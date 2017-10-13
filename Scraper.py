'''
ITU Python Programming Group 6 Scraper Sub-group

Author: Ming Li
        Xuguang Liu
        Yandong Xiao

Version: 2.4

Please substitute the path in line 79, 88 ,98
'''
import re
from urllib.request import *

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

main_url = 'http://www.google.com'


class Scraper:
    def __init__(self, stockName):
        self.url = main_url + '/finance?q=' + stockName + '&ei='


# Inheritance
class Crawler(Scraper):
    # Override the constructor
    def __init__(self, stockName):
        super(Crawler, self).__init__(stockName)
        html = urlopen(self.url)
        bsObj = BeautifulSoup(html,'html.parser')
        self.soup = bsObj

        if bsObj.find('div', id='image_chart') == None:
            self.invalid = True

        else:
            self.invalid = False
            self.financials = None
            self.chart = None
            self.price = None
            self.price_change = None
            self.price_change_rate = None
            self.information = None

            # news = bsObj.find('ul', {'id': 'navmenu'}).find('a', text='News')
            # news = main_url + news.attrs['href']

            financials = bsObj.find('ul', {'id': 'navmenu'}).find('a', text='Financials')
            if financials != None:
                financials = main_url + financials.attrs['href']

            chart = bsObj.find('div', id='image_chart').find('img')
            chart = main_url + chart.attrs['src'] + '.png'
            # chart_path = '/home/ming/Project/Python/chart/' + stockName + '.png'
            # urlretrieve(chart, chart_path)

            price_data = bsObj.findAll('span', id=re.compile('^(ref_)'))
            price = price_data[0].get_text()
            price_change = price_data[1].get_text()
            price_change_rate = price_data[2].get_text()

            all_information = bsObj.findAll('td', class_='val')
            information = []
            for i in all_information:
                information.append(i.get_text())

            self.financials = financials
            self.chart = chart
            self.price = price
            self.price_change = price_change
            self.price_change_rate = price_change_rate
            self.information = information

    def get_name(self):
        # The path of phantomjs is required
        browser = webdriver.PhantomJS('phantomjs')
        browser.get(self.url)
        bsObj = BeautifulSoup(browser.page_source,'html.parser')
        name = bsObj.find('div', class_='appbar-snippet-primary').span.get_text()
        nasdaq_name = bsObj.find('div', class_='appbar-snippet-secondary').span.get_text()
        return name, nasdaq_name

    def get_quarterly_chart(self):
        if self.financials != None:
            browser = webdriver.PhantomJS('phantomjs')
            browser.get(self.financials)
            bsObj = BeautifulSoup(browser.page_source,'html.parser')
            chart1 = bsObj.find('div', id="viz_chart4").find('img').attrs['src'].replace('//', '')
            chart2 = bsObj.find('div', id="viz_chart5").find('img').attrs['src'].replace('//', '')
            return chart1, chart2
        else:
            return None

    def get_logo(self, stockName):
        browser = webdriver.PhantomJS('phantomjs')
        browser.get('https://www.google.com')
        elem = browser.find_element_by_class_name('lst')
        key = stockName + ' wiki'
        elem.send_keys(key)
        elem.send_keys(Keys.RETURN)
        bsObj = BeautifulSoup(browser.page_source,'html.parser')
        wiki_url = bsObj.find('div', id='search').cite.get_text()
        html = urlopen(wiki_url)
        bsObj = BeautifulSoup(html,'html.parser')
        if(bsObj.find('td', style='text-align:center')==None):
            return None
        logo = bsObj.find('td', style='text-align:center').img
        if logo != None:
            logo = logo.attrs['src'].replace(r'//', '')

        return logo

    def get_news(self):
        news = str(self.soup.find_all('script'))

        # Define regular expression patterns
        pattern_titles = re.compile(r'\[\{t:".*?"')
        pattern_links = re.compile(r'lead_story_url:".*?"')

        # Return the results(list) that match the pattern we defined
        result_titles = re.findall(pattern_titles, news)
        result_links = re.findall(pattern_links, news)

        # These two lists are the final results that can be used by tkinter team.     
        titles = []
        links = []

        # Check if we get the results
        if result_titles:
            for title in result_titles:
                # Get the news title substring
                title = title[5:-1]
                # Put the title substrings to a new list
                titles.append(title)

        if result_links:
            for link in result_links:
                # Get the news link substring
                link = link[16:-1]
                # Put the link substrings to a new list
                links.append(link)

        return titles, links

    def get_related_companies(self):
        headers = ('User-Agent',
                   'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11')
        opener = build_opener()
        opener.addheaders = [headers]
        data = opener.open(self.url).read()
        dataString = data.decode('utf-8')
        soup = BeautifulSoup(data, "html.parser")

        # Description
        getContent = soup.find('div', id='summary').find('div', class_='companySummary')
        summaryStr = getContent.get_text()
        summaryStr = summaryStr[:-22]

        # Related companies
        gf = re.compile(r'related:\{.*?\}\]', re.I | re.M)
        gfinance = gf.findall(dataString)
        gf = gfinance[0]
        gf = gf[48:]
        gs = re.compile(r'values:\[(.*?)\]', re.I | re.M)
        gfs = gs.findall(gf)
        relatedCom = []

        for reCom in gfs:
            oriCom = reCom.split(',', 8)
            rigCom = []
            rigCom.append(oriCom[0])
            rigCom.append(oriCom[1])
            rigCom.append(oriCom[2])
            rigCom.append(oriCom[3])
            rigCom.append(oriCom[5])
            rigCom.append(oriCom[7])
            relatedCom.append(rigCom)

        return summaryStr, relatedCom
