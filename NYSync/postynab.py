
#posts transactions to specific budget utilizing ynab api token 

def postynab(newtr, data):#receives transactions that will be posted to ynab
    import requests
    import os

    BUDGETID_YNAB = data.get("BUDGETID_YNAB") #received from argument data
    TOKEN_YNAB = data.get("TOKEN_YNAB") #received from argument data

    url = "https://api.youneedabudget.com/v1/budgets/"+BUDGETID_YNAB+"/transactions"
    headers = {"Authorization": "Bearer "+TOKEN_YNAB}
    payload = newtr
    print("POST Payload: "+str(payload))
    r = requests.post(url, json=payload , headers=headers)
    print("POST request response text: "+ r.text)
    print("POST request response code: "+ str(r.status_code))
    return r.status_code
