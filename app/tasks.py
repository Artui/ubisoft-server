from celery import Celery
from app.models import Player
from app.utils import generate_task
from datetime import datetime
import random

app = Celery()
app.conf.broker_url = 'redis://localhost:6379/0'

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(5.0, task_handler, name='task_handler')

@app.task
def task_handler():
    players = Player.query.all()
    for player in players:
        player.refresh(force=True)
        tasks = player.tasks
        for task in player.tasks:
            if datetime.utcnow() > datetime.fromtimestamp(task/1000):
                tasks.remove(task)

        for i in range(4):
            randomer = random.randint(10, 600)
            if len(tasks) < 4 and randomer % 3 == 0 or len(tasks) == 0:
                tasks.append(generate_task(randomer))

        player.tasks = tasks
        player.save()
