from django.shortcuts import render

# Create your views here.
# eagle 오늘, 어제 경기 정보
from rest_framework.views import APIView
from slackbot import games, verify_requests
from datetime import date, timedelta
from rest_framework.response import Response
from rest_framework import status
import requests
import json


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

    if verify_requests(request.META, request.data):
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
    else:
      return Response(status=status.HTTP_401_UNAUTHORIZED)


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