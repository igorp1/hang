import os

basedir = os.path.abspath(os.path.dirname(__file__))

class BaseConfig:
    SECRET_KEY = "076e2b980c42e392faa35df24c71969c"
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, 'hang.db')

class TestConfig(BaseConfig):
    SECRET_KEY = 'TEST_KEY'
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, 'data-test.sqlite')

class ProdConfig(BaseConfig):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, 'hang.db')

configs = dict(
    dev = DevConfig,
    test = TestConfig,
    prod = ProdConfig
)