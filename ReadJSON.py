import pandas as pd
import json
import sqlite3
import os

def modify_json():
    file_name = "./gutenberg-metadata.json"
    df = pd.read_json(file_name)
    df.drop(['formaturi','language','rights'],axis=0, inplace=True)

    # # df.drop(df[any("Fiction" in sub for sub in df['subject'])].index, inplace=True)
    index = 1
    index_list = []
    for df_sing in df.values[1]: #subject
        if index == 131:
            pass
        if any("Fiction" in subject for subject in df_sing):
            index_list.append(index)
        elif any("fiction" in subject for subject in df_sing):
            index_list.append(index)
        index +=1


    df = df[index_list].copy()
    df.to_json('modified_gutenMeta.json')

def load_json(indvFile):
    script_dir = os.path.dirname(__file__)
    file_name = 'data/' + indvFile
    file_path = os.path.join(script_dir, file_name)

    # file_name = "modified_gutenMeta.json"
    df = pd.read_json(file_path)
    return df

def write_json(data, indvFile):
    script_dir = os.path.dirname(__file__)
    file_name = 'data/' + indvFile
    file_path = os.path.join(script_dir, file_name)
    with open(file_path, 'w') as outfile:
         json.dump(data, outfile)


def dictionaryToJson(inputDict):
    with open("sample.json", "w") as outfile:
        json.dump(inputDict, outfile)
        
def populate_DF(json_dir):
    df = pd.DataFrame(columns = ['time', 'sentence', 'highlight', 'title'])
    with open(json_dir) as json_data:
        df_data = json.load(json_data)
    for key in df_data:
        for value in df_data[key]:
            temp = {'time': key,'sentence':value[0], 'highlight':value[1],'title':value[2]}
            df2 = pd.DataFrame.from_dict([temp])
            df = pd.concat([df,df2])  
    return df
    
def create_sql(df):
    conn = sqlite3.connect('time_database')
    df.to_sql('time_database', conn, if_exists='replace', index = False)
    conn.commit()