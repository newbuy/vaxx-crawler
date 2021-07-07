#慈濟醫院 covid-19 疫苗 爬蟲

#from sys import displayhook
#from bs4.element import ResultSet
from bs4.element import NavigableString
import requests
from os import replace, spawnl
from bs4 import BeautifulSoup
from datetime import date, datetime
import re

ROOT_URL    = "https://reg-prod.tzuchi-healthcare.org.tw"
REG_URL     = "/tchw/HIS5OpdReg/OpdTimeShow?Pass=XD;0021"             #covid-19
REAL_URL    = ROOT_URL + REG_URL
TABLE_ID    = "MainContent_gvOpdList"
hosp_name   = "佛教慈濟醫療財團法人台北慈濟醫院"
vacc_type   = ""
reg_date    = ""
time_part   = ""
amount       = 0
crawl_date  = ""
comment     = "" 

HEADERS     = {
    'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    'accept-encoding': "gzip, deflate, br",
    'connection': "keep-alive",
    'dnt': "1",
    'user-agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.3325.146 Safari/537.36",
}

res = requests.get(REAL_URL, headers=HEADERS)
print ("REAL_URL = " + REAL_URL)
html = res.content
soup = BeautifulSoup(html, 'html.parser')
#table = soup.find('table', {'id':'MainContent_tblNote'}).find('span',{'id': 'MainContent_lblNote'}).find_all(text=True)
table = soup.find('table', {'id':'MainContent_tblNote'}).find('td').find_all(text=True)


#for i in table:print(i)
vaccs       = list()
temp_vaccs  = list()
for line in table:
    if line.strip() == 'AZ(AstraZeneca)疫苗':
        x=0
        vaccs.append(['AZ'])
    if line.strip() == '莫德納(Moderna)疫苗':
        x =1
        vaccs.append(['Moderna'])
    r = re.compile(r"((\d+\/\d).*.(上午|下午))")
    m = re.search(r, line)
    if m:
        temp_line = line.strip()
        temp_line = temp_line.replace('※'   ,'')
        temp_line = temp_line.replace('(一)' ,' ')
        temp_line = temp_line.replace('(二)' ,' ')
        temp_line = temp_line.replace('(三)' ,' ')
        temp_line = temp_line.replace('(四)' ,' ')
        temp_line = temp_line.replace('(五)' ,' ')
        temp_line = temp_line.replace('(六)' ,' ')
        temp_line = temp_line.replace('(日)' ,' ')
        temp_line = temp_line.replace('；'   ,'、')
        
        temp_line = temp_line.split('、')
        for i in range(len(temp_line)):
            if (temp_line[i] == '上午') | (temp_line[i] == '下午') | (temp_line[i] == '夜間'):
                temp_line[i] = temp_line[i-1].split(' ')[0] +  " " + temp_line[i]
        vaccs[x].extend(temp_line)
    
table = soup.find('table', {'id': TABLE_ID})
#print("TABLE_ID = " + TABLE_ID)
#print(table)

if table is not None:
    rows    = list()

    columns = [th.text.replace('\n', '') for th in table.find('tr').find_all('th')]
    print(columns)
    
    trs = table.find_all('tr')
    for tr in trs[1:]:
        x = 1
        tds         = tr.find_all('td')
        temp_year   = str(datetime.today().year)
        temp_month  = tds[0].text.replace('\n', '').split('月')[0]
        temp_day    = tds[0].text.split('月')[1].split('日')[0]
        reg_date    = temp_year + '/' + temp_month + '/' + temp_day
        for td in tds[1:]:
            time_part   = columns[x]
            comment     = ""
            amount      = 0
            vacc_type   = ""
            for vacc in vaccs:
                month_day_timepart = str(int(temp_month)) +'/' + str(int(temp_day)) + ' ' + time_part
                #print(month_day_timepart)
                if month_day_timepart in vacc:
                    if 'AZ' in vacc      : vacc_type = 'AZ'
                    if 'Moderna' in vacc : vacc_type = 'Moderna'
            for i in td:
                if ((type(i) == NavigableString) and (i.strip() !='')):amount = 0
                if i.name  == ('a')             :amount = 1
                if i.name  == ('span')          :comment= i.text.replace('COVID19疫苗接種','').replace('(',"").replace(')',"").strip()
                if i.name  == ('br'):
                    crawl_date  = datetime.now().strftime("%Y/%m/%d %H:%M:%S")    
                    rows.append([
                        hosp_name,  
                        vacc_type,
                        reg_date,
                        time_part,
                        amount,
                        crawl_date,
                        comment
                    ])
                    amount      = 0
                    comment     = ""
            x = x +1
for i in rows:print(i)