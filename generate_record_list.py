
from tqdm import tqdm
from hparams import xml_path, max_record_num, board_width
import xml.etree.ElementTree as etree

def get_str(record_str):
    result_str = ''
    history = record_str.split()

    for i in range(len(history)):
        result_str = result_str + \
                     str(board_width * (board_width - int(history[i][1:])) + ord(history[i][0]) - ord('a')) \
                         + ' '
    result_str += '\n'
    return result_str


def generate_record_list():
    xmID = etree.parse(xml_path)
    root = xmID.getroot()
    cnt = 0
    record_list = []

    for game in tqdm(root):
        if game.find("winby").text == "five":
            record = game.find("board").text
            if '--' in record:
                continue
            else:
                record_list.append(get_str(record))
                cnt += 1
        if cnt == max_record_num:
            break

    return record_list
