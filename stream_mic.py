import sys
import thread
import json
import websocket

from read_from_mic import record
from client import on_error, on_close


final_transcript = []
prior_message_id = None


def print_transcript(ws, message):
    global prior_message_id
    data = json.loads(message)
    if data['msgId'] == prior_message_id:
        return

    if data.get('status'):
        print(data)
        return

    print("\033c")

    if data['isFinal'] is True:
        final_transcript.append(data['text'])
        print_text = ' '.join(final_transcript)
        sys.stdout.write("\r%s" % print_text)
    else:
        final_words = ' '.join([w['text'] for w in data['words'] if w['intermed'] is False])
        intermed_words = ' '.join([w['text'] for w in data['words'] if w['intermed'] is True])
        partial_text = '\033[4m' + intermed_words + '\033[0m'
        print_text = ' '.join(final_transcript + [final_words, partial_text])
        sys.stdout.write("\r%s" % print_text)

    sys.stdout.flush()
    prior_message_id = data['msgId']


def talk_over_ws(ws):
    def run():
        for chunk in record():
            ws.send(chunk, opcode=websocket.ABNF.OPCODE_BINARY)

    thread.start_new_thread(run, ())


websocket.enableTrace(True)
ws = websocket.WebSocketApp("wss://%s/websocket?apiToken=%s" % (sys.argv[1], sys.argv[2]),
                            on_message=print_transcript,
                            on_error=on_error,
                            on_close=on_close)
websocket.enableTrace(False)
ws.on_open = talk_over_ws
ws.run_forever()
