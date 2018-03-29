class Config(object):
    DEBUG = False
    TESTING = False
    # MONGO_URI = 'mongodb://localhost:27017/followyourleaders_dev'
    # MONGO_DBNAME='followyourleaders_dev'

class ProductionConfig(Config):
    DEBUG = True
    MONGO_URI = 'mongodb://localhost:27017/followyourleaders'
    MONGO_DBNAME='followyourleaders'


class DevelopmentConfig(Config):
    DEBUG = True
    MONGO_URI = 'mongodb://localhost:27017/followyourleaders_dev'
    MONGO_DBNAME='followyourleaders_dev'

