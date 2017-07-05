"""
    Utilities for generating HMAC signature
"""

import hashlib
import hmac

DELIMITER = "\n"

# generate HMAC


def generate_hmac(secret_key, public_key, request_method, parameters, time_stamp):
    """meh"""
    # string to sign the request
    string_to_sign = public_key + DELIMITER + request_method + \
        DELIMITER + parameters + DELIMITER + time_stamp

    print("String to Sign: " + string_to_sign + "\n")

    # get the digest code
    dig = hmac.new(secret_key, msg=string_to_sign,
                   digestmod=hashlib.sha256).digest()

    # base64 decode
    signature = base64.b64encode(dig).decode()
    print("Signature: " + signature)

    return signature
