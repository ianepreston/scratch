# -*- coding: utf-8 -*-
"""
@author: John Ricco (formatting changes by Ian Preston)
"""
import copy
import requests
import pandas as pd
from bs4 import BeautifulSoup


class HtmlTables(object):
    """
    https://johnricco.github.io/2017/04/04/python-html/
    """

    def __init__(self, url):

        self.url = url
        self.r = requests.get(self.url)
        self.url_soup = BeautifulSoup(self.r.text, "lxml")
        self.tables = []
        self.tables_html = self.url_soup.find_all("table")

    def read(self):
        """
        Read the html table of the HTML table object, create a dataframe
        Returns:
        The HTML table in a pandas DF format
        """

        # Parse each table
        for n in range(0, len(self.tables_html)):

            n_cols = 0
            n_rows = 0

            for row in self.tables_html[n].find_all("tr"):
                col_tags = row.find_all(["td", "th"])
                if len(col_tags) > 0:
                    n_rows += 1
                    if len(col_tags) > n_cols:
                        n_cols = len(col_tags)

            # Create dataframe
            df = pd.DataFrame(
                index=range(0, n_rows), columns=range(0, n_cols))

            # Create list to store rowspan values
            skip_index = [0 for i in range(0, n_cols)]

            # Start by iterating over each row in this table...
            row_counter = 0
            for row in self.tables_html[n].find_all("tr"):
                # Skip row if it's blank
                if len(row.find_all(["td", "th"])) == 0:
                    next

                else:
                    # Get all cells containing data in this row
                    columns = row.find_all(["td", "th"])
                    col_dim = []
                    row_dim = []
                    col_dim_counter = -1
                    row_dim_counter = -1
                    col_counter = -1
                    this_skip_index = copy.deepcopy(skip_index)

                    for col in columns:
                        # Determine cell dimensions
                        colspan = col.get("colspan")
                        if colspan is None:
                            col_dim.append(1)
                        else:
                            col_dim.append(int(colspan))
                        col_dim_counter += 1

                        rowspan = col.get("rowspan")
                        if rowspan is None:
                            row_dim.append(1)
                        else:
                            row_dim.append(int(rowspan))
                        row_dim_counter += 1

                        # Adjust column counter
                        if col_counter == -1:
                            col_counter = 0
                        else:
                            col_counter = col_counter + col_dim[
                                col_dim_counter - 1]

                        while skip_index[col_counter] > 0:
                            col_counter += 1

                        # Get cell contents
                        cell_data = col.get_text()

                        # Insert data into cell
                        df.iat[row_counter, col_counter] = cell_data

                        # Record column skipping index
                        if row_dim[row_dim_counter] > 1:
                            this_skip_index[col_counter] = row_dim[
                                row_dim_counter]

                # Adjust row counter
                row_counter += 1

                # Adjust column skipping index
                skip_index = [i - 1 if i > 0 else i for i in this_skip_index]

            # Append dataframe to list of tables
            self.tables.append(df)

        return self.tables
