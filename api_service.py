import json
import requests

base_url = 'https://lichess.org/api/user/'
error_4xx_msg = 'I cannot find the user with the given username or game type on lichess. ' \
                'Check the correctness of the entered data. '
error_5xx_msg = 'Unfortunately, I cannot get a connection at this point. Please try again in a moment.'

chesscom_base_url = 'https://api.chess.com/pub/player/'
chesscom404 = 'Unfortunately, the user with the given name does not exist on chesscom'


def check_errors(response, *args):
    if 400 <= response.status_code < 500:
        return error_4xx_msg if not args else args[0]
    elif 500 <= response.status_code < 600:
        return error_5xx_msg
    elif 200 <= response.status_code < 300:
        return json.loads(response.content)


def get_chess_data_by_name(username):
    response = requests.get(base_url + username)
    return check_errors(response)


def get_chess_data_by_perf(username, perf):
    response = requests.get(base_url + f'{username}/perf/{perf}')
    return check_errors(response)


def get_rating_history(username):
    response = requests.get(base_url + f'{username}/rating-history')
    return check_errors(response)


def get_chesscom_data_basic(username):
    response = requests.get(chesscom_base_url + username)
    return check_errors(response, chesscom404)


def get_chesscom_stats(username):
    response = requests.get(chesscom_base_url + f'{username}/stats')
    return check_errors(response, chesscom404)
