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
        # 从表 sexpic_url_record 查询某某列column是否存在值value
        # sql="select * from sexpic_url_record limit 1"
        # sexpic_url_record
        sql="""select * from {} where {}='{}' limit 1;""".format(table,column,value)
        
        # print(sql)
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

        # finally:
            # self._db.close()
        

    def get_sexurl(self):
        # 从表 sex_url_record 中取100个未爬取过的url进行爬取
        # return:是一个列表，中的每一项都是一个字典
        sql="""select * from sex_url_record 
        where crawl_status='False' 
        and live_status!='True' 
        and exception_status !='True'
        and jpg_not_found!='True'
        and jpg_not_right!='True'
        limit 10"""#live_status='True' 说明已经爬取过了并确定该网站曾经活着
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

    def get_url(self):
        # 从表 sex_url_record 中取100个未爬取过的url进行爬取
        # return:是一个列表，中的每一项都是一个字典
        sql="""select * from DomainName 
        where title like '%音乐%'
        limit 10"""#live_status='True' 说明已经爬取过了并确定该网站曾经活着
        # 
        # and exception_status !='True'
        # and domain_not_found!='True'

        try:
            self._cursor.execute(sql)
            result=self._cursor.fetchall()
            self._db.commit()
        except Exception as e:
            print(e.args)
            self._db.rollback()
        finally:
            return result
            
    def insert_appinfo(self,app_chinese_name,app_type,app_pkgname,app_detail_url,app_samekind_ranking,app_thumbnail_url,app_type_num):
        sql="""insert into XIAOMI_APPSTORE (app_chinese_name,app_type,app_pkgname,app_detail_url,app_samekind_ranking,app_thumbnail_url,app_type_num,update_time) VALUES ('{}', '{}', '{}','{}','{}', '{}','{}','{}')""".format(app_chinese_name,app_type,app_pkgname,app_detail_url,app_samekind_ranking,app_thumbnail_url,app_type_num,time.strftime('%Y-%m-%d %H:%M:%S'))
        try:
            self._cursor.execute(sql)
            self._db.commit()
            return (app_chinese_name,'插入成功!')
        except Exception as e:
            print(e.args)
            self._db.rollback()
        # finally:
            # self._db.close()

    def insert_similarweb_appinfo(self,Name,Publisher,AppIndex,AppId,AppIndexChange,StoreRank,StoreRankChange,Url,IconUrl,PopupIconUrl,Price,StorePageUrl,Category,CategoryUrl,Filter_Store,Filter_Device,Filter_Country,Filter_Category,Filter_Mode,Filter_Platform,Filter_SortBy,Filter_Uri,has_data):
        sql="""insert into SimilarWeb (Name,Publisher,AppIndex,AppId,AppIndexChange,StoreRank,StoreRankChange,Url,IconUrl,PopupIconUrl,Price,StorePageUrl,Category,CategoryUrl,Filter_Store,Filter_Device,Filter_Country,Filter_Category,Filter_Mode,Filter_Platform,Filter_SortBy,Filter_Uri,has_data,update_time) VALUES ('{}', '{}', '{}','{}','{}', '{}','{}','{}','{}', '{}', '{}','{}','{}', '{}','{}','{}','{}', '{}', '{}','{}','{}', '{}','{}','{}')""".format(Name,Publisher,AppIndex,AppId,AppIndexChange,StoreRank,StoreRankChange,Url,IconUrl,PopupIconUrl,Price,StorePageUrl,Category,CategoryUrl,Filter_Store,Filter_Device,Filter_Country,Filter_Category,Filter_Mode,Filter_Platform,Filter_SortBy,Filter_Uri,has_data,time.strftime('%Y-%m-%d %H:%M:%S'))
        try:
            self._cursor.execute(sql)
            self._db.commit()
            return (Name,'插入成功!')
        except Exception as e:
            print(e.args)
            self._db.rollback()
    
            
    def update_sexurl_status(self,url,crawl_status,source_url,pic_num,live_status,exception_status,jpg_not_found,jpg_not_right):
    #update_sexurl_status(url,crawl_status,source_url,pic_num,live_status,exception_status,jpg_not_found,jpg_not_right)
        # pass
        sql="""update sex_url_record 
            set crawl_status='{}',
            source_url='{}',
            pic_num='{}',
            live_status='{}',
            exception_status='{}',
            jpg_not_found='{}',
            jpg_not_right='{}',
            request_time='{}'
            WHERE url='{}'""".format(crawl_status,source_url,pic_num,live_status,exception_status,jpg_not_found,jpg_not_right,time.strftime('%Y-%m-%d %H:%M:%S'),url)
        try:
            self._cursor.execute(sql)
            self._db.commit()
            return (url,'状态更新成功!')
        except Exception as e:
            print(e.args)
            self._db.rollback()
        # finally:
            # self._db.close()

    def update_domain_status(self,full_domain_name,title,keywords,description,
        crawl_status,live_status,exception_status,domain_not_found,domain_type,source):
        sql="""update DomainName 
            set title='{}',
            keywords='{}',
            description='{}',
            crawl_status='{}',
            live_status='{}',
            exception_status='{}',
            domain_not_found='{}',
            domain_type='{}',
            source='{}',
            request_time='{}'
            WHERE full_domain_name='{}'""".format(title,keywords,description,crawl_status,live_status,exception_status,domain_not_found,domain_type,source,time.strftime('%Y-%m-%d %H:%M:%S'),full_domain_name)
        try:
            self._cursor.execute(sql)
            self._db.commit()
            return (full_domain_name,'状态更新成功!')
        except Exception as e:
            print(e.args)
            self._db.rollback()
        # finally:
            # self._db.close()
            
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
    print(db.get_url())
    db.close()