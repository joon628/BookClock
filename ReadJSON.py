import pandas as pd
import json
import sqlite3

def modify_json():
    file_name = "gutenberg-metadata.json"
    df = pd.read_json(file_name)
    df.drop(['formaturi','language','rights'],axis=0, inplace=True)

    # # df.drop(df[any("Fiction" in sub for sub in df['subject'])].index, inplace=True)
    index = 1
    index_list = []
    for df_sing in df.values[1]: #subject
        if any("Fiction" in subject for subject in df_sing):
            index_list.append(index)
        elif any("fiction" in subject for subject in df_sing):
            index_list.append(index)
        index +=1

    df = df[index_list].copy()
    df.to_json('modified_gutenMeta.json')


def load_json():
    file_name = "modified_gutenMeta.json"
    df = pd.read_json(file_name)
    return df

def dictionaryToJson(inputDict):
    with open("sample.json", "w") as outfile:
        json.dump(inputDict, outfile)
        
def populate_DF(json):
    df = pd.DataFrame(columns = ['time', 'sentence', 'highlight', 'title'])
    for key in json:
        print(json[key])
        for value in json[key]:
            df = df.append({'time': key,'sentence':value[0], 'highlight':value[1],'title':value[2]}, ignore_index=True)
    return df
    
def create_sql(df):
    conn = sqlite3.connect('time_database')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS time (time datetime64,sentence text,  highlight text, title text)')
    conn.commit()
    df.to_sql('time_database', conn, if_exists='replace', index = False)