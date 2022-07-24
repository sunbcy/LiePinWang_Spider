import os
from lxml  import etree 

CURRENT_PATH=os.path.abspath('')
test_txt=open(r'C:\Users\Bcy\Desktop\猎聘网\TXT\www_liepin_com.txt','r',encoding='utf-8').read()
test_txt_2=open(r'C:\Users\Bcy\Desktop\猎聘网\TXT\www_liepin_comjob1948895625_shtml.txt','r',encoding='utf-8').read()
def main():
    html=etree.HTML(test_txt)
    title=html.xpath('head/title/text()')[0]
    print(html.xpath('//div[@class="header-title-item-text"]/text()'))
    #多属性匹配的写法
    print(html.xpath('//a[contains(@class,"header-title-item") or @class="header-title-item-active"]/@href'))
    #公司名字
    print(html.xpath('//a[@class="industry-content-comp-item"]/text()'))
    #公司href
    print(html.xpath('//a[@class="industry-content-comp-item"]/@href'))
    #获取公司在猎聘的id
    # liepin_company_id=href.split('company')[1].split('/')[1]

    #名企职位 12个
    print(html.xpath('//a[@class="home-comp-info"]/@href'))
    # print(html.xpath('head/title/text()')[0])

    print(html.xpath('//a[@class="hot-jobs-first-title"]/text()'))

    #二级热门职位
    hot_jobs={}
    print(html.xpath('//a[@class="hot-jobs-second-title"]/text()'))

    #三级热门职位
    print(html.xpath('//a[@class="hot-jobs-three-title"]/@href'))
    print(html.xpath('//a[@class="hot-jobs-three-title"]/text()'))

def second():
    html=etree.HTML(test_txt_2)
    # print(html.xpath('//span[@class="job-salary"]/text()'))

    # job_url=
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
    # job=html.xpath('//div[@class="job-detail-box"]')
    # job_title=job.xpath('//div[@class="ellipsis-1"]/@title')
    # print(job_title)
    # print(html.xpath('//div[@class="job-detail-box"]//div[@class="ellipsis-1"]/@title'))
    # print(html.xpath('//div[@class="job-detail-box"]//span[@class="ellipsis-1"]/text()'))
    # print(html.xpath('//div[@class="job-detail-box"]//span[@class="job-salary"]/text()'))
    # print(html.xpath('//div[@class="job-detail-box"]//span[@class="company-name ellipsis-1"]/text()'))
if __name__ == '__main__':
	# main()
    second() 