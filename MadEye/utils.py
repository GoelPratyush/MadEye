# Copyright (c) 2017 Uber Technologies, Inc.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

"""General utilities for command line examples."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from collections import namedtuple
from yaml import safe_load
import secrets
from math import sin, cos, sqrt, atan2, radians

from uber_rides.client import UberRidesClient
from uber_rides.session import OAuth2Credential
from uber_rides.session import Session


# set your app credentials here
CREDENTIALS_FILENAME = 'example/config.rider.yaml'

# where your OAuth 2.0 credentials are stored
STORAGE_FILENAME = 'example/oauth2_session_store.yaml'

DEFAULT_CONFIG_VALUES = frozenset([
    'INSERT_CLIENT_ID_HERE',
    'INSERT_CLIENT_SECRET_HERE',
    'INSERT_REDIRECT_URL_HERE',
])

Colors = namedtuple('Colors', 'response, success, fail, end')
COLORS = Colors(
    response='\033[94m',
    success='\033[92m',
    fail='\033[91m',
    end='\033[0m',
)


def success_print(message):
    """Print a message in green text.

    Parameters
        message (str)
            Message to print.
    """
    print(COLORS.success, message, COLORS.end)


def response_print(message):
    """Print a message in blue text.

    Parameters
        message (str)
            Message to print.
    """
    print(COLORS.response, message, COLORS.end)


def fail_print(error):
    """Print an error in red text.

    Parameters
        error (HTTPError)
            Error object to print.
    """
    print(COLORS.fail, error.message, COLORS.end)


def paragraph_print(message):
    """Print message with padded newlines.

    Parameters
        message (str)
            Message to print.
    """
    paragraph = '\n{}\n'
    print(paragraph.format(message))


def import_app_credentials(filename=CREDENTIALS_FILENAME):
    """Import app credentials from configuration file.

    Parameters
        filename (str)
            Name of configuration file.

    Returns
        credentials (dict)
            All your app credentials and information
            imported from the configuration file.
    """
    with open(filename, 'r') as config_file:
        config = safe_load(config_file)

    client_id = config['client_id']
    client_secret = config['client_secret']
    redirect_url = config['redirect_url']

    config_values = [client_id, client_secret, redirect_url]

    for value in config_values:
        if value in DEFAULT_CONFIG_VALUES:
            exit('Missing credentials in {}'.format(filename))

    credentials = {
        'client_id': client_id,
        'client_secret': client_secret,
        'redirect_url': redirect_url,
        'scopes': set(config['scopes']),
    }

    return credentials


def import_oauth2_credentials(filename=STORAGE_FILENAME):
    """Import OAuth 2.0 session credentials from storage file.

    Parameters
        filename (str)
            Name of storage file.

    Returns
        credentials (dict)
            All your app credentials and information
            imported from the configuration file.
    """
    with open(filename, 'r') as storage_file:
        storage = safe_load(storage_file)

    # depending on OAuth 2.0 grant_type, these values may not exist
    client_secret = storage.get('client_secret')
    redirect_url = storage.get('redirect_url')
    refresh_token = storage.get('refresh_token')

    credentials = {
        'access_token': storage['access_token'],
        'client_id': storage['client_id'],
        'client_secret': client_secret,
        'expires_in_seconds': storage['expires_in'],
        'grant_type': storage['grant_type'],
        'redirect_url': redirect_url,
        'refresh_token': refresh_token,
        'scopes': storage['scope'],
    }

    return credentials


def create_uber_client(credentials):
    """Create an UberRidesClient from OAuth 2.0 credentials.

    Parameters
        credentials (dict)
            Dictionary of OAuth 2.0 credentials.

    Returns
        (UberRidesClient)
            An authorized UberRidesClient to access API resources.
    """
    oauth2credential = OAuth2Credential(
        client_id=credentials.get('client_id'),
        access_token=credentials.get('access_token'),
        expires_in_seconds=credentials.get('expires_in_seconds'),
        scopes=credentials.get('scopes'),
        grant_type=credentials.get('grant_type'),
        redirect_url=credentials.get('redirect_url'),
        client_secret=credentials.get('client_secret'),
        refresh_token=credentials.get('refresh_token'),
    )
    session = Session(oauth2credential=oauth2credential)
    return UberRidesClient(session, sandbox_mode=True)

def estimate_of_ride(
        product_id=None,
        start_latitude=None,
        start_longitude=None,
        start_place_id=None,
        end_latitude=None,
        end_longitude=None,
        end_place_id=None,
        seat_count=None,
    ):
    try:
        """Estimate ride details given a product, start, and end location.

        Only pickup time estimates and surge pricing information are provided
        if no end location is provided.

        Parameters
            product_id (str)
                The unique ID of the product being requested. If none is
                provided, it will default to the cheapest product for the
                given location.
            start_latitude (float)
                The latitude component of a start location.
            start_longitude (float)
                The longitude component of a start location.
            start_place_id (str)
                The beginning or pickup place ID. Only "home" or "work"
                is acceptable.
            end_latitude (float)
                Optional latitude component of a end location.
            end_longitude (float)
                Optional longitude component of a end location.
            end_place_id (str)
                The final or destination place ID. Only "home" or "work"
                is acceptable.
            seat_count (str)
                Optional Seat count for shared products. Default is 2.


        Returns
            (Response)
                A Response object containing fare id, time, price, and distance
                estimates for a ride.
        """
        args = {
            'product_id': product_id,
            'start_latitude': start_latitude,
            'start_longitude': start_longitude,
            'start_place_id': start_place_id,
            'end_latitude': end_latitude,
            'end_longitude': end_longitude,
            'end_place_id': end_place_id,
            'seat_count': seat_count
        }

        call = _api_call('POST', 'v1.2/requests/estimate', args=args)
        return call
    except:

        # approximate radius of earth in km
        R = 6373.0

        lat1 = radians(start_latitude)
        lon1 = radians(start_longitude)
        lat2 = radians(end_latitude)
        lon2 = radians(end_longitude)

        dlon = lon2 - lon1
        dlat = lat2 - lat1

        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        distance = R * c
        if distance>=50:
            return 0
        else:
            return round(distance,2)

def price(distance):
    base = 50
    price_per_km = 6
    after_20 = 12
    duration_cost = 1.5*distance
    hike = 1.2
    cost = 0
    if distance < 20:
        cost = distance*price_per_km
        distance = 0
    else:
        cost = 20*price_per_km
        distance-=20
    cost = (base+cost+distance*after_20+duration_cost)*hike
    return round(cost,2)

def expected_time():
    pick = [0, 5, 8, 10, 15, 16, 22]
    return secrets.choice(pick)