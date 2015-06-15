# gnip-stream-with-datasift-mapper
Python app to pick tweets off a GNIP Stream and optionally map them to Datasift format.

# Setting up the streamer
1. Clone the repo into your virtual env
2. Install the requirements file

```pip install -r requirements```

3. Add the URL of your GNIP Stream (find it at http://consol.gnip.com) and your GNIP Username and Password to the config.py file
4. To output tweets in Datasift format ensure the OUTPUT_IN_DATASIFT_FORMAT key in config.py is set to true
5. The streamer automatically reconnects after 10 seconds, you can modify the length of time to wait for a reconnect by editing the value for SECONDS_BEFORE_RECONNECT key in config.py

# Running the streamer
By default the streamer will pretty print the tweets coming off your stream. Edit the streamer.py callback method to do something more interesting with your tweet

```python streamer.py```
