from rest_framework.response import Response
from rest_framework import status
import hmac
import time


def verify_slack_request(header, body):
  slack_signing_secret = '8c91f513bae502d0ed124a2d23c05cf2'
  ts = header['X-Slack-Request-Timestamp']

  if time.time() - ts > 60 * 5:
    return Response(status=status.HTTP_401_UNAUTHORIZED)

  sig_basestring = 'v0:' + ts + ':' + body
  my_signature = 'v0=' + hmac.compute_hash_sha256(slack_signing_secret, sig_basestring).hexdigest()

  slack_signature = header['X-Slack-Signature']

  if not hmac.compare(my_signature, slack_signature):
    return Response(status=status.HTTP_401_UNAUTHORIZED)