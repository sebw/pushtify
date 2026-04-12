import websocket
import ntfy
import json
import os
import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger(__name__)

pushover_userkey = os.environ['PUSHOVER_USERKEY']
gotify_host = os.environ['GOTIFY_HOST']
gotify_token = os.environ['GOTIFY_TOKEN']

# Gotify APPIDXX can be used to direct to a specific Pushover app
# You need to set an environment variable GOTIFY_APPID_XX with the desired pushover API token
# If no variable is found for the appid, message will be forwarded to the main pushover stream
appid_vars = {key: value for key, value in os.environ.items() if key.startswith("GOTIFY_APPID_")}

if 'GOTIFY_PROTOCOL' not in os.environ:
    websocket_protocol = 'wss'
else:
    if os.environ['GOTIFY_PROTOCOL'] == "http":
        websocket_protocol = 'ws'
    elif os.environ['GOTIFY_PROTOCOL'] == "https":
        websocket_protocol = 'wss'

def on_message(ws, message):
    msg = json.loads(message)
    if msg['priority'] == 0:
        pushover_prio = "-1"
    elif 1 <= msg['priority'] <= 3:
        pushover_prio = "0"
    elif 4 <= msg['priority'] <= 7:
        pushover_prio = "1"
    elif msg['priority'] > 7:
        pushover_prio = "2"

    if os.environ['PUSHTIFY_DEBUG']:
        logger.debug(msg)

    # Fetch appid in gotify message
    appid_string=str(msg["appid"])

    # Check if GOTIFY_APPID_XX has been set with a pushover app token
    gotify_appid="GOTIFY_APPID_" + appid_string
    pushover_token = appid_vars.get(gotify_appid)
    
    if pushover_token is not None:
        logger.debug("Found matching app ID " + appid_string + " > sending to Pushover app")
        ntfy.notify(msg['message'],msg['title'], priority=pushover_prio, backend='pushover', user_key=pushover_userkey, api_token=pushover_token)
    else:
        logger.debug("Found no matching app ID > sending to Pushover main stream")
        ntfy.notify(msg['message'],msg['title'], priority=pushover_prio, backend='pushover', user_key=pushover_userkey)

def on_error(ws, error):
    print(error)

def on_close(ws, close_status_code, close_msg):
    logger.debug("### closed connection ###")

def on_open(ws):
    logger.debug("### opening connection ###")

if __name__ == "__main__":
    wsapp = websocket.WebSocketApp(str(websocket_protocol) + "://" + str(gotify_host) + "/stream", header={"X-Gotify-Key": str(gotify_token)},
                              on_open=on_open,
                              on_message=on_message,
                              on_error=on_error,
                              on_close=on_close)
    wsapp.run_forever()
