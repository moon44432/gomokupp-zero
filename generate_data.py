
from datetime import datetime
from game import State
from dual_network import DN_OUTPUT_SIZE
import pickle
import os


def first_player_value(ended_state):
    if ended_state.is_lose():
        return -1 if ended_state.is_first_player() else 1
    return 0


def write_data(history):
    now = datetime.now()
    os.makedirs('./data/', exist_ok=True)
    path = './data/{:04}{:02}{:02}{:02}{:02}{:02}.history'.format(
        now.year, now.month, now.day, now.hour, now.minute, now.second)
    with open(path, mode='wb') as f:
        pickle.dump(history, f)


def play(record):
    history = []
    actions = [int(i) for i in record.split()]
    state = State()

    for action in actions:
        policies = [0] * DN_OUTPUT_SIZE
        policies[action] = 1

        history.append([[state.pieces, state.enemy_pieces], policies, None])

        state = state.next(action)

    # print(state)

    value = first_player_value(state)
    for i in range(len(history)):
        history[i][2] = value
        value = -value
    return history


def generate_data_from_records(record):
    history = []

    for i in range(len(record)):
        h = play(record[i])
        history.extend(h)

    write_data(history)
