# 개인 미니 프로젝트 : MBTI 궁합

## Python + Streamlit + 기타 사용

### 🔗 https://mbti-gunghab.streamlit.app
###
###
#### MBTI 궁합 테스트 앱 (MBTI Compatibility Test App)

##### 프로젝트 목적
- 나의 MBTI와 상대방의 MBTI를 선택해 궁합 결과를 확인하는 웹앱
- 재미 요소를 더한 카드형 UI로 관계 무드와 궁합 해석을 직관적으로 보여주는 미니 프로젝트

##### 사용 기술
- Python
- Pandas
- Streamlit
- Custom CSS

##### 핵심 기능
- MBTI 16가지 유형 선택
- MBTI 조합별 궁합 결과 계산
- 궁합 점수 및 관계 스타일 시각화
- 공유용 한 줄 문구 생성
- 궁합 등급 가이드 표 제공

##### 기술적 구현 포인트
- 16x16 궁합 매트릭스를 활용한 MBTI 조합별 결과 처리
- Streamlit selectbox와 button을 활용한 사용자 입력 기반 인터랙션 구현
- random.seed를 활용해 조합별 고정된 감성 메시지 제공
- Pandas DataFrame으로 궁합 등급 가이드 표 구성
- CSS 커스터마이징으로 카드형 UI와 감성적인 결과 화면 구현