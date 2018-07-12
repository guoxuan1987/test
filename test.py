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
                     "102": "�����ʵķ�������ȷ������֮������!",
                     "103": "��Ŀǰû�з���Ȩ�ޣ������������Ա!",
                     "600": "��ȱ�ٴ�����ȷ����ֵ�������޷�ִ��!",
                     "601": "�����˲���̫���˰ɣ�����Ϣһ������!",
                     "602": "������Ա���ڼӽ������У����Ե�!",
                     "700": "û���ҵ����������ļ�¼!",
                     "701":"��Ǹ�������ظ��ύ��",
                     "702":"��Ǹ���������ֻ��Ͷ��һ�Σ�"
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
        # ���岢����Ҫ�Ĳ����Ƿ����
        Find = {} if not iKwargs.has_key("Find") else iKwargs["Find"]  # ����
        Sort = [] if not iKwargs.has_key("Sort") else iKwargs["Sort"]  # ����
        Udmz = "" if not iKwargs.has_key("Udmz") else iKwargs["Udmz"]  # ��Χ
        Page = 0 if not iKwargs.has_key("Page") else iKwargs["Page"]  # ҳ��
        Size = 100 if not iKwargs.has_key("Size") else iKwargs["Size"]  # ��С
        # END

        # ת�����ݶ���
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

        # ���ݲ�������ƥ��������ʽ
        def ifmatch(iValue, iConval):
            count = 0
            nConval = ['']
            for k in iValue:
                v = iValue.get(k)
                if len(v) <= 1:  # �������ȱʧ��ֱ��������ֵ
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
                    # ƥ�����в���������������ʽ
                    if count == len(iValue):
                        return nConval
                    # END
            return []

        # END

        # ���ݲ�������ƥ������ʽ
        def srmatch(iValue, iSrtval):
            IAMSLoger.info(iValue)
            for v in iValue:
                if len(v) <= 1:  # �������ȱʧ��ֱ��������ֵ
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

                    # ƥ�����в���������������ʽ
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

            if iRead:  # �����ȡ��Ϊ�棬�򷵻ؿ���������
                self.gate.DBSrv.IWrite(TB.reload())
            return TB
        except Exception, e:
            IAMSLoger.error(str(e) + "\r\n" + traceback.format_exc())
            return self.send(600)

    def gprc(self, iKwargs):
        Result = self.find(iKwargs)
        if not isinstance(Result, TBHandler):
            return Result  # ��ѯ���̳����쳣

        Code = 200 if Result.SrcCount > 0 else 700
        return self.send(Code, {"Table": Result.SrcTable, "Total": Result.RecTotal})

    def geocode(self,address):
        url = 'http://api.map.baidu.com/geocoder/v2/'
        output = 'json'
        ak = 'p95NojO3aOaVrKpz6B10lcZjVo7GceRs'  # ���������Կ
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
            # ����Ψһ���
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
        # # 101����뱨�Ͻ�����Ϣ
        T2 = TBHandler(u'../Sql/Itil/Core/t_itil_1801090101.xlsx')
        IValue = {"f_itil_1801090101_E01": P01,
                  "f_itil_1801090101_001": iKwargs['f_itil_1801090100_002'],
                  "f_itil_1801090101_002": "ϵͳ��Ϊ���ɵ�,�����ĵȴ�",
                  "f_itil_1801090101_003":0,
                  "f_itil_1801090101_010":"�����ύ",
                  "f_itil_1801090101_013":0}
        T2.change("I", IValue, "f_itil_1801090101_S00")
        self.gate.DBDef.IWrite(T2.submit().reload())
        # �����ϼ��������Ĺ���ʦ�Ƿ��Ͷ��Ų������Ͱ�����Ϣ
        s=iKwargs["f_itil_1801090100_016"].split("/")[0]
        tb5=TBHandler(u'../Sql/Itil/Core/t_itil_1801090105.xlsx')
        tb5.ConByVal=["",["f_itil_1801090105_H04","<>",s]]
        self.gate.DBDef.IWrite(tb5.config().reload())
        for i in tb5.SrcTable:
            name=iKwargs["f_itil_1801090100_002"]+"("+iKwargs["f_itil_1801090100_003"]+")"
            ad=iKwargs["f_itil_1801090100_012"]+iKwargs["f_itil_1801090100_013"]+iKwargs["f_itil_1801090100_014"]
            iArgs = {"User": i["f_itil_1801090105_H03"], "params": {"name":name,"type":s,"ad":ad},
                         "TmlId": "SMS_137975027", "Auther": "�ų���ά"}
            InterFace.postface("smssdef", "send", **iArgs)
            # iArgs = {
            #          "acceptor":str([{"acceptorId":str(i["f_itil_1801090105_H12"]),"type":"4"}]).replace("'",'"'),
            #          "type": "notify",
            #          "notify": '{"title":"��ά��������","content1":"�������ͣ�%s",\
            #          "content2":"���ŵ�ַ��%s","content3":"����������%s",\
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
            if not v:  # ������ֵΪ�ղ�����ǩ��
                continue
            mList.append('{0}={1}'.format(k, v))
        mList.append('key={}'.format(iKey))  # ����Կ
        mKeys = '&'.join(mList)
        IAMSLoger.info(mKeys)
        return hashlib.md5(mKeys).hexdigest()

    def uprc(self, iKwargs):
        Result = self.find(iKwargs)
        if not isinstance(Result, TBHandler):
            return Result  # ��ѯ���̳����쳣

        IValue = iKwargs if not iKwargs.has_key("Rows") else iKwargs["Rows"]  # ����д
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
            return Result  # ��ѯ���̳����쳣

        # ���ַ�����ת��������ģ��
        try:
            Keys = iKwargs["Keys"]  # ǿ�ƻ�ȡ����
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