"""
For anything too small to make into a whole submodule
"""
import datetime
def mjd(date = None):
    """
    Quick function to get today's Modified Julian Day (MJD) or any specified date's. Works to an integer precision (i.e. +/-1).
    Input: 
    date (optional) : Default none get's today's date. If specifying, format as tuple of ints (YEAR,MONTH,DAY), i.e. "date=(2022,4,1)" for April 1, 2022.
    """
    if not date:
        ord_date = datetime.date.today().toordinal()
    else:
        ord_date = datetime.date(*date).toordinal()
        
    jd = ord_date + 1721425
    mjd = jd - 2400001
    return mjd