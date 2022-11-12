import numpy as np
import pandas as pd
import re
import sqlite3

# import data from csv file
df1 = pd.read_csv('sample.csv')

# pre-processing
df1.drop(columns=['Sticker taps', 'Content type', 'Replies', 'Results', 'Cost per result'], inplace=True)
# df1['Post time'] = pd.to_datetime(df1['Post time'])
df1 = df1.loc[df1['Caption'] != '***** updated their cover photo.'].reset_index(drop=True)
df1.insert(loc=0, column='postID', value=range(1, len(df1) + 1))
df1 = df1.reset_index(drop=True)
df1['postID'] = df1['postID'].astype(str)

# create a DataFrame for each table in a database file
dict_df2 = {'tagID':[], 'campaigns':[]}
dict_df3 = {'pk_postsAndTags':[], 'postID':[], 'tagID':[]}
# dict_df4 = {'tagID':[], 'courseName':[]}
# dict_df5 = {'customerID':[], ...}

# extract tags from Caption (exclude Thai language)
# indicate regular expression
pattern = re.compile('#[a-zA-Z0-9]+[\w$]') # indicate REGEX for retrieve tags
# Extract tags for each post into a new table
for index, row in df1.iterrows(): # find tags for each post (each row)
    result = pattern.findall(df1['Caption'][index]) # get tags from a comment column and get into a list
    lower_result = [e.lower() for e in result] # lowering case tags to make it consistent
    lower_result_remove_duplicate = list(set(lower_result)) # remove duplicated tags for each post
    if len(lower_result_remove_duplicate) != 0: # if post contains any tag
        # lower_result is a list containing tags for each post; [#tag1, #tag2, #tag3, ...]
        for e in lower_result_remove_duplicate: # for each tag in a post
            if e not in dict_df2['campaigns']: # if tag is not in record before, record it as a new one
                tag_id = len(dict_df2['tagID'])+1
                dict_df2['tagID'].append(str(tag_id))
                dict_df2['campaigns'].append(e)

            # define elements before inserting it to be the data
            postid = df1['postID'][index]
            i = dict_df2['campaigns'].index(e)
            tagid = dict_df2['tagID'][i]
            temp_tuple = str(tuple([postid, tagid]))
            # insert elements to be the data
            dict_df3['pk_postsAndTags'].append(temp_tuple)
            dict_df3['postID'].append(postid)
            dict_df3['tagID'].append(tagid)

df2 = pd.DataFrame(dict_df2)
df3 = pd.DataFrame(dict_df3)

# export as a database file
connection = sqlite3.connect('sample.db')
# define a function for query execution
def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query successful")
    except OSError as err:
        print(f"Error: '{err}'")

def insert_row(connection, query, row):
    cursor = connection.cursor()
    try:
        cursor.execute(query, row)
        connection.commit()
        print("Query successful")
    except OSError as err:
        print(f"Error: '{err}'")

# the database will consist of 3 tables; posts, postAndTags, campaigns
# create tables in database
query1_1 = '''
CREATE TABLE IF NOT EXISTS posts (
    postID TEXT,
    postTime TEXT, -- need to be transformed to DATETIME later
    caption TEXT,
    reach INT,
    likesAndReactions INT,
    postClicks INT,
    comments INT,
    shares INT,
    PRIMARY KEY (postID)
);
'''
query2_1 = '''
CREATE TABLE IF NOT EXISTS campaigns (
    tagID TEXT,
    campaign TEXT,
    PRIMARY KEY (tagID)
);
'''
# Bridge table
query3_1 = '''
CREATE TABLE IF NOT EXISTS postsAndTags (
    pk_postsAndTags TEXT,
    postID TEXT REFERENCES posts(postID),
    tagID TEXT REFERENCES campaigns(tagID),
    PRIMARY KEY (pk_postsAndTags)
);
'''
# query4 =

execute_query(connection, query1_1)
execute_query(connection, query2_1)
execute_query(connection, query3_1)

# insert data into tables
query1_2 = '''
        INSERT INTO posts (postID, postTime, caption, reach, likesAndReactions, postClicks, comments, shares)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?);
        '''
query2_2 = '''
        INSERT INTO campaigns (tagID, campaign)
        VALUES (?, ?);
        '''
query3_2 = '''
        INSERT INTO postsAndTags (pk_postsAndTags, postID, tagID)
        VALUES (?, ?, ?);
        '''

for index, row in df1.iterrows():
    insert_row(connection, query1_2, tuple(row))

for index, row in df2.iterrows():
    insert_row(connection, query2_2, tuple(row))

for index, row in df3.iterrows():
    insert_row(connection, query3_2, tuple(row))

connection.close()