import re
import sys

from file_read_backwards import FileReadBackwards
fread_backwards = FileReadBackwards

from models.Transaction import Transaction
from core.config import settings

def upgrade_ckpt_flag(value):
    return (value % 2) + 1

def op_identify(op):
    patterns = [r"<([^,]+),([^,]+),([^,]+),([^,]+)>", 
                r"<start (.*?)>", 
                r"<commit (.*?)>", 
                r"<START (.*?)\((.*?)\)>", 
                r"<END (.*?)>"]

    for i, pattern in enumerate(patterns):
        match = re.search(pattern, op)
        if match:
            return i, match

    return 0, None

def get_transaction_list_to_undo():
    commited_lst = list()
    tr_undo_lst = list()
    ckpt_flag = 0

    with fread_backwards(settings.LOG_FILENAME, encoding="utf-8") as log:
        for line in log:
            op_id, match = op_identify(line)
            if not match: sys.exit(settings.EXIT_MSG_INCLOG)
            tr_num = match.group(1)

            match op_id:
                case 0:
                    if tr_num not in commited_lst:
                        values = [item.strip() for item in [match.group(1), match.group(2), match.group(3), match.group(4)]]
                        tr_undo_lst.append(Transaction(*values))
                case 1 :
                    if tr_num not in commited_lst:
                        print(f"\"Transação {tr_num} realizou UNDO\"")
                case 2:
                    commited_lst.append(tr_num)
                case 3:
                    if ckpt_flag == 1:
                        ckpt_flag = upgrade_ckpt_flag(ckpt_flag)
                        break
                case 4:
                    ckpt_flag = upgrade_ckpt_flag(ckpt_flag)
                case _:
                     sys.exit(settings.EXIT_MSG_INCLOG)

    return tr_undo_lst
