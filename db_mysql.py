import os
import time
import pymysql
from pymysql.converters import escape_string
from settings import *#HOST,USER,PORT,PASSWORD,DATABASE,CHARSET
import logging
logging.captureWarnings(True)

class MysqlClient(object):
    ### sex_url_record
    # url/crawl_status/source_url/pic_num/live_status/exception_status/jpg_not_found/jpg_not_right/request_time 
    # from pymysql.converters import escape_string
    def __init__(self,host=MySQL_HOST,
                    port=MySQL_PORT,
                    user=MySQL_USER,
                    password=MySQL_PASSWORD,
                    database=MySQL_DATABASE,
                    charset=MySQL_CHARSET):
        if MySQL_PASSWORD:
            self._db=pymysql.connect(host=host,user=user,port=port,password=password,database=database,charset=charset,cursorclass=pymysql.cursors.SSDictCursor)
        else:
            self._db=pymysql.connect(host=host,user=user,port=port,database=database,charset=charset,cursorclass=pymysql.cursors.SSDictCursor)

        self._cursor=self._db.cursor()
        
    def query_existance(self,table,column,value):
        # 从表 LiePinCompanyInfo 查询某某列column是否存在值value
        sql="""SELECT * FROM {} WHERE {}='{}' LIMIT 1;""".format(table,column,value)
        try:
            self._cursor.execute(sql)
            result=self._cursor.fetchone()
            # print(result)
            self._db.commit()
            if result:
                return True
            else:
                return False
        except Exception as e:
            print(e.args)
            self._db.rollback()

    def query_company_fullname_existance(self,table,company_id):
        sql=f"""SELECT * FROM {table} WHERE company_id='{company_id}' LIMIT 1;"""
        try:
            self._cursor.execute(sql)
            result=self._cursor.fetchone()
            # print(result)
            self._db.commit()
            if result:
                return result['company_full_name']
            else:
                return False
        except Exception as e:
            print(e.args)
            self._db.rollback()

    def get_companies_jobs_unaccessed(self):
        # 从表 LiePinCompanyInfo 中取10个未爬取过的url进行爬取
        # return:是一个列表，中的每一项都是一个字典
        sql="""SELECT * FROM LiePinCompanyInfo 
        WHERE jobs_href_accessed='False' 
        LIMIT 10"""#live_status='True' 说明已经爬取过了并确定该网站曾经活着
        try:
            self._cursor.execute(sql)
            result=self._cursor.fetchall()
            self._db.commit()
        except Exception as e:
            print(e.args)
            self._db.rollback()
        finally:
            return result
            # self._db.close()

    def get_companies_no_fullname(self):
        # 从表 LiePinCompanyInfo 中取10个未爬取过的url进行爬取
        # return:是一个列表，中的每一项都是一个字典
        sql="""SELECT * FROM LiePinCompanyInfo 
        WHERE (company_full_name='' or company_full_name is NULL or jobs_href_accessed='False')
        LIMIT 1"""
        try:
            self._cursor.execute(sql)
            result=self._cursor.fetchall()
            self._db.commit()
        except Exception as e:
            print(e.args)
            self._db.rollback()
        finally:
            return result

    def get_jobs_no_detail(self):
        # 从表 LiePinCompanyInfo 中取10个未爬取过的url进行爬取
        # return:是一个列表，中的每一项都是一个字典
        sql="""SELECT * FROM LiePinJobsInfo
        WHERE (job_intro_content='' or job_intro_content is NULL or job_href_accessed='False')
        LIMIT 1"""#live_status='True' 说明已经爬取过了并确定该网站曾经活着
        try:
            self._cursor.execute(sql)
            result=self._cursor.fetchall()
            self._db.commit()
        except Exception as e:
            print(e.args)
            self._db.rollback()
        finally:
            return result

    def get_url(self):
        # 从表 sex_url_record 中取100个未爬取过的url进行爬取
        # return:是一个列表，中的每一项都是一个字典
        sql="""SELECT * FROM LiePinCompanyInfo 
        WHERE company_full_name LIKE '%音乐%'
        LIMIT 10"""#live_status='True' 说明已经爬取过了并确定该网站曾经活着

        try:
            self._cursor.execute(sql)
            result=self._cursor.fetchall()
            self._db.commit()
        except Exception as e:
            print(e.args)
            self._db.rollback()
        finally:
            return result
         
    def insert_basic_companyinfo(self,id,company_name,company_id,company_href,company_jobs_href,company_full_name,company_location,company_point,BusinessRegisterContentItem):
        sql=f"""INSERT INTO LiePinCompanyInfo (id,company_name,company_id,company_href,company_jobs_href,jobs_href_accessed,company_full_name,company_location,company_point,BusinessRegisterContentItem,ctime,mtime) VALUES ('{id}','{company_name}','{company_id}','{company_href}','{company_jobs_href}','{"False"}','{company_full_name}','{company_location}','{escape_string(company_point)}','{escape_string(BusinessRegisterContentItem)}','{time.strftime('%Y-%m-%d %H:%M:%S')}','{time.strftime('%Y-%m-%d %H:%M:%S')}')"""
        try:
            self._cursor.execute(sql)
            self._db.commit()
            return (company_id,'插入成功!')
        except Exception as e:
            print('2',e.args)
            self._db.rollback()

    def insert_companyinfo(self,id,company_name,company_href,company_id,company_jobs_href,jobs_href_accessed,company_full_name,company_location,BusinessRegisterContentItem,mtime):
        sql=f"""REPLACE INTO LiePinCompanyInfo (id,company_name,company_href,company_id,company_jobs_href,jobs_href_accessed,company_full_name,company_location,BusinessRegisterContentItem,ctime,mtime) VALUES ('{id}','{company_name}', '{company_href}', '{company_id}','{company_jobs_href}','{jobs_href_accessed}', '{company_full_name}','{company_location}','{escape_string(BusinessRegisterContentItem)}','{time.strftime('%Y-%m-%d %H:%M:%S')}','{mtime}')"""
        try:
            self._cursor.execute(sql)
            self._db.commit()
            return (company_name,'插入成功!')
        except Exception as e:
            print(e.args)
            self._db.rollback()

    def insert_hotlinks(self,id,company_name,company_href,company_id,company_jobs_href,jobs_href_accessed,mtime):
        sql=f"""INSERT INTO LiePinCompanyInfo (id,company_name,company_href,company_id,company_jobs_href,jobs_href_accessed,ctime,mtime) VALUES ('{id}','{company_name}', '{company_href}', '{company_id}','{company_jobs_href}','{jobs_href_accessed}','{time.strftime('%Y-%m-%d %H:%M:%S')}','{mtime}')"""
        try:
            self._cursor.execute(sql)
            self._db.commit()
            return (company_name,'插入成功!')
        except Exception as e:
            print(e.args)
            self._db.rollback()

    def update_companyinfo(self,company_id,company_location,company_point,company_full_name,BusinessRegisterContentItem):
        sql=f"""UPDATE LiePinCompanyInfo 
            SET company_location='{company_location}',
            company_point='{escape_string(company_point)}',
            company_full_name='{escape_string(company_full_name)}',
            BusinessRegisterContentItem='{escape_string(BusinessRegisterContentItem)}',
            mtime='{time.strftime('%Y-%m-%d %H:%M:%S')}'
            WHERE company_id='{company_id}'"""
        try:
            self._cursor.execute(sql)
            self._db.commit()
            return (company_id,'状态更新成功!')
        except Exception as e:
            print(e.args)
            self._db.rollback()
        # finally:
            # self._db.close()


    def update_company_jobs_num(self,company_id,jobs_num):
        sql=f"""UPDATE LiePinCompanyInfo
            SET jobs_num='{jobs_num}',
            mtime='{time.strftime('%Y-%m-%d %H:%M:%S')}'
            WHERE company_id='{company_id}'"""
        try:
            self._cursor.execute(sql)
            self._db.commit()
            return (company_id,'状态更新成功!')
        except Exception as e:
            print(e.args)
            self._db.rollback()

    def update_fullname2None(self,company_id):
        sql=f"""UPDATE LiePinCompanyInfo 
            SET company_full_name='{escape_string('无')}',
            mtime='{time.strftime('%Y-%m-%d %H:%M:%S')}'
            WHERE company_id='{company_id}'"""
        try:
            self._cursor.execute(sql)
            self._db.commit()
            return (company_id,'状态更新成功!')
        except Exception as e:
            print(e.args)
            self._db.rollback()

    # def update_four_job_column(company_id,company_full_name,company_location,company_point,BusinessRegisterContentItem):
    #     sql=f"""UPDATE LiePinCompanyInfo
    #         SET company_full_name='{escape_string(company_full_name)}',
    #         company_location='{company_location}',
    #         company_point='{escape_string(company_point)}',
    #         WHERE company_id='{company_id}'"""

    def update_company_href_status(self,company_id):#,job_href_accessed#将job_href_accessed设为True -->访问过了
        sql=f"""UPDATE LiePinCompanyInfo 
            SET jobs_href_accessed='{'True'}',
            mtime='{time.strftime('%Y-%m-%d %H:%M:%S')}'
            WHERE company_id='{company_id}'"""
        try:
            self._cursor.execute(sql)
            self._db.commit()
            return (company_id,'状态更新成功!')
        except Exception as e:
            print(e.args)
            self._db.rollback()

    def update_company_intro(self,company_id,company_intro):
        sql=f"""UPDATE LiePinCompanyInfo 
            SET company_intro='{escape_string(company_intro)}',
            mtime='{time.strftime('%Y-%m-%d %H:%M:%S')}'
            WHERE company_id='{company_id}'"""
        try:
            self._cursor.execute(sql)
            self._db.commit()
            return (company_id,'状态更新成功!')
        except Exception as e:
            print(e.args)
            self._db.rollback()


    # def update_domain_status(self,full_domain_name,title,keywords,description,
    #     crawl_status,live_status,exception_status,domain_not_found,domain_type,source):
    #     sql="""UPDATE DomainName 
    #         SET title='{}',
    #         keywords='{}',
    #         description='{}',
    #         crawl_status='{}',
    #         live_status='{}',
    #         exception_status='{}',
    #         domain_not_found='{}',
    #         domain_type='{}',
    #         source='{}',
    #         request_time='{}'
    #         WHERE full_domain_name='{}'""".format(title,keywords,description,crawl_status,live_status,exception_status,domain_not_found,domain_type,source,time.strftime('%Y-%m-%d %H:%M:%S'),full_domain_name)
    #     try:
    #         self._cursor.execute(sql)
    #         self._db.commit()
    #         return (full_domain_name,'状态更新成功!')
    #     except Exception as e:
    #         print(e.args)
    #         self._db.rollback()

    def insert_jobs_info(self,job_id,job_title,job_region,job_salary,job_tags,company_name,company_id,job_info_href,job_href_accessed):
        sql=f"""INSERT INTO LiePinJobsInfo (job_id,job_title,job_region,job_salary,job_tags,company_name,company_id,job_info_href,job_href_accessed,ctime,mtime) VALUES ('{job_id}','{escape_string(job_title)}','{escape_string(job_region)}','{job_salary}','{escape_string(job_tags)}','{escape_string(company_name)}','{company_id}','{job_info_href}','{job_href_accessed}','{time.strftime('%Y-%m-%d %H:%M:%S')}','{time.strftime('%Y-%m-%d %H:%M:%S')}')"""
        try:
            self._cursor.execute(sql)
            self._db.commit()
            return (job_title,'插入成功!')
        except Exception as e:
            print(e.args)
            self._db.rollback()
            
    def update_company_jobs_intro(self,job_id,job_tags,job_intro_content):
        sql=f"""UPDATE LiePinJobsInfo 
            SET job_tags='{escape_string(job_tags)}',
            job_intro_content='{escape_string(job_intro_content)}',
            mtime='{time.strftime('%Y-%m-%d %H:%M:%S')}'
            WHERE job_id='{job_id}'"""
        try:
            self._cursor.execute(sql)
            self._db.commit()
            return (job_id,'状态更新成功!')
        except Exception as e:
            print(e.args)
            self._db.rollback()

    def update_job_href_status(self,job_id):
        sql=f"""UPDATE LiePinJobsInfo
            SET job_href_accessed='{'True'}',
            mtime='{time.strftime('%Y-%m-%d %H:%M:%S')}'
            WHERE job_id='{job_id}'
            """
        try:
            self._cursor.execute(sql)
            self._db.commit()
            return (job_id,'状态更新成功!')
        except Exception as e:
            print(e.args)
            self._db.rollback()

    def close(self):
        self._db.close()
        
    def test_sentence(self):
        sql="""select * from sexpic_url_record limit 10"""
        try:
            self._cursor.execute(sql)
            result=self._cursor.fetchall()
            self._db.commit()
        except Exception as e:
            print(e.args)
            self._db.rollback()
        finally:
            return result
            # self._db.close()
            
    def db_report(self):
        """
        N天内记录
        WHERE TO_DAYS(NOW()) - TO_DAYS(时间字段) <= N
        今天的记录
        where date(时间字段)=date(now()) 或 where to_days(时间字段) = to_days(now());
        查询一周：
        select * from table   where DATE_SUB(CURDATE(), INTERVAL 7 DAY) <= date(column_time);
        查询一个月：
        select * from table where DATE_SUB(CURDATE(), INTERVAL INTERVAL 1 MONTH) <= date(column_time);
        """
        num=input('请问想获取几天内的数据？')
        sql="""select * from sex_url_record where DATE_SUB(CURDATE(), INTERVAL {} DAY) <= date(request_time)""".format(num)
        # sql="""select * from sex_url_record where day(request_time)=day(curdate()) """
        try:
            self._cursor.execute(sql)
            result=self._cursor.fetchall()
            self._db.commit()
        except Exception as e:
            print(e.args)
            self._db.rollback()
        finally:
            if int(num)==1:
                return '此前24h访问网站{}个；'.format(len(result))
            else:
                return '此前{}d访问网站{}个；'.format(num,len(result))

    def db_report_picnum(self):
        sql="""select * from sex_url_record where pic_num!='0' and DATE_SUB(CURDATE(), INTERVAL 1 DAY) <= date(request_time)"""
        try:
            self._cursor.execute(sql)
            result=self._cursor.fetchall()
            self._db.commit()
            pic_count=0
            for i in result:
                # print(i['pic_num'])
                pic_count+=i['pic_num']
            # print(pic_count)
        except Exception as e:
            pic_count=None
            print(e.args)
            self._db.rollback()
        finally:
            return '此前24h数据库新增图片链接{}个'.format(pic_count)
        # CURRENT_TIME=time.time()
        # print(CURRENT_TIME)
        
if __name__=='__main__':
    ##创建数据库实例
    db=MysqlClient()#HOST,USER,PORT,PASSWORD,DATABASE,CHARSET
    #调用数据库对象的方法
    # print(db.query_existance('crawl_status','True'))
    # print(db.test_sentence())
    # print(db.get_sexurl()[0]['url'])
    # print(db.get_sexurl())
    # print(db.insert_picurl('a','b'))
    # print(db.query_existance('sexpic_url_record','picurl','bb'))
    # print(db.query_existance('LiePinCompanyInfo','company_id','95043'))
    # print(db.get_companies_no_fullname())
    # print(type(db.query_company_fullname_existance('LiePinCompanyInfo','10010647')))
    print(db.get_jobs_no_detail())
    db.close()