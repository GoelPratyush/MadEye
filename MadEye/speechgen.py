from azure.cognitiveservices.speech import AudioDataStream, SpeechConfig, SpeechSynthesizer, SpeechSynthesisOutputFormat
from azure.cognitiveservices.speech.audio import AudioOutputConfig
import os
speech_key, service_region = "0e87f4dde3cf4c3f927f2f8227dbd833", "centralindia"
speech_config = SpeechConfig(subscription=speech_key, region=service_region)

synthesizer = SpeechSynthesizer(speech_config=speech_config, audio_config=None)
name="welcome1"
ssml_string = open("ssml.xml", "r").read()
result = synthesizer.speak_ssml_async(ssml_string).get()
name_save = os.path.join(os.getcwd(), 'myaudio', name + '.wav')
stream = AudioDataStream(result)
stream.save_to_wav_file(name_save)
