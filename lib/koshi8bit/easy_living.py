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
    def dict_append(_dict, index, elem, add_duplicate=False):
        if index in _dict:
            if add_duplicate:
                _dict[index].append(elem)
            else:
                if elem not in _dict[index]:
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
    separator_iso = 'T'
    separator_ui = '@'
    separator_file = '--'

    date_ui_format = '%Y-%m-%d'
    time_ui_format = '%H:%M:%S'
    time_ui_ms_format = time_ui_format + '.%f'

    date_file_format = date_ui_format
    time_file_format = '%H-%M-%S'
    time_file_ms_format = time_file_format + '-%f'

    @staticmethod
    def now(_format: str):
        return datetime.datetime.now().strftime(_format)

    @staticmethod
    def _format(dt: datetime.datetime, _format: str):
        if dt:
            return dt.strftime(_format)
        else:
            return Format.now(_format)

    # ui

    @staticmethod
    def date_ui(dt: datetime.datetime = None):
        return Format._format(dt, Format.date_ui_format)

    @staticmethod
    def time_ui(dt: datetime.datetime = None, show_ms=False):
        return Format._format(dt, Format.time_ui_ms_format if show_ms else Format.time_ui_format)

    @staticmethod
    def date_time_ui_format(show_ms=False, separator=separator_iso):
        return Format.date_ui_format + separator + (Format.time_ui_ms_format if show_ms else Format.time_ui_format)

    @staticmethod
    def date_time_ui(dt: datetime.datetime = None, show_ms=False, separator=separator_iso):
        f = Format.date_time_ui_format(show_ms, separator)
        return Format._format(dt, f)

    # file

    @staticmethod
    def date_file(dt: datetime.datetime = None):
        return Format._format(dt, Format.date_file_format)

    @staticmethod
    def time_file(dt: datetime.datetime = None, show_ms=False):
        return Format._format(dt, Format.time_file_ms_format if show_ms else Format.time_file_format)

    @staticmethod
    def date_time_file_format(show_ms=False, separator=separator_iso):
        return Format.date_file_format + separator + (Format.time_file_ms_format if show_ms else Format.time_file_format)

    @staticmethod
    def date_time_file(dt: datetime.datetime = None, show_ms=False, separator=separator_iso):
        f = Format.date_time_file_format(show_ms, separator)
        return Format._format(dt, f)

    # double

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
