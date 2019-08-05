import sys
import time
import thread
import websocket
import json

from client import on_error, on_close

final_transcript = []
prior_message_id = None
AUTHENTICATED = False


def read_file_in_chunks(file_object, chunk_size=2048):
    """Lazy function (generator) to read a file chunk by chunk."""
    i = 0
    while True:
        data = file_object.read(chunk_size)

        # strip headers from wav file on first iteration
        if i == 0:
            data = data[44:]
        i += 1

        if not data:
            break
        yield data


def print_transcript(ws, message):
    global prior_message_id
    global AUTHENTICATED

    data = json.loads(message)
    if data['msgId'] == prior_message_id:
        return

    if data.get('status'):
        print(data)

        if data['status'] == 'ready':
            AUTHENTICATED = True

        return
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


def send_file_over_ws(ws):
    global AUTHENTICATED

    with open(sys.argv[3], 'rb') as _in:
        data = _in.read()

    chunk_read_size = 2048
    num_frames = len(data)-44
    audio_duration_ms = (num_frames / 8000.0 / 2.0) * 1000.0
    num_chunks_to_read = len(data) / chunk_read_size
    ms_per_chunk = audio_duration_ms / num_chunks_to_read
    sec_per_chunk = ms_per_chunk / 1000.0

    def run():
        while AUTHENTICATED is False:
            continue

        f = open(sys.argv[3])
        start = time.time()
        for chunk in read_file_in_chunks(f, chunk_size=chunk_read_size):

            # the opcode is necessary otherwise the API won't
            # be able to consume the binary data!
            ws.send(chunk, opcode=websocket.ABNF.OPCODE_BINARY)

            # simulate playback speed uploading
            upload_time = (time.time()-start)
            wait_diff = (sec_per_chunk*0.95) - upload_time
            if wait_diff > 0.0:
                time.sleep(wait_diff)
            start = time.time()

    thread.start_new_thread(run, ())


websocket.enableTrace(True)
ws = websocket.WebSocketApp("ws://%s/websocket?apiToken=%s" % (sys.argv[1], sys.argv[2]),
                            on_message=print_transcript,
                            on_error=on_error,
                            on_close=on_close)
websocket.enableTrace(False)
ws.on_open = send_file_over_ws
ws.run_forever()
