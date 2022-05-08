import os
from datetime import datetime
from typing import Optional

from uaviak_timetable_backuper import VersionTimetable


class TimetableDirectory:
    FILE_HASH = '.last_version_hash'

    def __init__(self, directory_path: str):
        self.directory_path = directory_path

    @property
    def _file_hash(self) -> str:
        return os.path.join(self.directory_path, self.FILE_HASH)

    @property
    def _filename_for_new_version(self) -> str:
        date_path = datetime.now().strftime('%Y%m%dT%H%M%S')
        filename = f'{date_path}.html'

        return os.path.join(self.directory_path, filename)

    def _save_new_version(self, new_version: VersionTimetable) -> str:
        filename = self._filename_for_new_version

        with open(filename, 'w') as f:
            f.write(new_version.content)

        self._save_hash_new_version(new_version)

        return filename

    def _save_hash_new_version(self, new_version: VersionTimetable) -> None:
        with open(self._file_hash, 'w') as f:
            f.write(new_version.hash)

    def _get_hash_last_version(self) -> Optional[str]:
        if not os.path.exists(self._file_hash):
            return None

        with open(self._file_hash, 'r') as f:
            last_hash = f.read()

        return last_hash

    def add_new_version(self, new_version: VersionTimetable) -> Optional[str]:
        if not os.path.exists(self.directory_path):
            os.makedirs(self.directory_path, exist_ok=True)

        hash_last_version = self._get_hash_last_version()

        if new_version.hash == hash_last_version:
            return None

        return self._save_new_version(new_version)
