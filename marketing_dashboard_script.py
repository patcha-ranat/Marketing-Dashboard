import numpy as np
import pandas as pd
import re
import sqlite3

# what to modify in this script
# columns name is fixed, if it change --> rename columns

# import data from csv file
df1 = pd.read_csv('sample.csv')

# pre-processing
df1.drop(columns=['Sticker taps', 'Replies', 'Results', 'Cost per result'], inplace=True)
df1['Post time'] = pd.to_datetime(df1['Post time'])
df1 = df1.loc[df1['Caption'] != 'Skooldio updated their cover photo.'].reset_index(drop=True)
df1.insert(loc=0, column='postID', value=range(1, len(df1) + 1))
df1 = df1.reset_index(drop=True)

# extract tags from Caption (exclude Thai language)
# indicate regular expression
pattern = re.compile('#[a-zA-Z0-9]+[\w$]') # indicate tags
# Extract tags
for index, row in df1.iterrows():
    result = pattern.findall(df1['Caption'][index])
    lower_result = [e.lower() for e in result]
    # df['tags'][index] = lower_result

# collect tags for each post in new table

# create a DataFrame for each table in a database file
dict_df2 = {'postID':[], 'tagID':[]}
# dict_df3 = {'tagID':[], 'courseName':[]}
for index, row in df1.iterrows():
    result = pattern.findall(df1['Caption'][index])
    lower_result = [e.lower() for e in result]
    for e in lower_result:
        dict_df2['postID'].append(df1['ID'][index])
        dict_df2['tagID'].append(df2)

# export as a database file
# define a function for query execution
def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query successful")
    except Error as err:
        print(f"Error: '{err}'")

# the database will consist of 4 tables; posts, postAndTags, courses, transaction

connection = sqlite3.connect('skooldio-sample.db')
query1 = '''
CREATE TABLE IF NOT EXISTS posts (
    ID INT PRIMARY KEY,
    postTime TEXT, -- need to be transformed to DATETIME later
    caption TEXT,
    reach INT,
    likesAndReactions INT,
    postClicks INT,
    comments INT,
    shares INT
);
'''
query2 = '''
CREATE TABLE IF NOT EXISTS postAndTags (
    ID INT PRIMARY KEY,
    tag INT FOREIGN KEY
);
'''
query3 = '''
CREATE TABLE IF NOT EXISTS courses (
    
);
'''
# query4 =

execute_query(connection, query)


connection.close()