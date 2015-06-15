from utils.dictutils import deep_get, deep_set
from dateutil import parser
import time

mapping = {
    "interaction.twitter.lang": "gnip.language.value",
    "interaction.twitter.filter_level": "twitter_filter_level",
    "interaction.twitter.text": "body",
    "interaction.twitter.created_at": "object.postedTime",  # check format
    "interaction.twitter.source": "generator.displayName",
    "interaction.twitter.user.lang": "actor.languages",
    "interaction.twitter.user.utc_offset": "actor.utcOffset",
    "interaction.twitter.user.id_str": "actor.id",
    "interaction.twitter.user.favourites_count": "actor.favoritesCount",
    "interaction.twitter.user.description": "actor.summary",
    "interaction.twitter.user.friends_count": "actor.friendsCount",
    "interaction.twitter.user.url": "actor.links",
    "interaction.twitter.user.created_at": "actor.postedTime",
    "interaction.twitter.user.time_zone": "actor.twitterTimeZone",
    "interaction.twitter.user.profile_image_url": "actor.image",
    "interaction.twitter.user.id": "actor.id",
    "interaction.twitter.user.followers_count": "actor.followersCount",
    "interaction.twitter.user.screen_name": "actor.preferredUsername",
    "interaction.twitter.user.location": "actor.location.displayName",
    "interaction.twitter.user.statuses_count": "actor.statusesCount",
    "interaction.twitter.user.verified": "actor.verified",
    "interaction.twitter.user.listed_count": "actor.listedCount",
    "interaction.twitter.user.profile_image_url_https": "actor.image",
    "interaction.twitter.user.name": "actor.displayName",
    "interaction.twitter.media": "twitter_entities.media",
    "interaction.twitter.mentions": "twitter_entities.user_mentions",
    "interaction.twitter.hashtags": "twitter_entities.hashtags",
    "interaction.twitter.urls": "twitter_entities.urls",
    "interaction.twitter.id": "id",
    "interaction.twitter.gnip_geo.latitude": "location.geo",
    "interaction.twitter.place.full_name": "location.displayName",
    "interaction.twitter.place.url": "location.link",
    "interaction.twitter.place.country": "location.country_code",
    "interaction.twitter.place.country_code": "location.twitter_country_code",
    "interaction.twitter.place.name": "location.name",
    "interaction.interaction.created_at": "postedTime",
    "interaction.interaction.author.username": "actor.preferredUsername",
    "interaction.interaction.author.name": "actor.displayName",
    "interaction.interaction.author.language": "actor.languages",
    "interaction.interaction.author.link": "actor.link",
    "interaction.interaction.author.avatar": "actor.image",
    "interaction.interaction.author.id": "actor.id",
    "interaction.interaction.content": "body",
    "interaction.interaction.source": "generator.displayName",
    "interaction.interaction.link": "link",
    "interaction.interaction.received_at": "postedTime",
    "interaction.interaction.type": "_set_to_twitter",
    "interaction.interaction.mentions": "twitter_entities.user_mentions",
    "interaction.interaction.hashtags": "twitter_entities.hashtags",
    "interaction.interaction.gnip_geo": "location.geo",
    "interaction.language.tag": "gnip.language.value",
    "interaction.gnip.verb": "verb",
    "interaction.gnip.original_object": "object"
}

transformations_map = {
    "interaction.twitter.user.lang": "transform_language",
    "interaction.twitter.user.id_str": "transform_id",
    "interaction.twitter.user.profile_image_url": "transform_https_url",
    "interaction.twitter.user.id": ["transform_id", "string_to_int"],
    "interaction.twitter.user.utc_offset": "string_to_int",
    "interaction.twitter.user.url": "transform_user_url",
    "interaction.twitter.user.created_at": "transform_date",
    "interaction.twitter.mentions": "transform_mentions",
    "interaction.twitter.created_at": "transform_date",
    "interaction.twitter.id": "transform_id",
    "interaction.interaction.id": "transform_id",
    "interaction.interaction.created_at": "transform_date",
    "interaction.interaction.received_at": "transform_date_epoch",
    "interaction.interaction.author.language": "transform_language",
    "interaction.interaction.author.id": ["transform_id", "string_to_int"],
    "interaction.interaction.author.avatar": "transform_https_url",
    "interaction.interaction.type": "set_to_twitter",
    "interaction.interaction.mentions": "transform_mentions",
    "interaction.interaction.link": "transform_http_url",
    "interaction.gnip.original_object": "transform_original_object"
}


class TweetMapper(object):

    def map_from_gnip_to_datasift(self, gnip_json):
        remapped_tweet = {}
        for destination_path, source_path in mapping.iteritems():
            value = deep_get(gnip_json, source_path)
            if destination_path in transformations_map:
                transformations = transformations_map[destination_path]
                if isinstance(transformations, str):
                    transformations = [transformations]
                for transformation in transformations:
                    value = getattr(self, transformation)(value)
            if value is not None:
                deep_set(remapped_tweet, destination_path, value)
        return remapped_tweet

    def transform_language(self, value):
        return value[0]

    def transform_id(self, value):
        return value.split(":")[-1]

    def set_to_twitter(self, value):
        return "twitter"

    def transform_mentions(self, value):
        return [mention["screen_name"] for mention in value]

    def transform_user_url(self, value):
        try:
            return value[0]["href"]
        except:
            return None

    def transform_http_url(self, value):
        return value.replace("http://", "https://")

    def transform_https_url(self, value):
        return value.replace("https://", "http://")

    def string_to_int(self, value):
        try:
            return int(value)
        except:
            return None

    def transform_date(self, value):
        date = parser.parse(value)
        return date.strftime("%a, %d %b %Y %H:%M:%S %z")

    def transform_date_epoch(self, value):
        date = parser.parse(value)
        return time.mktime(date.timetuple())

    def transform_original_object(self, value):
        value["id"] = self.transform_id(value["id"])
        return value
