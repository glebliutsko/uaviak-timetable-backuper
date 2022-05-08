from functools import cached_property
from hashlib import sha256


class VersionTimetable:
    def __init__(self, content: str):
        self.content = content

    @cached_property
    def hash(self) -> str:
        return sha256(self.content.encode('UTF-8')).hexdigest()
