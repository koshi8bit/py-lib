import datetime
from threading import Timer


class Format:

    @staticmethod
    def date():
        return '%Y-%m-%d'

    ###

    @staticmethod
    def date_ui():
        return Format.date()

    @staticmethod
    def separator_ui():
        return '@'

    @staticmethod
    def time_ui(show_ms):
        result = '%H:%M:%S'
        if show_ms:
            result = result + '.%f'
        return result

    @staticmethod
    def date_time_ui(show_ms):
        return Format.date_ui() + Format.separator_ui() + Format.time_ui(show_ms)

    ###

    @staticmethod
    def date_file():
        return Format.date()

    @staticmethod
    def separator_file():
        return '--'

    @staticmethod
    def time_file():
        return '%H-%M-%S'

    @staticmethod
    def date_time_file():
        return Format.date_file() + Format.separator_file() + Format.time_file()

    ###

    @staticmethod
    def double(value, precision=3, scientific_notation=False, show_group_separator=False, separator_sign='.'):
        assert isinstance(value, (float, int))
        assert isinstance(precision, int)
        assert isinstance(scientific_notation, bool)

        result = None
        if scientific_notation:
            f = f'%.{precision}E'
        else:
            f = f'%.{precision}f'

        result = f % value

        if separator_sign != '.':
            result = result.replace('.', ',')

        # assert isinstance(result, type(None))
        return result


###


class BackgroundWorker(object):
    def __init__(self, interval, function, *args, **kwargs):
        self._timer = None
        self.interval = interval
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.is_running = False
        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False
