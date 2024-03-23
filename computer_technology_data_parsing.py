import mysql.connector
import os
import json
import re
from datetime import datetime
from getConnection import getConfig, getConnCursor, closeConnCursor, closeConnCursor, parseStockData, updateDictKey
from sqlStatements import *


configFile = 'computer_technology_config.json'

host, user, password, database, filepath, column, column_type, method =  getConfig(configFile)

conn, cursor = getConnCursor(host, user, password, database)

### create tables 
for tablequery in CREATE_COMPUTER_TECHNOLOGY_TABLES:
    print(tablequery)
    cursor.execute(tablequery)

## load data
data_files = os.listdir(filepath)
screen_filler_files = [i for i in data_files if i.lower().__contains__(".json")]
print(screen_filler_files)

for file in screen_filler_files:
    filep = os.path.join(filepath, file)

    with open(filep, 'r') as fp:
        try:
            json_content = json.load(fp)
        except Exception as e:
            print("Exception : ", e)
            print(f"File ({filep}) does not get executed.")
            continue

        for key, stock_info in json_content.items():
            stock_info = updateDictKey(stock_info)
            args = parseStockData(stock_info, column, column_type)
            temp_module = __import__('sqlStatements')
            if args:
                sr_method = getattr(temp_module, method)
                query = sr_method(*args)
                print(query)
                cursor.execute(query)

    # create archive dir if not exists
    if not os.path.exists(os.path.join(filepath,'archive')):
        os.makedirs(os.path.join(filepath,'archive'))
    
    archive_file = file.split(".")[0] + "_" + datetime.now().strftime("%d_%m_%Y__%H_%M_%S") + "." + file.split(".")[1]
    
    replace_file = os.path.join(filepath, 'archive', archive_file)
    os.replace(filep, replace_file)

closeConnCursor(conn=conn, cursor=cursor)

