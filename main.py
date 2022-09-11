from flask import Flask
from src.di.Container import Container
from src.delivery.api import api
# import pymysql


def create_app() -> Flask:
    container = Container()

    container.config.db_user.from_env("DB_USER", required=True)
    container.config.db_pass.from_env("DB_PASS", required=True)
    container.config.db_host.from_env("DB_HOST", required=True)
    container.config.db_name.from_env("DB_NAME", required=True)
    container.wire(modules=[__name__])

    app = Flask(__name__)
    app.container = container
    container.wire(modules=[__name__])
    app.register_blueprint(api)

    return app


if __name__ == "__main__":
    app = create_app()

    app.run(host="0.0.0.0", port=5050, debug=True)

