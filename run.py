import requests
import re
import math
import os
from multiprocessing.dummy import Pool #multi thread
import pandas #range date


def download_date(date):
    MYDIR = ("FIX")
    CHECK_FOLDER = os.path.isdir(MYDIR)
    # If folder doesn't exist, then create it.
    if not CHECK_FOLDER:
        os.makedirs(MYDIR,exist_ok=True)
        # print("created folder : ", MYDIR)
    print('start download '+date)
    def count_page(date):
        ## added user agent to avoid cloudflare captcha
        try:
            url = 'https://www.cubdomain.com/domains-registered-by-date/'+date+'/1'
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36 OPR/90.0.4480.100'}
            response = requests.get(url,headers=headers)
            html = response.content.decode('utf-8')
        except:
            print('error requests count page, open log')
            open(MYDIR+'/logs_error.txt','a').write(date+' : count_page requests error (maybe internet blocked)\n')
            return None
            pass
        try:
            ## count total page from total domain list, each page estimated has 5000 domain list
            domain_count = re.search(r':</strong> (.*?)</li>', html).group(1)
            page_count = float(domain_count)/5000
            page_count = int(math.ceil(page_count))
            return page_count
        except:
            print('error count page, open log')
            open(MYDIR+'/logs_error.txt','a').write(date+' : count_page error (maybe 404 not found)\n')
            pass
    
    def save_domain(url):
        # url = 'https://www.cubdomain.com/domains-registered-by-date/'+date+'/'+page
        try:
            date=url.split('/')[4].strip()
            page=url.split('/')[5].strip()
            year=date.split('-')[0].strip()
            month=date.split('-')[1].strip()
            
            if not os.path.isdir(MYDIR+"/"+year+"/"+month):
                os.makedirs(MYDIR+"/"+year+"/"+month,exist_ok=True)
                # print("created folder : ", MYDIR+"/"+year+"/"+month)
            
            
            
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36 OPR/90.0.4480.100'}
            response = requests.get(url,headers=headers)
            html = response.content.decode('utf-8')
            domain_list = re.findall('<a href="https://www.cubdomain.com/site/(.*?)">', html)
            for items in domain_list:
                    open(MYDIR+"/"+year+"/"+month+'/'+date+'.tmp','a').write('http://'+items+'\n')
            print('Date : '+date+' Page : '+page+' Downloaded : '+str(len(domain_list))+'')
        except:
            print('error save domain, open log')
            open(MYDIR+'/logs_error.txt','a').write(url+' : save_domain error\n')
            pass
        
    page=count_page(date)
    if page is not None:
        try:
            i_i=[]
            sites = [ i_i.append('https://www.cubdomain.com/domains-registered-by-date/'+date+'/'+str(i)+'/') for i in range(1,count_page(date)+1) ]
            zm = Pool(page)
            zm.map(save_domain, i_i)
            zm.close()
            zm.join()
        except:
            print('error create pool, open log')
            open(MYDIR+'/logs_error.txt','a').write('date : '+str(date)+' page total '+str(page)+' : create pool error\n')
            pass
    

date1 = '2020-09-26'
date2 = '2020-09-26'
# download_date(date1)

dc=[d.strftime('%Y-%m-%d') for d in pandas.date_range(date1,date2)]
zm = Pool(1)
zm.map(download_date, dc)
zm.close()
zm.join()
