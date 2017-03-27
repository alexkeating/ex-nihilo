import os
from flask_migrate import Migrate, MigrateCommand
from flask_script import Shell, Manager

from app import create_app, db

settings = os.getenv('APP_SETTINGS')


def _make_context():
    return dict(
        app=create_app(settings),
        db=db,
    )

app = create_app(config=settings)

migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)
manager.add_command("shell", Shell(make_context=_make_context, use_ipython=True))

if __name__ == "__main__":
     manager.run()
