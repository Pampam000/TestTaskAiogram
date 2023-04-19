import os

from .schemas import Poll


def create_poll(poll_info: dict) -> Poll:
    filename = os.path.basename(__file__)
    filepath = os.path.abspath(__file__).replace(filename, 'group_id.txt')

    poll_variants = list(poll_info.values())[1:]
    with open(filepath, 'r') as file:
        group_id = file.read()
    return Poll(group_id=group_id, question=poll_info['question'],
                variants=poll_variants)


def get_group_id(group_id: str) -> str:
    filename = os.path.basename(__file__)
    filepath = os.path.abspath(__file__).replace(filename, 'group_id.txt')
    try:
        with open(filepath, 'r'):
            return 'ID группы уже получен'

    except FileNotFoundError:
        with open(filepath, 'w') as file:
            file.write(group_id)
        return "Бот успешно получил ID группы"
