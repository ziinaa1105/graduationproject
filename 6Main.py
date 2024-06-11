from flask import Flask, request, render_template, redirect, url_for
import json
from bert_score import score

app = Flask(__name__)

# case_preprocessed.json
with open('testcase.json', 'r', encoding='utf-8') as f:
    case_data = json.load(f)

@app.route('/')
def index():
    return render_template('main.html')

@app.route('/search', methods=['POST'])
def search():
    user_input = request.form['userinput']
    
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
    
    # 가장 유사한 판례
    top_case = similar_cases[0]

    # 유사도가 2등, 3등, 4등인 판례
    recommend_cases = similar_cases[1:4]

    return render_template('result.html', query=user_input, top_case=top_case, recommend_cases=recommend_cases)

@app.route('/recommend')
def recommend():
    recommend_cases = request.args.get('recommend_cases')
    return render_template('recommend.html', recommend_cases=json.loads(recommend_cases))

if __name__ == '__main__':
    app.run(debug=True)
