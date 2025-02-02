import json


def extract_data(file):
    
    myjson=open(file,'r')
    json_data=myjson.read()


    #parse in obj
    obj=json.loads(json_data)

    theme=obj['main_theme']
    subthemes=obj['subthemes']
    
    return theme, subthemes


