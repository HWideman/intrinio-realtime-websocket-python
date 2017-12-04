# Intrinio realtime websocket python
IEX real-time feed for [Intrinio](https://intrinio.com/) implemented in Python  
Based upon implementation found at: https://github.com/jorymorrison/real-time-intrinio-python  

Modified to include websocket heartbeat & support for multiple securities as command line arguments

## How to
1. Set INTRINIO_USER and INTRINIO_PASSWORD environment variables

## Usage
python realtime_websocket.py AAPL  
python realtime_websocket.py AAPL MSFT