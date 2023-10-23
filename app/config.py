class Config:
    @staticmethod
    def init_app():
        pass


class DevelopmentConfig(Config):
    DEBUG=True
    SQLALCHEMY_DATABASE_URI= "sqlite:///project.sqlite"


class ProductionConfig(Config):
    DEBUG=False
    # postgresql://username:password@localhost:portnumber/dbname
    SQLALCHEMY_DATABASE_URI= "postgresql://flask:207301@localhost:5432/jumia"



projectConfig={
    "dev": DevelopmentConfig,
    'prd': ProductionConfig
}
