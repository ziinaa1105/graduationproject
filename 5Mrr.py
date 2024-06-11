import json
from bert_score import score


# github 제출용 json / case_preprocessed.json
with open('testcase.json', 'r', encoding='utf-8') as f:
    case_data = json.load(f)


with open('5MrrInput.json', 'r', encoding='utf-8') as f:
    case_questions = json.load(f)

true_case_ids = [item['case_id'] for item in case_questions]
user_inputs = [item['question'] for item in case_questions]


def calculate_mrr(user_inputs, true_case_ids):
    total_rr = 0
    reciprocal_ranks = [] 
    for user_input, true_case_id in zip(user_inputs, true_case_ids):

        similar_cases = []
        
        for case_id, contents in case_data.items():
            판시사항_text = contents.get("판시사항", "")
            판결요지_text = contents.get("판결요지", "")
                        
            combined_text = 판시사항_text + " " + 판결요지_text
            
            if combined_text.strip():  
                
                P, R, F1 = score([user_input], [combined_text], model_type='xlm-roberta-large', lang='ko', verbose=False)
                f1_mean = F1.mean().item()

                similar_cases.append({
                    "case_id": case_id,
                    "score": f1_mean,
                    "판시사항": 판시사항_text,
                    "판결요지": 판결요지_text
                })

        similar_cases = sorted(similar_cases, key=lambda x: x["score"], reverse=True)

        # 1/rank의 합 구하기
        rr = 0
        for rank, result in enumerate(similar_cases, start=1):
            if result['case_id'] == true_case_id:
                rr = 1 / rank
                break
        total_rr += rr

        # 각 쿼리에 대한 RR 저장
        reciprocal_ranks.append((user_input, true_case_id, rr))  

    # Mean Reciprocal Rank (MRR) 계산
    mrr = total_rr / len(user_inputs)
    return mrr, reciprocal_ranks


mrr, reciprocal_ranks = calculate_mrr(user_inputs, true_case_ids)
print(f"MRR: {mrr:.4f}")


print("각 판례에 대한 Reciprocal Rank:")
for user_input, true_case_id, rr in reciprocal_ranks:
    print(f"정답 판례 ID: {true_case_id}\n 사용자 입력: {user_input}\n Reciprocal Rank: {rr:.4f}\n")

