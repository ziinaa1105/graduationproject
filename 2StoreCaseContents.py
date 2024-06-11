# 판례목록조회API를 통해 획득한 case_numbers.txt를 이용하여
# 판례본문조회API로 판례 본문 가져오기

import requests
import json
from tqdm import tqdm
import xml.etree.ElementTree as ET

def store_caseinfo(case_number):
    url = f"http://www.law.go.kr/DRF/lawService.do?OC=tollin0116&target=prec&ID={case_number}&type=XML"
    response = requests.get(url)
    if response.status_code == 200:
        root = ET.fromstring(response.content)
        case_info = {
            "판례정보일련번호": root.findtext("판례정보일련번호"),
            "사건명": root.findtext("사건명"),
            "사건번호": root.findtext("사건번호"),
            "판시사항": root.findtext("판시사항"),
            "판결요지": root.findtext("판결요지"),
            "참조조문": root.findtext("참조조문"),
            "판례내용": root.findtext("판례내용")
        }
        return case_info
    else:
        print(f"Failed {case_number}:", response.status_code)
        return None

def create_json_file(case_numbers, output_file):
    case_json = {}
    for case_number in tqdm(case_numbers):
        case_info = store_caseinfo(case_number)
        if case_info:
            case_json[case_number] = case_info
    
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(case_json, file, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    
    with open("case_numbers.txt", "r") as file:
        case_numbers = [line.strip() for line in file.readlines()]
    
    if case_numbers:
        create_json_file(case_numbers, "case_contents.json")
        print("Case Contents are Stored")
    else:
        print("Failed.")