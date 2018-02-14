import os
from hang import db, build_app
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

# Import models
from hang.models import Word

# Build app
CONFIG_NAME  = os.getenv('APP_ENV') or 'dev'
app = build_app(CONFIG_NAME)

# setup manager
manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)

if __name__ == "__main__":
    manager.run()