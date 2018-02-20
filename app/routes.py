from app.views import (IndexView, PlayersByCoordinatesView, PlayerByCoordinatesView,
                       StartTaskByCoordinatesView, StopTaskByCoordinatesView)

routes = [{"handler": IndexView, "path": "/"},
          {"handler": PlayersByCoordinatesView, "path": "/players/"},
          {"handler": StartTaskByCoordinatesView, "path": "/start/"},
          {"handler": StopTaskByCoordinatesView, "path": "/stop/"},
          {"handler": PlayerByCoordinatesView, "path": "/player/"}]


def add_routes(app):
    for route in routes:
        app.add_route(route.get('handler').as_view(), f"/game{route.get('path')}")
