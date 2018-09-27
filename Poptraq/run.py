import app
from app import db, migrate


def create_app():
    db.app = app
    db.init_app(app)
    migrate.init_app(app, db)
    return app


application = create_app()

if __name__ == '__main__':
    application.run(debug=True)
