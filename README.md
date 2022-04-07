# 중요해씨_백엔드
- 최종 서비스 명을 위 괄호 부분에 작성하세요.
- 최종 서비스의 한 줄 소개를 작성하세요.


## 프로젝트 구성 안내

* `bullet point 에 적힌 내용을 수정해 주시면 됩니다.`

* `초기 기획은 언제든 수정될 수 있으니 웹서비스 결과를 내는데 초점을 두시기 바랍니다.`

## 1. 백엔드 팀원
| 팀원 | 파트 |
|------|---|
| 김혜민 | 백엔드 |
| 진병수 | 백엔드 |

1. 김혜민: 백엔드 담당

- 기획 단계: 구체적인 설계와 지표에 따른 프로젝트 제안서 작성
- 개발 단계: 팀원간의 일정 등 조율 + 프론트 or 백엔드 or 인공지능 개발
- 수정 단계: 기획, 스크럼 진행, 코치님 피드백 반영해서 수정, 발표 준비

2. 진병수: 백엔드 담당

- 기획 단계: 큰 주제에서 문제 해결 아이디어 도출, 와이어프레임 작성
- 개발 단계: 와이어프레임을 기반으로 API 및 데이터베이스 완성
- 수정 단계: 피드백 반영해서 백엔드 설계 수정


## 2. 백엔드 사용 기술
**주요 스킬**
  - Python
  - Django
  - GitLab
  - MySQL
  - Azure

**패키지 관리**
  - poetry

**코딩 컨벤션**
  - flake8
  - black
  - isort

**서버 및 미들웨어**
  - Nginx
  - Gunicorn

## 3. Poetry 설치 및 실행
```shell
# poetry 설치
> curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python

# 환경변수 설정
> source $HOME/.poetry/env

# poetry 프로젝트에서 최초 생성시
> poetry new my-project

# poetry 가상환경 실행
> poetry shell
```
```shell
# 특정 패키지 설치 명령어
> poetry add <패키지명>

# .toml 파일에 작성된 패키지 설치(requirements.txt 와 유사)
> poetry update
```
## 4. Mysql 연결 및 명령어
## 5. Nginx, Gunicorn 연결 및 실행 명령어
