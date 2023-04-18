"""Getting Started Example for Python 2.7+/3.3+"""
from gpiozero import LED, Button, LEDBoard
from boto3 import Session
from botocore.exceptions import BotoCoreError, ClientError
from contextlib import closing
import os
import sys
import subprocess
from tempfile import gettempdir
from time import sleep

import asyncio

# This example uses the sounddevice library to get an audio stream from the
# microphone. It's not a dependency of the project but can be installed with
# `pip install sounddevice`.
import sounddevice


from amazon_transcribe.client import TranscribeStreamingClient
from amazon_transcribe.handlers import TranscriptResultStreamHandler
from amazon_transcribe.model import TranscriptEvent


leds =  LEDBoard(18,23,24,pwm=True)
leds.value=(0,0,0)
#ledb1=LEDBoard(24).values
#ledb2=LEDBoard(23).values
#ledb3=LEDBoard(18).values
button = Button(21) 
b=0
a=""
# Create a client using the credentials and region defined in the [adminuser]
# section of the AWS credentials file (~/.aws/credentials).
session = Session(profile_name="default")
polly = session.client("polly")

def awstts(string_input):
    response = polly.synthesize_speech(Text=string_input, OutputFormat="mp3",
                                        VoiceId="Seoyeon")
    # Access the audio stream from the response
    if "AudioStream" in response:
            with closing(response["AudioStream"]) as stream:
                output = os.path.join(gettempdir(), "speech.mp3")

                try:
                 # Open a file for writing the output as a binary stream
                    with open(output, "wb") as file:
                          file.write(stream.read())
                except IOError as error:
                    # Could not write to file, exit gracefully
                    print(error)
                    sys.exit(-1)

    else:
        # The response didn't contain audio data, exit gracefully
        print("Could not stream audio")
        sys.exit(-1)

    # Play the audio using the platform's default player
    if sys.platform == "win32":
        os.startfile(output)
    else:
        # The following works on macOS and Linux. (Darwin = mac, xdg-open = linux).
        subprocess.call(["mpg321", output])



class MyEventHandler(TranscriptResultStreamHandler):
    async def handle_transcript_event(self, transcript_event: TranscriptEvent):
        # This handler can be implemented to handle transcriptions as needed.
        # Here's an example to get started.
        results = transcript_event.transcript.results
        for result in results:
            for alt in result.alternatives:
                print(alt.transcript)
                a=alt.transcript
                if a=="Every own" and leds.value!=(1,1,1):
                    print("킴")
                    leds.on()
                    awstts("LED를 모두 켰어요")
                elif a=="Every kid."and leds.value!=(0,0,0):
                    print("LED를 껐어요")
                    leds.off()
                    awstts("LED를 모두 껐어요")
                elif a=="Read on" and leds.value!=(1,0,0):
                    print("LED를 껐어요")
                    leds.value=(1,0,0)
                    awstts("빨간 LED를 켰어요")    
                elif a=="Yellow own."and leds.value!=(0,1,0):
                    print("LED를 껐어요")
                    leds.value=(0,1,0)
                    awstts("노란 LED를 켰어요")
                elif a=="Green on"and leds.value!=(0,0,1):
                    print("LED를 껐어요")
                    leds.value=(0,0,1)
                    awstts("초록 LED를 켰어요")
                elif a=="Green kill."and leds.value!=(0,0,0):
                    print("LED를 껐어요")
                    leds.value=(0,0,0)
                    awstts("초록 LED를 껐어요")
                elif a=="Yellow kid."and leds.value!=(0,0,0):
                    print("LED를 껐어요")
                    leds.value=(0,0,0)
                    awstts("노란 LED를 껐어요")
                elif a=="Rather kid."and leds.value!=(0,0,0):
                    print("LED를 껐어요")
                    leds.value=(0,0,0)
                    awstts("빨간 LED를 껐어요")      
                elif a=="Down."and leds.value!=(0.2,0.2,0.2):
                    print("LED를 껐어요")
                    leds.value=(0.2,0.2,0.2)
                    awstts("밝기를 낮추어 드릴게요")
                elif a=="Oh,"and leds.value!=(1,1,1):
                    print("LED를 껐어요")
                    leds.value=(1,1,1)
                    awstts("밝기를 높여 드릴게요")    
                elif a=="Being being"and leds.value!=(0,0,1):
                    print("LED를 껐어요")
                    awstts("빙빙 돌아라 이야압")
                    for i in range (11):
                        leds.value=(1,0,0)
                        sleep(0.2)
                        leds.value=(0,1,0)
                        sleep(0.2)
                        leds.value=(0,0,1)
                        sleep(0.2)
                elif a=="Back."and leds.value!=(0,1,0):
                    print("LED를 껐어요")
                    awstts("거꾸로 돌아라 이야압")
                    for i in range (10):
                        leds.value=(0,1,0)
                        sleep(0.2)
                        leds.value=(1,0,0)
                        sleep(0.2)
                        leds.value=(0,0,1)
                        sleep(0.2)
                        leds.value=(0,1,0)
                elif a=="Show."and leds.value!=(1,0,1):
                    awstts("신나게 춤을 춰봐요")
                    for i in range (5):
                        leds.on()
                        sleep(0.1)
                        leds.off()
                        sleep(0.1)
                        leds.value=(1,0,0)
                        sleep(0.2)
                        leds.value=(0,1,0)
                        sleep(0.2)
                        leds.value=(0,0,1)
                        sleep(0.2)
                        leds.value=(1,1,0)
                        sleep(0.2)
                        leds.value=(0,1,1)
                        sleep(0.2)
                        leds.value=(1,0,1)
                        sleep(0.2)
                        leds.off()

                    
async def mic_stream():
    # This function wraps the raw input stream from the microphone forwarding
    # the blocks to an asyncio.Queue.
    loop = asyncio.get_event_loop()
    input_queue = asyncio.Queue()

    def callback(indata, frame_count, time_info, status):
        loop.call_soon_threadsafe(input_queue.put_nowait, (bytes(indata), status))

    # Be sure to use the correct parameters for the audio stream that matches
    # the audio formats described for the source language you'll be using:
    # https://docs.aws.amazon.com/transcribe/latest/dg/streaming.html
    stream = sounddevice.RawInputStream(
        channels=1,
        samplerate=44100,
        callback=callback,
        blocksize=1024 * 2,
        dtype="int16",
    )
    # Initiate the audio stream and asynchronously yield the audio chunks
    # as they become available.
    with stream:
        while True:
            indata, status = await input_queue.get()
            yield indata, status


async def write_chunks(stream):
    # This connects the raw audio chunks generator coming from the microphone
    # and passes them along to the transcription stream.
    async for chunk, status in mic_stream():
        await stream.input_stream.send_audio_event(audio_chunk=chunk)
    await stream.input_stream.end_stream()


async def basic_transcribe():
    # Setup up our client with our chosen AWS region
    client = TranscribeStreamingClient(region="us-west-2")

    # Start transcription to generate our async stream
    stream = await client.start_stream_transcription(
        language_code="en-US",
        media_sample_rate_hz=44100,
        media_encoding="pcm",
    )

    # Instantiate our handler and start processing events
    handler = MyEventHandler(stream.output_stream)
    await asyncio.gather(write_chunks(stream), handler.handle_events())



if __name__ == "__main__":
    awstts("등록하신 기능을 말씀하세요")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(basic_transcribe())
    loop.close()

