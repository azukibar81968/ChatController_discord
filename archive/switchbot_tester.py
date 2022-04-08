import urllib.request
if __name__ == "__main__"

    ###infrastructure
    token = 'dc5a7aadc853a2ba876df7e91b31502b5711ebe2f768e0f65dbf5f34d44795381037944055282f05a9425748c4a56efd'
    header_switchbot_API = {
        'Authorization': token, 
        'Content-Type' : 'application/json; charset=utf8'
    }
    reqData_nul = None


    deviceID_airconditioner = "01-202111261043-97541592"
    deviceID_airconditioner = "01-202111261043-97541592"

    url_switchbot_API_test = 'https://api.switch-bot.com/v1.0/devices'
    method_switchbot_API_test = 'GET'


    url_switchbot_API_commands = "https://api.switch-bot.com/v1.0/devices/" + deviceID_airconditioner + "/commands"
    reqData_switchbot_API_commands = {
        "command": "setAll",
        "parameter": "26,1,3,on",
        "commandType": "command"
    }
    method_switchbot_API_commands = 'POST'




    req = urllib.request.Request(
        url_switchbot_API_test, 
        reqData_nul, 
        header_switchbot_API, 
        method = method_switchbot_API_test
    )

    with urllib.request.urlopen(req) as res:
        body = res.read()
        print(body)


