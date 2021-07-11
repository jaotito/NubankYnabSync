#intakes the nubank statements list and outputs the same list
#with naive local time

def fixtime(nu_transactions, data):

    import pytz
    from datetime import datetime
    testcount = 0
    USER_TIMEZONE = data.get("USER_TIMEZONE")

    localtz = pytz.timezone(USER_TIMEZONE)
    for item in nu_transactions:
        no_tz_datetime = datetime.strptime(item.get('time'),"%Y-%m-%dT%H:%M:%SZ")
        datetime = no_tz_datetime.replace(tzinfo=pytz.utc)
        local_datetime = datetime.astimezone(tz=localtz).replace(tzinfo=None)
        local_datetime = local_datetime.replace(hour=0, minute=0, second=0, microsecond=0)
        item['time'] = local_datetime

    for item in nu_transactions:
        item["amount"] = item.get("amount") * -10 #making amount compatible with ynab

    return nu_transactions
