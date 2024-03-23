import mysql.connector

import json
import re
import pandas as pd
from datetime import datetime

def updateDictKey(temp):
    new_dict = dict()
    for key, val in temp.items():
        new_key = re.sub(r'\W', '', key)
        new_dict[new_key] = val
    return new_dict

def getDefaultValue(dtype):
    if dtype in ['date']:
        return '1990-01-01'
    elif dtype in ['varchar', 'string', 'str', 'text']:
        return 'null'
    elif dtype in ['int', 'integer']:
        return 0
    elif dtype in ['decimal', 'double']:
        return 0.0
    else:
        return None

def parseStockData(data, columns, column_type) -> list:
    returnList = []
    columnlist = list(zip(columns.split(","), column_type.split(",")))
    
    for col,col_type in columnlist:
        val = ''
        if col in data:
            if col_type in ['date']:
                val = data[col]
                val = datetime.strptime(val, "%Y-%m-%d")
                val = val.strftime('%Y-%m-%d')
            elif col == 'MarketRank':
                val = data[col]
                reg = re.match(r'([\d\.]*) of 5 stars', val)
                if reg:
                    val =reg.group(1)
            else:
                val = data[col]
                val = str(val).replace("%", '').replace("$", "").replace(",", "").replace("'","")

        if (not val or (pd.isna(val)) or (val == 'nan')):
            val = getDefaultValue(col_type)

        returnList.append(val)

    return returnList


def getConfig(filepath = 'Config.json'):
    configJson = None
    with open(filepath, 'r') as fp:
        configJson = json.load(fp)
    host = configJson.get("host", None)
    user = configJson.get("user", None)
    password = configJson.get("password", None)
    database = configJson.get("database", None)
    file_path = configJson.get("data_path", None)
    fields = configJson.get("fields", None)
    fields = fields.split(",")
    fields = [ re.sub(r'\W', '', i) for i in fields ] 
    fields = ','.join(fields)
    fields_type = configJson.get("fields_type", None)
    method = configJson.get("method", None)
    return (host, user, password, database, file_path, fields, fields_type, method)



def getConnCursor(host = None, user = None, password = None, database = None):

    # Connect to the MySQL server
    cnx = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )

    # Create a cursor object to execute SQL queries
    cursor = cnx.cursor()

    return cnx, cursor


def closeConnCursor(conn = None, cursor = None):
    cursor.close()
    conn.commit()
    conn.close()


def update_none(stock_info):
    temp_list = []
    for info in stock_info:
        if type(info) == type(None):
            temp_list.append('0.0')
        else:
            temp_list.append(info)
    
    return temp_list