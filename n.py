from undo.log import get_transaction_list_to_undo

t_list = get_transaction_list_to_undo()
print("\nitens para performar undo :: ", end="")
for item in t_list:
    print(f"{item}, ")