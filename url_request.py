import requests
from fake_headers import Headers
from lxml import etree
# from settings import *
import re
import sys
import time
import random
import pyautogui
import socket 
# import socks 
from stem import Signal
from stem.control import Controller
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import os
# from db_mysql import *

headers=Headers(headers=True).generate()
CURRENT_PATH=os.path.abspath('')
IAMGE_SAVE_PATH=os.path.join(CURRENT_PATH,'GOT','SEXIMAGE')
bot_warning="""<div class="Paragraph">As you were browsing similarweb.com something about your browser made us think you were a bot. There are a few reasons this might happen:</div>"""

class liepin_spider(object):
    def __init__(self,url):
        self.USER_AGENTS = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
            'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.71 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1.2 Safari/605.1.15',
            'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_6; en-en) AppleWebKit/533.19.4 (KHTML, like Gecko) Version/5.0.3 Safari/533.19.4',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/603.3.8 (KHTML, like Gecko) Version/10.1.2 Safari/603.3.8',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/534.59.10 (KHTML, like Gecko) Version/5.1.9 Safari/534.59.10',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/E7FBAF',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10; rv:33.0) Gecko/20100101 Firefox/33.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/601.7.8 (KHTML, like Gecko)',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/601.7.7 (KHTML, like Gecko) Version/9.1.2 Safari/601.7.7',
            'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_4; de-de) AppleWebKit/525.18 (KHTML, like Gecko) Version/3.1.2 Safari/525.20.1',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:16.0) Gecko/20100101 Firefox/16.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1',
            'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0',
        ]
        self.url =url
        self.headers = {
                        'referer':'https://www.liepin.com/',
                        'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                        'accept-encoding':'gzip, deflate, br',
                        'user-agent':random.choice(self.USER_AGENTS)}

    def run(self):
        r = requests.get(self.url,headers=self.headers)
        doc = etree.HTML(r.text)
        print(doc.xpath('head/title/text()'))

def am_I_a_bot(content):
    result=re.findall(bot_warning,content)
    if result:
        return True
    else:
        return False

def mouseClick(clickTimes,lOrR,img,reTry):
    if reTry == 1:
        while True:
            location=pyautogui.locateCenterOnScreen(img,confidence=0.9)
            print(location)
            if location is not None:
                pyautogui.click(location.x,location.y,clicks=clickTimes,interval=10,duration=10,button=lOrR)
                break
            print("未找到匹配图片,0.1秒后重试")
            time.sleep(0.1)
    elif reTry == -1:
        while True:
            location=pyautogui.locateCenterOnScreen(img,confidence=0.9)
            if location is not None:
                pyautogui.click(location.x,location.y,clicks=clickTimes,interval=0.2,duration=0.2,button=lOrR)
            time.sleep(0.1)
    elif reTry > 1:
        i = 1
        while i < reTry + 1:
            location=pyautogui.locateCenterOnScreen(img,confidence=0.9)
            if location is not None:
                pyautogui.click(location.x,location.y,clicks=clickTimes,interval=0.2,duration=0.2,button=lOrR)
                print("重复")
                i += 1
            time.sleep(0.1)

def random_sleep(mu=1, sigma=0.4):
    '''正态分布随机睡眠
    :param mu: 平均值
    :param sigma: 标准差，决定波动范围
    '''
    secs = random.normalvariate(mu, sigma)
    if secs <= 0:
        secs = mu  # 太小则重置为平均值
    # time.sleep(secs)
    return secs

def get_proxy():
    PROXY_POOL_URL='http://127.0.0.1:5555/random'
    """
    从代理池获取代理
    """
    try:
        response=requests.get(PROXY_POOL_URL)
        if response.status_code==200:
            print('Get Proxy',response.text)
            return response.text
        return None
    except requests.ConnectionError:
        return None

def url_python_request(url):
    try:
        res=requests.get(url,headers=headers,timeout=5,verify=True)
        # ,proxies={'https':'https://127.0.0.1:7890'}
        if res:
            print('Python Requests访问 {} ing！！'.format(url))
            res.encoding=res.apparent_encoding##将返回的网页源码转换成合适的编码
            print('{} 状态码:{}'.format(url, res.status_code))
            if am_I_a_bot(res.text):
                print('本次访问被鉴定为爬虫!!')
            else:
                if res.status_code == 200:
                    save_name=os.path.join(os.path.abspath(''),'TXT',url.split('://')[1].replace('.','_').replace('/','')+'.txt')
                    with open(save_name,'w',encoding='utf-8') as f:
                        try:
                            f.write(res.text)
                        except TypeError as e:
                            pass
                    return res.text
    except Exception as e:
        print('Crawling Failed', url)
        print(e.args)
        return None

def url_python_request_proxy(url):

    try:
        res=requests.get(url,headers=headers,proxy=get_proxy(),timeout=5,verify=False)
        if res:
            print('Python Requests with proxy访问 {} ing！！'.format(url))
            res.encoding=res.apparent_encoding##将返回的网页源码转换成合适的编码
            print('{} 状态码:{}'.format(url, res.status_code))
            if res.status_code == 200:
                save_name=os.path.join(os.path.abspath(''),'TXT',url.split('://')[1].replace('.','_').replace('/','')+'.txt')
                with open(save_name,'w',encoding='utf-8') as f:
                    try:
                        f.write(res.text)
                    except TypeError as e:
                        pass
                return res.text
    except Exception as e:
        print('Crawling Failed', url)
        print(e.args)
        return None
        
def getdata(html):
    pass

def url_selenium_phantomjs_request(url):
    #Windows 下使用版本为selenium==2.48.0,如果是新版本可能不支持PhantomJS，这个版本下以下chrome的无头模式函数不可用，与其互斥
    ##平均10s访问一个页面
    dcap=dict(DesiredCapabilities.PHANTOMJS)
    dcap["phantomjs.page.settings.userAgent"]=('Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36')
    try:
        driver= webdriver.PhantomJS(PhantomJSPath,desired_capabilities=dcap,service_args=['--ignore-ssl-errors=true'])#
        driver.get(url)
        print('PhantomJS访问 {} ing！！'.format(url))
        time.sleep(random_sleep(mu=2, sigma=0.4))
        driver.get_screenshot_as_file('before_login.png')
        html=driver.page_source
        return html
        
    except Exception as e:
        print(e.args)
        # html='404 Not Found --Bcy'
        driver.quit()
        return None
    finally:
        driver.quit()
        
def url_selenium_request(url):
    ##平均10s访问一个页面,最新版本为selenium4.1.0
    ch_options = Options()# ChromeOptions()
    ch_options.add_experimental_option("excludeSwitches", ['enable-automation'])
    
    # print(ch_options)
    # ch_options.headless=True# => 为Chrome配置无头模式

    # ch_options.add_argument("--headless")  # => 为Chrome配置无头模式
    # ch_options.add_experimental_option('excludeSwitches', ['enable-automation'])
    # ch_options.add_experimental_option('useAutomationExtension', False)
    # 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'
    try:
        driver = webdriver.Chrome(options=ch_options) # r'C:\Users\liuyan\Desktop\chrome_driver_98\chromedriver.exe',,options=ch_options # => 注意这里的参数
        # driver= webdriver.PhantomJS(PhantomJSPath,desired_capabilities=dcap,service_args=['--ignore-ssl-errors=true'])#
        driver.maximize_window()
        driver.get(url)
        print('Selenium Headless访问 {} ing！！'.format(url))
        time.sleep(random_sleep(mu=2, sigma=0.4))
        save_name=os.path.join(os.path.abspath(''),'TXT',url.split('://')[1].replace('.','_').replace('/','')+'.txt')
        pic_save_name=os.path.join(CURRENT_PATH,'GOT','IMAGE',url.split('://')[1].replace('.','_').replace('/','')+'.png')
        driver.get_screenshot_as_file(pic_save_name)
        html=driver.page_source
        if am_I_a_bot(html):
            print('本次访问被鉴定为爬虫!!')
            # time.sleep(3)
            img=os.path.join(CURRENT_PATH,'test.jpg')
            reTry=1
            mouseClick(1,'left',img,reTry)
            time.sleep(3)
            mouseClick(1,'left',img,reTry)
            # print('源码又怎么获取呢?')
            html=driver.page_source
        with open(save_name,'w',encoding='utf-8') as f:
            try:
                f.write(html)
            except TypeError as e:
                pass
        return html
    except Exception as e:
        print(e.args)
        # print('UNKNOWN ERROR')
        driver.quit()
        return None
    finally:
        driver.quit()
        
def url_proxy_selenium_request(url):
    ##需要做一个带代理的方法来访问例如www.ipip.net的对ip进行ipv4精准画像的网站
    # pass
    # chrome_opt.add_argument("--proxy-server=http://111.11.1.111:8080")
    ch_options = Options()
    ch_options.headless=True
    ch_options.add_argument("--proxy-server=http://{}".format(get_proxy()))
    try:
        driver = webdriver.Chrome(options=ch_options) # r'C:\Users\liuyan\Desktop\chrome_driver_98\chromedriver.exe',,options=ch_options # => 注意这里的参数
        # driver= webdriver.PhantomJS(PhantomJSPath,desired_capabilities=dcap,service_args=['--ignore-ssl-errors=true'])#
        driver.get(url)
        print('Selenium Headless访问 {} ing！！'.format(url))
        time.sleep(5)
        pic_save_name=url.split('://')[1].replace('.','_').replace('/','')+'.png'
        driver.get_screenshot_as_file(pic_save_name)
        html=driver.page_source
        return html
    except Exception as e:
        print(e.args)
        # html='404 Not Found --Bcy'
        driver.quit()
        return None
    finally:
        driver.quit()
# 通过Tor切换ip
def switchIP():
    with Controller.from_port() as controller:#port = 9151
        controller.authenticate()
        controller.signal(Signal.NEWNYM) 

    # now_ip=requests.get("http://checkip.amazonaws.com").text 

    # return now_ip

#checkip
# def checkIP(ip):
#     a=requests.get("http://checkip.amazonaws.com").text 

def url_tor_proxy_python_request(url):
    switchIP()
    proxies = {'http': 'socks5://127.0.0.1:9150',
               'https': 'socks5://127.0.0.1:9150'}
    try:
        now_ip=requests.get("http://checkip.amazonaws.com",proxies=proxies).text 
    except requests.exceptions.ConnectionError as e:
        print(f"貌似Tor断开了,请手动重连,具体原因如下:{e.args}")
        switchIP()
        # continue
        # sys.exit()
    # print(now_ip)
    # print(requests.get("http://checkip.amazonaws.com",proxies=proxies).text)
    try:
        res=requests.get(url,headers=headers,proxies=proxies)
        
    except Exception as e:
        print('Crawling Failed', url)
        print(e.args)
        return None
    if res:
        print('Tor+Python Requests访问 {} ing by {}！！'.format(url,now_ip))
        res.encoding=res.apparent_encoding##将返回的网页源码转换成合适的编码
        print('{} 状态码:{}'.format(url, res.status_code))
        if res.status_code == 200:
            save_name=os.path.join(os.path.abspath(''),'TXT',url.split('://')[1].replace('.','_').replace('/','')+'.txt')
            with open(save_name,'w',encoding='utf-8') as f:
                try:
                    f.write(res.text)
                except TypeError as e:
                    pass
            return res.text
    else:
        print('Crawling Failed', url)


def url_tor_proxy_selenium_request(url):
    now_ip=switchIP()
    # socks.set_default_proxy(socks.SOCKS5,"127.0.0.1",9150) 
    # socket.socket=socks.socksocket
    ch_options = Options()
    PROXY='127.0.0.1:9150'#Tor Browser的默认端口
    
    ch_options.headless=True
    ch_options.add_argument('--proxy-server=SOCKS5://{}'.format(PROXY))
    ch_options.add_argument('blink-settings=imagesEnabled=false') #不加载图片, 提升速度
    try:
        driver = webdriver.Chrome(options=ch_options)
        driver.get(url)
        print('Tor+Selenium Headless访问 {} ing by {}！！'.format(url,now_ip))
        time.sleep(5)
        save_name=os.path.join(os.path.abspath(''),'TXT',url.split('://')[1].replace('.','_').replace('/','')+'.txt')
        pic_save_name=url.split('://')[1].replace('.','_').replace('/','')+'.png'
        driver.get_screenshot_as_file(pic_save_name)
        html=driver.page_source#Tor
        if am_I_a_bot(html):
            print('本次访问被鉴定为爬虫!!')
            # time.sleep(3)
            img=os.path.join(CURRENT_PATH,'test.jpg')
            reTry=1
            mouseClick(1,'left',img,reTry)
            time.sleep(3)
            mouseClick(1,'left',img,reTry)
            # print('源码又怎么获取呢?')
            html=driver.page_source
        with open(save_name,'w',encoding='utf-8') as f:
            try:
                f.write(html)
            except TypeError as e:
                pass
        return html
    except Exception as e:
        print(e.args)
        # html='404 Not Found --Bcy'
        driver.quit()
        return None
    finally:
        driver.quit()


def download_pic(picurl,count):
    db=MysqlClient()
    query_result=db.query_pic2download(picurl)
    # query_result=db.query_existance('sexpic_url_record','picurl',picurl)
    print(query_result)
    if picurl[:4] !='http' or query_result:
        pass
    else:
        try:
            res=requests.get(url,headers=headers,timeout=5,verify=False)
        except:
            print('UNKNOWN ERROR')
            pass
        if res and ('404' not in res.text) and ('error' not in res.text) and ('Error' not in res.text) and ('html' not in res.text):
            count+=100
            image_name=os.path.join(IAMGE_SAVE_PATH,'image_{:0>9}.jpg'.format(count))
            print('*Downloading {}!!!'.format(image_name))
            with open(image_name,'wb') as pic:
                pic.write(res.content)
    db.close()
    
def save_pagecode(url):
    # content=url_selenium_request(url)
    content=url_python_request(url)##在这里切换请求方法
    save_name=os.path.join(os.path.abspath(''),'GOT',url.split('://')[1].replace('.','_').replace('/','')+'.txt')
    with open(save_name,'w',encoding='utf-8') as f:
        try:
            f.write(content)
        except TypeError as e:
            pass
    # print(content)

if __name__=='__main__':
    # url='http://www.hzsycx.com/'
    # url='https://www.amazon.com'
    # url='https://www.ctrip.com'
    # url='http://ips.chacuo.net/view/s_BJ'
    # url='https://www.ipip.net/'##国家及地区IP段
    # url='https://www.eastmoney.com/'
    # url='http://kuihua2020.com'
    # url='https://help.aliyun.com/document_detail/35751.html'
    """
    url_python_request
    url_selenium_phantomjs_request
    url_selenium_request
    url_tor_proxy_python_request
    url_tor_proxy_selenium_request
    """
    # url='http://www.baidu.com'
    # url='http://1.007milf.com/mstrbg/1204/50011081.jpg'
    # url='https://app.mi.com/catTopList/10'
    # url='https://www.similarweb.com/zh/apps/top/google/app-index/us/all/top-free/'
    # url='https://www.similarweb.com/zh/apps/top/apple/store-rank/cn/all/top-free/iphone/'
    # url='https://www.liepin.com/'
    url='https://www.liepin.com/job/1948895625.shtml'
    # url_python_request(url)
    # download_pic(url,0)
    url_python_request(url)

    # a=liepin_spider(url)
    # a.run()

    # print(get_proxy())