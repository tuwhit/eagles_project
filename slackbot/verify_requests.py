from rest_framework.response import Response
from rest_framework import status
import hmac
import hashlib
import time


def verify(header, data):
  if 'HTTP_X_SLACK_REQUEST_TIMESTAMP' not in header or 'HTTP_X_SLACK_SIGNATURE' not in header:
    return Response(status=status.HTTP_401_UNAUTHORIZED)

  timestamp = header['HTTP_X_SLACK_REQUEST_TIMESTAMP']
  signature = header['HTTP_X_SLACK_SIGNATURE']
  slack_signing_secret = '8c91f513bae502d0ed124a2d23c05cf2'

  if time.time() - float(timestamp) > 60 * 5:
    return Response(status=status.HTTP_401_UNAUTHORIZED)

  sig_basestring = 'v0:' + timestamp + ':' + data.urlencode()
  my_signature = 'v0=' + hmac.new(bytes(slack_signing_secret, 'utf-8'), sig_basestring.encode('utf-8'), hashlib.sha256).hexdigest()

  if not hmac.compare_digest(my_signature, signature):
    return Response(status=status.HTTP_401_UNAUTHORIZED)