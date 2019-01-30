from django.http import QueryDict
from django.shortcuts import render
from rest_framework.views import APIView
from slackbot import games
from datetime import date, timedelta
from rest_framework.response import Response
from rest_framework import status
import time
import requests
import json
import logging
import hmac
import hashlib
import base64


def index(request):
  return render(request, 'slackbot/index.html')


class eagles(APIView):
  def post(self, request):
    response = {
      'response_type': 'in_channel',
      'text': '한화 이글스 스코어',
      'attachments': [
        {
          'text': None
        }
      ]
    }

    try:
      if 'text' in request.data and request.data['text']:
        score_str = games.get_game_score('HH', request.data['text'])
      else:
        # 오늘, 어제 경기 스코어 가져옴
        today = date.today()
        yesterday = today - timedelta(1)

        score_str = games.get_game_score('HH', str(yesterday)) + '\n' + games.get_game_score('HH', str(today))

      response['attachments'][0]['text'] = score_str

      return Response(response, status=status.HTTP_200_OK)
    except:
      response['attachments'][0]['text'] = '스코어를 불러오는데 문제가 발생했습니다.'

      return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class kbo(APIView):
  def post(self, request):
    response = {
      'response_type': 'in_channel',
      'text': 'KBO 스코어',
      'attachments': [
        {
          'text': None
        }
      ]
    }

    slack_signing_secret = '8c91f513bae502d0ed124a2d23c05cf2'
    ts = request.META['HTTP_X_SLACK_REQUEST_TIMESTAMP']

    if time.time() - float(ts) > 60 * 5:
      return Response(status=status.HTTP_401_UNAUTHORIZED)

    print('request_print', request.data)
    sig_basestring = 'v0:' + ts + ':' + request.data.urlencode()
    print('sig_gasestring_print', sig_basestring)
    my_signature = 'v0=' + hmac.new(bytes(slack_signing_secret), sig_basestring.encode('utf-8'), hashlib.sha256).hexdigest()
    print('my_signature_print', my_signature)
    # my_signature = 'v0=' + hmac.compute_hash_sha256(slack_signing_secret, sig_basestring).hexdigest()

    slack_signature = request.META['HTTP_X_SLACK_SIGNATURE']
    print('slack signature', slack_signature)

    if not hmac.compare_digest(my_signature, slack_signature):
      return Response(status=status.HTTP_401_UNAUTHORIZED)

    try:
      if 'text' in request.data and request.data['text']:
        score_str = games.get_all_games(request.data['text'])
      else:
        # 오늘, 어제 경기 스코어 가져옴
        today = date.today()
        yesterday = today - timedelta(1)

        score_str = games.get_all_games(str(yesterday)) + '\n' +  games.get_all_games(str(today))

      response['attachments'][0]['text'] = score_str

      return Response(response, status=status.HTTP_200_OK)
    except:
      response['attachments'][0]['text'] = '스코어를 불러오는데 문제가 발생했습니다.'

      return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class auth(APIView):
  def get(self, request):
    code = request.query_params['code']
    data = {
      'client_id': '519504107603.518871462800',
      'client_secret': 'a5eba39c4d6606516b53ff3468ca7459',
      'code': code
    }

    # TODO: 예외 처리
    r = requests.post('https://slack.com/api/oauth.access', data)
    response = json.loads(r.text)

    # 이건 어따쓰는거지?
    # access_token = response['access_token']

    # TODO: template  수정
    if response['ok']:
      return render(request, 'slackbot/auth_success.html')
    else:
      return render(request, 'slackbot/auth_fail.html')