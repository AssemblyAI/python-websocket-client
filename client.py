import json


def on_message(ws, message):
    data = json.loads(message)
    print(data)


def on_error(ws, error):
    print("Error: %s" % error)


def on_close(ws):
    print("### closed ###")
