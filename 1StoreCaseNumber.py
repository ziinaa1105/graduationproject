# 판례 목록조회 API를 통해서 판례 일련번호 가져오기

import pandas as pd  
import xml.etree.ElementTree as ET  
from urllib.request import urlopen  
from tqdm import trange  


url = "https://www.law.go.kr/DRF/lawSearch.do?OC=tollin0116&target=prec&type=XML"
response = urlopen(url).read()
# XML 데이터 파싱해서 ElementTree 객체로 만들기
xmlresult = ET.fromstring(response)  

# 검색 결과의 총 count
totalCnt = int(xmlresult.find('totalCnt').text)

page = 1  
case_numbers = []

for i in trange(int(totalCnt / 20)):  
    try:
        items = xmlresult[5:]
    except:
        break
        

    for node in items:
        판례일련번호 = node.find('판례일련번호').text
        case_numbers.append(판례일련번호)
        
    page += 1
    
    url = "https://www.law.go.kr/DRF/lawSearch.do?OC=tollin0116&target=prec&type=XML&page={}".format(page)
    response = urlopen(url).read()
    xmlresult = ET.fromstring(response)  # 다음 페이지의 XML 데이터 가져와 파싱


with open("case_numbers.txt", "w") as file:
    for case_number in case_numbers:
        file.write("%s\n" % case_number)