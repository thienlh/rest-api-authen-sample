"""Construct a simple HTTP GET request and send it to the dummy server"""

import argparse
import urllib.request
import urllib.parse
import urllib.error
import datetime
import utils


def send_request(secret_key, public_key, value):
    """
        Construct the request and send it to server
    """
    # get current utc time as time stamp
    time_stamp = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S+00:00")

    # generate the signature
    signature = utils.generate_hmac(secret_key, public_key, "GET", value, time_stamp)

    # construct the request
    signed_request = "http://localhost:9394?value=" + value + \
                     "&publicKey=" + public_key + \
                     "&signature=" + urllib.parse.quote(signature) + \
                     "&timeStamp=" + urllib.parse.quote(time_stamp)

    print("Signed request: " + signed_request + "\n")

    # send to server and print response
    print("Response: ")
    print(urllib.request.urlopen(signed_request).read())


if __name__ == '__main__':
    # parse the command line arguments
    parser = argparse.ArgumentParser(description='Rest API authentication demo.')
    parser.add_argument('public-key', type=str, help='Public key')
    parser.add_argument('secret-key', type=str, help='Secret key')
    parser.add_argument('value', type=str, help='Some demo value')

    # parser.add_argument('--sum', dest='accumulate', action='store_const',
    #                     const=sum, default=max,
    #                     help='sum the integers (default: find the max)')
    args = vars(parser.parse_args())

    print(args)

    # send request
    send_request(args['secret-key'], args['public-key'], args['value'])
