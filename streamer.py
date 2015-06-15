#!/usr/bin/env python
import json
import time
import config
from mapping.tweet_mapper import TweetMapper
from pprint import pprint
from stream_consumer import StreamConsumer

tweet_mapper = TweetMapper()


def callback(event):
    if len(event) > 0:
        tweet_json = json.loads(event)

        # Do something more interesting with your tweet here
        if config.MAP_TO_DATASIFT_FORMAT:
            datasift_tweet_json = tweet_mapper.map_from_gnip_to_datasift(tweet_json)
            print "------- DATASIFT MAPPED TWEET -------"
            pprint(datasift_tweet_json)
        else:
            print "------- GNIP TWEET -------"
            pprint(tweet_json)

consumer = StreamConsumer(callback,
                          config.GNIP_URL,
                          (config.GNIP_USERNAME, config.GNIP_PASSWORD))

if __name__ == "__main__":
    while True:
        try:
            consumer.start()
            print "Consumer disconnected. Will attempt to reconnect in 10s"
            time.sleep(config.SECONDS_BEFORE_RECONNECT)
        except KeyboardInterrupt:
            break
        except:
            raise
