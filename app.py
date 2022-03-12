import threading

from flask import Flask, request, render_template
from api_service import *
from models import Player

# server application
app = Flask(__name__)


def get_data_by_name(player, username):
    player_details = get_chess_data_by_name(username)  # get basic player stats using api

    if type(player_details) is str:  # error message !
        errors_messages.append(player_details)
    else:
        player.set_player_stats(player_details)


def get_rantings_history(player, username):
    player_ratings_history = get_rating_history(username)  # get rating history using api

    if type(player_ratings_history) is str:  # error message !
        errors_messages.append(player_ratings_history)
    else:
        player.set_rating_history(player_ratings_history)


def get_player_perf_info(player, username, game_type):
    # if game_type is not None we can display more stats from different api
    if game_type and game_type != 'unspecified':
        player_performance = get_chess_data_by_perf(username, game_type)  # get player special stats about game type

        if type(player_performance) is str:
            errors_messages.append(player_performance)
        else:
            player.set_player_performance_details(player_performance)


def get_chesscom_basic(player, username):
    basic_info = get_chesscom_data_basic(username)

    if type(basic_info) is str:  # error message !
        chesscom_errors.append(basic_info)
    else:
        player.set_chesscom_basic_info(basic_info)


def chesscom_stats(player, username, game_type):
    stats = get_chesscom_stats(username)

    if type(stats) is str:  # error message !
        chesscom_errors.append(stats)
    else:
        player.set_chesscom_stats(stats)


# GET - display index.html
@app.route('/', methods=['GET'])
def show_home_view():
    return render_template('index.html')


# POST - get data from form
@app.route('/player_stats', methods=['POST'])
def show_player_stats():
    errors_messages.clear()
    chesscom_errors.clear()

    # get username and game_type from form
    username = request.form.get("username")
    game_type = request.form.get("game_type")

    player = Player()
    get_chesscom_basic(player, username)
    chesscom_stats(player, username, game_type)

    # asynchronous queries -> the server connects to many external services at the same time
    basic_info = threading.Thread(target=get_data_by_name, args=(player, username,))
    ratings_history = threading.Thread(target=get_rantings_history, args=(player, username,))
    perf_info = threading.Thread(target=get_player_perf_info, args=(player, username, game_type,))

    basic_info.start()
    ratings_history.start()
    perf_info.start()

    basic_info.join()
    ratings_history.join()
    perf_info.join()

    if errors_messages and chesscom_errors:
        return render_template('error_info.html', message='The user you are looking for does not exist on both '
                                                          'lichess.org and chess.com. Check the correctness of the '
                                                          'entered data')

    return render_template('player_stats.html', username=username, player=player, game_type=game_type,
                           lichess=errors_messages, chesscom=chesscom_errors)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('error_info.html', message='The page you are looking for does not exist. '
                                                      'Check that the entered address is correct.')


@app.errorhandler(500)
def server_error(error):
    return render_template('error_info.html', message='I have a little problem now. Try to come back in a few minutes.')


@app.errorhandler(Exception)
def another_error(error):
    msg = 'Unfortunately, I detected a small problem. I cannot view your content. ' \
          'Please try in a moment or check if the data is correct.'
    return render_template('error_info.html', message=msg)


if __name__ == "__main__":
    errors_messages = []
    chesscom_errors = []
    app.run()
