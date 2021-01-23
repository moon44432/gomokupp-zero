

from tensorflow.keras.models import load_model
from tensorflow.keras import backend as K
from shutil import copy
from game import State
from pv_mcts import pv_mcts_action

# 파라미터 준비
EN_GAME_COUNT = 30  # 평가 1회 당 게임 수(오리지널: 400)
EN_TEMPERATURE = 1.0  # 볼츠만 분포 온도
EN_AVERAGE_POINT = 0.5


def first_player_point(ended_state):
    if ended_state.is_lose():
        return 0 if ended_state.is_first_player() else 1
    return 0.5


def play(next_actions):
    state = State()

    while True:
        if state.is_done():
            break

        next_action = next_actions[0] if state.is_first_player() else next_actions[1]
        action = next_action(state)

        state = state.next(action)

    return first_player_point(state)


def update_best_player():
    copy('./model/latest.h5', './model/best.h5')
    print('Updating best player...')


def evaluate_network():
    model0 = load_model('./model/latest.h5')

    model1 = load_model('./model/best.h5')

    next_action0 = pv_mcts_action(model0, EN_TEMPERATURE)
    next_action1 = pv_mcts_action(model1, EN_TEMPERATURE)
    next_actions = (next_action0, next_action1)

    total_point = 0
    for i in range(EN_GAME_COUNT):
        if i % 2 == 0:
            total_point += play(next_actions)
        else:
            total_point += 1 - play(list(reversed(next_actions)))

        print('\rEvaluating... ({}/{})'.format(i + 1, EN_GAME_COUNT), end='')
    print('')

    average_point = total_point / EN_GAME_COUNT
    print('Average point: ', average_point)

    K.clear_session()
    del model0
    del model1

    # 베스트 플레이어 교대
    if average_point > EN_AVERAGE_POINT:
        update_best_player()
        return True
    else:
        return False
