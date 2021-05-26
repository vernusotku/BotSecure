import json, os
if os.path.exists(os.getcwd()+'/config.json'):
    with open('config.json') as json_file:
        data = json.load(json_file)
        TOKEN_BOT = data['TOKEN_BOT']