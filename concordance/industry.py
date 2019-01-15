# -*- coding: utf-8 -*-
"""
Created on Thu Mar  1 10:07:16 2018
ToDo: Real Docstring for the module.
@author: e975360
"""
# import pandas as pd
from concordance.html_table import HtmlTables


def industry_reclass(
    url, from_year, to_year, newnames, from_class='naics', to_class='naics'
):
    """
    Call in a basic concordance table from StatsCan to convert NAICs tables

    Keyword Arguments:
    url: the url of the concordance table
    from_year: the year we're mapping from
    to_year: the year we're mapping to

    Returns: DataFrame of concordance table

    ToDo: Check how broadly applicable this is
    """

    table = HtmlTables(url)
    df = table.read()[0]
    # column names start as range index
    from_year = str(from_year)
    to_year = str(to_year)
    from_class = from_class + '_'
    to_class = to_class + '_'
    df.columns = newnames
    # First row is part of the header
    df = df.loc[1:].copy()
    # For code splits there's one top entry and then blanks on subsequent rows
    # pad fills these blanks with the last nonblank entry
    df.fillna(method='pad', axis='index', inplace=True)
    for n in newnames:
        df[n] = df[n].astype(str)
    for y, code in [(from_year, from_class), (to_year, to_class)]:
        sec = code + y + '_sector'
        code = code + y + '_code'
        df[sec] = df[code].map(lambda x: str(x)[0:2])
        df[code] = df[code].astype('category')
        from_sec = from_class + from_year + '_sector'
        to_sec = to_class + to_year + '_sector'
    df['sec_match'] = df[from_sec] == df[to_sec]
    df[from_sec] = df[from_sec].astype('category')
    df[to_sec] = df[to_sec].astype('category')
    return df


def naics_1997_2002():
    """Wrapper for industry reclass for NAICS 1997 to 2002"""
    url = 'http://www.statcan.gc.ca/eng/subjects/standard/concordances/naics1997-2002'  # noqa
    from_year = 1997
    to_year = 2002
    newnames = [
        'naics_1997_code',
        'naics_1997_title',
        'naics_2002_code',
        'naics_2002_title',
        'notes'
        ]
    return industry_reclass(url, from_year, to_year, newnames)


def naics_2002_2007():
    """Wrapper for industry reclass for NAICS 2002 to 2007"""
    url = 'http://www.statcan.gc.ca/eng/subjects/standard/concordances/t2007_2'
    from_year = 2002
    to_year = 2007
    newnames = [
        'naics_2002_code',
        'naics_2002_title',
        'status',
        'p',
        'naics_2007_code',
        'naics_2007_title',
        'description'
        ]
    return industry_reclass(url, from_year, to_year, newnames)


def naics_2007_2012():
    """Wrapper for industry reclass for NAICS 2007 to 2012"""
    url = 'http://www.statcan.gc.ca/eng/subjects/standard/naics/2012/concordances-2007-2012-2'  # noqa
    from_year = 2007
    to_year = 2012
    newnames = [
        'naics_2007_code',
        'naics_2007_title',
        'status',
        'p',
        'naics_2012_code',
        'naics_2012_title',
        'notes'
        ]
    return industry_reclass(url, from_year, to_year, newnames)


def naics_2012_2017v2():
    """Wrapper for industry reclass for NAICS 2012 to 2017v2"""
    url = 'http://www.statcan.gc.ca/eng/subjects/standard/naics/2017v2/concordance-2012-2017v2'  # noqa
    from_year = 2012
    to_year = 2017
    newnames = [
        'naics_2012_code',
        'naics_2012_title',
        'status',
        'part of class',
        'naics_2017_code',
        'naics_2017_title',
        'notes'
        ]
    return industry_reclass(url, from_year, to_year, newnames)


def sice_1980_naics_2002():
    """Wrapper for industry reclass for SIC-e1980 to NAICS 2002"""
    url = 'http://www.statcan.gc.ca/eng/subjects/standard/concordances/sice1980-naics2002'  # noqa
    from_year = 1980
    to_year = 2002
    newnames = [
        'sic-e_1980_code',
        'sic-e_1980_title',
        'naics_2002_code',
        'naics_2002_title',
        'notes'
        ]
    df = industry_reclass(
        url, from_year, to_year, newnames, from_class='sic-e'
        )
    return df


if __name__ == '__main__':
    naics_1997_2002 = naics_1997_2002()
    naics_2002_2007 = naics_2002_2007()
    naics_2007_2012 = naics_2007_2012()
    sice_1980_naics_2002 = sice_1980_naics_2002()
