# rest-api-authen-sample

A simple server-client REST API HMAC authentication using Python.

## Usage:
1. Run `python3 server.py`. The dummy server will run on `http://localhost:9394`.
2. Run 'python3 client.py <publicKey> <privateKey> <sampleValue>' to send the request to server.

Notice: The request timeout will be 1 minute to prevent replay attack.