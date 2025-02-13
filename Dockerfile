# 1. Python 이미지에서 시작
FROM python:3.10-slim

# 2. 작업 디렉토리 설정
WORKDIR /app

# 3. 요구 사항 파일 복사 및 설치
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# 4. 애플리케이션 코드 복사
COPY . /app

# 5. FastAPI 애플리케이션 실행
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8081"]
