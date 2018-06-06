from src.model.database import mongo
from src.model.story_comment import StoryComment
from src.model.story import Story
from src.model.user import User


def create_indexes():
    # indexes for User
    User._get_users_db().create_index("username")

    # indexes for Story
    Story._get_stories_db().create_index("username")

    # indexes for Comments
    StoryComment._get_comments_db().create_index("story_id")
