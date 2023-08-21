import websocket
import ntfy
import json
import os

pushover_userkey = os.environ['PUSHOVER_USERKEY']
gotify_host = os.environ['GOTIFY_HOST']
gotify_token = os.environ['GOTIFY_TOKEN']

def on_message(ws, message):
    print(message)
    msg = json.loads(message)
    ntfy.notify(msg['message'],msg['title'], backend='pushover', user_key=pushover_userkey)

def on_error(ws, error):
    print(error)

def on_close(ws, close_status_code, close_msg):
    print("### closed ###")

def on_open(ws):
    print("Opened connection")

if __name__ == "__main__":
    wsapp = websocket.WebSocketApp("wss://" + str(gotify_host) + "/stream", header={"X-Gotify-Key": str(gotify_token)},
                              on_open=on_open,
                              on_message=on_message,
                              on_error=on_error,
                              on_close=on_close)
    wsapp.run_forever()
