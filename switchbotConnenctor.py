import requests, json, singleton
from zmq import device
import datetime
import sqlInterface

class KadenControll:
    def __init__(self):
        self._kadenConnector = SwitchBotConnector()
        return
    
    def deal(self, command):
        controller = None
        print(command)
        if command["option"]["task"]["head"] == "airconditioner":
            controller = AirConditionerControll()
        elif command["option"]["task"]["head"] == "light":
            controller = LightControll()


        controller.deal(command)   


class AirConditionerControll:
    def __init__(self):
        self.mode = ""
        self.fanspeed = ""
        self.temp = ""
        self.powerstate = ""
        self.inputJson = {}
        self._kadenConnector = SwitchBotConnector()
        

    def deal(self, command):
        try:
            self.powerstate = command["option"]["task"]["option"]["action"]["head"]
            if self.powerstate == "on":
                self.fanspeed = "1" 
#                self.temp = command["option"]["task"]["option"]["action"]["option"]["?temp"] #TODO: tempがあってもなくても動くようにしたい
                if command["option"]["task"]["option"]["action"]["option"]["mode"] == "hot":
                    self.mode = "5"
                elif command["option"]["task"]["option"]["action"]["option"]["mode"] == "cool":
                    self.mode = "2"

                self.inputJson = {
                        "command": "setAll",
                        "parameter": self.temp + "," + self.mode + "," + self.fanspeed + "," + self.powerstate,
                        "commandType": "command"
                    }
                
            elif self.powerstate == "off":
                self.inputJson = {
                    "command": "turnOff",
                    "commandType": "command"
                }
                

        except Exception as e:
            print('=== エラー内容 ===')
            print('type:' + str(type(e)))
            print('args:' + str(e.args))
            print('message:' + e.message)
            print('e自身:' + str(e))
            print("ERROR: aircon Commandの辞書見出しが不正です。")
        
        self._kadenConnector.device_control(
            self._kadenConnector.DEVICEID_airConditioner, 
            self.inputJson
        )
        print("switchbot query = " + str(self.inputJson))


class LightControll:
    def __init__(self):
        self.powerstate = ""
        self._kadenConnector = SwitchBotConnector()

    def deal(self, command):
        try:
            self.powerstate = command["option"]["task"]["option"]["action"]["head"]
        except Exception as e:
            print('=== エラー内容 ===')
            print('type:' + str(type(e)))
            print('args:' + str(e.args))
            print('message:' + e.message)
            print('e自身:' + str(e))
            print("ERROR: Commandの辞書見出しが不正です。")

        if self.powerstate == "on":
            self._kadenConnector.device_control(
                self._kadenConnector.DEVICEID_light, 
                {
                    "command": "turnOn",
                    "commandType": "command"
                }
            )
        elif self.powerstate == "off":

            self._kadenConnector.device_control(
                self._kadenConnector.DEVICEID_light, 
                {
                    "command": "turnOff",
                    "commandType": "command"
                }
            )
        




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

        self.regist_to_DB(deviceID, body)


    def regist_to_DB(self, deviceID, command):
        headers = {'content-type': 'application/json'}
        TODAY = datetime.date.today()
        dt_now = datetime.datetime.now()
        
        DEVICE = ""
        if deviceID == self.DEVICEID_airConditioner:
            DEVICE = "Air Conditioner"
        elif deviceID == self.DEVICEID_light:
            DEVICE = "Light"

        #SQLクエリを作成
        queryDict = {
            "data" : [
                ["date", "\'" + str(TODAY) + "\'"],
                ["time", "\'" + str(dt_now.hour).zfill(2)+str(dt_now.minute).zfill(2) + "\'"],
                ["checked", "false"],
                ["device", "\'" + DEVICE + "\'"],
                ["command", "\'" + str(command).replace("\'", "\"") + "\'"],
            ],
            "table" : "Switchbot_DeviceLog"
        }  

        return requests.post("http://10.0.1.94:5000/insert/", data=json.dumps(queryDict), headers=headers)



if __name__ == '__main__':
    # 処理呼び出し
    body = {
        # 操作内容
        "command":"turnOff",
        "commandType":"command"
    }
    SwitchBotConnector().device_control(SwitchBotConnector().DEVICEID_light, body)