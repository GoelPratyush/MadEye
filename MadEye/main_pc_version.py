from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import tinify
import datetime
import random as rand
from xml.etree import ElementTree
import re
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from msrest.authentication import CognitiveServicesCredentials
import http.client, urllib.parse
from builtins import input
from utils import create_uber_client
from utils import fail_print
from utils import import_oauth2_credentials
from utils import paragraph_print
from utils import response_print
from utils import success_print
from uber_rides.client import SurgeError
from uber_rides.errors import ClientError
from uber_rides.errors import ServerError
import face_recognition
import os
import shutil
from time import sleep
import urllib.request
import pyap
import playsound
import azure.cognitiveservices.speech as speechsdk
import requests
import json
from PIL import Image
import cv2
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from pynput import keyboard
from pynput.keyboard import Key
import time
import subprocess
import soundfile as sf
import pyttsx3
import socket
import connect_to_internet
import sys
import dlib
import imutils
from imutils.video import VideoStream
from imutils.face_utils import FaceAligner
import geocoder

if os.path.exists(os.path.join(os.getcwd(), 'folder_images')):
    pass
else:
    os.mkdir(os.path.join(os.getcwd(), 'folder_images'))

if os.path.exists(os.path.join(os.getcwd(), 'tempimages')):
    pass
else:
    os.mkdir(os.path.join(os.getcwd(), 'tempimages'))

if os.path.exists(os.path.join(os.getcwd(), 'majortempaud')):
    # os.rmdir(os.path.join(os.getcwd(), 'majortempaud'))
    shutil.rmtree(os.path.join(os.getcwd(), 'majortempaud'))
    os.mkdir(os.path.join(os.getcwd(), 'majortempaud'))
else:
    os.mkdir(os.path.join(os.getcwd(), 'majortempaud'))

if os.path.exists(os.path.join(os.getcwd(), 'temp.mp3')):
    os.remove('temp.mp3')

bingMapsKey = 'AjrMuCn_mhj4OpWb0BYeh8foytxO6xpaRwc6v1fUqVCQcDzimbgGwOWTb7xxcrXW'
tinify.key = "9XjdCVxnjNjqpfsK48qXlwxLhtwDS4pQ"
state = 0
latitude=''
longitude=''

def on_release_d(key):
    try:
        print(' {0} is pressed'.format(key))
        if key == Key.up:
            # Stop listener
            return False
    except AttributeError:
        print('Wrong key {0} pressed'.format(key))


def on_release_generic(key):
    try:
        global state
        print(' {0} is presses'.format(key))
        if key == Key.right:
            state=1
            return False
        elif key == Key.down:
            state=3
            return False
        elif key == Key.up:
            speak_label('goodbye')
            os._exit(0)
            return False
        elif key ==Key.left:
            state=2
            return False
        elif key.char == 'o':
            voiceassist()
            state=0
            return False
    except AttributeError:
        print(' Wrong key {0} pressed'.format(key))

def on_release_news(key):
    try:
        global state
        print(' {0} pressed'.format(key))
        if key == Key.right:
            state = 1
            return False
        elif key == Key.down:
            state = 2
            return False
        elif key == Key.left:
            state = 3
            return False
        elif key == Key.up:
            state = 4
            return False
    except AttributeError:
        print(' Wrong key {0} pressed'.format(key))  

def on_release_asd(key):
    try:
        global state
        print(' {0} is pressed'.format(key))
        if key == Key.down:
            state = 1
            return False
        elif key == Key.right:
            state = 2
            return False
        elif key == Key.left:
            state = 3
            return False
        elif key == Key.up:
            state = 4
            return False
    except AttributeError:
        print(' Wrong Key {0} pressed'.format(key))

def on_release_q(key):
    try:
        print(' {0} is pressed'.format(key))
        if key == Key.up:
            speak_label('goodbye')
            os._exit(0)
            return False
        else:
            return False
    except AttributeError:
        print(' Wrong Key {0} pressed'.format(key))

def internet(host="8.8.8.8", port=53, timeout=3):
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except Exception as e:
        print(e)
        return False

def playerasync():
    subprocess.run(['python', 'speech_init.py'])


def checker():
    with keyboard.Events() as events:
        event = events.get(sound_dur)
        # if event is not None:
        #     with keyboard.Listener(on_release=on_release_d) as listener:
        #         listener.join()
        print("Press Now")


class TextToSpeech(object):
    def __init__(self, subscription_key, texty):
        self.subscription_key = subscription_key
        self.tts = texty
        self.timestr = time.strftime("%Y%m%d-%H%M")
        self.access_token = None

def get_token(self):
    fetch_token_url = "https://centralindia.api.cognitive.microsoft.com/sts/v1.0/issuetoken"
    headers = {
        'Ocp-Apim-Subscription-Key': self.subscription_key
    }
    response = requests.post(fetch_token_url, headers=headers)
    self.access_token = str(response.text)

def save_audio(self, uid):
    base_url = 'https://centralindia.tts.speech.microsoft.com/'
    path = 'cognitiveservices/v1'
    constructed_url = base_url + path
    headers = {
        'Authorization': 'Bearer ' + self.access_token,
        'Content-Type': 'application/ssml+xml',
        'X-Microsoft-OutputFormat': 'riff-24khz-16bit-mono-pcm',
        'User-Agent': 'MadEyeSpeech'
    }
    xml_body = ElementTree.Element('speak', version='1.0')
    xml_body.set('{http://www.w3.org/XML/1998/namespace}lang', 'en-IN')
    voice = ElementTree.SubElement(xml_body, 'voice')
    voice.set('{http://www.w3.org/XML/1998/namespace}lang', 'en-IN')
    voice.set('name', 'Microsoft Server Speech Text to Speech Voice (en-IN, NeerjaNeural)')
    voice.text = self.tts
    body = ElementTree.tostring(xml_body)

    response = requests.post(constructed_url, headers=headers, data=body)
    if response.status_code == 200:
        with open(os.path.join(os.getcwd(), 'majortempaud', uid + '.wav'), 'wb') as audio:
            audio.write(response.content)

    else:
        print("\nStatus code: " + str(
            response.status_code) + "\nSomething went wrong. Check your subscription key and headers.\n")

def clock():
    try:
        something = pyttsx3.init()
        something.setProperty('rate', 160)
        something.say(datetime.datetime.now().strftime('today is %d    %m, the time is %H %M'))
        something.runAndWait()

    except Exception as e:
        print(e)

def voiceassist():
    try:
        urly = 'https://australiaeast.api.cognitive.microsoft.com/luis/prediction/v3.0/apps/4a8d7554-ab53-4710-b45a-47b86b038067/slots/staging/predict?subscription-key=ccf815c9d447441782073e716f6558ff&verbose=true&show-all-intents=true&log=true&query='
        save_speech(rand.choice(['greet1','greet2','greet3','greet4']))
        request_said = speech2text()
        response = urllib.request.urlopen(urly + urllib.parse.quote(request_said, safe='')).read().decode('utf-8')
        weathery = json.loads(response)
        intent_classified = weathery['prediction']['topIntent']
        print(intent_classified)
        eval(intent_classified + '()')

    except Exception as e:
        print(e)
        save_speech('unknownError')
        pass

def modular_speech(text):
    try:
        global sound_dur
        subscription_key = "0e87f4dde3cf4c3f927f2f8227dbd833"
        now = datetime.datetime.now()
        uid = str(now.date()) + str(now.hour) + str(now.minute) + str(now.second)
        app = TextToSpeech(subscription_key, text)
        get_token(app)
        save_audio(app, uid)
        sound_template = sf.SoundFile(os.path.join(os.getcwd(), 'majortempaud', uid + '.wav'))
        sound_dur = len(sound_template) / sound_template.samplerate
        proc = subprocess.Popen(['python', 'speech_init.py', uid])
        checker()
        proc.kill()
        sleep(2)

    except Exception as e:
        print(e)

def speak_label(mytext):
    playsound.playsound(os.path.join(os.getcwd(), 'tempaud', mytext + '.wav'))

def navigator(loc):
    try:
        """Press    -> for next direction 
                    down arrow key for current direction
                    <- for previous direction
                    up arrow key to quit the direction selection
        """
        # input information
        # longitude = mlon
        # latitude = mlat
        destination = str(loc)
        encodedDest = urllib.parse.quote(destination, safe='')
        routeUrl = "http://dev.virtualearth.net/REST/V1/Routes/Driving?wp.0=" + str(latitude) + "," + str(
            longitude) + "&wp.1=" + encodedDest + "&key=" + bingMapsKey

        request = urllib.request.Request(routeUrl)
        response = urllib.request.urlopen(request)

        r = response.read().decode(encoding="utf-8")
        result = json.loads(r)
        # print(result)
        itineraryItems = result["resourceSets"][0]["resources"][0]["routeLegs"][0]["itineraryItems"]
        route_distance = result["resourceSets"][0]["resources"][0]["travelDistance"]

        directions = []
        main_dist = []

        # pprint.pprint(result)
        for item in itineraryItems:
            if float(item["travelDistance"]) < 1:
                org_distance = str(float(item["travelDistance"]) * 1000) + ' metre '
            else:
                org_distance = str(item["travelDistance"]) + ' kilometre'

            directions.append(item["instruction"]["text"] + ' in ' + org_distance)
            main_dist.append(float(item["travelDistance"] * 1000))

        # print(main_dist)
        if(len(directions)<1):
            print("No direction found")
        count=0
        modular_speech(directions[count])

        # print(directions)
        # print(main_dist)

        while count!=len(directions):
            with keyboard.Listener(on_release=on_release_asd) as listener:
                listener.join()

            if state == 2:
                count+=1
            elif state == 3:
                count-=1
                if count<0:
                    count=0
                    print("To choose next, press ->")
                    continue
            elif state == 4:
                break
            modular_speech(directions[count])

    except Exception:
        pass

def location(address):

    try:
        g = geocoder.bing(address, key='AjrMuCn_mhj4OpWb0BYeh8foytxO6xpaRwc6v1fUqVCQcDzimbgGwOWTb7xxcrXW')
        g = geocoder.bing([g.lat,g.lng], method='reverse', key='AjrMuCn_mhj4OpWb0BYeh8foytxO6xpaRwc6v1fUqVCQcDzimbgGwOWTb7xxcrXW')
        return g.address

    except Exception  as e:
        print(e)
        pass

def speech2text():
    speech_key, service_region = "0e87f4dde3cf4c3f927f2f8227dbd833", "centralindia"
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)

    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)
    result = speech_recognizer.recognize_once()

    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print("Recognized: {}".format(result.text))
        return result.text
    elif result.reason == speechsdk.ResultReason.NoMatch:
        print("No speech could be recognized: {}".format(result.no_match_details))
        return 'None'
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print("Speech Recognition canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))
        return 'None'

def find_loc_address(address):

    try:
        # encoded_dest = urllib.parse.quote(address, safe='')
        # endpoint = 'http://dev.virtualearth.net/REST/v1/Locations?q=' + encoded_dest + '&key=' + bingMapsKey
        # request = urllib.request.Request(endpoint)
        # response = urllib.request.urlopen(request)
        # r = response.read().decode(encoding="utf-8")
        # result = json.loads(r)
        # res_Check = result["resourceSets"][0]["resources"][0]['geocodePoints'][1]['coordinates']
        if address[-1]=='.':
            address = address[:-1]
        g = geocoder.bing(address, key=bingMapsKey)
        return (g.lat,g.lng)

    except Exception:
        pass

def my_current_location():
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.support.ui import WebDriverWait

    chrome_options = Options()
    chrome_options.add_argument("--use-fake-ui-for-media-stream")
    timeout = 20
    driver = webdriver.Chrome(executable_path = './chromedriver.exe',options=chrome_options)
    driver.get("https://mycurrentlocation.net/")
    wait = WebDriverWait(driver, timeout)
    longitude = driver.find_elements_by_xpath('//*[@id="longitude"]')
    longitude = [x.text for x in longitude]
    longitude = float(longitude[0])
    latitude = driver.find_elements_by_xpath('//*[@id="latitude"]')
    latitude = [x.text for x in latitude]
    latitude = float(latitude[0])
    driver.quit()
    return [latitude, longitude]


def save_speech(mytext):
    playsound.playsound(os.path.join(os.getcwd(), 'tempaud', mytext + '.wav'))

def currentip():
    try:
        send_url = "http://api.ipstack.com/check?access_key=c687e4498fc801d7a66e9b42fb2f6e50"
        geo_req = requests.get(send_url)
        geo_json = json.loads(geo_req.text)
        ip = geo_json['ip']
        return ip
    except Exception:
        pass

def directions():
    try:
        save_speech('whereDoYouWantToGo')
        speech = speech2text()
        try:
            loc = location(speech)
        except IndexError:
            loc = speech
        loc = speech
        navigator(loc)
    except Exception as e:
        print(e)
        save_speech('error')


def weather():
    try:
        endpoint = 'http://api.openweathermap.org/data/2.5/weather?'
        api_key = 'e33c84cc9eb1157c533611a494f638a3'
        nav_request = 'lat={}&lon={}&APPID={}'.format(latitude, longitude, api_key)
        request = endpoint + nav_request
        # Sends the request and reads the response.
        response = urllib.request.urlopen(request).read().decode('utf-8')
        weather = json.loads(response)
        current_temp = weather['main']['temp']
        temp_c = current_temp - 273.15
        temp_c_str = str(int(temp_c)) + ' degree Celsius'
        descript_place = weather['name']
        modular_speech(descript_place + ' ' + temp_c_str)

    except Exception as e:
        print(e)


def uber():
    try:
        UFP_PRODUCT_ID = '26546650-e557-4a7b-86e7-6a3942445247'

        SURGE_PRODUCT_ID = 'd4abaae7-f4d6-4152-91cc-77523e8165a4'

        save_speech('whereDoYouWantToGo')
        speech = speech2text()
        try:
            loc = location(speech)
        except IndexError:
            loc = speech
        loc = speech
        END_LAT, END_LNG = find_loc_address(loc)
        def estimate_ride(api_client):

            try:
                estimate = api_client.estimate_ride(
                    product_id=SURGE_PRODUCT_ID,
                    start_latitude=latitude,
                    start_longitude=longitude,
                    end_latitude=END_LAT,
                    end_longitude=END_LNG,
                    seat_count=2
                )

            except (ClientError, ServerError) as error:
                fail_print(error)

            else:
                success_print(estimate.json)

        def update_surge(api_client, surge_multiplier):

            try:
                update_surge = api_client.update_sandbox_product(
                    SURGE_PRODUCT_ID,
                    surge_multiplier=surge_multiplier,
                )

            except (ClientError, ServerError) as error:
                fail_print(error)

            else:
                success_print(update_surge.status_code)

        def update_ride(api_client, ride_status, ride_id):

            try:
                update_product = api_client.update_sandbox_ride(ride_id, ride_status)

            except (ClientError, ServerError) as error:
                fail_print(error)

            else:
                message = '{} New status: {}'
                message = message.format(update_product.status_code, ride_status)
                success_print(message)

        def request_ufp_ride(api_client):

            try:

                estimate = api_client.estimate_ride(
                    product_id=UFP_PRODUCT_ID,
                    start_latitude=latitude,
                    start_longitude=longitude,
                    end_latitude=END_LAT,
                    end_longitude=END_LNG,
                    seat_count=2
                )
                fare = estimate.json.get('fare')

                request = api_client.request_ride(
                    product_id=UFP_PRODUCT_ID,
                    start_latitude=latitude,
                    start_longitude=longitude,
                    end_latitude=END_LAT,
                    end_longitude=END_LNG,
                    seat_count=2,
                    fare_id=fare['fare_id']
                )

            except (ClientError, ServerError) as error:
                fail_print(error)
                return

            else:
                success_print(estimate.json)
                success_print(request.json)
                return request.json.get('request_id')

        def request_surge_ride(api_client, surge_confirmation_id=None):

            try:
                request = api_client.request_ride(
                    product_id=SURGE_PRODUCT_ID,
                    start_latitude=latitude,
                    start_longitude=longitude,
                    end_latitude=END_LAT,
                    end_longitude=END_LNG,
                    surge_confirmation_id=surge_confirmation_id,
                    seat_count=2
                )

            except SurgeError as e:
                surge_message = 'Confirm surge by visiting: \n{}\n'
                surge_message = surge_message.format(e.surge_confirmation_href)
                response_print(surge_message)

                confirm_url = 'Copy the URL you are redirected to and paste here: \n'
                result = input(confirm_url).strip()

                querystring = urlparse(result).query
                query_params = parse_qs(querystring)
                surge_id = query_params.get('surge_confirmation_id')[0]

                # automatically try request again
                return request_surge_ride(api_client, surge_id)

            except (ClientError, ServerError) as error:
                fail_print(error)
                return

            else:
                success_print(request.json)
                return request.json.get('request_id')

        def get_ride_details(api_client, s):

            try:
                ride_details = api_client.get_ride_details(ride_id)

            except (ClientError, ServerError) as error:
                fail_print(error)

            else:
                success_print(ride_details.json)

        if __name__ == '__main__':
            credentials = import_oauth2_credentials()
            api_client = create_uber_client(credentials)

            # ride request with upfront pricing flow

            modular_speech("Request a ride with upfront pricing product.")
            ride_id = request_ufp_ride(api_client)

            modular_speech("Update ride status to accepted.")
            update_ride(api_client, 'accepted', ride_id)

            modular_speech("Updated ride details.")
            get_ride_details(api_client, ride_id)
            update_ride(api_client, 'in_progress', ride_id)

            modular_speech("Updated ride details.")
            get_ride_details(api_client, ride_id)

            modular_speech("Update ride status to completed.")
            update_ride(api_client, 'completed', ride_id)

            modular_speech("Updated ride details.")
            get_ride_details(api_client, ride_id)

            # ride request with surge flow

            modular_speech("Ride estimates before surge.")
            estimate_ride(api_client)

            modular_speech("Activate surge.")
            update_surge(api_client, 2.0)

            modular_speech("Ride estimates after surge.")
            estimate_ride(api_client)

            modular_speech("Request a ride with surging product.")
            ride_id = request_surge_ride(api_client)

            modular_speech("Update ride status to accepted.")
            update_ride(api_client, 'accepted', ride_id)

            modular_speech("Updated ride details.")
            get_ride_details(api_client, ride_id)
            update_ride(api_client, 'in_progress', ride_id)

            modular_speech("Updated ride details.")
            get_ride_details(api_client, ride_id)

            modular_speech("Update ride status to completed.")
            update_ride(api_client, 'completed', ride_id)

            modular_speech("Updated ride details.")
            get_ride_details(api_client, ride_id)

            modular_speech("Deactivate surge.")
            update_surge(api_client, 1.0)

    except Exception as e:
        print(e)
        pass

def whatsthat():
    try:
        samplenum=10
        count=0
        cap = cv2.VideoCapture(0)
        while True:
            now = datetime.datetime.now()
            timer = str(now.date()) + str(now.hour) + str(now.minute) + str(now.second)
            name_docu = os.path.join(os.getcwd(), 'tempimages', timer + '.jpeg')
            r, image = cap.read()
            count+=1
            cv2.waitKey(200)
            if count==samplenum:
                cv2.imwrite(name_docu, image)
                break
        cap.release()
        source = tinify.from_file(os.path.join(os.getcwd(), 'tempimages', timer + '.jpeg'))
        url = source.url

        subscription_key="a4022d424e8148f5916655d9da342cfb"
        endpoint="https://madeyecv.cognitiveservices.azure.com/"
        # Create client
        client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))
        language = "en"
        max_descriptions = str(3)
        analysis = client.describe_image(url, max_descriptions, language)
        # print(analysis)
        if len(analysis.captions) > 0:
            captionn = analysis.captions[0].text
            print(captionn)
            modular_speech(captionn)

        else:
            save_speech('unknownError')

    except Exception as e:
        print(e)

def remember():

    try:
        print("Turning ON The Video Feed")
        vs = VideoStream(src=0).start()
        
        #Loading the HOG detector
        detector = dlib.get_frontal_face_detector()
        predictor = dlib.shape_predictor('./shape_predictor_68_face_landmarks.dat')
        fa = FaceAligner(predictor , desiredFaceWidth = 256)

        samplenum=1
        count=0
        stop_time=5
        #   Timer for 5 seconds
        start = time.time()
        while (time.time()-start < stop_time and count!=samplenum):
            #reading the frames
            frame = vs.read()
            #Resize the frame
            frame = imutils.resize(frame, width=800)
            #grayscaling the image
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            #detecting faces in it
            faces = detector(gray_frame, 0)
            cv2.imshow("Live Feed",frame)
            key = cv2.waitKey(100) & 0xFF
            # if the `q` key was pressed, break from the loop
            if key == ord("q"):
                break
            if len(faces)<1:
                continue
            for face in faces:
                count+=1
                face_aligned = fa.align(frame, gray_frame, face)
                # cv2.imshow("Aligned", face_aligned)
                save_speech('nameOfPerson')
                name_person = speech2text()
                name_person.replace('.','')
                cv2.imwrite(os.path.join(os.getcwd(), 'folder_images', name_person + '.jpeg'), face_aligned)
                break

        if count==0:
            save_speech('noFaces')
        cv2.destroyAllWindows()
        vs.stop()

    except Exception as e:
        print(e)
        save_speech('unknownError')
        pass


def whoisthat():
    try:
        known_face_encodings = []
        known_face_names = []

        for i in os.listdir(os.path.join(os.getcwd(), 'folder_images')):
            shaaran_image = face_recognition.load_image_file(os.path.join(os.getcwd(), 'folder_images', i))
            shaaran_encoding = face_recognition.face_encodings(shaaran_image)[0]
            known_face_encodings.append(shaaran_encoding)
            known_face_names.append(os.path.splitext(i)[0])
        
        print("Turning ON The Video Feed")
        vs = VideoStream(src=0).start()
        
        #Loading the HOG detector
        detector = dlib.get_frontal_face_detector()
        predictor = dlib.shape_predictor('./shape_predictor_68_face_landmarks.dat')
        fa = FaceAligner(predictor , desiredFaceWidth = 256)

        samplenum=1
        count=0
        stop_time=5
        #   Timer for 5 seconds
        start = time.time()
        while (time.time()-start < stop_time and count!=samplenum):
            #reading the frames
            frame = vs.read()
            #Resize the frame
            frame = imutils.resize(frame, width=800)
            #grayscaling the image
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            #detecting faces in it
            faces = detector(gray_frame, 0)
            cv2.imshow("Live Feed",frame)
            key = cv2.waitKey(100) & 0xFF
            # if the `q` key was pressed, break from the loop
            if key == ord("q"):
                break
            if len(faces)<1:
                continue
            for face in faces:
                count+=1
                face_aligned = fa.align(frame, gray_frame, face)
                face_locations = face_recognition.face_locations(face_aligned)
                face_encodings = face_recognition.face_encodings(face_aligned, face_locations)
                face_names = []
                for face_encoding in face_encodings:

                    matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                    name = "Unknown"
                    
                    if True in matches:
                        first_match_index = matches.index(True)
                        name = known_face_names[first_match_index]

                    face_names.append(name)

                for faces in face_names:
                    modular_speech(faces)
                break

        if count==0:
            save_speech('noFaces')
        cv2.destroyAllWindows()
        vs.stop()

    except Exception as e:
        print(e)
        save_speech('unknownError')
        pass


def facts():
    try:
        subscription_key = "53977e3fbf6a412e995f5513896339e2"
        host = 'api.bing.microsoft.com'
        path = '/v7.0/search'

        save_speech('answer')
        query = speech2text()
        mkt = 'en-US'
            
        headers = {"Ocp-Apim-Subscription-Key" : subscription_key, "X-MSEdge-ClientIP":currentip()}
        params = '?mkt=' + mkt + '&q=' + urllib.parse.quote (query)
        conn = http.client.HTTPSConnection (host)
        conn.request ("GET", path + params, None, headers)
        response = conn.getresponse ()
        entity_data = json.loads(response.read())

        if entity_data['entities']['value']:
            main_entities = [entity for entity in entity_data['entities']['value'] if entity['entityPresentationInfo']['entityScenario'] == "DominantEntity"]
            if main_entities:
                main_string = main_entities[0]['description']
                print(main_string)
                modular_speech(main_string)
                
    except AttributeError:
        save_speech('unknownError')


def readit():
    try:
        subscription_key="a4022d424e8148f5916655d9da342cfb"
        endpoint="https://madeyecv.cognitiveservices.azure.com/"
        client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))
        samplenum=10
        count=0
        cap = cv2.VideoCapture(0)
        name_docu = 'tempface.jpeg'
        while True:
            r, image = cap.read()
            count+=1
            cv2.waitKey(200)
            if count==samplenum:
                cv2.imwrite(name_docu, image)
                break
        cap.release()

        source = tinify.from_file(os.path.join(os.getcwd(), name_docu))
        url = source.url
        numberOfCharsInOperationId = 36

        save_speech('waitForText')
        rawHttpResponse = client.read(url, language="en", raw=True)
        operationLocation = rawHttpResponse.headers["Operation-Location"]
        idLocation = len(operationLocation) - numberOfCharsInOperationId
        operationId = operationLocation[idLocation:]
        
        result = client.get_read_result(operationId)
        
        while result.status in [OperationStatusCodes.running, OperationStatusCodes.not_started]:
            time.sleep(1)
            result = client.get_read_result(operationId)

        main_string = ''

        if result.status == OperationStatusCodes.succeeded:

            for line in result.analyze_result.read_results[0].lines:
                main_string = main_string + ' ' + line.text

            main_string = re.sub("!|/|;|:|-", "", main_string)
            main_string = main_string.replace('|', '')
            main_string = main_string.replace('*', '')

            modular_speech(main_string)

        else:
            save_speech('unknownError')

    except Exception as e:
        print(e)
        pass

def check(text_inlet):
    try:
        text_key = '700e9ea833f047ecba5269c051a382ad'
        text_analytics_base_url = "https://madeyeta.cognitiveservices.azure.com/text/analytics/v2.1/"
        key_phrase_api_url = text_analytics_base_url + "keyPhrases"
        documents = {'documents': [
            {'id': '1', 'language': 'en',
             'text': text_inlet}
        ]}
        headers = {'Ocp-Apim-Subscription-Key': text_key}
        response = requests.post(key_phrase_api_url, headers=headers, json=documents)
        key_phrases = response.json()
        stringy = ''
        for i in key_phrases['documents'][0]['keyPhrases']:
            stringy = stringy + ' ' + i
        return stringy
    except Exception as e:
        print(e)
        pass


def news(search_term=None):
    
    try:
        subscription_key = "53977e3fbf6a412e995f5513896339e2"
        search_url = "https://api.bing.microsoft.com/v7.0/news/search"

        if search_term == None:
            save_speech('newsspeak')
            speech = speech2text()
            search_term = check(speech)
        
        headers = {"Ocp-Apim-Subscription-Key" : subscription_key}
        params  = {"q": search_term, "textDecorations": True}
        response = requests.get(search_url, headers=headers, params=params)
        news_result = json.loads(response.text)

        if news_result['value']:
            count=0
            records = len(news_result['value'])
            while(count!=records):
            # for k in news_result['value']:
                k = news_result['value'][count]
                modular_speech(k['name'])
                with keyboard.Listener(on_release=on_release_news) as listener:
                    listener.join()

                if state == 1:
                    count+=1
                    continue

                elif state == 2:
                    print(k['description'])
                    modular_speech(k['description'])
                    sleep(0.5)
                    count+=1
                    continue

                elif state == 3:
                    count-=1
                    if count<0:
                        break
                    else:
                        continue

                elif state == 4:
                    # speak_label('goodbye')
                    # os._exit(0)
                    break

        else:
            save_speech("nonews")
        
    except Exception as e:
        save_speech('unknownError')

def numbers_to_instruction(argument):
    switcher = {
        0: weather,
        1: clock,
        2: directions,
        3: uber,
        4: whatsthat,
        5: remember,
        6: whoisthat,
        7: facts,
        8: readit,
        9: news
    }
    # Get the function from switcher dictionary
    return switcher.get(argument, "Invalid instruction")

def number_to_string(argument):
    switcher = {
        0: 'weather',
        1: 'clock',
        2: 'directions',
        3: 'uber',
        4: 'whatsthat',
        5: 'remember',
        6: 'whosthat',
        7: 'facts',
        8: 'readit',
        9: 'news'
    }
    # Get the function from switcher dictionary
    return switcher.get(argument, 'Invalid choice')

def main():
    print("Please Wait ...")
    print("Finding your Location")
    global latitude
    global longitude
    latitude, longitude = my_current_location()
    print("Current Latitude is " + str(latitude) + " and longitude is " + str(longitude))
    try:
        save_speech('welcome1')
        sleep(3)

        """ Uncomment when shifting to rpy """
        # if internet():
        #     pass
        # else:
        #     connect_to_internet.main()
        count_main = 0
        while count_main != 10:
            if count_main<0:
                print("Select the right arrow key to choose the next option or down arrow key to select current option")
                count_main%=10
                continue
            speak_label(number_to_string(count_main))

            with keyboard.Listener(on_release=on_release_generic) as listener:
                listener.join()
            
            # button_next = arrow right
            # button_ok   = arrow down
            # button_back = arrow left
            # button_exit = arrrow up
            # button_voice_assist = 'o'
            if count_main==9 and state==1:
                print("press up arrow key to exit or any other key to continue looping")
                with keyboard.Listener(on_release=on_release_q) as listener:
                    listener.join()
                count_main=-1

            if state==1:
                count_main+=1
            elif state==2:
                count_main-=1
            elif state==3:
                inst = numbers_to_instruction(count_main)
                inst()
                if count_main==9:
                    print("press up arrow key to exit or any other key to continue looping")
                    with keyboard.Listener(on_release=on_release_q) as listener:
                        listener.join()
                    count_main=-1
                count_main+=1
    except KeyboardInterrupt:
        os._exit(0)
        


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        os._exit(0)
        
