from sqlalchemy import create_engine, Engine

from config import config


engine = create_engine(f'sqlite+pysqlite:///{config.sqlite.filename}')
