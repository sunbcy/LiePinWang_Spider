import os,re,json,time
from lxml  import etree 
from url_request import *
from urllib.parse import unquote
from db_mysql import *
import configparser


# print(config['config']['company_num'])
# print(config['config']['job_num'])
# quit()
CURRENT_PATH=os.path.abspath('')
test_txt=open(r'./TXT/www_liepin_com.txt','r',encoding='utf-8').read()
test_txt_2=open(r'./TXT/www_liepin_comjob1948895625_shtml.txt','r',encoding='utf-8').read()
test_txt_3=open(r'./TXT/www_liepin_com-company-2174886-.txt','r',encoding='utf-8').read()

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
        id=company_num
        company_name=i
        company_href=HomeCompany_Dict[i]
        company_id=HomeCompany_Dict[i].split('/')[-2]
        company_jobs_href='https://www.liepin.com/company-jobs/'+str(company_id)
        jobs_href_accessed='False'
        company_full_name=''
        company_location=''
        BusinessRegisterContentItem=''
        mtime=time.strftime('%Y-%m-%d %H:%M:%S')
        print(f"插入{i,HomeCompany_Dict[i]}")
        #company_name company_href company_id company_jobs_href jobs_href_accessed有值
        db.insert_companyinfo(id,company_name,company_href,company_id,company_jobs_href,jobs_href_accessed,company_full_name,company_location,BusinessRegisterContentItem,mtime)
        # break
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

def second(content):
    html=etree.HTML(content)
    # print(html.xpath('//span[@class="job-salary"]/text()'))

    # job_url=
    try:
        job_title=html.xpath('//div[@class="job-apply-content"]//span[@class="name ellipsis-1"]/text()')[0]
        job_salary=html.xpath('//div[@class="job-apply-content"]//span[@class="salary"]/text()')[0]
        job_properties=html.xpath('//div[@class="job-apply-content"]//div[@class="job-properties"]/span/text()')
        comapny_url=html.xpath('//main//content//div[@class="title-box"]//span/a/@href')[0]
        comapny_name=html.xpath('//main//content//div[@class="title-box"]//span/a/text()')[0]
        job_intro_tag=html.xpath('//main//content//section[@class="job-intro-container"]//ul/li/text()')
        job_intro_content=html.xpath('//main//content//dd[@data-selector="job-intro-content"]//text()')[0]
        company_intro=html.xpath('//main//content//section[@class="company-intro-container"]//div[@class="inner ellipsis-3"]/text()')[0]
        company_label=html.xpath('//main//content//section[@class="company-intro-container"]//div[@class="inner ellipsis-3"]/text()')
        
        print(job_title)
        print(job_salary)
        print(job_properties)
        print(comapny_url)
        print(comapny_name)
        print(job_intro_tag)
        print(job_intro_content)
        print(company_intro)
    except IndexError as e:
        # print(e.args)
        web_title=html.xpath('//head/title/text()')
        print(web_title)
    # job=html.xpath('//div[@class="job-detail-box"]')
    # job_title=job.xpath('//div[@class="ellipsis-1"]/@title')
    # print(job_title)
    # print(html.xpath('//div[@class="job-detail-box"]//div[@class="ellipsis-1"]/@title'))
    # print(html.xpath('//div[@class="job-detail-box"]//span[@class="ellipsis-1"]/text()'))
    # print(html.xpath('//div[@class="job-detail-box"]//span[@class="job-salary"]/text()'))
    # print(html.xpath('//div[@class="job-detail-box"]//span[@class="company-name ellipsis-1"]/text()'))

def bad_web_content(content):
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
        company_jobs_href='https://www.liepin.com/company-jobs/'+str(company_id)
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
    # print(RecruitItem)
    # print(RecruitItemName)
    # print(RecruitItemSalary)
    # print(RecruitItemInfoBox)
    # print(RecruitItemLabelBox)
    # print(type(BusinessRegisterContentItem))
    print(BusinessRegisterContentItem)
    # # print(CommonHotLinksContentHref)
    # # print(CommonHotLinksContentTitle)
    # print(CommonHotLinks_Dicts)
    # quit()
    try:
        
        #对现存的部分网页TXT中的信息录入做判断,信息不对称时SQL不要用REPLACE语句
        if db.query_existance('LiePinCompanyInfo','company_id',company_id):
            db.update_companyinfo(company_id,company_location,company_point,company_full_name,BusinessRegisterContentItem)
        else:
            company_num=str(int(company_num)+1)
            id=company_num
            company_href='https://www.liepin.com/company/'+str(company_id)+'/'
            db.insert_basic_companyinfo(id,company_name,company_id,company_href,company_jobs_href,company_full_name,company_location,company_point,BusinessRegisterContentItem)
        # db.update_companyinfo(company_id,company_location,company_point,company_full_name,BusinessRegisterContentItem)
    except UnboundLocalError as e:
        if "local variable 'company_id' referenced before assignment" in e.args:
            pass
    CommonHotLinksContentHref=html.xpath('//div[@class="common-hot-links-content"]/a/@href')
    CommonHotLinksContentTitle=html.xpath('//div[@class="common-hot-links-content"]/a/@title')
    CommonHotLinks_Dict=dict(zip(CommonHotLinksContentTitle,CommonHotLinksContentHref))
    CommonHotLinks_Dicts={}
    for i in CommonHotLinks_Dict:
        if 'city-' not in CommonHotLinks_Dict[i] and '/company/' in CommonHotLinks_Dict[i]:
            CommonHotLinks_Dicts[i]=CommonHotLinks_Dict[i]
            company_num=str(int(company_num)+1)
            id=company_num
            company_name=i
            company_href=CommonHotLinks_Dict[i]
            new_company_id=CommonHotLinks_Dict[i].split('/')[-2]
            if new_company_id==company_id:
                continue
            company_jobs_href='https://www.liepin.com/company-jobs/'+str(new_company_id)
            jobs_href_accessed='False'
            mtime=time.strftime('%Y-%m-%d %H:%M:%S')
            print(f"插入{i,CommonHotLinks_Dict[i]}")
            db.insert_hotlinks(id,company_name,company_href,new_company_id,company_jobs_href,jobs_href_accessed,mtime)
    config.set('config','company_num',company_num)
    config.write(open('config.ini','w'))
    
    db.close()
    
 
if __name__ == '__main__':
    """抓取首页"""
    # main()

    """抓取现有TXT"""
    company_list=[i for i in os.listdir(os.path.join(os.path.abspath(''),'TXT')) if ('company' in i and 'job' not in i)]
    for i in company_list:
        company_info_content=open(os.path.join(os.path.abspath(''),'TXT',i),'r',encoding='utf-8').read()
        print(f"提取{i}")
        bad_web_content(company_info_content)

    # second(test_txt_2)
    # bad_web_content(test_txt_3)

    # for i in uncraweled_company_href_list:
    #     second(url_python_request(i))
    #     break

    