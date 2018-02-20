from sanic.response import json, text
from sanic.views import HTTPMethodView
from sanic.exceptions import InvalidUsage

from app.models import Player
import random
from app.utils import generate_task, get_top_and_bottom, get_row_and_column


class IndexView(HTTPMethodView):
    async def get(self, request):
        return text("ok")


class PlayersByCoordinatesView(HTTPMethodView):
    async def get(self, request):
        top_coords, bottom_coords = get_top_and_bottom(request.args)
        include_tasks = request.args.get('include_tasks', True)
        row_criteria = (bottom_coords[1], top_coords[1]) if top_coords and bottom_coords else (0, 512)

        column_criteria = (bottom_coords[0], top_coords[0]) if top_coords and bottom_coords else (0, 512)

        players_cursor = Player.query.filter(row=row_criteria).filter(column=column_criteria).order_by('column').all()
        for player in players_cursor:
            player.refresh(force=True)
        players = [player.to_json(include_tasks) for player in players_cursor]

        return json({"players": players},
                    status=200)


class PlayerByCoordinatesView(HTTPMethodView):
    async def get(self, request):
        row, column = get_row_and_column(request.args)

        player = Player.query.filter(row=(row, row)).filter(column=(column, column)).order_by('column').all()

        if not player:
            raise InvalidUsage("No such player.")

        player = player[0]
        player.refresh(force=True)
        return json({"player": player.to_json()},
                    status=200)


class StartTaskByCoordinatesView(HTTPMethodView):
    async def put(self, request):
        row, column = get_row_and_column(request.json)

        player = Player.query.filter(row=row, column=column).all()
        if not player:
            raise InvalidUsage("No such player.")

        player = player[0]
        player.refresh(force=True)
        tasks = player.tasks

        if len(tasks) >= 4:
            raise InvalidUsage("Cannot add more tasks.")
        tasks.append(generate_task(random.randint(10, 600)))
        player.tasks = tasks
        player.save()
        return json({"tasks": player.tasks},
                    status=200)


class StopTaskByCoordinatesView(HTTPMethodView):
    async def put(self, request):
        print(request.json)
        row, column = get_row_and_column(request.json)
        task_index = request.json.get('task')

        player = Player.query.filter(row=row, column=column).all()
        if not player:
            raise InvalidUsage("No such player.")

        player = player[0]
        player.refresh(force=True)
        tasks = player.tasks

        if len(tasks) <= task_index:
            raise InvalidUsage("Invalid task index.")
        tasks.remove(tasks[task_index])
        player.tasks = tasks
        player.save()
        return json({"tasks": player.tasks},
                    status=200)
