import random
import time
from datetime import datetime, timedelta

from app.models import Player


def check_db():
    players = Player.query.all()
    for player in players:
        tasks = player.tasks
        for task in player.tasks:
            if datetime.utcnow() > datetime.strptime(task, "%Y-%m-%dT%H:%M:%S.%f"):
                tasks.remove(task)
        player.tasks = tasks
        player.save()

        randomer = random.randint(10, 600)
        if len(tasks) < 4 and randomer % 3 == 0 or len(tasks) == 0:
            new_task = (datetime.utcnow() + timedelta(seconds=randomer)).isoformat()
            tasks.append(new_task)

        player.tasks = tasks
        player.save()


if __name__ == "__main__":
    while True:
        check_db()
        time.sleep(5)
