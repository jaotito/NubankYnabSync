#gets the last date of a transaction
def getynab(data):

    from datetime import datetime, timedelta
    import pytz
    import requests
    import os

    USER_TIMEZONE = data.get("USER_TIMEZONE")
    BUDGETID_YNAB = data.get("BUDGETID_YNAB")
    ACCOUNTID_YNAB = data.get("ACCOUNTID_YNAB")
    TOKEN_YNAB = data.get("TOKEN_YNAB")
    Max_days = data.get("Max_days")


    #define since_date based on USER_TIMEZONE + Max_days and format to

    since_datetime = datetime.now() - timedelta(days = int(Max_days))
    since_datetime = since_datetime.replace(hour=0, minute=0, second=0, microsecond=0)
    print("since_datetime",str(since_datetime))
    since_date = since_datetime.strftime("%Y-%m-%d")
    print("since_date",str(since_date))


    url = "https://api.youneedabudget.com/v1/budgets/"+BUDGETID_YNAB+"/accounts/"+ACCOUNTID_YNAB+"/transactions"
    headers = {"Authorization": "Bearer "+TOKEN_YNAB}
    payload = {"since_date":since_date}

    r = requests.get(url, params=payload, headers=headers)
    if r.status_code != 200:
        print("bad data from ynab",str(r.status_code),r.text)

    ynab_response_data = dict(r.json())

    ynab_transactions_list = ynab_response_data.get("data").get("transactions")

    last_transaction_date = since_datetime
    print("first last_transaction_date",str(last_transaction_date))

    for transaction in ynab_transactions_list:
        datetime = datetime.strptime(transaction.get("date"),"%Y-%m-%d")
        transaction["date"] = datetime

        if (datetime > last_transaction_date)and(transaction.get("amount")<0):
            last_transaction_date = datetime
    print("last_transaction_date: ",last_transaction_date)
    last_transactions_list = []
    for transaction in ynab_transactions_list:
        if transaction.get("date") == last_transaction_date:
            last_transactions_list.append(transaction)

    print("last_transactions_list: ",last_transactions_list)

    returndict = dict(date=last_transaction_date,transactions=last_transactions_list)
    return returndict
