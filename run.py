import requests
import re
import math
import os
from multiprocessing.dummy import Pool #multi thread
import pandas #range date


def download_date(date):
    MYDIR = ("result")
    CHECK_FOLDER = os.path.isdir(MYDIR)
    # If folder doesn't exist, then create it.
    if not CHECK_FOLDER:
        os.makedirs(MYDIR)
        print("created folder : ", MYDIR)
    print('start download '+date)
    def count_page(date):
        ## added user agent to avoid cloudflare captcha
        url = 'https://www.cubdomain.com/domains-registered-by-date/'+date+'/1'
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36 OPR/90.0.4480.100'}
        response = requests.get(url,headers=headers)
        html = response.content.decode('utf-8')
        
        
        ## count total page from total domain list, each page estimated has 5000 domain list
        domain_count = re.search(r':</strong> (.*?)</li>', html).group(1)
        page_count = float(domain_count)/5000
        page_count = int(math.ceil(page_count))
        return page_count
    
    def save_domain(url):
        # url = 'https://www.cubdomain.com/domains-registered-by-date/'+date+'/'+page
        date=url.split('/')[4].strip()
        page=url.split('/')[5].strip()
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36 OPR/90.0.4480.100'}
        response = requests.get(url,headers=headers)
        html = response.content.decode('utf-8')
        domain_list = re.findall('<a href="https://www.cubdomain.com/site/(.*?)">', html)
        for items in domain_list:
                open(MYDIR+'/'+date+'.tmp','a').write('http://'+items+'\n')
        print('Date : '+date+' Page : '+page+' Downloaded : '+str(len(domain_list))+'')
    i_i=[]
    sites = [ i_i.append('https://www.cubdomain.com/domains-registered-by-date/'+date+'/'+str(i)+'/') for i in range(1,count_page(date)+1) ]
    zm = Pool()
    zm.map(save_domain, i_i)
# download_date(date)


#SETTING DATE
date1 = '2022-08-12'
date2 = '2022-09-12'

dc=[d.strftime('%Y-%m-%d') for d in pandas.date_range(date1,date2)]
# print(dc)
# exit()
zm = Pool()
zm.map(download_date, dc)



for file in os.listdir("result"):
    if file.endswith(".tmp"):
        print(os.path.join("result", file))
        pattern = re.compile("^(.*)(\..*$)")
        for i, line in enumerate(open(os.path.join("result", file))):
            for match in re.finditer(pattern, line):
                # print('Found on line %s: %s' % (i+1, match.group(2)))
                file = open("result/domain_"+match.group(2)+".domain","a").write(line)

for file in os.listdir("result"):
    if file.endswith(".domain"):
        total = os.popen("cat "+os.path.join("result", file)+" | wc -l").read().strip()
        if int(total)>10000:
            print(file+' ok' + total)
        else:
            os.popen("cat "+os.path.join("result", file)+">>'result/domain_.other.domain'").read().strip()
            os.popen("rm "+os.path.join("result", file)).read().strip()
        
                
