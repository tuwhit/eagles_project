from django.shortcuts import render

# Create your views here.
import requests
import datetime
from bs4 import BeautifulSoup


def get_eagles_recent_score():
    try:
        resp = requests.get('http://www.hanwhaeagles.co.kr/html/main/main.asp')
        soup = BeautifulSoup(resp.text, 'html.parser')

        prev = soup.find("div", "prevGame")
        prev_left_team = prev.find("div", "left").find('img', alt=True)['alt']
        prev_right_team = prev.find("div", "right").find('img', alt=True)['alt']
        prev_score = prev.find_all("strong")
        prev_tmp = prev.find("div", "date").get_text()
        str = prev_tmp + '\n' + prev_left_team + ' ' + prev_score[0].get_text() + ' : ' + prev_score[
            1].get_text() + ' ' + prev_right_team + '\n\n'

        recent = soup.find("div", "liveGame")
        recent_list = recent.find_all("strong")
        recent_tmp = recent.find("div", "date").get_text()
        str += recent_tmp + '\n' + recent_list[0].get_text() + ' ' + recent_list[2].get_text() + ' : ' + recent_list[
            3].get_text() + ' ' + recent_list[1].get_text()

        response = {
            "text": "Recent Games",
            "attachments": [
                {
                    "text": str
                }
            ]
        }

    except:
        response = {
            "text": "Recent Games",
            "attachments": [
                {
                    "text": "Not Baseball Season"
                }
            ]
        }

    return response


def get_all_games(date):
    try:
        # TODO: team setting
        year = date.split('-')[0]
        month = date.split('-')[1]
        day = date.split('-')[2]
        weekday = get_weekday(date)
        resp = f'{date}({weekday})'

        url = f'https://sports.news.naver.com/kbaseball/schedule/index.nhn?date=20190323&month={month}&year={year}'

        score_page = requests.get(url)
        soup = BeautifulSoup(score_page.text, 'html.parser')

        search_text = str(int(month)) + '.' + str(int(day))
        date_td = soup.find('strong', string=search_text)

        if date_td:
            tbody = date_td.parent.parent.parent.parent

            if tbody.find('span', 'td_none'):
                resp += ' 경기가 없습니다.'
            else:
                rows = tbody.find_all('tr')

                for row in rows:
                    left_team = row.find('span', 'team_lft').text
                    right_team = row.find('span', 'team_rgt').text
                    score = row.find('strong', 'td_score').text
                    stadium = row.find_all('span', 'td_stadium')[1].text

                    resp += f'\n{left_team} {score} {right_team} ({stadium}구장)'
        else:
            resp += ' 경기가 없습니다.'

        return resp

    except:
        print('error')


def get_game_score(team, date):
    try:
        # TODO: team setting
        year = date.split('-')[0]
        month = date.split('-')[1]
        day = date.split('-')[2]
        weekday = get_weekday(date)
        resp = f'{date}({weekday}) '

        url = f'https://sports.news.naver.com/kbaseball/schedule/index.nhn?date=20190323&month={month}&year={year}&teamCode={team}'

        score_page = requests.get(url)
        soup = BeautifulSoup(score_page.text, 'html.parser')

        search_text = str(int(month)) + '.' + str(int(day))
        date_td = soup.find('strong', string=search_text)

        if date_td:
            row = date_td.parent.parent.parent

            if row.find('span', 'td_none'):
                resp += '경기가 없습니다.'
            else:
                left_team = row.find('span', 'team_lft').text
                right_team = row.find('span', 'team_rgt').text
                score = row.find('strong', 'td_score').text
                stadium = row.find_all('span', 'td_stadium')[1].text

                resp += f'{left_team} {score} {right_team} ({stadium}구장)'
        else:
            resp += '경기가 없습니다.'

        return resp

    except:
        print('error')


def get_weekday(date):
    week_day = ['월', '화', '수', '목', '금', '토', '일']
    date = datetime.date(int(date.split('-')[0]), int(date.split('-')[1]), int(date.split('-')[2]))

    return week_day[date.weekday()]