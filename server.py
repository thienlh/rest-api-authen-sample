# !/usr/bin/env python
"""
    Simulate a simple HTTP server with signature-base authentication
"""

from http.server import BaseHTTPRequestHandler, HTTPServer

import urllib.parse
import urllib.request
import urllib.error
import csv
import datetime
import utils


class S(BaseHTTPRequestHandler):
    """
        The server handle class
    """

    def _set_headers(self, response_code):
        self.send_response(response_code)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        """
            Handle GET requests
        """
        # get request parameters
        query = urllib.parse.urlparse(self.path).query
        parameters = dict(qc.split("=") for qc in query.split("&"))
        key_pairs = {}
        print(parameters)

        # read credentials into dictionary
        with open('credentials.csv', 'rb') as csv_file:
            next(csv_file)
            for row in csv.reader(csv_file, delimiter=',', quotechar='"'):
                key_pairs[row[0]] = row[1]

        public_key = parameters['publicKey']

        # decode the time stamp from request
        time_stamp = urllib.parse.unquote(parameters['timeStamp'])

        # parse the requested time to compare with current server time
        requested_time = datetime.datetime.strptime(
            time_stamp, "%Y-%m-%dT%H:%M:%S+00:00")
        print("Requested time: ", requested_time)
        # different in seconds between current time and requested time
        second_diff = (datetime.datetime.utcnow() - requested_time).seconds

        print("Remain second(s): ", 60 - second_diff)

        # response 408 if the request is timeout
        if second_diff > 60:
            print("Signature timeout!")
            self._set_headers(408)
            self.wfile.write(
                "<html><body><h1>REJECTED</h1><p>Request timeout</p></body></html>")
            return

        # decode the signature from request
        signature = urllib.parse.unquote(parameters['signature'])
        value = parameters['value']

        try:
            # get secret key (if exist)
            secret_key = key_pairs[public_key]

            # generate server's signature
            server_signature = utils.generate_hmac(
                secret_key, public_key, "GET", value, time_stamp)
            print("Server signature: " + server_signature)
            print("Signature: " + signature)
        except KeyError:
            print("Public key does not exist")
            server_signature = '-1'

        if signature == server_signature:
            # request accepted
            print("Request accepted!")
            self._set_headers(200)
            self.wfile.write(
                "<html><body><h1>SUCCESS</h1><p>Request allowed</p></body></html>")
        else:
            # request denied
            print("Request denied!")
            self._set_headers(403)
            self.wfile.write(
                "<html><body><h1>DENIED</h1><p>Request denied!</p></body></html>")


def run(server_class=HTTPServer, handler_class=S, port=9394):
    """
        Run the dummy server
    """
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print('Server started on port 9394...')
    httpd.serve_forever()


if __name__ == "__main__":
    run()
