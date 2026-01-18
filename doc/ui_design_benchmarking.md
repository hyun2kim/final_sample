# 🎨 UI Design Benchmarking: Duolingo Style

이 문서는 **Architecture Gym**의 챕터 섹션을 **Duolingo(듀오링고)**의 학습 경로 UI로 개편한 내용을 정리한 리포트입니다.

---

## 1. 벤치마킹 대상: Duolingo Learn Path
Duolingo의 'Learn' 페이지는 사용자의 학습 동기를 유발하기 위해 다음과 같은 게임화(Gamification) 요소를 사용합니다.
- **수직적 학습 경로 (Vertical Path)**: 선형적인 학습 흐름을 시각적으로 표현.
- **지그재그 배치 (Zig-zag Nodes)**: 단조로움을 피하기 위한 노드의 변칙적 배치.
- **유닛 시스템 (Unit Banner)**: 대단위 주제를 강렬한 색상의 배너로 구분.
- **3D 입체 디자인**: 버튼에 깊이감(Shadow)을 주어 누르고 싶은 욕구 자극.

---

## 2. 적용 내용 (Architecture Gym)

### 🧩 챕터 섹션 구조 개편
기존의 그리드(Grid) 형태 카드 나열 방식에서 **수직 스네이크 경로(Snake Path)** 방식으로 전면 개편했습니다.

1.  **Unit Banner (단위 배너)**:
    - 각 챕터를 하나의 'Unit'으로 정의.
    - 챕터별 고유 컬러(초록, 파랑, 주황 등)를 적용하여 시각적 구분을 명확히 함.
2.  **Path Nodes (학습 노드)**:
    - 원형 버튼 형태의 노드를 배치.
    - `4n+1`, `4n+2` 등의 CSS 규칙을 활용하여 Duolingo 특유의 지그재그 경로 구현.
    - 노드 클릭 시 해당 챕터로 진입하는 인터랙션 유지.
3.  **Visual Feedback (시각적 피드백)**:
    - **Hover Tooltip**: 노드 위에 마우스를 올리면 챕터 설명이 툴팁으로 표시됨.
    - **3D Effect**: 버튼 하단에 두꺼운 보더를 주어 입체적인 느낌 구현 (Active 상태 시 눌리는 효과).
    - **Connection Line**: 노드와 노드 사이를 가느다란 선으로 연결하여 경로의 연속성 표현.

### 🎨 디자인 시스템 (CSS)
- `var(--primary)` 외에도 챕터별로 활기찬 색상 팔레트 추가.
- `backdrop-filter: blur(10px)`를 활용한 유리질 효과(Glassmorphism)와 조합하여 현대적인 느낌 유지.

---

## 3. 기대 효과
- **성취감 증대**: 경로를 따라 내려가는 시각적 연출을 통해 게임을 클리어하는 듯한 피드백 제공.
- **UI 몰입감 향상**: 텍스트 위주의 구성에서 그래픽 중심의 직관적인 구성으로 변경되어 사용자 이탈 방지.
- **브랜드 아이덴티티**: 'Gym(체육관)'이라는 컨셉에 맞춰 훈련 코스를 완주하는 느낌을 강화함.

---

## 🛠️ 수정 파일 내역
- `frontend/index.html`: 챕터 섹션 HTML 구조 변경
- `frontend/assets/style.css`: 수직 경로 및 노드 스타일 추가
- `frontend/js/app.js`: 챕터별 색상 데이터 추가
