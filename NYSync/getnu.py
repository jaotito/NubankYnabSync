def getnu(data):

    import os
    from pynubank import Nubank
    import base64



    CERT_NU = data.get("CERT_NU")
    SENHA_NU = data.get("SENHA_NU")
    CPF_NU = data.get("CPF_NU")

    
    with open("certnew.p12", "wb") as f:
        cert_content = base64.b64decode(CERT_NU)
        f.write(cert_content)

    nu = Nubank()
    nu.authenticate_with_cert(CPF_NU, SENHA_NU,"certnew.p12")
    statements = nu.get_card_statements()
    # print(os.path.abspath("certnew.p12"))
    os.remove("certnew.p12")
    # print(os.path.abspath("certnew.p12"))
    # statements_dict = dict(statements)
    #
    # with open("../Tests/statements_dict.json", "w") as f:
    #     json.dump(statements_dict, f)
    return statements
