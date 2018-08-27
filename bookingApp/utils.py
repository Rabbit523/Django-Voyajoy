from random import sample

from bookingApp.models import Listing

__author__ = 'eMaM'




def find_between(s, first, last):
    try:
        start = s.index(first) + len(first)
        end = s.index(last, start)
        return s[start:end]
    except ValueError:
        return ""



def is_404(ulr):
    pass


def extractNumberFromText(value):
    return int(filter(str.isdigit, value))