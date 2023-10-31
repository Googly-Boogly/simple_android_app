import threading
import pyaudio
import websockets
import asyncio
import os  # For file path manipulation
from pydub import AudioSegment  # For MP3 playback

# Constants for audio streaming
CHUNK_SIZE = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

class AudioStreamingService:
    def __init__(self, websocket_uri):
        self.websocket_uri = websocket_uri
        self.audio_stream = None
        self.websocket = None
        self.received_message = None  # Initialize the variable to store received messages

    def start(self):
        # Initialize audio streaming and WebSocket communication
        self.audio_stream = pyaudio.PyAudio()
        self.audio_stream_thread = threading.Thread(target=self.stream_audio)
        self.audio_stream_thread.daemon = True
        self.audio_stream_thread.start()

        # Create and set up an event loop for this thread
        self.audio_event_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.audio_event_loop)

        # Start a background task to handle incoming messages
        self.audio_event_loop.create_task(self.receive_messages())

    def stop(self):
        # Stop audio streaming and close WebSocket connection
        if self.audio_stream:
            self.audio_stream_thread.join()
            self.audio_stream.terminate()
        if self.websocket:
            self.audio_event_loop.run_until_complete(self.websocket.close())

    def stream_audio(self):
        # Create and set up an event loop for this thread
        audio_event_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(audio_event_loop)

        stream = self.audio_stream.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            frames_per_buffer=CHUNK_SIZE,
            input_device_index=1
        )

        async def send_audio_to_server(audio_stream):
            async with websockets.connect(self.websocket_uri) as websocket:
                self.websocket = websocket
                while True:
                    audio_chunk = audio_stream.read(CHUNK_SIZE)
                    await websocket.send(audio_chunk)

        audio_event_loop.run_until_complete(send_audio_to_server(stream))

    async def receive_messages(self):
        async with websockets.connect(self.websocket_uri) as websocket:
            self.websocket = websocket
            while True:
                message = await websocket.recv()
                self.handle_message(message)

    def handle_message(self, message):
        # Handle the incoming message and store it in the variable
        self.received_message = message

        # Check if the message content indicates the need to play an MP3 file
        if self.received_message == "play_mp3":
            self.play_mp3("your_mp3_file.mp3")  # Replace with your MP3 file path

    def play_mp3(self, mp3_file):
        # Check if the MP3 file exists
        if os.path.isfile(mp3_file):
            # Load and play the MP3 file
            audio = AudioSegment.from_mp3(mp3_file)
            audio.play()
        else:
            print("MP3 file not found:", mp3_file)

if __name__ == "__main__":
    # Replace 'ws://your_server_ip:port' with the actual WebSocket server URI
    service = AudioStreamingService("ws://your_server_ip:port")
    service.start()

    # You can access received messages in the variable service.received_message
    while True:
        if service.received_message:
            print("Received Message:", service.received_message)
            service.received_message = None  # Clear the message variable to avoid processing it again
