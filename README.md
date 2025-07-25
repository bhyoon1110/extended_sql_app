# Extended SQL App (Deliverable #5)

## 개요
SQLite DB를 기반으로 복잡한 SQL 예제를 웹 UI로 실행해 볼 수 있는 Flask 애플리케이션입니다.

## 설치 및 실행
```bash
git clone https://github.com/bhyoon1110/extended_sql_app.git
cd extended_sql_app
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python database_setup.py     # DB 초기화
python app.py                # 서버 실행 (http://localhost:5000)
