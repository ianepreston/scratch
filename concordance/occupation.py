# -*- coding: utf-8 -*-
"""
Created on Mon Mar  5 07:25:43 2018
ToDo: Real Docstring for the module,
make wrappers straight from NOC 2006 to 2011 (with NOC S 2006 as intermediate)
Maybe make a split and not split function?
@author: e975360
"""
from html_table import HtmlTables
import pandas as pd


def occ_reclass(url, newnames):
    """
    Call in a basic concordance table from StatsCan to convert NOC tables

    Keyword Arguments:
    url: the url of the concordance table
    from_year: the year we're mapping from
    to_year: the year we're mapping to

    Returns: DataFrame of concordance table
    """
    df = HtmlTables(url).read()[0]
    # First two rows should have been column headers, drop them
    df = df.loc[2:, :].copy()
    df.columns = newnames
    # For code splits there's one top entry and then blanks on subsequent rows
    # pad fills these blanks with the last nonblank entry
    df.fillna(method='pad', axis='index', inplace=True)
    # We record all claims at 4 digit level NOC, only need those codes
    mask = df['noc_s2006_code'].str.len() == 4
    df = df.loc[mask].copy()
    return df


def noc_s2006_noc2006():
    """
    Returns a pandas dataframe that maps NOC-S 2006 to NOC 2006
    Needed because AWCBC publishes in NOC 2006, we record in NOC 2011, and
    concordance tables only exist for 2011 to S 2006

    Returns:
    Dataframe of concordance
    """
    url = (
        'http://www.statcan.gc.ca/eng/subjects/standard/concordances/nocs2006-noc2006'  # noqa
        )
    newnames = [
        'noc_s2006_code',
        'noc_2006_code',
        'title'
        ]
    return occ_reclass(url, newnames)


def noc_s2006_noc2011():
    """
    Convert from NOC-S 2006 to NOC 2011
    """
    url = "http://www.statcan.gc.ca/eng/subjects/standard/noc/2011/noc-s2006-noc2011"  # noqa
    newnames = [
        'noc_s2006_code',
        'noc_s2006_title',
        'noc_s2006_status',
        'noc_2011_p',
        'noc_2011_code',
        'noc_2011_title',
        'noc_2011_notes'
        ]
    df = occ_reclass(url, newnames)
    # can't figure out why I have to do this. but I do.
    mask = df['noc_s2006_code'] == 'A131'
    df.loc[mask, 'noc_s2006_status'] = 'NU'
    return df


def noc2011_noc_s2006():
    """
    Convert from NOC 2011 to NOC-S 2006
    """
    url = "http://www.statcan.gc.ca/eng/subjects/standard/noc/2011/noc2011-noc-s2006"  # noqa
    newnames = [
        'noc_2011_code',
        'noc_2011_title',
        'noc_2011_status',
        'noc_s2006_p',
        'noc_s2006_code',
        'noc_s2006_title',
        'noc_s2006_notes'
        ]
    return occ_reclass(url, newnames)


def noc2006_noc2011():
    """
    Convert straight from NOC 2006 to NOC 2011
    """
    s2006 = noc_s2006_noc2006()
    s2006_2011 = noc_s2006_noc2011()
    df = pd.merge(s2006_2011, s2006, on='noc_s2006_code', how='left')
    df.drop(columns=['noc_s2006_code', 'noc_s2006_title'], inplace=True)
    df.rename(
        columns={
            'noc_s2006_status': 'noc_2006_status',
            'title': 'noc_2006_title'
            },
        inplace=True
        )
    df = df[[
        'noc_2006_code',
        'noc_2006_title',
        'noc_2006_status',
        'noc_2011_p',
        'noc_2011_code',
        'noc_2011_title',
        'noc_2011_notes'
        ]]
    return df


def noc2011_noc2006():
    """
    Convert straight from NOC 2011 to NOC 2006
    """
    s2006 = noc_s2006_noc2006()
    n2011_s2006 = noc2011_noc_s2006()
    df = pd.merge(n2011_s2006, s2006, how='left', on='noc_s2006_code')
    df.drop(columns=['noc_s2006_code', 'noc_s2006_title'], inplace=True)
    df.rename(
        columns={
            'noc_s2006_status': 'noc_2006_status',
            'title': 'noc_2006_title',
            'noc_s2006_p': 'noc_2006_p',
            'noc_s2006_notes': 'noc_2006_notes'
            },
        inplace=True
        )
    df = df[[
        'noc_2011_code',
        'noc_2011_title',
        'noc_2011_status',
        'noc_2006_code',
        'noc_2006_title',
        'noc_2006_p',
        'noc_2006_notes'
        ]]
    return df


if __name__ == '__main__':
    noc2011_2006 = noc2011_noc2006()
    noc2006_2011 = noc2006_noc2011()
