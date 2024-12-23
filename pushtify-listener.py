import websocket
import ntfy
import json
import os

pushover_userkey = os.environ['PUSHOVER_USERKEY']
gotify_host = os.environ['GOTIFY_HOST']
gotify_token = os.environ['GOTIFY_TOKEN']

if 'GOTIFY_PROTOCOL' not in os.environ:
    websocket_protocol = 'wss'
else:
    if os.environ['GOTIFY_PROTOCOL'] == "http":
        websocket_protocol = 'ws'
    elif os.environ['GOTIFY_PROTOCOL'] == "https":
        websocket_protocol = 'wss'

def on_message(ws, message):
    print(message)
    msg = json.loads(message)
    if msg['priority'] == 0:
        pushover_prio = "-1"
    elif 1 <= msg['priority'] <= 3:
        pushover_prio = "0"
    elif 4 <= msg['priority'] <= 7:
        pushover_prio = "1"
    elif msg['priority'] > 7:
        pushover_prio = "2"
    ntfy.notify(msg['message'],msg['title'], priority=pushover_prio, backend='pushover', user_key=pushover_userkey)

def on_error(ws, error):
    print(error)

def on_close(ws, close_status_code, close_msg):
    print("### closed ###")

def on_open(ws):
    print("Opened connection")

if __name__ == "__main__":
    wsapp = websocket.WebSocketApp(str(websocket_protocol) + "://" + str(gotify_host) + "/stream", header={"X-Gotify-Key": str(gotify_token)},
                              on_open=on_open,
                              on_message=on_message,
                              on_error=on_error,
                              on_close=on_close)
    wsapp.run_forever()
