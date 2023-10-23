import re
import sys

from file_read_backwards import FileReadBackwards
fread_backwards = FileReadBackwards

from models.Transaction import Transaction
from core.config import settings

def upgrade_ckpt_flag(value):
    return (value % 2) + 1

def op_identify(op):

    #       formatos de transacao identificaveis :
    #
    # 0     <Transacao, id_tupla, coluna, valor_antigo>
    # 1     <start Transacao>
    # 2     <commit Transacao>
    # 3     <START ckpt_name(Transacao)>
    # 4     <END ckpt_name>
    patterns = [r"<([^,]+),([^,]+),([^,]+),([^,]+)>", 
                r"<start (.*?)>", 
                r"<commit (.*?)>", 
                r"<START (.*?)\((.*?)\)>", 
                r"<END (.*?)>"]

    for op_id, pattern in enumerate(patterns):
        match = re.search(pattern, op)
        if match:
            return op_id, match

    return None, None

def get_transaction_list_to_undo():
    commited_lst = list()   # tr ja em disco
    tr_undo_lst = list()    # tr que sofrerao undo
    ckpt_flag = 0           # flag para o estado do ckpt :: 0: !end e !start | 1: end e !start | 2: end e start
    with fread_backwards(settings.LOG_FILENAME, encoding="utf-8") as log:
        for line in log:
            # identificar e capturar info da transacao da linha
            op_id, match = op_identify(line)
            if not match: sys.exit(settings.EXIT_MSG_INCLOG)
            # capturar transacao da linha 
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
