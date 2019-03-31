# -*- coding: utf-8 -*-
import xaparser
import xalogger
import win32com.client

log = xalogger.XALogger(__name__)
class _XAQueryEvents:
    def __init__(self):
        self.status = 0
        self.code = None
        self.msg = None

    def reset(self):
        self.status = 0
        self.code = None
        self.msg = None

    def OnReceiveData(self, szTrCode):
        log.debug(" - [%s:%s] OnReceiveData" % (szTrCode, xaparser.parseTR(szTrCode)))
        self.status = 1

    def OnReceiveMessage(self, systemError, messageCode, message):
        self.code = str(messageCode)
        self.msg = str(message)
        if self.code != "00000":
            log.debug(" - [%s:%s] OnReceiveMessage" % (self.code, self.msg))
            
    def OnReceiveChartRealData(self):
        pass

    def OnReceiveSearchRealData(self):
        pass

class Query:
    """TR 조회를 위한 XAQuery 확장 클래스
        :param type: TR 번호
        :type type: str
        :param callNext: callNext가 False인 경우, 한번만 조회, True일 경우, 다음(occur)이 있으면 계속 조회 (기본값은 True)
        :type callNext: bool
        ::

            query = Query("t8407")
            query = Query("t1101", False)
    """
    def __init__(self, tr_code, call_next=True):
        self.query = win32com.client.DispatchWithEvents("XA_DataSet.XAQuery", _XAQueryEvents)
        self.query.LoadFromResFile("C:/Users/Jisung/Desktop/xingpy/xingpy/res/" + tr_code + ".res")
        self.tr_code = tr_code
        self.call_next = call_next

    def _parseInput(self,param):
        log.info(">>>>> [%s-Query] 입력:%s" % (self.tr_code, param))
        for v in param.keys():
            if v != "Service":
                self.inputName = v
        self.input = param[self.inputName]
        self.compress = "comp_yn" in self.input.keys() and self.input["comp_yn"] == "Y"
        if "Service" in param:
            self.service = param["Service"]
        pass

    def _parseOutput(self,param):
        self.output = {}
        for k,v in param.items():
            if isinstance(v, DataFrame):
				#occur
                self.output[k] = v
            else:
                self.output[k] = {}
                for p in v:
                    self.output[k][p] = None

    def request(self):
        try :		
            if not input:
                input = {"InBlock": {}}
            if not isNext:
                self.query.reset()
                self._parseInput(input)
                self._parseOutput(output)
        
            for k,v in self.input.items():
                self.query.SetFieldData(self.type + self.inputName, k, 0, v)
        
        except Exception:
            traceback.print_exc(file=sys.stdout)
if __name__ == "__main__":
    query = Query('t8407')
    query.request({
			 		"InBlock" : {
			 			"nrec" : 2,
			 			"shcode" : "".join(["005930","035420"])
			 		}
			 	},{
			 		"OutBlock1" : DataFrame(columns=("shcode","hname","price","open","high",
							"low","sign","change","diff","volume"))
				})
#     query = Query("t8407")
#     print(dir(query))
#     print(query)
#     print("".join(["005930","035420"]))