
from dual_network import dual_network
from self_play import self_play
from train_network import train_network
from evaluate_network import evaluate_network
from generate_record_list import generate_record_list
from generate_data import generate_data_from_records
from hparams import record_batch_size, train_cycle

if __name__ == "__main__":
    dual_network()

    CALL_COUNT = 0
    INITIAL_COUNT = 14
    record_list = generate_record_list()

    if INITIAL_COUNT > 0:
        CALL_COUNT = INITIAL_COUNT

    for i in range(train_cycle):
        print('Training {:04d}'.format(i + 1))

        # 기보로 학습 데이터 생성 파트
        if CALL_COUNT * record_batch_size >= len(record_list):
            CALL_COUNT = 0

        print('Record {}~{}'.format(CALL_COUNT * record_batch_size + 1, (CALL_COUNT + 1) * record_batch_size))
        # 기보 데이터
        record = record_list[CALL_COUNT * record_batch_size:(CALL_COUNT + 1) * record_batch_size]

        print('Generating data from records...')
        generate_data_from_records(record)
        CALL_COUNT += 1

        # 셀프 플레이로 데이터 생성 파트
        # print('Generating data from self playing...')
        # self_play()

        # 파라미터 갱신 파트
        print('Training network...')
        train_network()

        # 신규 파라미터 평가 파트
        print('Evaluating network...')
        evaluate_network()
