from undo.log import get_transaction_list_to_undo

t_list = get_transaction_list_to_undo()
print("\nitens para performar undo :: ", end="")
for item in t_list:

    # lenisson ini
    itens = str(item).replace('<', '').replace('>', '').split('|')
    print(itens)
    # lenisson fim

    print(f"{item}, ")