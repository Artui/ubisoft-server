import random
from datetime import datetime, timedelta

from redis import StrictRedis

from app.config import REDIS_PORT, REDIS_HOST, REDIS_DB
from app.models import Player


def distribute_players():
    players = []
    player_field = [[0 for i in range(512)] for j in range(512)]

    while len(players) != 20000:
        index_x = random.randrange(512)
        index_y = random.randrange(512)
        temp = random.randint(1, 13)
        criteria = [temp % 2 == 0,
                    player_field[index_x].count(1) <= 40,
                    player_field[index_x][index_y] != 1]

        if all(criteria):
            player_field[index_x][index_y] = 1
            players.append((index_x, index_y))

    return players


def generate_tasks():
    tasks = []
    number_of_tasks = random.randint(1, 4)
    for task in range(number_of_tasks):
        task_time = random.randint(10, 600)
        task_finished_at = (datetime.utcnow() + timedelta(seconds=task_time)).timestamp() * 1000
        tasks.append(task_finished_at)
    return tasks


def seed_db():
    client = StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
    client.flushdb()
    players = distribute_players()
    for player in players:
        tasks = generate_tasks()
        redis_player = Player(row=player[0],
                              column=player[1],
                              tasks=tasks)
        redis_player.save()
