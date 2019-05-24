### Websocket Client Demo

**Install Python dependencies (Mac OSX only)**

> This will work on Ubuntu as well, you'll just need to use `apt` to install `portaudio` (below) instead of `brew`.

```
brew install portaudio
```

> If you don't have Homebrew, you can install it with `/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"`

```
pip install -r requirements.txt
```

### Stream Audio File

This script will stream an audio file to the AssemblyAI WebSocket API. Transcripts will show up in the terminal as the file is uploaded.

```
python stream_file.py websocket.assemblyai.com <your api token> /path/to/file.wav
```

**Audio files must be in the following format:**

- **Single channel (mono)**
- **8000 sampling rate** 
- **16-bit Signed Integer PCM encoding (wav file)**

If you are unsure, we recommend using `sox` to inspect the audio file by running: `soxi /path/to/audio.wav`. The output should look something like this:

```
Input File     : '/Users/me/Downloads/myaudiofile.wav'
Channels       : 1
Sample Rate    : 8000
Precision      : 16-bit
Duration       : 00:00:32.94 = 263499 samples ~ 2470.3 CDDA sectors
File Size      : 527k
Bit Rate       : 128k
Sample Encoding: 16-bit Signed Integer PCM
```

### Stream from Microphone

This script will stream audio from your machine's microphone to the AssemblyAI WebSocket API. Transcripts will show up in the terminal as you speak. 

```
python stream_mic.py <hostname of API, eg: websocket.assemblyai.com>
```


