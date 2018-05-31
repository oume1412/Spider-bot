# SoftwareII
# Project Spider Bot
# Developer
# Natakorn Thongdee 5901012620037
# Saranporn Thitakasikorn 5901012620169
# Last Edit: 5/28/2018

from urllib.request import urlopen
import re
from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from multiprocessing.dummy import Pool
from urllib.error import URLError, HTTPError
import os
import dill
from glob import glob
from datetime import datetime
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from threading import Thread

class UiMainWindow(QtWidgets.QMainWindow):
    '''This class used to construct GUI.'''
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.setupUi()
        self.show()
        self.item_limit = 1000
        self.rank = None

    # Set up GUI
    def setupUi(self):
        self.setObjectName("self")
        self.setWindowTitle("Spider Bot")

        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")

        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")

        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")

        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 979, 628))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")

        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.scrollAreaWidgetContents)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")

        self.bot = QtWidgets.QWidget()
        self.bot.setObjectName("bot")

        self.gridLayout_2 = QtWidgets.QGridLayout(self.bot)
        self.gridLayout_2.setObjectName("gridLayout_2")

        self.start = QtWidgets.QPushButton(self.bot)
        self.start.setObjectName("start")
        self.start.setText("Start")
        self.start.clicked.connect(spider.start_crawl)
        self.gridLayout_2.addWidget(self.start, 1, 0, 1, 1)

        self.stop = QtWidgets.QPushButton(self.bot)
        self.stop.setObjectName("stop")
        self.stop.setText("Stop")
        self.stop.clicked.connect(spider.stop_crawl)
        self.gridLayout_2.addWidget(self.stop, 1, 1, 1, 1)

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)

        self.lineEdit = QtWidgets.QLineEdit(self.bot)
        self.lineEdit.setSizePolicy(sizePolicy)
        self.lineEdit.setObjectName("lineEdit")
        # self.lineEdit.cursorPositionChanged.connect()
        self.gridLayout_2.addWidget(self.lineEdit, 0, 0, 1, 2)
        sizePolicy.setHeightForWidth(self.lineEdit.sizePolicy().hasHeightForWidth())

        self.bot_list_widget = QtWidgets.QListWidget(self.bot)
        self.bot_list_widget.setObjectName("bot_list_widget")
        self.gridLayout_2.addWidget(self.bot_list_widget, 3, 0, 1, 2)

        self.search = QtWidgets.QWidget()
        self.search.setObjectName("search")

        self.tab = QtWidgets.QTabWidget(self.scrollAreaWidgetContents)
        self.tab.setObjectName("tab")
        self.tab.setTabText(self.tab.indexOf(self.bot), "Bot")
        self.tab.setTabText(self.tab.indexOf(self.search), "Seach")
        self.tab.addTab(self.bot, "Bot")
        self.tab.addTab(self.search, "Search")

        self.gridLayout = QtWidgets.QGridLayout(self.search)
        self.gridLayout.setObjectName("gridLayout")

        self.search_button = QtWidgets.QToolButton(self.search)
        self.search_button.setObjectName("search_button")
        self.search_button.setText("Search")
        self.search_button.clicked.connect(self.list_web)
        self.gridLayout.addWidget(self.search_button, 0, 1, 1, 1)

        self.clear_button = QtWidgets.QToolButton(self.bot)
        self.clear_button.setObjectName("clearbutton")
        self.clear_button.setText("Clear")
        self.clear_button.clicked.connect(self.clear_list_widget)
        self.gridLayout_2.addWidget(self.clear_button, 4, 0, 1, 2)

        self.search_line = QtWidgets.QLineEdit(self.search)
        self.search_line.textChanged.connect(self.list_web)
        self.search_line.setObjectName("search_edit")
        self.gridLayout.addWidget(self.search_line, 0, 0, 1, 1)

        self.search_list_widget = QtWidgets.QListWidget(self.search)
        self.search_list_widget.setObjectName("search_list_widget")
        self.search_list_widget.itemDoubleClicked.connect(self.open_link)
        self.gridLayout.addWidget(self.search_list_widget, 1, 0, 1, 2)

        self.horizontalLayout_2.addWidget(self.tab)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout_2.addWidget(self.scrollArea)
        self.setCentralWidget(self.centralwidget)

        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1003, 26))
        self.menubar.setObjectName("menubar")
        self.setMenuBar(self.menubar)

        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuFile.setTitle("File")

        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)

        self.actionOpen = QtWidgets.QAction(self)
        self.actionOpen.setObjectName("actionOpen")
        self.actionOpen.setText("Open")
        self.actionOpen.setShortcut("Ctrl+O")
        self.actionOpen.triggered.connect(self.openFileDialog)
        self.menuFile.addAction(self.actionOpen)

        self.menubar.addAction(self.menuFile.menuAction())
        self.tab.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(self)

    # Clear all Qlistwidget items
    def clear_list_widget(self):
        self.bot_list_widget.clear()

    # Delete excess of Qlistwidget items corresponding to limit of Qlistwidget items
    def delete_list_widget(self, widget):
        while widget.count()>= self.item_limit:
            widget.takeItem(0)

    # Open file
    def openFileDialog(self):
        '''Get loaded file name.'''
        directory = QtWidgets.QFileDialog.getOpenFileName()
        directory = str(directory[0])
        if directory != '':
            file_path = directory.split('/')
            if len(file_path) >= 3:
                if '.' in file_path[-1]:
                    extension = file_path[-1].split('.')[-1]
                    file_path = '/'.join(file_path[-3:])

                    if extension == 'dill':
                        try:
                            file = spider.load_file(file_path)
                            self.rank = file['rank']
                        except:
                            pass

    # Display first five ranks of webpage corresponding to keyword
    def list_web(self):
        self.search_list_widget.clear()
        word = self.search_line.text().lower()
        if self.rank is not None:
            if word in self.rank:
                if len(self.rank[word]) >= 5:
                    sorted_links = spider._sort_dict(self.rank[word])
                    ranks = spider.list_rank(5, sorted_links)
                    for each_rank in ranks:
                        rank_str = 'url: {0}  numbers: {1}'.format(each_rank[0], each_rank[1])
                        item = QtWidgets.QListWidgetItem(rank_str)
                        self.search_list_widget.addItem(item)
    # Open url link
    def open_link(self, item):
        item_link = item.text().split(' ')[1]
        os.startfile(item_link)

class File:
    '''This class used to manipulate file.'''
    def __init__(self):
        self.data_path = 'data'
        self._create_directory(self.data_path)

    # Create a directory to store file if it's empty
    def _create_directory(self, directory_path):
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)

    # Create file name according to datetime
    def create_file_name(self):
        return  datetime.now().strftime('%Y_%m_%d_%H-%M-%S') + '.dill'

    # Save file in dill format
    def save_file(self, file_path, data):
        '''Save file.'''
        with open(file_path, 'wb') as file:
            dill.dump(data, file)

    # Load file from dill format
    def load_file(self, file_path):
        '''Load file.'''
        with open(file_path, 'rb') as file:
            return dill.load(file)

    # Get the recent file according to datetime
    def get_last_file(self, path):
        json_files = glob(path + '/*.dill')
        ts_last_file = 0
        last_file = None

        for each_file in json_files:
            modify_ts = os.path.getmtime(each_file)
            if modify_ts > ts_last_file:
                ts_last_file = modify_ts
                last_file = each_file

        return last_file

class HTML:
    '''This class used to manipulate html tag.'''
    def __init__(self):
        self.http_error = dict()
        self.url_error = dict()

    # Get html web page and decode
    def get_html(self, url):
        html = None
        error = None
        if url not in self.url_error:
            try:
                html = urlopen(url, timeout=2.0)
            except HTTPError as e:
                self.http_error[url] = e.code
                error = '{0} Error code: {1}, Error reason: {2}'.format(url, e.code, e.reason)
                # print(error)
                return error, html
            except URLError as e:
                self.url_error[url] = e.reason
                error = '{0} Error reason: {1}'.format(url, e.reason)
                # print(error)
                return error, html
            except Exception as e:
                error = '{0} Error: {1}'.format(url, e)
                # print(error)
                return error, html

            if html is not None:
                try:
                    my_bytes = html.read()
                    return error, my_bytes.decode("ISO-8859-1")

                except UnicodeDecodeError as e:
                    error = '{0} Error: {1}'.format(url, e)
                    # print(error)
                    return error, html

                except Exception as e:
                    error = '{0} Error: {1}'.format(url, e)
                    # print(error)
                    return error, html

        return '{0}: url error'.format(url), html

    # Delete html tag from html page
    def clean_html_tag(self, html):
        page = re.compile(r'<.*?>')
        return page.sub('', html)

    # Get links those contain in html page
    def get_link(self, html):
        links = BeautifulSoup(html, 'html.parser')
        collected_links = list()
        for eachLink in links.select('a'):
            if eachLink.has_attr('href') and 'http' in eachLink['href']:
                collected_links.append(eachLink['href'])
        return collected_links

class Counter:
    '''This class used to count and rank the recorded data'''
    def __init__(self):
        self.rank = dict()
        self.wnl = WordNetLemmatizer()

    # Word stem and count word in html page
    def count(self, text, url):
        text = text.split('\n')

        for each_line in text:
            words = word_tokenize(each_line)

            for each_word in words:
                try:
                    each_word = each_word.lower()
                    each_word = self.wnl.lemmatize(each_word)
                    if each_word not in self.rank:
                        self.rank[each_word] = {url : 1}
                    else:
                        if url not in self.rank[each_word]:
                            self.rank[each_word][url] = 1
                        else:
                            self.rank[each_word][url] += 1
                except Exception as e:
                    print(e)
                    pass

    # Sort the recorded data
    def _sort_dict(self, dict_words):
        sorted_dict = [(k, dict_words[k]) for k in sorted(dict_words, key=dict_words.get, reverse=True)]
        return sorted_dict

    # Rank first n list
    def list_rank(self, number, rank):
        return rank[:number]


class Spider(Counter, HTML, File):
    '''This class is used to crawl web page'''
    allow_crawl = True

    def __init__(self):
        HTML.__init__(self)
        Counter.__init__(self)
        File.__init__(self)
        self.pool = None
        self.p = None
        self.last_links = list()
        self.crawled = set()
        self.dir_name = None

    # Create a directory of start crawling point
    def create_dir_name(self, url):
        url = url.replace('//', '_')
        url = url.replace('/', '_')
        url = url.replace('.', '_')
        url = url.replace(':', '_')
        return 'data/' + url

    # Get and set environment for crawling
    def start_crawl(self):
        last_file = None
        url = ui.lineEdit.text()
        self.dir_name = self.create_dir_name(url)
        self._create_directory(self.dir_name)
        if os.path.exists(self.dir_name):
            last_file = self.get_last_file(self.dir_name)

        if url != '':
            if last_file is not None:
                file = self.load_file(last_file)

                self.rank = file['rank']
                self.http_error = file['http_error']
                self.url_error = file['url_error']
                self.last_links = file['last_links']

                self.crawled = file['crawled']

            Spider.allow_crawl = True

            if len(self.last_links) != 0:
                self.p = Thread(target=self.crawl, args=(self.last_links,))
                self.p.start()
            else:
                self.p = Thread(target=self.crawl, args=(url,))
                self.p.start()

    # Stop crawling
    def stop_crawl(self):
        Spider.allow_crawl = False
        self.pool.terminate()
        self.pool.join()
        self.p.join(timeout=5)
        data = {'rank':self.rank, 'http_error':self.http_error, 'url_error':self.url_error, 'last_links':self.last_links, 'crawled': self.crawled}
        file_path = self.dir_name + '/' + self.create_file_name()

        self.save_file(file_path, data)

    # Process of each crawling
    def process(self, url):
        if url not in self.crawled:
            error, html = self.get_html(url)
            if html is not None:
                if type(html) is str:
                    if ui.bot_list_widget.count() > ui.item_limit:
                        pool = Pool(1)
                        pool.apply_async(ui.delete_list_widget, args=(ui.bot_list_widget, ))

                    text = 'Retrieved {}.'.format(url)
                    text_item = QtWidgets.QListWidgetItem(text)
                    ui.bot_list_widget.addItem(text_item)
                    plain_text = self.clean_html_tag(html)
                    self.count(plain_text, url)
                    return [url, self.get_link(html)]

            else:
                if ui.bot_list_widget.count() > ui.item_limit:
                    pool = Pool(1)
                    pool.apply_async(ui.delete_list_widget, args=(ui.bot_list_widget, ))

                text = '{}'.format(error)
                text_item = QtWidgets.QListWidgetItem(text)
                ui.bot_list_widget.addItem(text_item)

    # Second crawl step
    def _continue_crawl(self, url):
        url = list(filter(None, url))
        links = list()
        file_path = self.dir_name + '/' + self.create_file_name()
        for each_link in self.pool.imap_unordered(self.process, url):
            if each_link is not None:
                if each_link[1] is not None:
                    links.extend(each_link[1])
                    self.crawled.add(each_link[0])

        if len(links) != 0:
            self.last_links = links

            data = {'rank': self.rank, 'http_error': self.http_error, 'url_error': self.url_error,
                    'last_links': self.last_links, 'crawled': self.crawled}
            self.save_file(file_path, data)

            while Spider.allow_crawl and len(self.last_links) != 0:
                links = list()
                # url = list(filter(None, url))
                # url = list(itertools.chain.from_iterable(url))
                for each_link in self.pool.imap_unordered(self.process, self.last_links):
                    if each_link is not None:
                        if each_link[1] is not None:
                            links.extend(each_link[1])
                            self.crawled.add(each_link[0])

                data = {'rank': self.rank, 'http_error': self.http_error, 'url_error': self.url_error,
                        'last_links': self.last_links, 'crawled': self.crawled}
                self.save_file(file_path, data)

                if len(links) != 0:
                    self.last_links = links

    # First crawl step
    def crawl(self, url):
        self.pool = Pool(30)

        if type(url) is not list:
            links = self.pool.apply(self.process, args=(url,))
            if links is not None:
                links[1] = list(filter(None, links[1]))
                if len(links[1]) != 0:
                    self.last_links = links[1]
                    self.crawled.add(links[0])
                    self._continue_crawl(links[1])
        else:
            self._continue_crawl(url)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    spider = Spider()
    ui = UiMainWindow()
    # self.crawl('https://en.wikipedia.org/wiki/Computer')
    sys.exit(app.exec_())
