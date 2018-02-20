from datetime import datetime, timedelta
from sanic.exceptions import InvalidUsage


def get_top_and_bottom(args):
    top = parse_str_to_list(args.getlist('top'))
    bottom = parse_str_to_list(args.getlist('bottom'))
    return top, bottom

def get_row_and_column(args):
    row = args.get('row')
    column = args.get('column')
    if row is None or column is None:
        raise InvalidUsage("'row' and 'column' required")
    return row, column

def parse_str_to_list(args):
    if isinstance(args, list):
        return args[0].split(',')
    return None


def generate_task(randomer):
    new_task = (datetime.utcnow() + timedelta(seconds=randomer)).timestamp() * 1000
    return new_task
