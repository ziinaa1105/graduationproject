실행 방법
1. 1StoreCaseNumber.py 로 판례 일련번호 저장한 case_numbers.txt 생성
2. 2StoreCaseContents.py로 판례 목록 저장한 case_contents.json 생성
3. 3PreprocessCase.py로 case_preprocessed.json 생성
4. 6Main.py로 실행

4FindCase_BERTScore_ver.py : BERTScore으로 유사도 비교를 진행할 수 있는 모델 이용

4FindCase_Cos_ver.py : 임베딩 후 코사인 유사도로 유사도 비교 진행하는 모델 이용

5Mrr.py : Mrr 계산하기

5MrrInput.json : 판례일련번호-사용자 질문 쌍 목록

용량 문제로 github에 case_contents.json, case_preprocessed.json 업로드 불가하여 testcase.json 파일 업로드해두었습니다.
(testcase.json : 판례 100개만 있는 작은 파일)
