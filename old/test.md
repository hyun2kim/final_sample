
API 속도 제한 장치 (design rate limiter)

핵심 챌린지: DoS 공격 방지, 트래픽 제어 알고리즘(token bucket 등), 분산 환경에서의 카운터 공유.

웹 크롤러 (design web crawler)

핵심 챌린지: 중복 수집 방지, 로봇 배제 표준(robots.txt) 준수, 대규모 병렬 처리.

2. 소셜 미디어 및 콘텐츠 (Social & Content)
대규모 트래픽 처리와 데이터의 빠른 읽기/쓰기 전략을 묻습니다.

SNS 뉴스 피드 설계 (Design News Feed - Instagram/Twitter)

핵심 챌린지: Fan-out (확산) 전략(Push vs Pull), 팔로워가 많은 유저(Celebrity) 처리, 최신 피드 캐싱.

채팅 시스템 설계 (Design Chat System - WhatsApp/KakaoTalk)

핵심 챌린지: 실시간 통신(WebSocket), 메시지 순서 보장, 읽음 표시 처리, 1:1 vs 단체 채팅 구조.

동영상 스트리밍 서비스 (Design YouTube/Netflix)

핵심 챌린지: CDN 활용, 비디오 인코딩/압축, 대역폭 최적화, 이어보기 기능.

3. 위치 기반 서비스 (Location Based Service)
지리 정보 데이터베이스와 검색 효율성을 묻습니다.

승차 공유 서비스 (Design Uber/Grab/Kakao Taxi)

핵심 챌린지: 실시간 위치 업데이트, 지리적 인덱싱(Geohash, QuadTree), 운전자와 승객 매칭 알고리즘.

주변 친구/장소 찾기 (Design Nearby Friends/Yelp)

핵심 챌린지: 반경 검색 쿼리 최적화, 사용자 이동에 따른 데이터 갱신 부하 처리.

4. 전자상거래 및 결제 (E-commerce & Transaction)
데이터의 일관성(Consistency)과 동시성 제어가 가장 중요합니다.

플래시 세일/수강신청 시스템 (Design Flash Sale System)

핵심 챌린지: 순간적인 트래픽 폭주(Spike) 처리, 재고 초과 판매(Overselling) 방지, 대기열 큐 구현.

장바구니 및 결제 시스템 (Design Shopping Cart & Payment)

핵심 챌린지: 분산 트랜잭션 처리, 멱등성(Idempotency - 여러 번 요청해도 결과가 같아야 함) 보장.

5. 검색 및 추천 (Search & Recommendation)
빅데이터 처리와 빠른 응답 속도를 묻습니다.

검색어 자동완성 (Design Typeahead/Autocomplete)

핵심 챌린지: 트라이(Trie) 자료구조 활용, 인기 검색어 캐싱, 실시간 검색어 순위 반영.

인기 검색어/리더보드 시스템 (Design Top K Leaderboard)

핵심 챌린지: 실시간 데이터 집계(Stream Processing), 스트리밍 데이터 처리(Kafka, Spark Streaming).

**핵심 평가 항목:**
*   **요구사항 명확화:** 모호한 요구사항을 질문을 통해 구체적인 기술적 목표(TPS, 데이터 규모, 가용성 수준 등)로 변환하는 능력
*   **확장성(Scalability):** 트래픽 증가에 따른 수평 확장 전략과 데이터 파티셔닝 설계 능력
*   **트레이드오프(Trade-off):** 성능, 비용, 일관성 사이에서 최적의 선택을 내리고 그 이유를 논리적으로 설명하는 능력
*   **의사소통:** 설계 과정을 시각화하고 면접관과 협력하여 해결책을 도출하는 능력

### 2-2. URL 단축기(URL Shortener) 설계
*   **시스템 개요:** 긴 URL을 짧은 URL로 변환하고, 짧은 URL로 접속 시 원래의 URL로 리다이렉션해주는 서비스 (예: bit.ly, tinyurl)

**1. 주요 요구사항:**
*   **기능적 요구사항:** URL 단축, 리다이렉션, 커스텀 단축 코드 지원, 만료 기간 설정
*   **비기능적 요구사항:** 높은 가용성(High Availability), 낮은 지연 시간(Low Latency), 확장성(Scalability)

**2. 핵심 설계 고려사항:**
*   **단축 ID 생성 전략:**
    *   **해시 함수 (MD5, SHA):** 충돌 가능성이 있으며 문자열이 길어질 수 있음
    *   **Base62 인코딩:** 숫자 0-9, 대소문자 a-z, A-Z를 사용하여 짧고 가독성 있는 ID 생성 가능
    *   **분산 ID 생성기 (Snowflake 등):** 여러 서버에서 유일성을 보장하는 ID 생성
*   **데이터베이스 선택:**
    *   **NoSQL (DynamoDB, Cassandra):** 수평 확장성이 뛰어나고 읽기/쓰기 성능이 좋음 (단순 <단축 ID, 원본 URL> 매핑에 적합)
    *   **RDBMS (PostgreSQL, MySQL):** 데이터 일관성이 중요하거나 복잡한 쿼리가 필요한 경우 사용
*   **캐싱:** 빈번하게 조회되는 'Hot URL'을 Redis 등에 캐싱하여 데이터베이스 부하 감소 및 응답 속도 향상

**3. 트레이드오프(Trade-off):**
*   **데이터 일관성 vs 가용성:** 리다이렉션 서비스는 가용성이 더 중요하므로, NoSQL의 최종 일관성(Eventual Consistency)을 수용하는 설계가 일반적입니다.
*   **URL 중복 허용 여부:** 동일한 URL에 대해 매번 새로운 단축 URL을 생성할지, 기존 것을 재사용할지에 따라 저장 공간과 성능 간의 차이가 발생합니다.
*   **ID 길이 vs 확장성:** ID가 짧으면 입력하기 편하지만 표현 가능한 URL 개수가 제한됩니다. (예: 7글자 Base62는 약 3.5조 개의 URL 표현 가능)
