import requests, json, singleton


class SwitchBotConnector(singleton.Singleton):

    def __init__(self):
        # パラメーター
        self.DEVICEID_airConditioner="01-202111261043-97541592"
        self.DEVICEID_light="01-202111261049-19784894"
        self.ACCESS_TOKEN="dc5a7aadc853a2ba876df7e91b31502b5711ebe2f768e0f65dbf5f34d44795381037944055282f05a9425748c4a56efd"
        self.API_BASE_URL="https://api.switch-bot.com"

    # Send device control commandsコマンド（POST）
    def device_control(self, deviceID, body):
        headers = {
            # ヘッダー
            'Content-Type': 'application/json; charset: utf8',
            'Authorization': self.ACCESS_TOKEN
        }
        url = self.API_BASE_URL + "/v1.0/devices/" + deviceID + "/commands"

        inputJson = json.dumps(body)
        print(inputJson) # 入力
        res = requests.post(url, data=inputJson, headers=headers)
        print(res.text) # 結果



if __name__ == '__main__':
    # 処理呼び出し
    body = {
        # 操作内容
        "command":"turnOff",
        "commandType":"command"
    }
    SwitchBotConnector().device_control(SwitchBotConnector().DEVICEID_light, body)