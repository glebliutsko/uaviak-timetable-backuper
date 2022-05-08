if __package__ is None:  # Direct call __main__.py
    import os, sys

    path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, path)


import os
from dataclasses import dataclass

import requests

from uaviak_timetable_backuper import TimetableDirectory, VersionTimetable


@dataclass(frozen=True)
class Timetable:
    url: str
    save_path: str


SAVE_PATH = os.getenv('TIMETABLE_SAVE_PATH', os.path.abspath('./timetable'))
TIMETABLES = [
    Timetable('https://uaviak.ru/pages/raspisanie-/', os.path.join(SAVE_PATH, 'student')),
    Timetable('https://uaviak.ru/pages/raspisanie/', os.path.join(SAVE_PATH, 'teacher'))
]


def main() -> None:
    for timetable in TIMETABLES:
        response = requests.get(timetable.url)

        version = VersionTimetable(response.text)

        directory = TimetableDirectory(timetable.save_path)
        filename = directory.add_new_version(version)
        if filename is not None:
            print(f'Save to {filename}')
        else:
            print('Skip')


if __name__ == '__main__':
    main()
