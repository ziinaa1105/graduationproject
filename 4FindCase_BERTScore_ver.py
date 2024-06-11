#BERTScore으로 계산하는 버전

import json
from bert_score import score

# 사용자 입력 예시
# 238185 : 청소년 할인 보조금을 부정하게 지급받은 시외버스 운송사업자에 대한 처분은 무엇인가?
# 238455 : 근로자가 임금을 목적으로 종속적인 관계에서 사용자에게 근로를 제공하는지 판단하는 기준은 무엇인가?
# 238197  : 임대인이 목적 주택에 실제 거주하려는 경우에 해당한다는 점을 증명하기 위해 고려해야 할 기준은 무엇인가?
user_input = "임대인이 목적 주택에 실제 거주하려는 경우에 해당한다는 점을 증명하기 위해 고려해야 할 기준은 무엇인가?"

#  github 제출용 용량줄인 판례 100개 버전 / case_preprocessed.json
with open('testcase.json', 'r', encoding='utf-8') as f:
    case_data = json.load(f)

# 유사도와 해당 판례 ID를 저장할 리스트 초기화
similar_cases = []

# 각 판례와 사용자 입력 간의 유사도 계산
for case_id, contents in case_data.items():
    판시사항_text = contents.get("판시사항", "")
    판결요지_text = contents.get("판결요지", "")
    사건번호_text= contents.get("사건번호", "")  
    
    
    combined_text = 판시사항_text + " " + 판결요지_text
    
    if combined_text.strip():  # 빈 문자열이 아닌 경우에만 BERTScore 계산
        # BERTScore 계산
        P, R, F1 = score([user_input], [combined_text], model_type='xlm-roberta-large', lang='ko', verbose=False)
        f1_mean = F1.mean().item()

        similar_cases.append({
            "case_id": case_id,
            "score": f1_mean,
            "사건번호": 사건번호_text,
            "판시사항": 판시사항_text,
            "판결요지": 판결요지_text
        })

# 유사도 점수로 정렬
similar_cases = sorted(similar_cases, key=lambda x: x["score"], reverse=True)

# 상위 3개의 판례 출력
print("가장 유사한 상위 3개의 판례:")
for result in similar_cases[:3]:
    case_id = result['case_id']
    score = result['score']
    사건번호_text = result['사건번호']
    판시사항_text = result['판시사항']
    판결요지_text = result['판결요지']
    print(f"판례 ID: {case_id}\n유사도 점수: {score}\n사건번호: {사건번호_text}\n판시사항: {판시사항_text}\n판결요지: {판결요지_text}\n")