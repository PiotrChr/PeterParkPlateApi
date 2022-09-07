from flask import Flask
from src.infrastructure.di.Container import Container
from src.delivery.api import api

app = Flask(__name__)
app.register_blueprint(api)

if __name__ == "__main__":
    container = Container()

    container.config.db_user.from_env("DB_USER", required=True)
    container.config.db_pass.from_env("DB_PASS", required=True)
    container.config.db_host.from_env("DB_HOST", required=True)
    container.wire(modules=[__name__])

    app.run()
