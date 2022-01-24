import datetime
import os
import shutil
from threading import Timer
from pathlib import Path


class Utils:

    @staticmethod
    def dir_create(path: str):
        Path(path).mkdir(parents=True, exist_ok=True)

    @staticmethod
    def dir_rm(_path: str):
        shutil.rmtree(_path)

    @staticmethod
    def dir_exist(_path: str):
        return os.path.isdir(_path)

    @staticmethod
    def dict_append(_dict, index, elem):
        if index in _dict:
            _dict[index].append(elem)
        else:
            _dict[index] = [elem]

    @staticmethod
    def json_get_val(_json, path, default_value=None):
        """
        Get value from JSON
        :param _json:
        :param path:
        :param default_value:
        :return: value. If not found - default_value
        """
        cur = _json
        for section in path:
            if section not in cur:
                return default_value
            cur = cur[section]
        return cur


class Format:

    @staticmethod
    def date():
        return '%Y-%m-%d'

    ###

    @staticmethod
    def date_ui(now: bool):
        f = Format.date()
        if now:
            return Format.now(f)
        else:
            return f

    @staticmethod
    def separator_ui():
        return '@'

    @staticmethod
    def time_ui(now: bool, show_ms: bool):
        f = '%H:%M:%S'
        if show_ms:
            f = f + '.%f'

        if now:
            return Format.now(f)
        else:
            return f

    @staticmethod
    def date_time_ui(now: bool, show_ms: bool):
        f = Format.date_ui(False) + Format.separator_ui() + Format.time_ui(False, show_ms)
        if now:
            return Format.now(f)
        else:
            return f

    ###

    @staticmethod
    def date_file(now: bool):
        f = Format.date()
        if now:
            return Format.now(f)
        else:
            return f

    @staticmethod
    def separator_file():
        return '--'

    @staticmethod
    def time_file(now: bool):
        f = '%H-%M-%S'
        if now:
            return Format.now(f)
        else:
            return f

    @staticmethod
    def date_time_file(now: bool):
        f = Format.date_file(False) + Format.separator_file() + Format.time_file(False)
        if now:
            return Format.now(f)
        else:
            return f

    @staticmethod
    def now(template: str):
        return datetime.datetime.now().strftime(template)

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


