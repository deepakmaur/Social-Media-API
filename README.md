# SetUp the env first
```
DATABASE_HOSTNAME=localhost
DATABASE_PORT=5432
DATABASE_PASSWORD=###
DATABASE_NAME=
DATABASE_USERNAME=
SECRET_KEY=
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=
```


# requirment
```
pip install -r requirements.txt
```

# Run database setup
```
alembic upgrade head
```



# Finally, start the FastAPI application 
```
uvicorn app.main:app --reload
```


At last open the URL
```
http://127.0.0.1:8000/docs
```
