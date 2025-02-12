# FastAPI-Blog
Blog를 Fast API로 구현하여 Fast API 이해 및 숙련도를 상승시키기.


```
uvicorn main:app --port=8081 --reload
fastapi dev main.py 
```

## MySQL Container
```
docker run --name mysql-container -e MYSQL_ROOT_PASSWORD=1234qwer -p 3306:3306 -d mysql:latest
```