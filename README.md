# 붕괴3rd 앙증 함대 강적 결과 자동 기록 프로그램

Python 3.6
이미지 1920 * 810 사이즈에서만 작동

2019.03.30.


## run

1. pip3 install -r requirements.txt
2. n_participate.txt 파일에 오늘 강적 친 인원수 기입
3. n_fleet.txt 파일에 현재 함대 인원수 기입
4. image_source/s_atk 에 오늘 강적 스샷들 넣기
5. image_source/s_fleet 에 현재 함대 인원 스샷들 넣기
6. autokey.py 실행


## output

images_result/{오늘날짜}/ 경로에 위치

1. {오늘날짜}.txt - 강적 친 사람들 ID순으로 정렬. 1 참여. -1 미참여. 구글시트에 그대로 붙이면 된다.

2. {오늘날짜}_강적O - 보여주기용. 오늘 강적 친 사람들 스샷
3. {오늘날짜}_강적X - 보여주기용. 오늘 강적 안 친 사람들 스샷
4. {오늘날짜}_강적결과 - 보여주기용. 오늘 강적 결과


## To do

1. 데미지 표기되게 바꾸기. {데미지} / 0 / -1 세가지로 구분 되게 변경.
2. 마우스 움직임을 통해 자동 스샷 찍기 구현.
3. 다른 이미지 해상도에서도 문제 없이 작동되게 구현.