# Transcendence
sunko, youngcki, hyungjuk, surkim, yeonwkan 과 함께하는 신나는 트센 :-)

과제 목표 : VanilaJS와 Django를 이용해 핑퐁 게임 웹사이트 구현

과제 명세사항 및 세부 구현, 제한사항은 [여기](https://github.com/dudcks0994/transcendence/blob/main/subject.md)

#### Backend
- Django와 Django REST framework를 사용하여 API서버 구현
	- Restful API에 대한 기본적인 이해와 Django REST framework 사용
	- Django ORM을 사용하여 기본 유저 모델 커스터마이징 및 친구기능 구현
	- Oauth 2.0을 통한 소셜 로그인 구현 및 Session과 JWT를 이용한 인증
	- 인증을 위한 JWT추가 및 JWT검증하는 커스텀 Middleware 구현
- Unicorn, Uvicorn을 이용한 웹소켓 사용
	- 웹소켓 프로토콜에 대한 기본적인 이해
	- 비동기 프로그래밍에 대한 기본적인 이해와 Django의 Channels에 대한 이해
	- 친구의 온라인/오프라인 스테이터스를 실시간으로 확인하기 위한 웹소켓 구현
	- 핑퐁게임 토너먼트의 실시간 원격플레이를 위한 로직 구현

#### Docker
- Docker를 사용하여 Django 백엔드 서버와 Nginx 프론트엔드 서버, PostgreSQL 데이터베이스를 컨테이너화
	- Dockerfile과 docker-compose.yml을 사용하여 docker compose up으로 서버 실행
	- 바인드 볼륨을 이용해 코드 수정시 서버 재시작 없이 반영되도록하고 데이터베이스 데이터 보존을 위해 볼륨 사용
	- Nginx 컨테이너에 자체 인증서를 통한 HTTPS 적용 및 라우팅 규칙에 따른 백엔드/프론트엔드 프록시 설정
- ELK 구축
	- Elasticsearch을 사용하기 위한 RDBMS와의 차이 및 구조 이해
	- Django의 로그를 적절하게 수집하기 위한 grok pattern 작성 및 logstash 설정
	- Kibana를 통해 시각화하기 위해 kibana API를 사용하여 대시보드, 인덱스패턴 생성 및 라이프사이클 관리하는 쉘 스크립트 작성
	- TLS적용을 위해 certutil을 사용하여 인증서를 생성하고 세 컨테이너에 적용시키는 쉘 스크립트 작성

### 배운 점
- Git을 통한 협업
	- 컨벤션을 지켜가면서 이슈관리 및 커밋, PR 메세지 작성
	- PR을 통한 코드리뷰 및 머지
- Django
	- 기본적인 Django의 구조 상 원래의 User모델을 기준으로 기능들이 구현되어 있어 이를 커스터마이징 할 경우 어떻게 해야하는지에 대한 이해
	- 미들웨어의 구조를 이해하여 뷰 함수에 들어오기 전에 인증을 처리하고, 편의를 위해 JWT토큰을 request에 넣어주는 미들웨어 구현
	- 다른 팀원이 종종 Django가 데이터베이스 테이블 관련 문제로 에러를 겪음 -> 도커 컨테이너 첫 실행 시에 cache를 지우고 새로 마이그레이션 생성 및 마이그레이트 실행하게 함 -> 제대로 데이터베이스 자체가 안만들어지는 경우가 있는데, 앱 별로 migrations폴더 내에 __init__.py파일이 없을 경우 마이그레이션 대상이 되지 않는다는것을 알게됌
	- 동시접속이 되면 게임플레이가 비정상적으로 바뀌어 동시접속을 막아야하는데, Django의 기본 Session은 동시접속이 가능하게끔 되어있어, 친구 온라인/오프라인을 보여주는 웹소켓을 이용해 기존유저가 있을 경우 신규접속 유저의 연결 끊고 프론트에서 로그아웃하게끔 변경
	- 닉네임 변경API를 추가하면서, 기존 온라인/오프라인 스테이터스 웹소켓에서 반영되지 않는 문제발생 -> 닉네임 변경시에도 웹소켓으로 변경된 닉네임을 보내서 기존 명단에서 수정하는식으로만 변경
	- 유저 한명 접속시 해당 유저가 친구인 사람에게만 갱신이 이루어지게끔 웹소켓 메세지를 보내기 전에 서버에서 친구를 확인하는 로직 추가
	- 위의 Webserv를 만들 당시 OPTIONS 메소드에 대해알고만 있었는데, 프론트와 합치면서 cors에러를 겪으면서 개발자 도구를 통해 OPTIONS메소드가 무엇인지 Preflight방식에 대해서도 알고, django-cors-headers 패키지를 설치하여 해결함(혹은 수동으로 헤더에 Access-Control-Allow-Origin을 넣어주는 방법도 있음)\
