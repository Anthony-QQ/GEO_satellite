import math
from datetime import datetime


'''
Converts datetime and mjd

Copied from https://gist.github.com/jiffyclub/1294443
'''


def mjd_to_jd(mjd):
    return mjd + 2400000.5


def jd_to_mjd(jd):
    return jd - 2400000.5


def date_to_jd(year, month, day):
    if month == 1 or month == 2:
        yearp = year - 1
        monthp = month + 12
    else:
        yearp = year
        monthp = month

    # this checks where we are in relation to October 15, 1582, the beginning
    # of the Gregorian calendar.
    if ((year < 1582) or
            (year == 1582 and month < 10) or
            (year == 1582 and month == 10 and day < 15)):
        # before start of Gregorian calendar
        B = 0
    else:
        # after start of Gregorian calendar
        A = math.trunc(yearp / 100.)
        B = 2 - A + math.trunc(A / 4.)

    if yearp < 0:
        C = math.trunc((365.25 * yearp) - 0.75)
    else:
        C = math.trunc(365.25 * yearp)

    D = math.trunc(30.6001 * (monthp + 1))

    jd = B + C + D + day + 1720994.5

    return jd


def jd_to_date(jd):
    """
    Convert Julian Day to date.

    Algorithm from 'Practical Astronomy with your Calculator or Spreadsheet',
        4th ed., Duffet-Smith and Zwart, 2011.

    Parameters
    ----------
    jd : float
        Julian Day

    Returns
    -------
    year : int
        Year as integer. Years preceding 1 A.D. should be 0 or negative.
        The year before 1 A.D. is 0, 10 B.C. is year -9.

    month : int
        Month as integer, Jan = 1, Feb. = 2, etc.

    day : float
        Day, may contain fractional part.

    Examples
    --------
    Convert Julian Day 2446113.75 to year, month, and day.

    jd_to_date(2446113.75)
    (1985, 2, 17.25)

    """
    jd = jd + 0.5

    F, I = math.modf(jd)
    I = int(I)

    A = math.trunc((I - 1867216.25) / 36524.25)

    if I > 2299160:
        B = I + 1 + A - math.trunc(A / 4.)
    else:
        B = I

    C = B + 1524

    D = math.trunc((C - 122.1) / 365.25)

    E = math.trunc(365.25 * D)

    G = math.trunc((C - E) / 30.6001)

    day = C - E + F - math.trunc(30.6001 * G)

    if G < 13.5:
        month = G - 1
    else:
        month = G - 13

    if month > 2.5:
        year = D - 4716
    else:
        year = D - 4715

    return year, month, day


def hmsm_to_days(hour=0, minute=0, sec=0, micro=0):
    """
    Convert hours, minutes, seconds, and microseconds to fractional days.

    Parameters
    ----------
    hour : int, optional
        Hour number. Defaults to 0.

    min : int, optional
        Minute number. Defaults to 0.

    sec : int, optional
        Second number. Defaults to 0.

    micro : int, optional
        Microsecond number. Defaults to 0.

    Returns
    -------
    days : float
        Fractional days.

    Examples
    --------
    hmsm_to_days(hour=6)
    0.25

    """
    days = sec + (micro / 1000000.)
    days = minute + (days / 60.)
    days = hour + (days / 60.)

    return days / 24.


def days_to_hmsm(days):
    """
    Convert fractional days to hours, minutes, seconds, and microseconds.
    Precision beyond microseconds is rounded to the nearest microsecond.

    Parameters
    ----------
    days : float
        A fractional number of days. Must be less than 1.

    Returns
    -------
    hour : int
        Hour number.

    min : int
        Minute number.

    sec : int
        Second number.

    micro : int
        Microsecond number.

    Raises
    ------
    ValueError
        If `days` is >= 1.

    Examples
    --------
    days_to_hmsm(0.1)
    (2, 24, 0, 0)

    """
    hours = days * 24.
    hours, hour = math.modf(hours)

    mins = hours * 60.
    mins, min = math.modf(mins)

    secs = mins * 60.
    secs, sec = math.modf(secs)

    micro = round(secs * 1000000.)

    return int(hour), int(min), int(sec), int(micro)


def datetime_to_jd(date):
    days = date.day + hmsm_to_days(date.hour, date.minute, date.second, date.microsecond)
    return date_to_jd(date.year, date.month, days)


def datetime_to_mjd(date):
    return jd_to_mjd(datetime_to_jd(date))


def jd_to_datetime(jd):
    """
    Convert a Julian Day to an `jdutil.datetime` object.

    Parameters
    ----------
    jd : float
        Julian day.

    Returns
    -------
    dt : `jdutil.datetime` object
        `jdutil.datetime` equivalent of Julian day.

    Examples
    --------
    jd_to_datetime(2446113.75)
    datetime(1985, 2, 17, 6, 0)

    """
    year, month, day = jd_to_date(jd)

    frac_days, day = math.modf(day)
    day = int(day)

    hour, minute, sec, micro = days_to_hmsm(frac_days)

    return datetime(year, month, day, hour, minute, sec, micro)