import os
from flask import Flask, request, Response
from NYSync.getnu import getnu
from NYSync.fix_time import fixtime
from NYSync.getynab import getynab
from NYSync.converttr import converttr
from NYSync.postynab import postynab


app = Flask(__name__)
app.config.from_mapping(SECRET_KEY=os.getenv("SECRET_KEY_FLASK"))
@app.route("/webhook", methods=["GET"])
def sync():

    env_vars = dict(
        CERT_NU = os.getenv("CERT_NU"),
        SENHA_NU = os.getenv("SENHA_NU"),
        CPF_NU = os.getenv("CPF_NU"),
        USER_TIMEZONE = os.getenv("USER_TIMEZONE"),
        BUDGETID_YNAB = os.getenv("BUDGETID_YNAB"),
        ACCOUNTID_YNAB = os.getenv("ACCOUNTID_YNAB"),
        TOKEN_YNAB = os.getenv("TOKEN_YNAB"),
        Max_days = os.getenv("Max_days")
        )

    rawnutr = getnu(env_vars)#Gets all card negative transactions from nu
    nutr = fixtime(rawnutr, env_vars)#returns nu transactions with time and ammounts comparable with ynab
    ynab = getynab(env_vars)#Gets data from last ynab registered transactions
    lytd = ynab.get("date")#last Ynab Transaction Date (ignores positive transactions)
    lytr = ynab.get("transactions")#last Ynab TRansactions that happened on the lytd

    deltatr = [] # here we will append all Nu transactions that will be sync'd
    samedatetr = []# this list will hold nu transactions that happened on the lytd
    for tr in nutr:
        ntd = tr.get("time")
        if ntd < lytd :
            continue
        elif ntd > lytd:
            print("current item ntd: ",ntd,"lytd: ",lytd)
            deltatr.append(tr)
            print("current item added to deltatr: ",tr)
            print("current state of deltatr: ", deltatr)
        elif ntd == lytd:
            print("current item ntd: ",ntd,"lytd: ",lytd)
            samedatetr.append(tr)
            print("added to samedatetr: ",tr)
            print("current state of samedatetr: ", samedatetr)

    lytr_amounts = [d['amount'] for d in lytr if 'amount' in d]
    print("lytr_amounts: ",lytr_amounts)
    for tr in samedatetr:
        if len(samedatetr) <= len(lytr):
            print("number of samedatetr<= lytr")
            break
        if int(tr.get("amount")) not in lytr_amounts:
            samedatetr.remove(tr)
            deltatr.append(tr)
            print("deltatr after samedatetr additions: ",deltatr)
            continue

    newtr = converttr(deltatr,env_vars)

    print("post to ynab result:",postynab(newtr,env_vars))

    return Response (status=200)
