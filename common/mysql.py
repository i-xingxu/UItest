# coding=utf-8
import pymysql
from common import conf


class Mysql():
    '''
    Mysql类
    '''

    def connect_mysql(self):
        '''
        连接数据库方法,传入配置文件地址，获取连接数据库信息，返回游标对象
        :param mysqinfo: 数据库连接信息
        :return:
        '''
        cf=conf.Conf()
        mysqlInfo=cf.get_conf_data("SqlInfo")
        try:
            db = pymysql.connect(host=mysqlInfo["ip"], port=int(mysqlInfo["port"]), user=mysqlInfo["usr"],
                                 passwd=mysqlInfo["password"], db=mysqlInfo["database"], charset='utf8')
            self.cur = db.cursor()
            print("成功连接%s数据库" % mysqlInfo["ip"])

        except Exception as e:
            print("数据库连接失败！")
            print(e)

    def close_connect(self):
        '''
        关闭数据库连接
        :return:
        '''
        try:
            self.cur.close()
            print("成功关闭连接！")
        except Exception as e:
            print(e)

    def get_mysql_data(self, casename):
        '''
        获取数据库数据
        :return:
        '''
        # select id from case_name where case_name=casename
        sql = "select id from case_name where case_name=\'" + casename + "\'"
        try:
            self.cur.execute(sql)
            caseId = self.cur.fetchone()[0]
            dataSql = "select * from test_data where cid=" + str(caseId)
            try:
                self.cur.execute(dataSql)
                data = self.cur.fetchall()
                caseDatas = []
                for d in data:
                    caseData = []
                    for i in range(0, len((d[2]).split(";"))):
                        caseData.append((d[2]).split(";")[i])
                    caseData.append(d[3])
                    caseDatas.append(caseData)
                return caseDatas
            except Exception as a:
                print(a)
                print("执行sql语句%s出错" % dataSql)
        except Exception as e:
            print(e)
            print("执行sql语句%s出错" % sql)


# mysqlinfo = {"ip": "192.168.2.157", "port": "3306", "usr": "root", "password": "root", "database": "autotest"}
# m = Mysql()
# c = m.connect_mysql(mysqlinfo)
# data = m.get_mysql_data("退出")
# print(data)
# m.close_connect()
