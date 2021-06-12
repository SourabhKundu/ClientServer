import json
state_file_name = "current_state.json"

def check_status():
    state= json.load(open(state_file_name,"r"))
    print(state)
    return state

check_status()