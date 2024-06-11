# 저장된 판례 데이터 전처리 과정

import json
import re

def preprocess_text(text):
    if text is None:
        return ""  # 텍스트가 None인 경우 빈 문자열 반환
    
    # HTML 태그 제거
    text = re.sub(r'<[^>]+>', '', text)

    # 【 】를 공백으로 변경
    text = re.sub(r'【[^】]+】', ' ', text)

    # 유니코드 제외 특수문자 제거
    text = re.sub(r'[^\w\s\dㄱ-ㅎㅏ-ㅣ가-힣]', '', text)

    # 여러 개의 공백을 하나의 공백으로 변경
    text = re.sub(r'\s+', ' ', text)

    return text.strip()

# 전처리 전 파일 : case_contents.json / 전처리 후 파일 : case_preprocessed
input_file = "case_contents.json"
output_file = "case_preprocessed.json"


with open(input_file, 'r', encoding='utf-8') as f:
    data = json.load(f)


for case_id, case_info in data.items():
    for key, value in case_info.items():
        # "판례내용" 전처리
        if key == "판례내용":
            if value is not None:
                # 【주 문】 이전의 내용 제거
                match = re.search(r'【주\s*문】', value)

                if match:
                    value = value[match.end():]  # "【주 문】" 이후의 내용을 추출하여 value에 대입
                case_info[key] = preprocess_text(value)

       # "판례내용"이 아닌 경우 전처리
        else:
            case_info[key] = preprocess_text(value)

# 저장하기
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print("Preprocessing Contents is Done")