import requests,pymysql
from fake_user_agent.main import user_agent
from lxml import etree

class main:
    ua = user_agent()
    url = 'https://proxy.seofangfa.com/'
    headers = {
        'User-Agen': ua
    }
    varlist_ip = []
    varlist_ports = []
    res = requests.get(url, headers=headers)

    def __init__(self):
        if self.res.status_code == 200:
            if self.getip():
                if self.write_to_mysql():
                    print('写入数据成功')
                else:
                    print('写入数据失败')
            else:
                print('获取数据失败')
        else:
            print('请求数据失败')

    def getip(self):
        try:
            response = self.res.content.decode('utf-8')
            self.res_html = etree.HTML(response)
            res_html = etree.HTML(response)
            ips = res_html.xpath('//table[@class="table"]//tr/td[1]/text()')[1:]
            ports = res_html.xpath('//table[@class="table"]//tr/td[2]/text()')[1:]

            for i in range(0,len(ips)):
                ip = ips[i]
                port = ports[i]

                self.varlist_ip.append(ip)
                self.varlist_ports.append(port)

            return True
        except:
            return False


    def write_to_mysql(self):
        conn = pymysql.connect(host='10.195.43.208',
                                     port=3306,
                                     user='root',
                                     password='密码',
                                     db='账户名',
                                     charset='utf8mb4',
                                     # database ='get_ip'
                                    )
        cursor = conn.cursor()

        try:
            for i in range(0,len(self.varlist_ports)):
                # print(self.varlist_ports[i])
                # 存入数据到数据库中
                cursor.execute("insert into get_ip(ip,port) values ('%s','%s');" % (self.varlist_ip[i],self.varlist_ports[i]))
                conn.commit()
            return True
        except:
                # cursor.rollback()
            return False
        cursor.close()
        conn.close()

main()

