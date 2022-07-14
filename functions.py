import re

def trim(text):
    return re.sub("\s+", " ", text.strip())

def getTableData(table):
    # Get all th of the row
    th = table.thead.tr.find_all("th")

    # Get all headers
    table_header = [trim(i.text).upper() for i in th]

    # Get all td of the row
    td = table.tbody.tr.find_all("td")

    # Get all values
    table_data = [trim(i.text) for i in td]

    # Convert lists to dictionary
    return dict(zip(table_header, table_data))