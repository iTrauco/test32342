import json

STATE_FILE = 'state.json'

def read_state():
    try:
        with open(STATE_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        return {}

def write_state(state):
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f)
