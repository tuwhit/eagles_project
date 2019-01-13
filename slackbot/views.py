from django.shortcuts import render

# Create your views here.
# eagle 오늘, 어제 경기 정보
from rest_framework.views import APIView
from slackbot import games
from datetime import date, timedelta
from rest_framework.response import Response
from rest_framework import status


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