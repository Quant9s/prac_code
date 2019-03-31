import win32com.client
import pythoncom
import time

import xing_login


class XQuery_t1301:
def __init__(self):
self.is_data_received = False
self.ctstime = ""

def OnReceiveData(self, tr_code):
self.is_data_received = True
count = self.GetBlockCount("t1301OutBlock1") # 반복데이터(Occurs) 갯수 가져오기
print("count = {0}".format(count))
print("TR code ==> {0}".format(tr_code))

for i in range(count):
chetime = self.GetFieldData("t1301OutBlock1", "chetime", i)
price = self.GetFieldData("t1301OutBlock1", "price", i)
volume = self.GetFieldData("t1301OutBlock1", "volume", i)
print("{3} - 거래시간;{0}, 현재가;{1},누적거래량;{2}".format(chetime, price, volume, i))

self.ctstime = self.GetFieldData("t1301OutBlock", "cts_time", 0)
print("--{0}--".format(self.ctstime))

if self.ctstime != "": # self.ctstime 값이 존재하면, 연속 data 가 있다는 의미...
time.sleep(0.5) # TR 횟수 제한때문에...
self.continue_search(self.ctstime)

def occurs_request(self, stockcode):
self.ResFileName = "C:\\eBEST\\xingAPI\\Res\\t1301.res" # RES 파일 등록
self.SetFieldData("t1301InBlock", "shcode", 0, stockcode)
# self.SetFieldData("t1301InBlock", "starttime", 0, "1001")
# self.SetFieldData("t1301InBlock", "endtime", 0, "1210")
err_code = self.Request(False) # data 요청하기 -- 연속조회인경우만 True

if err_code < 0:
print("error... {0}".format(err_code))

def continue_search(self, ctstime):
"""
연속조회하기
"""
print("-----------------------------------------")
self.is_data_received = False
self.SetFieldData("t1301InBlock", "cts_time", 0, ctstime)
err_code = self.Request(True) # 연속조회인경우만 True

if err_code < 0:
print("error... {0}".format(err_code))

@classmethod
def get_instance(cls):
xq_t1301 = win32com.client.DispatchWithEvents("XA_DataSet.XAQuery", cls)
return xq_t1301



if __name__ == "__main__":
def get_occurs_continue_data():
xq_t1301 = XQuery_t1301.get_instance()
xq_t1301.occurs_request("005930")

while xq_t1301.is_data_received == False:
pythoncom.PumpWaitingMessages()


xsession = xing_login.XSession.get_instance()
xsession.api_login()

get_occurs_continue_data()


출처: https://freeprog.tistory.com/343 [취미로 하는 프로그래밍 !!!]