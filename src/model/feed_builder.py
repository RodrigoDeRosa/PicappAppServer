import time

from business_rules import run_all
from business_rules.actions import BaseActions, rule_action
from business_rules.fields import FIELD_NUMERIC
from business_rules.variables import (BaseVariables,
                                      numeric_rule_variable,
                                      string_rule_variable)
from src.model.user import User
from src.model.story import Story
from src.utils.logger_config import Logger

INITIAL_SCORE = 10
MANY_LIKES_BONUS = 2
MANY_DISLIKES_PENALTY = 2
TOO_OLD_PENALTY = 1
MANY_COMMENTS_BONUS = 3


class FeedBuilder(object):

    @staticmethod
    def get_feed_for_username(username):
        Logger(__name__).info('Getting feed for user {}.'.format(username))

        # get all stories by iterating over usernames, use username to filter private, non-friend ones
        stories_feed_data = User.get_feed_data(username)

        Logger(__name__).info('Prioritizing {} stories for user {}\'s feed.'.format(
            len(stories_feed_data), username))

        # calculate priorities
        # FIXME: add priorities
        prioritized_stories = [story_feed_data['story_id'] for story_feed_data in stories_feed_data]

        Logger(__name__).info('Serving feed for user {}.'.format(username))
        # get stories in according order, add feed-specific fields of user's name and profile pic
        return [FeedBuilder._format_feed_story(story_id) for story_id in prioritized_stories]

    @staticmethod
    def _format_feed_story(story_id):
        serialized_story = Story.get_story(story_id)
        uploader = serialized_story['username']
        profile_preview = User.get_profile_preview(uploader)

        serialized_story['name'] = profile_preview['name']
        serialized_story['profile_pic'] = profile_preview['profile_pic']
        return serialized_story


def epochs_as_days(epochs):
    """Returns rounded number of days elapsed in number of epochs given"""
    return round(epochs/86400)  # number of epochs in 1 day


