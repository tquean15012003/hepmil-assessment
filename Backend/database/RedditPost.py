from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class RedditPost(Base):
    __tablename__ = "reddit_posts"
    id = Column(String, primary_key=True)
    body = Column(Text, nullable=True)
    link = Column(String, nullable=False)
    title = Column(String, nullable=False)
    no_comments = Column(Integer, nullable=False)
    upvotes = Column(Integer, nullable=False)
    created_at = Column(Integer, nullable=False)
    session_key = Column(String, nullable=False)
    
    def as_dict(self):
        return {
            "id": getattr(self, "id"),
            "body": getattr(self, "body"),
            "link": getattr(self, "link"),
            "title": getattr(self, "title"),
            "no_comments": getattr(self, "no_comments"),
            "upvotes": getattr(self, "upvotes"),
            "created_at": getattr(self, "created_at"),
            "session_key": getattr(self, "session_key"),
        }
