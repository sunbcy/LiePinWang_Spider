import os,re,json,time
from lxml  import etree 
from url_request import *
from urllib.parse import unquote
from db_mysql import *
import configparser
from queue import Queue

CURRENT_PATH=os.path.abspath('')
test_txt=open(r'./TXT/www_liepin_com.txt','r',encoding='utf-8').read()
test_txt_2=open(r'./TXT/www_liepin_comjob1948895625_shtml.txt','r',encoding='utf-8').read()
test_txt_3=open(r'./TXT/www_liepin_com-company-2174886-.txt','r',encoding='utf-8').read()
test_txt_4=open(r'./TXT/www_liepin_com-company-jobs-2174886-.txt','r',encoding='utf-8').read()
test_html_1=open('./TXT/www.liepin.com_job_1910066221.html','r',encoding='utf-8').read()

uncraweled_company_href_list=[]
company_name_list=[]
def main():
    config=configparser.ConfigParser()
    config.read('config.ini')
    company_num=config['config']['company_num']
    # job_num=config['config']['job_num']
    db=MysqlClient()
    html=etree.HTML(test_txt)
    title=html.xpath('head/title/text()')[0]
    # print(html.xpath('//div[@class="header-title-item-text"]/text()'))
    #多属性匹配的写法
    # print(html.xpath('//a[contains(@class,"header-title-item") or @class="header-title-item-active"]/@href'))
    #公司名字
    Company_Name_List=html.xpath(' //a[@class="industry-content-comp-item"]/text()')
    # print(Company_Name_List)
    #公司href
    Company_Href_List=html.xpath('//a[@class="industry-content-comp-item"]/@href')
    # print(Company_Href_List)
    HomeCompany_Dict=dict(zip(Company_Name_List,Company_Href_List))
    for i in HomeCompany_Dict:
        company_num=str(int(company_num)+1)
        # id=company_num
        company_name=i
        company_href=HomeCompany_Dict[i]
        company_id=HomeCompany_Dict[i].split('/')[-2]
        company_jobs_href='https://www.liepin.com/company-jobs/'+str(company_id)+'/'
        jobs_href_accessed='False'
        company_full_name=''
        company_location=''
        BusinessRegisterContentItem=''
        mtime=time.strftime('%Y-%m-%d %H:%M:%S')
        print(f"插入{i,HomeCompany_Dict[i]}")
        #company_name company_href company_id company_jobs_href jobs_href_accessed有值
        db.insert_companyinfo(company_name,company_href,company_id,company_jobs_href,jobs_href_accessed,company_full_name,company_location,BusinessRegisterContentItem,mtime)
    config.set('config','company_num',company_num)
    config.write(open('config.ini','w'))

    for i in Company_Href_List:
        if i not  in uncraweled_company_href_list:
            uncraweled_company_href_list.append(i)
    #获取公司在猎聘的id
    # liepin_company_id=href.split('company')[1].split('/')[1]

    #首页名企职位 12个
    HomeCompanyHref_List=html.xpath('//a[@class="home-comp-info"]/@href')
    # print(HomeCompanyHref_List)
    for i in HomeCompanyHref_List:
        if i not  in uncraweled_company_href_list: 
            uncraweled_company_href_list.append(i)

    # print(html.xpath('head/title/text()')[0])

    #一级热门职位
    # FirstLevelHotJobsHref_List=html.xpath('//a[@class="hot-jobs-first-title"]/@href')
    FirstLevelHotJobsName_List=html.xpath('//a[@class="hot-jobs-first-title"]/text()')
    # print(f'一级热门职位Name:\n{FirstLevelHotJobsName_List}')
    # print(f'一级热门职位Href:\n{FirstLevelHotJobsHref_List}')

    #二级热门职位
    hot_jobs={}
    SecondLevelHotJobsHref_List=html.xpath('//a[@class="hot-jobs-second-title"]/@href')
    SecondLevelHotJobsName_List=html.xpath('//a[@class="hot-jobs-second-title"]/text()')
    # print(SecondLevelHotJobsHref_List)
    # print(SecondLevelHotJobsName_List)

    #三级热门职位
    ThreeLevelHotJobsHref_List=html.xpath('//a[@class="hot-jobs-three-title"]/@href')
    ThreeLevelHotJobsName_List=html.xpath('//a[@class="hot-jobs-three-title"]/text()')
    # print(ThreeLevelHotJobsHref_List)
    # print(ThreeLevelHotJobsName_List)
    db.close()

def UPDATE_JOBS_DETAILS(job_id,given_company_id,content):
    db=MysqlClient()
    html=etree.HTML(content)
    if content:
        ##DEBUG
        # print(html.xpath('//head/title/text()')[0])
        # print(html.xpath('//div[@class="job-apply-content"]//span[@class="name ellipsis-1"]/text()')[0])
        # print(html.xpath('//div[@class="job-apply-content"]//span[@class="salary"]/text()')[0])
        # print(html.xpath('//div[@class="job-apply-content"]//div[@class="job-properties"]/span/text()'))
        # print(html.xpath('//main//content//div[@class="title-box"]//span/a/@href')[0])
        # print(html.xpath('//main//content//div[@class="title-box"]//span/a/@href')[0].split('/')[-2])
        # print(html.xpath('//main//content//div[@class="title-box"]//span/a/text()')[0].split('·')[1].strip())
        # print(html.xpath('//main//content//section[@class="job-intro-container"]//ul/li/text()'))
        # print(html.xpath('//main//content//dd[@data-selector="job-intro-content"]//text()')[0])
        # print(html.xpath('//main//content//section[@class="company-intro-container"]//div[@class="inner ellipsis-3"]/text()')[0])
        # quit()
        # print(html.xpath('//span[@class="job-salary"]/text()'))

        try:
            job_id=job_id
            job_title=html.xpath('//div[@class="job-apply-content"]//span[@class="name ellipsis-1"]/text()')[0]
            job_salary=html.xpath('//div[@class="job-apply-content"]//span[@class="salary"]/text()')[0]
            job_properties=html.xpath('//div[@class="job-apply-content"]//div[@class="job-properties"]/span/text()')
            company_url=html.xpath('//main//content//div[@class="title-box"]//span/a/@href')[0]
            company_id=company_url.split('/')[-2]
            # company_name=html.xpath('//main//content//div[@class="title-box"]//span/a/text()')[0].split('·')[1].strip()##反例 【临床研究员CRA招聘】_泰格医药招聘信息-猎聘 没有特殊分隔符
            job_intro_tag=html.xpath('//main//content//section[@class="job-intro-container"]//ul/li/text()')
            job_tags=str(tuple(job_properties+job_intro_tag))
            job_intro_content=html.xpath('//main//content//dd[@data-selector="job-intro-content"]//text()')[0]
            try:
                company_intro=html.xpath('//main//content//section[@class="company-intro-container"]//div[@class="inner ellipsis-3"]/text()')[0]
            except IndexError as e:
                company_intro=html.xpath('//main//content//section[@class="company-intro-container"]//div[@class="inner ellipsis-3"]/text()')
                if (not company_intro):
                    company_intro=''
                print(f"company_intro为{company_intro}")

            print(job_title)
            print(job_salary)
            print(job_tags)
            # print(company_url)
            # print(company_id)
            # print(company_name)
            print(job_intro_content)#岗位职责/职位要求
            print(company_intro)#公司简介
            db.update_company_jobs_intro(job_id,job_tags,job_intro_content)
            db.update_company_intro(company_id,company_intro)
            find_hot_links(html,company_id,db)#寻找友链
            return 'OK'
        except IndexError as e:
            web_title=html.xpath('//head/title/text()')
            if web_title:
                web_title=web_title[0]
                company_id=given_company_id
                print(f"IndexError_2: {web_title}")
                find_hot_links(html,company_id,db)#寻找友链
                if web_title=='猎聘安全中心':
                    # with open(os.path.join(os.path.abspath(''),'TXT',web_title+'-'+time.strftime('%Y-%m-%d %H:%M:%S')+'.txt'),'w',encoding='utf-8') as f:
                    #     f.write(content)
                    quit()
                    return 'NoRet'
                    
                else:
                    return 'other'
            else:
                return 'other'
        # find_hot_links(html,company_id,db)#寻找友链
    else:
        return 'other'

    db.close()

    # job=html.xpath('//div[@class="job-detail-box"]')
    # job_title=job.xpath('//div[@class="ellipsis-1"]/@title')
    # print(job_title)
    # print(html.xpath('//div[@class="job-detail-box"]//div[@class="ellipsis-1"]/@title'))
    # print(html.xpath('//div[@class="job-detail-box"]//span[@class="ellipsis-1"]/text()'))
    # print(html.xpath('//div[@class="job-detail-box"]//span[@class="job-salary"]/text()'))
    # print(html.xpath('//div[@class="job-detail-box"]//span[@class="company-name ellipsis-1"]/text()'))

def update_four_job_columns(given_company_id,content):
    db=MysqlClient()
    html=etree.HTML(content)
    web_title=html.xpath('//head/title/text()')[0]
    company_name=web_title.split('招聘')[0][1:]
    config_mode='{(.*)}'#
    head_script_config=html.xpath('//head/script/text()')[-1]
    #工商信息
    BusinessRegisterContentItem=html.xpath('//div[@class="business-register-content-item"]/p[@class="text"]/text()')
    BusinessRegisterContentItem=str(BusinessRegisterContentItem)
    try:
        company_config='{'+re.findall(config_mode,head_script_config,re.S|re.M)[0]+'}'
        company_config=json.loads(company_config)
        company_id=company_config['compId']
        if company_id:
            company_id=company_id
        else:
            company_id=given_company_id
        try:
            company_location=unquote(company_config['address'])
        except KeyError as e:
            if 'address' in e.args:
                company_location=''
        try:
            company_longitude=json.loads(company_config['point'])['lng']
            company_latitude=json.loads(company_config['point'])['lat']
            company_point=str((company_longitude,company_latitude))
        except KeyError as e:
            if 'lng' in e.args:
                company_point=''
        try:
            compProductList=unquote(company_config['compProductList'])
        except KeyError as e:
            if 'compProductList' in e.args:
                compProductList=''
        company_full_name=unquote(company_config['compFullName'])
        db.update_companyinfo(company_id,company_location,company_point,company_full_name,BusinessRegisterContentItem)
        # db.update_companyinfo(company_id,company_full_name,company_location,company_point,BusinessRegisterContentItem)
    except IndexError as e:
        company_id=given_company_id
        print(f"跳过{web_title}")
        # print(re.findall(config_mode,head_script_config,re.S|re.M))
        # quit()
    find_hot_links(html,company_id,db)#寻找友链
    db.close()


def bad_web_content(content):#本函数扩充了公司的友链
    config=configparser.ConfigParser()
    config.read('config.ini')
    company_num=config['config']['company_num']
    db=MysqlClient()
    html=etree.HTML(content)
    web_title=html.xpath('//head/title/text()')[0]
    company_name=web_title.split('招聘')[0][1:]
    print(company_name)

    config_mode='{(.*)}'
    #找到Config中的最后一个script段
    head_script_config=html.xpath('//head/script/text()')[-1]
    try:
        company_config='{'+re.findall(config_mode,head_script_config,re.S|re.M)[0]+'}'
        company_config=json.loads(company_config)
        company_id=company_config['compId']
        #由company_jobs_href获取到更多的该公司的岗位,可能涉及到翻页,频繁访问.注意伪装
        company_jobs_href='https://www.liepin.com/company-jobs/'+str(company_id)+'/'
        company_location=unquote(company_config['address'])
        try:
            company_longitude=json.loads(company_config['point'])['lng']
            company_latitude=json.loads(company_config['point'])['lat']
            company_point=str((company_longitude,company_latitude))
        except KeyError as e:
            if 'lng' in e.args:
                company_point=''
        compProductList=unquote(company_config['compProductList'])
        company_full_name=unquote(company_config['compFullName'])
        print(company_location)
        print(company_jobs_href)
        # # print(company_config)
        print(company_point)
        # print(compProductList)
        print(company_full_name)
    except IndexError as e:
        print(f"跳过{web_title}")
        # quit()
    # RecruitItem=html.xpath('//ul[@class="hot-recruit-content"]/li[@class="recruit-item"]/a[@class="name-box"]/div[@class="name"]/text()')
    RecruitItemName=html.xpath('//ul[@class="hot-recruit-content"]/li[@class="recruit-item"]/a[@class="name-box"]/div[@class="name"]/text()')
    RecruitItemSalary=html.xpath('//ul[@class="hot-recruit-content"]/li[@class="recruit-item"]/a[@class="name-box"]/div[@class="salary"]/text()')
    RecruitItemInfoBox=html.xpath('//ul[@class="hot-recruit-content"]/li[@class="recruit-item"]/div[@class="info-box"]')
    RecruitItemLabelBox=html.xpath('//ul[@class="hot-recruit-content"]/li[@class="recruit-item"]/div[@class="label-box"]')
    #工商信息
    BusinessRegisterContentItem=html.xpath('//div[@class="business-register-content-item"]/p[@class="text"]/text()')
    BusinessRegisterContentItem=str(BusinessRegisterContentItem)
    print(BusinessRegisterContentItem)
    try:
        #对现存的部分网页TXT中的信息录入做判断,信息不对称时SQL不要用REPLACE语句
        if db.query_existance('LiePinCompanyInfo','company_id',company_id):
            db.update_companyinfo(company_id,company_location,company_point,company_full_name,BusinessRegisterContentItem)
        else:
            company_num=str(int(company_num)+1)
            # id=company_num
            company_href='https://www.liepin.com/company/'+str(company_id)+'/'
            db.insert_basic_companyinfo(company_name,company_id,company_href,company_jobs_href,company_full_name,company_location,company_point,BusinessRegisterContentItem)
        # db.update_companyinfo(company_id,company_location,company_point,company_full_name,BusinessRegisterContentItem)
    except UnboundLocalError as e:
        if "local variable 'company_id' referenced before assignment" in e.args:
            pass
    # CommonHotLinksContentHref=html.xpath('//div[@class="common-hot-links-content"]/a/@href')
    # CommonHotLinksContentTitle=html.xpath('//div[@class="common-hot-links-content"]/a/@title')
    # CommonHotLinks_Dict=dict(zip(CommonHotLinksContentTitle,CommonHotLinksContentHref))
    # CommonHotLinks_Dicts={}
    # for i in CommonHotLinks_Dict:
    #     if 'city-' not in CommonHotLinks_Dict[i] and '/company/' in CommonHotLinks_Dict[i]:
    #         CommonHotLinks_Dicts[i]=CommonHotLinks_Dict[i]
    #         company_num=str(int(company_num)+1)
    #         # id=company_num
    #         company_name=i
    #         company_href=CommonHotLinks_Dict[i]
    #         new_company_id=CommonHotLinks_Dict[i].split('/')[-2]
    #         if new_company_id==company_id:
    #             continue
    #         company_jobs_href='https://www.liepin.com/company-jobs/'+str(new_company_id)+'/'
    #         jobs_href_accessed='False'
    #         mtime=time.strftime('%Y-%m-%d %H:%M:%S')
    #         print(f"插入{i,CommonHotLinks_Dict[i]}")
    #         db.insert_hotlinks(company_name,company_href,new_company_id,company_jobs_href,jobs_href_accessed,mtime)

    find_hot_links(html,company_id,db)#寻找友链
    config.set('config','company_num',company_num)
    config.write(open('config.ini','w'))
    db.close()
    
def get_pagination(jobs_num):
    page_head=int(jobs_num/30)
    page_tail=jobs_num%30
    if page_head and page_tail>0:
        pagination=page_head+1
    elif page_head and page_tail==0:
        pagination=page_head
    else:
        pagination=page_head
    return pagination,page_tail

def get_job_info(given_company_name,company_id,job_web_content):#提取/pnxx/一个页面的全部职位信息并更新到数据库中
    db=MysqlClient()
    html=etree.HTML(job_web_content)
    try:
        company_name=html.xpath('//head/title/text()')[0].split('招聘')[0][1:]
    except IndexError as e:
        company_name=given_company_name
    company_id=company_id
    
    one_page_jobs_info={}
    company_tags_item_list=html.xpath('//div[@class="tags-item"]/span/text()')
    
    job_detail_job_info_href=html.xpath('//a[@data-nick="job-detail-job-info"]/@href')
    # job_info_href_list收集了职位href的集合
    job_info_href_list=[i.split('?')[0] if ('?' in i) else i for i in job_detail_job_info_href ]# and 'shtml' not in i
    # if '?' in i else i.split('/')[-1].split('.')[0]
    # print(len(job_info_href_list))
    job_info_href_list=['https://www.liepin.com/lptjob' if not i else i for i in job_info_href_list ]
    # print(job_info_href_list)
    job_id_list=[i.split('/')[-1].split('.')[0] if 'lptjob' not in i else ('lptjob'+i.split('/')[-1]) for i in job_info_href_list]
    job_id_list=[ 'lptjob'+str(time.time()) if i.split('/')[-1]=='lptjob' else i for i in job_id_list ]
    job_title_list=html.xpath('//div[@class="job-title-box"]/div[@class="ellipsis-1"]/text()')
    job_region_list=html.xpath('//div[@class="job-title-box"]/div[@class="job-dq-box"]/span[@class="ellipsis-1"]/text()')
    job_salary_list=html.xpath('//div[@class="job-title-box"]/../span[@class="job-salary"]/text()')
    job_tag=html.xpath('//div[@class="job-title-box"]/../../div[@class="job-labels-box"]')
    # print(len(job_tag))
    job_tags_list=[]
    for i in job_tag:
        job_tags=etree.HTML(etree.tostring(i, method='html')).xpath('//span[@class="labels-tag"]/text()')
        job_tags_list.append(tuple(job_tags))
    job_href_accessed='False'
    jobs_num=len(job_id_list)
    # print(jobs_num)
    try:
        for i in range(0,jobs_num):##先把job相关的信息添加到dict里面,随时可以导出.
            if 'lptjob' not in job_id_list[i]:
                one_page_jobs_info[job_id_list[i]]={'job_title':job_title_list[i],'job_info_href':job_info_href_list[i],'job_region':job_region_list[i],'job_salary':job_salary_list[i],'job_tags':job_tags_list[i]}
            else:
                one_page_jobs_info[job_id_list[i]]={'job_title':job_title_list[i],'job_info_href':('https://www.liepin.com/lptjob/'+str(job_id_list[i].split('lptjob')[-1])),'job_region':job_region_list[i],'job_salary':job_salary_list[i],'job_tags':job_tags_list[i]}
    except IndexError as e:
        print(e.args)
    for job in one_page_jobs_info:#插入职位数据表
        job_id=job
        job_title=one_page_jobs_info[job]['job_title']
        job_region=one_page_jobs_info[job]['job_region']
        job_salary=one_page_jobs_info[job]['job_salary']
        job_tags=one_page_jobs_info[job]['job_tags']
        job_info_href=one_page_jobs_info[job]['job_info_href']
        job_href_accessed='False'
        try:
            db.insert_jobs_info(job_id,job_title,job_region,job_salary,str(job_tags),company_name,company_id,job_info_href,job_href_accessed)
        except TypeError as e:
            print(job_title)

    find_hot_links(html,company_id,db)#寻找友链
    db.close()

def find_hot_links(html,company_id,db):
    #获取该公司首页的其他公司友链,并扩充到LiePinCompanyInfo里去  **此处待完善
    CommonHotLinksContentHref=html.xpath('//div[@class="common-hot-links-content"]/a/@href')
    CommonHotLinksContentTitle=html.xpath('//div[@class="common-hot-links-content"]/a/@title')
    CommonHotLinks_Dict=dict(zip(CommonHotLinksContentTitle,CommonHotLinksContentHref))
    CommonHotLinks_Dicts={}
    for i in CommonHotLinks_Dict:
        if 'city-' not in CommonHotLinks_Dict[i] and '/company/' in CommonHotLinks_Dict[i]:
            CommonHotLinks_Dicts[i]=CommonHotLinks_Dict[i]
            company_name=i
            company_href=CommonHotLinks_Dict[i]
            new_company_id=CommonHotLinks_Dict[i].split('/')[-2]
            if new_company_id==company_id:
                continue
            company_jobs_href='https://www.liepin.com/company-jobs/'+str(new_company_id)+'/'
            jobs_href_accessed='False'
            mtime=time.strftime('%Y-%m-%d %H:%M:%S')
            print(f"插入友链 {i,CommonHotLinks_Dict[i]}")
            # print(company_name)
            db.insert_hotlinks(company_name,company_href,new_company_id,company_jobs_href,jobs_href_accessed,mtime)


    #粗略获取每个公司的职位发布
def GET_JOBS_FROM_COMPANY(given_company_name,company_jobs_href,content):#获取company_jobs相关的3000个职位的URL页面
    """未登录情况下,每个公司的company_jobs是3000个岗位,每页30个,pn1-pn100"""
    db=MysqlClient()
    html=etree.HTML(content)
    try:
        company_name=html.xpath('//head/title/text()')[0].split('招聘')[0][1:]
    except IndexError as e:
        # print(html.xpath('//head/title/text'))#[0].split('招聘')#不合理
        # quit()
        company_name=given_company_name
    company_id=company_jobs_href.split('/')[-2]
    get_job_info(given_company_name,company_id,content)#将第一页的30个职位单独提取
    #热招职位-jobs_num 
    try:
        jobs_num=int(html.xpath('//div/a[@class="active"]/text()')[0].split('(')[1][:-1])
        print(f"{company_name}的职位数目:{int(jobs_num)}")
        db.update_company_jobs_num(company_id,jobs_num)
        pages,last_page_job_num=get_pagination(jobs_num)
        #获取除了pn1以外的剩下的页面的职位
        for i in range(1,pages+1):
            # if i<pages:
            #     page_job_num=31
            # elif i==pages and last_page_job_num<30:
            #     page_job_num=last_page_job_num+1
            # else:
            #     page_job_num=31
            # for j in range(1,page_job_num):#将不同数量职位的页面统一化处理
            if i==1:
                continue
            elif i>1 and i<101:
                job_page_url=company_jobs_href+'pn'+str(i)+'/'
            else:
                continue
            job_web_content=url_python_request(job_page_url)
            #若公司发布的职位数超过30个,从第二页开始进行职位提取
            get_job_info(company_name,company_id,job_web_content)


        find_hot_links(html,company_id,db)#寻找友链
        # #获取该公司首页的其他公司友链,并扩充到LiePinCompanyInfo里去  **此处待完善
        # CommonHotLinksContentHref=html.xpath('//div[@class="common-hot-links-content"]/a/@href')
        # CommonHotLinksContentTitle=html.xpath('//div[@class="common-hot-links-content"]/a/@title')
        # CommonHotLinks_Dict=dict(zip(CommonHotLinksContentTitle,CommonHotLinksContentHref))
        # CommonHotLinks_Dicts={}
        # for i in CommonHotLinks_Dict:
        #     if 'city-' not in CommonHotLinks_Dict[i] and '/company/' in CommonHotLinks_Dict[i]:
        #         CommonHotLinks_Dicts[i]=CommonHotLinks_Dict[i]
        #         company_name=i
        #         company_href=CommonHotLinks_Dict[i]
        #         new_company_id=CommonHotLinks_Dict[i].split('/')[-2]
        #         if new_company_id==company_id:
        #             continue
        #         company_jobs_href='https://www.liepin.com/company-jobs/'+str(new_company_id)+'/'
        #         jobs_href_accessed='False'
        #         mtime=time.strftime('%Y-%m-%d %H:%M:%S')
        #         print(f"插入{i,CommonHotLinks_Dict[i]}")
        #         db.insert_hotlinks(company_name,company_href,new_company_id,company_jobs_href,jobs_href_accessed,mtime)
        return 'OK'
    except IndexError as e:
        print(f"当前 {company_name} 暂无职位发布!Quit!")
        jobs_num=0
        db.update_company_jobs_num(company_id,jobs_num)
        return 'Nojobs'
    db.close()
 
if __name__ == '__main__':
    # """1 抓取首页"""
    # main()

    # """2 抓取现有TXT"""
    # company_list=[i for i in os.listdir(os.path.join(os.path.abspath(''),'TXT')) if ('company' in i and 'job' not in i)]
    # for i in company_list:
    #     company_info_content=open(os.path.join(os.path.abspath(''),'TXT',i),'r',encoding='utf-8').read()
    #     print(f"提取{i}")
    #     bad_web_content(company_info_content)

    """3 抓取公司粗略的职位信息GET_JOB_FROM_COMPANY func"""
    # db=MysqlClient()
    # q=Queue(maxsize=1)#将数据库中公司信息不完整的/或者未爬取过职位的公司查询到,入队列,取出来待用!并更新LiePinCompanyInfo的爬取状态
    # while(q.qsize()==0):
    #     companies_list=db.get_companies_no_fullname()
    #     for i in range(len(companies_list)):#入队列
    #         q.put(companies_list[i])
    #     while (q.qsize()):#当队列不为空时,爬取职位填充(插入)到新的数据表LiePinJobsInfo,并将队列数量减一直至为零
    #         company=q.get()
    #         company_name=company['company_name']
    #         print(f"队列取出 {company_name}")
    #         company_jobs_href=company['company_jobs_href']
    #         web_content=url_python_request(company_jobs_href)#从公司的职位首页源代码出发获取该公司的所有职位(未登录情况下的前3000个)
    #         result=GET_JOBS_FROM_COMPANY(company_name,company_jobs_href,web_content)#新增30个职位以及获取n页更多的职位
    #         # quit()
    #         company_id=company['company_id']
    #         company_href=company['company_href']
    #         if db.query_company_fullname_existance('LiePinCompanyInfo',company_id):
    #             pass
    #         else:
    #             if result=='Nojobs':
    #                 db.update_fullname2None(company_id)
    #             else:
    #                 company_content=url_python_request(company_href)#https://www.liepin.com/company/xxx/
    #                 update_four_job_columns(company_id,company_content)
    #         update_result=db.update_company_href_status(company_id)#将该href设为已访问
    #         print(f"更新状态:{update_result}")
    #         # print(q.qsize())
    #         # print(q.get())#出队列并返回LiePinCompanyInfo数据表中的一条公司的数据
    #         # time.sleep(1)
    # db.close()

    """4 抓取公司详细的职位信息GET_JOB_FROM_COMPANY func"""
    db=MysqlClient()
    q=Queue(maxsize=1)
    while(q.qsize()==0):
        companies_job_details_list=db.get_jobs_no_detail()
        for i in range(len(companies_job_details_list)):#入队列
            q.put(companies_job_details_list[i])
        while (q.qsize()):
            job=q.get()
            job_id=job['job_id']
            job_title=job['job_title']
            company_name=job['company_name']
            print(f"队列取出 {job_title} from {company_name}")
            company_id=job['company_id']
            job_info_href=job['job_info_href']
            web_content=url_python_request(job_info_href)
            ret=UPDATE_JOBS_DETAILS(job_id,company_id,web_content)
            # print(job_title,' from ',company_name)
            if ret=='OK':
                db.update_job_href_status(job_id)
            elif ret=='other':
                db.update_job_href_status(job_id)
            else:
                db.update_job_href_status(job_id)
    db.close()

#test_html_1
    # UPDATE_JOBS_DETAILS('1111',test_html_1)

    # content=
    # 

    # second(test_txt_2)
    # bad_web_content(test_txt_3)

    # for i in uncraweled_company_href_list:
    #     second(url_python_request(i))
    #     break

    