#雙和醫院 covid-19 疫苗 爬蟲

import requests
from os import replace
from bs4 import BeautifulSoup
from datetime import datetime

ROOT_URL    = "https://www.shh.org.tw/page"
REG_URL     = "/ShhregVaccine.aspx"             #covid-19
REAL_URL    = ROOT_URL + REG_URL
TABLE_ID    = "ContentPlaceHolder1_gvShift"
result      = list()
HEADERS     = {
    'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    'accept-encoding': "gzip, deflate, br",
    'connection': "keep-alive",
    'dnt': "1",
    'user-agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.3325.146 Safari/537.36",
}

res = requests.get(REAL_URL, headers=HEADERS)
#print(REAL_URL)
html = res.content
soup = BeautifulSoup(html, 'html.parser')

gvshift = 1
search_week = (datetime.today().isoweekday()) 
#print(search_week)
while gvshift <= 3: 
    search_table_id = TABLE_ID + str(gvshift)
    table           = soup.find('table', {'id': search_table_id})
    #print(search_table_id)

    trs     = table.find_all('tr')
    rows    = list()
    for tr in trs:
        rows.append([td.text.replace('\n', '').replace('\xa0', '').strip() for td in tr.find_all('td')])
    #print(rows)
    

    hosp_name   = "衛生福利部雙和醫院(委託臺北醫學大學興建經營)"
    vaccine_type= "Moderna" #雙和醫院目前只打這種
    #reg_date    = "1100101"
    if gvshift == 1:
        time_part   = "上午"
    else:
        if gvshift == 2:
            time_part   ="下午"
        else:
            if gvshift == 3:
                time_part = "夜間"
    #amout       = "0"
    #crawl_date  = ""
    #comment     = "" 


    for y in range(len(rows)):
        if y >=1:
            for x in range(len(rows[y])):
                if ((x > 1) & (x >= search_week) ):
                    amout = 0
                    if ((rows[y][x] == '預約')):
                        #print(rows[y][x])
                        amout = amout + 1
                    reg_date    = str(int(rows[0][x][0:3]) + 1911) + "-" + rows[0][x][3:5] + "-" +rows[0][x][5:7]
                    crawl_date  = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
                    comment     = rows[y][0]
                    result.append([
                        hosp_name,
                        vaccine_type,
                        reg_date,  
                        time_part,
                        amout,
                        crawl_date,
                        comment]
                    )
    gvshift = gvshift +1
#print(result)
for i in range(len(result)):
    print(result[i])