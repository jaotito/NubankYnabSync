#converts nu transactions that will be synced to ynab to the appropriate format
def converttr(deltatr,data):
    from datetime import datetime
    import json

    USER_TIMEZONE = data.get("USER_TIMEZONE")
    BUDGETID_YNAB = data.get("BUDGETID_YNAB")
    ACCOUNTID_YNAB = data.get("ACCOUNTID_YNAB")
    TOKEN_YNAB = data.get("TOKEN_YNAB")
    Max_days = data.get("Max_days")

    listoftransactiondictionaries = []
    for item in deltatr:
        itemdict = {}
        itemdict["account_id"] = ACCOUNTID_YNAB
        itemdict["amount"] = item.get("amount")
        itemdict["payee_id"] = None
        itemdict["payee_name"] = item.get("description")
        itemdict["cleared"] = "cleared"
        itemdict["approved"] = False
        itemdict["flag_color"] = None
        itemdict["import_id"] = None

        time = item.get('time')
        strisotime = time.strftime("%Y-%m-%d")
        itemdict["date"] = strisotime
        listoftransactiondictionaries.append(itemdict)

    print("List of transaction dictionaries: "+str(listoftransactiondictionaries))
    newtr = {}
    newtr["transactions"] = listoftransactiondictionaries

    with open("newtransaction.json", "w") as outfile:
        json.dump(newtr, outfile)

    return newtr
