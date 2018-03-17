class Config(object):
    DEBUG = False
    TESTING = False
    MONGO_URI = 'mongodb://localhost:27017/fyl_Umich'
    MONGO_DBNAME='fyl_Umich'

class ProductionConfig(Config):
    DEBUG = True
    MONGO_URI = 'mongodb://localhost:27017/fyl_Umich'
    MONGO_DBNAME='fyl_Umich'


class DevelopmentConfig(Config):
    DEBUG = True
    MONGO_URI = 'mongodb://localhost:27017/fyl_Umich'
    MONGO_DBNAME='fyl_Umich'

