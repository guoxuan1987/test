#!/usr/bin/python2.7
# coding=utf-8
import random
import traceback, json
from Iams.core.V1709061001 import IAMSLoger
from Iams.core.V1709061004 import TBHandler
import uuid
from Iams.core.V1710220801 import InterFace
import hashlib,urllib,urllib2,json
import time
class GC1801090100():
    def __init__(self, iGate):
        self.gate = iGate
        self.msgs = {"200": "",
                     "102": "您访问的方法不正确，请检查之后再试!",
                     "103": "您目前没有访问权限，请联络管理人员!",
                     "600": "您缺少传入正确参数值，操作无法执行!",
                     "601": "年青人操作太快了吧，请休息一会再试!",
                     "602": "工作人员正在加紧处理中，请稍等!",
                     "700": "没有找到符合条件的记录!",
                     "701":"抱歉，不能重复提交！",
                     "702":"抱歉，五分钟内只能投诉一次！"
                     }

        self.__sqlstr = u'../Sql/Itil/Core/t_itil_1801090100.xlsx'
        self.__prikey = "f_itil_1801090100_S00"
        self.__conval = [["", ["f_itil_1801090100_S00", "", "(?)"]],
                         ["", ["f_itil_1801090100_P01", "", "(?)"]],
                         ["", ["f_itil_1801090100_S03", "", "(?)"]],
                         ["", ["f_itil_1801090100_009", "", "(?)"]],
                         ["", ["f_itil_1801090100_011", "", "(?)"]],
                         ["", ["f_itil_1801090100_017", "", "(?)"]],
                         ["", ["f_itil_1801090100_016", "", "(?)"]],
                         ["", ["f_itil_1801090100_018", "", "(?)"]],
                         ["", ["f_itil_1801090100_007", "", "(?)"]],
                         ["", ["f_itil_1801090100_003", "", "(?)"]]]

        self.__srtval = [[["f_itil_1801090100_S00", "(?)"], ["f_itil_1801090100_002", "(?)"]]]

        self.__field = {"G": [],
                        "I": [],
                        "U": []}

        # a={"f_itil_1801090100_S00":["in","123"]}
        # a=[["f_itil_1801090100_S00","asc"],
        #   ["f_itil_1801090100_002","desc"]]

    def send(self, iCode, iArgs={}):
        mCode = str(iCode)
        self.gate.Outval["Message"] = self.msgs[mCode]
        self.gate.Outval["RetCode"] = str(iCode)
        self.gate.Outval["OutData"] = iArgs
        return self.gate.Outval

    def find(self, iKwargs, iRead=True):
        # 定义并检查必要的参数是否存在
        Find = {} if not iKwargs.has_key("Find") else iKwargs["Find"]  # 条件
        Sort = [] if not iKwargs.has_key("Sort") else iKwargs["Sort"]  # 排序
        Udmz = "" if not iKwargs.has_key("Udmz") else iKwargs["Udmz"]  # 范围
        Page = 0 if not iKwargs.has_key("Page") else iKwargs["Page"]  # 页码
        Size = 100 if not iKwargs.has_key("Size") else iKwargs["Size"]  # 大小
        # END

        # 转换数据对象
        try:
            Find = {} if Find == "" else Find
            if not isinstance(Find, dict):
                # Find = json.loads(Find)
                Find = eval(Find)

            Sort = [] if Sort == "" else Sort
            if not isinstance(Sort, list):
                Sort = Sort
                # Sort=json.loads(Sort)

        except Exception, e:
            pass

        # END

        # 依据参数智能匹配条件公式
        def ifmatch(iValue, iConval):
            count = 0
            nConval = ['']
            for k in iValue:
                v = iValue.get(k)
                if len(v) <= 1:  # 传入参数缺失，直接跳过该值
                    continue
                for i in range(0, len(iConval)):
                    for j in range(1, len(iConval[i])):
                        if iConval[i][j][2] != "(?)":
                            count += 1
                            continue
                        if iConval[i][j][0] != k:
                            continue
                        iConval[i][j][1] = v[0]
                        iConval[i][j][2] = v[1]
                        nConval.append(iConval[i][j])
                        count += 1
                    # 匹配所有参数，返回条件公式
                    if count == len(iValue):
                        return nConval
                    # END
            return []

        # END

        # 依据参数智能匹配排序公式
        def srmatch(iValue, iSrtval):
            IAMSLoger.info(iValue)
            for v in iValue:
                if len(v) <= 1:  # 传入参数缺失，直接跳过该值
                    continue

                for i in range(0, len(iSrtval)):
                    # if len(iSrtval[i])-0!=len(iValue):
                    #     continue
                    count = 0
                    for j in range(0, len(iSrtval[i])):
                        if iSrtval[i][j][1] != "(?)":
                            count += 1
                            continue

                        if iSrtval[i][j][0] != v[0]:
                            continue

                        iSrtval[i][j][1] = v[1]
                        count += 1

                    # 匹配所有参数，返回条件公式
                    if count == len(iValue):
                        return iSrtval[i]
                    # END
            return []

        # END

        try:
            TB = TBHandler(self.__sqlstr)
            Where = ifmatch(Find, self.__conval[:])
            if iKwargs.has_key("f_itil_1801090100_009"):
                Where.append(["f_itil_1801090100_009", "==", iKwargs['f_itil_1801090100_009']])
            TB.conval(Where, True)
            # IAMSLoger.info(srmatch(Sort,self.__srtval[:]))
            TB.srtval([['f_itil_1801090100_S00', 'desc']], True)
            TB.filter("Ins", self.__field["I"])
            TB.filter("Upd", self.__field["U"])
            TB.filter("Sel", self.__field["G"])
            TB.DecField = self.__field["G"]
            TB.PageCode = Page
            TB.PageSize = Size
            TB.config()

            if iRead:  # 如果读取不为真，则返回空数据配置
                self.gate.DBSrv.IWrite(TB.reload())
            return TB
        except Exception, e:
            IAMSLoger.error(str(e) + "\r\n" + traceback.format_exc())
            return self.send(600)

    def gprc(self, iKwargs):
        Result = self.find(iKwargs)
        if not isinstance(Result, TBHandler):
            return Result  # 查询过程出现异常

        Code = 200 if Result.SrcCount > 0 else 700
        return self.send(Code, {"Table": Result.SrcTable, "Total": Result.RecTotal})

    def geocode(self,address):
        url = 'http://api.map.baidu.com/geocoder/v2/'
        output = 'json'
        ak = 'p95NojO3aOaVrKpz6B10lcZjVo7GceRs'  # 浏览器端密钥
        values = {"address": address, "ak": ak,"output":output}
        data = urllib.urlencode(values)
        request = urllib2.Request(url, data)
        response = urllib2.urlopen(request)
        res = response.read()
        temp = json.loads(res)
        lat = temp['result']['location']['lat']
        lng = temp['result']['location']['lng']
        return lng,lat

    def iprc(self, iKwargs):
        lon,lat=self.geocode(iKwargs["f_itil_1801090100_012"]+iKwargs["f_itil_1801090100_013"]+iKwargs["f_itil_1801090100_014"]+iKwargs["f_itil_1801090100_015"])
        try:
            # 生成唯一编号
            TB = TBHandler(self.__sqlstr)
            P01 = str(time.time()).replace('.', '')
            if len(P01)<12:
                P01+="0"*(12-len(P01))
            randcode="".join([random.choice([chr(x) for x in range(ord("A"),ord("Z")+1)]) for i in range(4)])
            P01 = randcode+P01
            iKwargs.update({"f_itil_1801090100_P01": P01})
            iKwargs.update({"f_itil_1801090100_011": iKwargs["UserId"]})
            iKwargs.update({"f_itil_1801090100_017": time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))})
            iKwargs.update({"f_itil_1801090100_031": lon})
            iKwargs.update({"f_itil_1801090100_032": lat})
            TB.change("I", iKwargs, self.__prikey)
            self.gate.DBDef.IWrite(TB.submit().reload())
        except Exception, e:
            IAMSLoger.error(str(e) + "\r\n" + traceback.format_exc())
            return self.send(600)
        iResult = {"Table": [iKwargs], "Total": "OK"}
        # # 101表插入报障进度信息
        T2 = TBHandler(u'../Sql/Itil/Core/t_itil_1801090101.xlsx')
        IValue = {"f_itil_1801090101_E01": P01,
                  "f_itil_1801090101_001": iKwargs['f_itil_1801090100_002'],
                  "f_itil_1801090101_002": "系统正为您派单,请耐心等待",
                  "f_itil_1801090101_003":0,
                  "f_itil_1801090101_010":"订单提交",
                  "f_itil_1801090101_013":0}
        T2.change("I", IValue, "f_itil_1801090101_S00")
        self.gate.DBDef.IWrite(T2.submit().reload())
        # 给符合技能条件的工程师们发送短信并并推送艾米消息
        s=iKwargs["f_itil_1801090100_016"].split("/")[0]
        tb5=TBHandler(u'../Sql/Itil/Core/t_itil_1801090105.xlsx')
        tb5.ConByVal=["",["f_itil_1801090105_H04","<>",s]]
        self.gate.DBDef.IWrite(tb5.config().reload())
        for i in tb5.SrcTable:
            name=iKwargs["f_itil_1801090100_002"]+"("+iKwargs["f_itil_1801090100_003"]+")"
            ad=iKwargs["f_itil_1801090100_012"]+iKwargs["f_itil_1801090100_013"]+iKwargs["f_itil_1801090100_014"]
            iArgs = {"User": i["f_itil_1801090105_H03"], "params": {"name":name,"type":s,"ad":ad},
                         "TmlId": "SMS_137975027", "Auther": "古诚运维"}
            InterFace.postface("smssdef", "send", **iArgs)
            # iArgs = {
            #          "acceptor":str([{"acceptorId":str(i["f_itil_1801090105_H12"]),"type":"4"}]).replace("'",'"'),
            #          "type": "notify",
            #          "notify": '{"title":"运维订单提醒","content1":"报障类型：%s",\
            #          "content2":"上门地址：%s","content3":"问题描述：%s",\
            #          "clickUrl":"https://itil.skytek.com.cn/Itil/Htm/iuser/index.htm?gcsbh=%s&jd=%s&wd=%s&zt=%s"}'%(
            #              str(iKwargs["f_itil_1801090100_016"]),
            #              str(iKwargs["f_itil_1801090100_014"]+str(iKwargs["f_itil_1801090100_015"])),
            #              str(iKwargs["f_itil_1801090100_004"]),
            #              str(i["f_itil_1801090105_P01"]),
            #              str(i["f_itil_1801090105_H13"]),
            #              str(i["f_itil_1801090105_H14"]),
            #              "1")
            #          }
            # # https: // devpython.iwifi.com:8081
            # InterFace.postface("wchat", "A102", **iArgs)
        # END
        return self.send(200, iResult)
    def sendaimi(self,l,iKwargs):
        pass
    def GetJsApiParameters(self, iKwargs, iKey, iTime):
        mList = []
        mDict = {"appId": iKwargs["appid"], "timeStamp": iTime, "nonceStr": iKwargs['nonce_str'], "signType": "MD5",
                 "package": "prepay_id=" + iKwargs['prepay_id']}
        for k in sorted(mDict.keys()):
            v = mDict.get(k)
            if not v:  # 参数的值为空不参与签名
                continue
            mList.append('{0}={1}'.format(k, v))
        mList.append('key={}'.format(iKey))  # 接密钥
        mKeys = '&'.join(mList)
        IAMSLoger.info(mKeys)
        return hashlib.md5(mKeys).hexdigest()

    def uprc(self, iKwargs):
        Result = self.find(iKwargs)
        if not isinstance(Result, TBHandler):
            return Result  # 查询过程出现异常

        IValue = iKwargs if not iKwargs.has_key("Rows") else iKwargs["Rows"]  # 多行写
        if not isinstance(IValue, dict) and not isinstance(IValue, list):
            IValue = iKwargs

        try:
            Result.change("U", IValue, self.__prikey)
            Result.submit()
            self.gate.DBSrv.IWrite(Result.reload())
        except Exception, e:
            IAMSLoger.error(str(e) + "\r\n" + traceback.format_exc())
            return self.send(600)

        Code = 200 if Result.SrcCount > 0 else 700
        return self.send(Code, {"Table": Result.SrcTable, "Total": Result.RecTotal})

    def mprc(self, iKwargs):
        IValue = []
        Result = self.find(iKwargs, False)
        if not isinstance(Result, TBHandler):
            return Result  # 查询过程出现异常

        # 将字符串参转换成数组模型
        try:
            Keys = iKwargs["Keys"]  # 强制获取出错
            Keys = [] if Keys == "" else Keys
            if not isinstance(Keys, list):
                Keys = json.loads(Keys)

            for i in range(0, len(Keys)):
                Key = {self.__prikey: Keys[i]}
                IValue.append(Key)

        except Exception, e:
            IAMSLoger.error(str(e) + "\r\n" + traceback.format_exc())
            return self.send(600)
        # END

        try:
            Result.change("M", IValue, self.__prikey)
            Result.submit()
            self.gate.DBSrv.IWrite(Result.reload())
        except Exception, e:
            IAMSLoger.error(str(e) + "\r\n" + traceback.format_exc())
            return self.send(600)

        Code = 200 if Result.SrcCount > 0 else 700
        return self.send(Code, {"Table": Result.SrcTable, "Total": Result.RecTotal})
        # END

    def call(self, iKwargs):
        pass