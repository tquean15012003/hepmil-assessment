import os

from typing import List
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from database.RedditPost import RedditPost

Base = declarative_base()


class DatabaseManager:
    def __init__(self):

        self.engine = create_engine(os.getenv("DATABASE_URL"))
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    async def save_post(self, posts: List[RedditPost]):
        self.session.add_all(posts)
        self.session.commit()

    def __del__(self):
        self.session.close()
