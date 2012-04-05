# -*- coding:utf-8 -*-

from re import sub
import translitcodec


def slugEncode(string):
    """
    Replaces multiples spaces by '_' and spanish chars to their
    closes representation
    """
    return sub("\s+", "_", string).encode('translit/long')


class Paginator():
    current = 0
    pages = 0
    total = 0
    has_previous = False
    has_next = False

    def __init__(self, current, total):

        assert current >= 0, "Current page must be a at least zero"
        assert total - 1 >= current, "Current page can't be greater than total pages"

        self.current = current
        self.total = total

        self.pages = range(total)

        if self.current > 0:
            self.has_previous = True

        if self.current < self.total - 1:
            self.has_next = True
