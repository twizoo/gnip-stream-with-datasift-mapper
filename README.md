# gnip-stream-with-datasift-mapper
Python app to pick tweets off a GNIP Stream and optionally map them to Datasift format.

By default the streamer will pretty print the tweets coming off your stream. Edit the streamer.py callback method to do something more interesting with your tweet

Mappings can be altered / overridden in the tweet_mapper.py

## Setting up the streamer
- Clone the repo into your virtual env
- pip install the requirements file

```pip install -r requirements```

- Add the URL of your GNIP Stream (find it at http://consol.gnip.com) and your GNIP Username and Password to the config.py file
- To output tweets in Datasift format ensure set OUTPUT_IN_DATASIFT_FORMAT config.py to true
- The streamer automatically reconnects after 10 seconds, you can modify the length of time to wait for a reconnect by editing the value for SECONDS_BEFORE_RECONNECT in config.py

## Running the streamer

```python streamer.py```
