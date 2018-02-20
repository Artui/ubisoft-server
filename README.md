To start this project, Redis is required.
1. Create virtual env for python.
2. Install requirements with ```pip install -r requirements.txt```
3. Launch Redis. In project root directory, open python and seed_database with following:
```
>>> from app.tools import seed_db
>>> seed_db()
```
4. In a separate console start a celery worker with 
```
celery -A app.tasks worker -B -l info --concurrency=1
```
5. Start the server itself with 
```
python run.py
```

You can also specify env variables for 
```HOST, PORT, REDIS_HOST, REDIS_PORT and REDIS_DB```