import os
import json
import praw
import logging
import asyncio

from typing import List
from dotenv import load_dotenv

from api.crawl.model import TimeFilter
from database.RedditPost import RedditPost
from utils.SessionKey import get_session_key
from helpers.RedisManager import RedisManager
from database.DatabaseManager import DatabaseManager

logger = logging.getLogger(__name__)


class CrawlHanlder:
    SUB_REDDIT = "memes"
    MAX_TOP_POSTS = 20

    def __init__(self):
        logger.info("CrawlHanlder initialized")
        self.reddit_client = praw.Reddit(
            client_id=os.getenv("REDDIT_CLIENT_ID"),
            client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
            user_agent=os.getenv("REDDIT_USER_AGENT"),
        )
        self.db_manager = DatabaseManager()
        self.redis_manager = RedisManager()

    async def retrieve_top_posts(
        self, time_filter: TimeFilter = "day", no_post: int = 20
    ) -> List[RedditPost]:
        logger.info(
            f"retrieve_top_posts called with arguments: no_post: {no_post}, time_filter: {time_filter}"
        )
        self._check_top_post(no_post=no_post)

        # Retrieve from Redis
        redis_key = get_session_key()
        data = self.redis_manager.get(key=redis_key)
        if data is not None:
            logger.info("Retrieved data from cache!")
            return json.loads(data)[:no_post]

        # Retrieve with Reddit API
        subreddit = self.reddit_client.subreddit(self.SUB_REDDIT)
        top_posts = subreddit.top(time_filter=time_filter, limit=self.MAX_TOP_POSTS)
        top_posts_last_24_hours = [
            RedditPost(
                id=f"{post.id}-{redis_key}",
                body=post.selftext,
                link=post.url,
                title=post.title,
                no_comments=post.num_comments,
                upvotes=post.score,
                created_at=post.created_utc,
                session_key=redis_key,
            )
            for post in top_posts
        ]
        top_posts_last_24_hours.sort(key=lambda post: post.upvotes, reverse=True)

        # Save to Redis Cache after return
        asyncio.create_task(
            self._save_top_post_to_redis(
                redis_key=redis_key, posts=top_posts_last_24_hours
            )
        )
        asyncio.create_task(self.db_manager.save_post(top_posts_last_24_hours))

        logger.info(f"Top posts: {top_posts_last_24_hours}")
        return self._base_reddit_post_list_dict(top_posts_last_24_hours[:no_post])

    def _base_reddit_post_list_dict(self, posts: List[RedditPost]):
        return [post.as_dict() for post in posts]

    async def _save_top_post_to_redis(self, redis_key, posts: List[RedditPost]):
        logger.info("Saving result to Redis Cache")
        posts_json = self._base_reddit_post_list_dict(posts)
        self.redis_manager.set(key=redis_key, value=json.dumps(posts_json))

    def _check_top_post(self, no_post: int):
        if no_post > self.MAX_TOP_POSTS:
            raise ValueError(f"no_post cannot exceed {self.MAX_TOP_POSTS}")


# Run the main function in an event loop
async def main():
    load_dotenv()  # Load environment variables
    crawl_handler = CrawlHanlder()
    await crawl_handler.retrieve_top_posts()


# Start the event loop
if __name__ == "__main__":
    asyncio.run(main())
