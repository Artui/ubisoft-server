import asyncio
import redis
from rom import util
from app import app, config
from app.routes import add_routes

if __name__ == "__main__":
    app.config.from_object(config)
    add_routes(app)
    util.set_connection_settings(host=config.REDIS_HOST, db=config.REDIS_DB)
    server = app.create_server(
        host=app.config.HOST,
        port=app.config.PORT,
        debug=app.config.DEBUG
    )
    loop = asyncio.get_event_loop()
    loop.run_until_complete(server)
    loop.run_forever()