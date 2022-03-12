# functions for processing received data
from datetime import datetime


def get_no_games(game_type, result):
    if game_type:
        return game_type["record"][result]
    return 0


class Player:
    def __init__(self):
        self.username = None
        self.title = None
        self.created_date = None
        self.online = None
        self.country = None
        self.location = None
        self.first_name = None
        self.last_name = None
        self.no_games = None
        self.games_against_ai = None
        self.games_against_human = None
        self.no_draws = None
        self.no_wins = None
        self.no_losses = None
        self.rating_specify = None
        self.percentile = None
        self.progress_specify = None
        self.rank = None
        self.perfs = None
        self.profile = None
        self.count = None
        self.best_win = []
        self.worst_loss = []
        self.ratings_history = []
        self.chesscom_followers = None
        self.chesscom_last_online = None
        self.chesscom_joined = None
        self.chesscom_daily = None
        self.chesscom_rapid = None
        self.chesscom_bullet = None
        self.chesscom_blitz = None

    def get_all_chesscom_games(self):
        no_games = 0
        no_games += self.get_all_chesscom_games_by_result('win') + self.get_all_chesscom_games_by_result('draw') + \
                    self.get_all_chesscom_games_by_result('loss')

        return no_games

    def get_all_chesscom_games_by_result(self, result):
        no_games = 0
        no_games += get_no_games(self.chesscom_daily, result)
        no_games += get_no_games(self.chesscom_rapid, result)
        no_games += get_no_games(self.chesscom_bullet, result)
        no_games += get_no_games(self.chesscom_blitz, result)
        return no_games

    def set_chesscom_basic_info(self, response):
        self.chesscom_followers = response.get('followers', 'no data')
        self.chesscom_joined = datetime.fromtimestamp(response.get('joined', 0))
        self.chesscom_last_online = datetime.fromtimestamp(response.get('last_online', 0))

    def set_chesscom_stats(self, response):
        self.chesscom_daily = response.get('chess_daily', None)
        self.chesscom_rapid = response.get('chess_rapid', None)
        self.chesscom_bullet = response.get('chess_bullet', None)
        self.chesscom_blitz = response.get('chess_blitz', None)

    def set_player_stats(self, response):
        self.username = response.get('username', 'no data')
        self.title = response.get('title', 'amateur')
        self.created_date = datetime.fromtimestamp(response.get('createdAt', 0) // 1000)
        self.online = 'yes' if response.get('online', '') else 'no'
        self.profile = response.get('profile', 'no data')
        self.count = response.get('count', 'no_data')
        self.perfs = response.get('perfs', '')

        keys_to_delete = []
        if self.perfs:
            for key, value in self.perfs.items():
                if key in ['bullet', 'blitz', 'rapid', 'classical', 'correspondence', 'puzzle']:
                    for vkey, vvalue in value.items():
                        if vkey == 'games' and vvalue == 0:
                            keys_to_delete.append(key)
                else:
                    keys_to_delete.append(key)

            for k in keys_to_delete:
                self.perfs.pop(k, None)

        self.set_profile_details()
        self.set_games_details()

    def set_player_performance_details(self, response):
        self.rating_specify = response.get('perf').get('glicko').get('rating', 'no data')
        self.percentile = response.get('percentile', 'no data')
        self.percentile = 'no data' if not self.percentile else self.percentile
        self.progress_specify = response.get('perf').get('progress', 'no data')
        self.rank = response.get('rank', 'no data')
        self.rank = 'no data' if not self.rank else self.rank
        self.best_win = response.get('stat').get('bestWins').get('results')
        self.best_win = self.best_win[0].get('opInt') if self.best_win else 'no data'
        self.worst_loss = response.get('stat').get('worstLosses').get('results')
        self.worst_loss = self.worst_loss[0].get('opInt') if self.worst_loss else 'no data'

    def get_perf_details(self, game_type):
        game = None
        if game_type == 'bullet':
            game = self.chesscom_bullet
        elif game_type == 'blitz':
            game = self.chesscom_blitz
        elif game_type == 'rapid':
            game = self.chesscom_rapid
        elif game_type == 'classical' or game_type == 'correspondence' or game_type == 'daily':
            game = self.chesscom_daily
        if game:
            last_date = 'no data' if not game.get('last', '') else datetime.fromtimestamp(game.get('last', 0).get('date', ''))
            best_date = 'no data' if not game.get('best', '') else datetime.fromtimestamp(game.get('best', 0).get('date', ''))
            last_rating = 'no data' if not game.get('last', '') else game.get('last', None).get('rating', '')
            best_rating = 'no data' if not game.get('best', '') else game.get('best', None).get('rating', '')
            wins = game['record']['win']
            draws = game['record']['draw']
            losses = game['record']['loss']

            return [last_date, last_rating, best_date, best_rating, wins, draws, losses]
        return ['no data' for _ in range(7)]

    def set_games_details(self):
        if type(self.count) is dict:
            self.no_games = self.count.get('all', 'no data')
            self.games_against_ai = self.count.get('ai', 'no data')
            self.games_against_human = self.count.get('rated', 'no data')
            self.no_draws = self.count.get('draw', 'no data')
            self.no_wins = self.count.get('win', 'no data')
            self.no_losses = self.count.get('loss', 'no data')

    def set_profile_details(self):
        if type(self.profile) is dict:
            self.country = self.profile.get('country', 'no data')
            self.location = self.profile.get('location', 'no data')
            self.first_name = self.profile.get('firstName', 'no data')
            self.last_name = self.profile.get('lastName', 'no data')

    def get_win_percentage(self):
        return round((self.no_wins * 100) / self.no_games, 2)

    def get_loss_percentage(self):
        return round((self.no_losses * 100) / self.no_games, 2)

    def get_draw_percentage(self):
        return round((self.no_draws * 100) / self.no_games, 2)

    def get_chesscom_win_percentage(self):
        return round((self.get_all_chesscom_games_by_result('win') * 100) / self.get_all_chesscom_games(), 2)

    def get_chesscom_loss_percentage(self):
        return round((self.get_all_chesscom_games_by_result('loss') * 100) / self.get_all_chesscom_games(), 2)

    def get_chesscom_draw_percentage(self):
        return round((self.get_all_chesscom_games_by_result('draw') * 100) / self.get_all_chesscom_games(), 2)

    def set_rating_history(self, response):
        ratings_array = []

        for points in response:
            if points.get('name', None) in ['Bullet', 'Blitz', 'Rapid', 'Classical', 'Correspondence']:
                ratings_array.append((points.get('name', None), points.get('points', None)))

        self.ratings_validation(ratings_array)

    def ratings_validation(self, data):
        if data:
            for rating in data:
                if rating[1]:
                    self.ratings_history.append({
                        "name": f'{rating[0]}',
                        "dates": [f'{d[2]}%2F{d[1]}%2F{d[0]}' for d in rating[1]],
                        "points": [p[3] for p in rating[1]],
                        "chart_url": ''
                    })
            self.set_url()

    def set_url(self):
        for rating_set in self.ratings_history:
            chart = ChartVisualizer()
            chart.set_chtt(f'chtt={rating_set["name"]}%20ratings')  # <=> e.g. 'bullet ratings'
            chart.set_chxt('chxt=x%2Cy')  # <=> 'x,y'
            chart.set_cht('cht=lc')  # line chart
            chart.set_chs('chs=700x300')
            chart.set_chxl('chxl=0%3A%7C' + '%7C'.join(rating_set['dates']))
            chart.set_chd(f'chd=t:{",".join(str(p) for p in rating_set["points"])}')
            chart.set_chds(f'chds={str(min(rating_set["points"]))}%2C{str(max(rating_set["points"]))}')
            chart.set_chxs('chxs=0,s')

            rating_set['chart_url'] = chart.chart_url()

    def games_stats_chart_url(self):
        chart = ChartVisualizer()
        chart.set_cht('cht=p')  # pie chart
        chart.set_chs('chs=200x200')
        chart.set_chdl('chdl=wins%7Cdraws%7Closses')
        chart.set_chl(
            f'chl={self.get_win_percentage()}%%7C{self.get_draw_percentage()}%%7C{self.get_loss_percentage()}%')
        chart.set_chd(f'chd=t:{self.get_win_percentage()},{self.get_draw_percentage()},{self.get_loss_percentage()}')

        return chart.chart_url()

    def games_chesscom_stats_chart_url(self):
        chart = ChartVisualizer()
        chart.set_cht('cht=p')  # pie chart
        chart.set_chs('chs=200x200')
        chart.set_chdl('chdl=wins%7Cdraws%7Closses')
        chart.set_chl(
            f'chl={self.get_chesscom_win_percentage()}%%7C{self.get_chesscom_draw_percentage()}%%7C{self.get_chesscom_loss_percentage()}%')
        chart.set_chd(f'chd=t:{self.get_chesscom_win_percentage()},{self.get_chesscom_draw_percentage()},{self.get_chesscom_loss_percentage()}')

        return chart.chart_url()


class ChartVisualizer:
    def __init__(self):
        self.base_url = 'https://image-charts.com/chart?'
        self.chd = ''  # chart data
        self.chs = ''  # chart size in pixels
        self.cht = ''  # chart type (e.g. linear)
        self.chxt = ''  # which axis legend should be displayed
        self.chtt = ''  # chart title
        self.chxl = ''  # chart x-axis legend values
        self.chds = ''
        self.chdl = ''
        self.chl = ''
        self.chxs = ''

    def set_chd(self, chd):
        self.chd = chd

    def set_chds(self, chds):
        self.chds = chds + '&'

    def set_chs(self, chs):
        self.chs = chs + '&'

    def set_chxs(self, chxs):
        self.chxs = chxs + '&'

    def set_cht(self, cht):
        self.cht = cht + '&'

    def set_chxt(self, chxt):
        self.chxt = chxt + '&'

    def set_chtt(self, chtt):
        self.chtt = chtt + '&'

    def set_chxl(self, chxl):
        self.chxl = chxl + '&'

    def set_chdl(self, chdl):
        self.chdl = chdl + '&'

    def set_chl(self, chl):
        self.chl = chl + '&'

    def chart_url(self):
        return self.base_url + self.chds + self.chs + self.cht + self.chxt + self.chtt + self.chxl + self.chxs + \
               self.chdl + self.chl + self.chd
