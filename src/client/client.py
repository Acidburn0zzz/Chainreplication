import da
PatternExpr_0 = da.pat.TuplePattern([da.pat.ConstantPattern('REPLY'), da.pat.FreePattern('reqID'), da.pat.FreePattern('outcome'), da.pat.FreePattern('accountNumber'), da.pat.FreePattern('balance')])
PatternExpr_1 = da.pat.TuplePattern([da.pat.ConstantPattern('HEAD_UPDATE'), da.pat.FreePattern('bankName'), da.pat.FreePattern('head')])
PatternExpr_2 = da.pat.FreePattern('master')
PatternExpr_3 = da.pat.TuplePattern([da.pat.ConstantPattern('TAIL_UPDATE'), da.pat.FreePattern('bankName'), da.pat.FreePattern('tail')])
PatternExpr_4 = da.pat.TuplePattern([da.pat.ConstantPattern('REPLY'), da.pat.BoundPattern('_BoundPattern16_'), da.pat.FreePattern(None), da.pat.FreePattern(None), da.pat.FreePattern(None)])
PatternExpr_6 = da.pat.TuplePattern([da.pat.ConstantPattern('REPLY'), da.pat.BoundPattern('_BoundPattern34_'), da.pat.FreePattern(None), da.pat.FreePattern(None), da.pat.FreePattern(None)])
PatternExpr_8 = da.pat.TuplePattern([da.pat.ConstantPattern('REPLY'), da.pat.BoundPattern('_BoundPattern52_'), da.pat.FreePattern(None), da.pat.FreePattern(None), da.pat.FreePattern(None)])
PatternExpr_10 = da.pat.TuplePattern([da.pat.ConstantPattern('TAIL_UPDATE'), da.pat.FreePattern(None), da.pat.FreePattern(None)])
import json
import sys
from itertools import chain
import time
import random
from common_headers import opOutcome


class Bank:

    def __init__(self, name, head, tail):
        self.name = name
        self.head = head
        self.tail = tail


class Client(da.DistProcess):

    def __init__(self, parent, initq, channel, props):
        super().__init__(parent, initq, channel, props)
        self._ClientReceivedEvent_3 = []
        self._ClientReceivedEvent_4 = []
        self._ClientReceivedEvent_5 = []
        self._ClientReceivedEvent_6 = []
        self._events.extend([
        da.pat.EventPattern(da.pat.ReceivedEvent, '_ClientReceivedEvent_0', PatternExpr_0, sources=None, destinations=None, timestamps=None, record_history=None, handlers=[self._Client_handler_0]), 
        da.pat.EventPattern(da.pat.ReceivedEvent, '_ClientReceivedEvent_1', PatternExpr_1, sources=[PatternExpr_2], destinations=None, timestamps=None, record_history=None, handlers=[self._Client_handler_1]), 
        da.pat.EventPattern(da.pat.ReceivedEvent, '_ClientReceivedEvent_2', PatternExpr_3, sources=None, destinations=None, timestamps=None, record_history=None, handlers=[self._Client_handler_2]), 
        da.pat.EventPattern(da.pat.ReceivedEvent, '_ClientReceivedEvent_3', PatternExpr_4, sources=None, destinations=None, timestamps=None, record_history=True, handlers=[]), 
        da.pat.EventPattern(da.pat.ReceivedEvent, '_ClientReceivedEvent_4', PatternExpr_6, sources=None, destinations=None, timestamps=None, record_history=True, handlers=[]), 
        da.pat.EventPattern(da.pat.ReceivedEvent, '_ClientReceivedEvent_5', PatternExpr_8, sources=None, destinations=None, timestamps=None, record_history=True, handlers=[]), 
        da.pat.EventPattern(da.pat.ReceivedEvent, '_ClientReceivedEvent_6', PatternExpr_10, sources=None, destinations=None, timestamps=None, record_history=True, handlers=[])])

    def main(self):
        bankName = self.bank_name
        tail = None
        time.sleep(8)
        self.register(self.bank_name)

        def ExistentialOpExpr_3():
            for (_, _, (_ConstantPattern80_, _, _)) in self._ClientReceivedEvent_6:
                if (_ConstantPattern80_ == 'TAIL_UPDATE'):
                    if True:
                        return True
            return False
        _st_label_93 = 0
        while (_st_label_93 == 0):
            _st_label_93+=1
            if ExistentialOpExpr_3():
                _st_label_93+=1
            else:
                super()._label('_st_label_93', block=True)
                _st_label_93-=1
        reqSent = 0
        acNumber = random.randint(2000, 3000)
        if (len(self.reqList) == 0):
            while (reqSent <= self.totalReq):
                val = random.random()
                amnt = random.randint(1, 1000)
                if (val <= self.getP):
                    self.getBalance(self.bank_name, acNumber, self.tryC)
                elif (val <= (self.getP + self.depP)):
                    self.deposit(self.bank_name, acNumber, amnt, self.tryC)
                elif (val <= ((self.getP + self.depP) + self.withP)):
                    self.withdraw(self.bank_name, acNumber, amnt, self.tryC)
                reqSent+=1
        else:
            for tup in self.reqList:
                acNumber = tup['accNo']
                if (tup['type'] == 'getBalance'):
                    self.getBalance(self.bank_name, acNumber, self.tryC)
                elif (tup['type'] == 'deposit'):
                    self.deposit(self.bank_name, acNumber, tup['amt'], self.tryC)
                elif (tup['type'] == 'withdraw'):
                    self.withdraw(self.bank_name, acNumber, tup['amt'], self.tryC)
        _st_label_115 = 0
        while (_st_label_115 == 0):
            _st_label_115+=1
            if 0:
                _st_label_115+=1
            else:
                super()._label('_st_label_115', block=True)
                _st_label_115-=1

    def setup(self, cId, bank_name, master, bankList, totalReq, getP, depP, withP, reqList, dropRate):
        self.withP = withP
        self.cId = cId
        self.depP = depP
        self.getP = getP
        self.reqList = reqList
        self.bank_name = bank_name
        self.master = master
        self.totalReq = totalReq
        self.dropRate = dropRate
        self.bankList = bankList
        self.seq = (-1)
        self.T = 3
        self.tryC = 3
        self.responses = []

    def register(self, bankName):
        self._send(('REGISTER', bankName), self.master)

    def retrieveHead(self, bankName):
        self._send(('HEAD_INFO', bankName), self.master)

    def retrieveTail(self, bankName):
        self._send(('TAIL_INFO', bankName), self.master)

    def getBalance(self, bankName, accountNum, nretries):
        if (nretries == self.tryC):
            self.seq = (self.seq + 1)
        reqID1 = ((((str(bankName) + '.') + str(self.cId)) + '.') + str(self.seq))
        bankIndex = [x for x in self.bankList if (x.name == bankName)]
        self.output(('Client: Sending getBalance ' + reqID1))
        self.psend('BALANCE', reqID1, accountNum, 0, bankIndex[0].tail)

        def ExistentialOpExpr_0():
            for (_, _, (_ConstantPattern28_, _BoundPattern29_, _, _, _)) in self._ClientReceivedEvent_3:
                if (_ConstantPattern28_ == 'REPLY'):
                    if (_BoundPattern29_ == reqID1):
                        if True:
                            return True
            return False
        _st_label_42 = 0
        self._timer_start()
        while (_st_label_42 == 0):
            _st_label_42+=1
            if ExistentialOpExpr_0():
                self.output(('Client: get balance response received for ' + str(reqID1)))
                return 
                _st_label_42+=1
            elif self._timer_expired:
                nretries = (nretries - 1)
                if (nretries > 0):
                    self.output(((((('Client: Resending for request Id ' + str(bankName)) + '.') + str(self.cId)) + '.') + str(self.seq)))
                    self.getBalance(bankName, accountNum, nretries)
                else:
                    self.output('Client: maximun Retry count for reqId')
                    pass
                _st_label_42+=1
            else:
                super()._label('_st_label_42', block=True, timeout=self.T)
                _st_label_42-=1

    def deposit(self, bankName, accountNum, amount, nretries):
        if (nretries == self.tryC):
            self.seq = (self.seq + 1)
        reqID2 = ((((str(bankName) + '.') + str(self.cId)) + '.') + str(self.seq))
        bankIndex = [x for x in self.bankList if (x.name == bankName)]
        self.output(((('Client: Sending Deposit ' + reqID2) + ' ') + str(amount)))
        self.psend('DEPOSIT', reqID2, accountNum, amount, bankIndex[0].head)

        def ExistentialOpExpr_1():
            for (_, _, (_ConstantPattern46_, _BoundPattern47_, _, _, _)) in self._ClientReceivedEvent_4:
                if (_ConstantPattern46_ == 'REPLY'):
                    if (_BoundPattern47_ == reqID2):
                        if True:
                            return True
            return False
        _st_label_58 = 0
        self._timer_start()
        while (_st_label_58 == 0):
            _st_label_58+=1
            if ExistentialOpExpr_1():
                self.output(('Client: deposit received for ' + reqID2))
                return 
                _st_label_58+=1
            elif self._timer_expired:
                nretries = (nretries - 1)
                if (nretries > 0):
                    self.output(((((('Client: Resending for request Id ' + str(bankName)) + '.') + str(self.cId)) + '.') + str(self.seq)))
                    self.deposit(bankName, accountNum, amount, nretries)
                else:
                    self.output('Client: maximum retry count reached for deposit')
                    pass
                _st_label_58+=1
            else:
                super()._label('_st_label_58', block=True, timeout=self.T)
                _st_label_58-=1

    def withdraw(self, bankName, accountNum, amount, nretries):
        if (nretries == self.tryC):
            self.seq = (self.seq + 1)
        reqID = ((((str(bankName) + '.') + str(self.cId)) + '.') + str(self.seq))
        bankIndex = [x for x in self.bankList if (x.name == bankName)]
        self.output(((('Client: Sending withdraw ' + reqID) + ' ') + str(amount)))
        self.psend('WITHDRAW', reqID, accountNum, amount, bankIndex[0].head)

        def ExistentialOpExpr_2():
            for (_, _, (_ConstantPattern64_, _BoundPattern65_, _, _, _)) in self._ClientReceivedEvent_5:
                if (_ConstantPattern64_ == 'REPLY'):
                    if (_BoundPattern65_ == reqID):
                        if True:
                            return True
            return False
        _st_label_74 = 0
        self._timer_start()
        while (_st_label_74 == 0):
            _st_label_74+=1
            if ExistentialOpExpr_2():
                self.output(('Client: withdraw received for ' + str(reqID)))
                return 
                _st_label_74+=1
            elif self._timer_expired:
                nretries = (nretries - 1)
                if (nretries > 0):
                    self.output(((((('Client: Resending for request Id ' + str(bankName)) + '.') + str(self.cId)) + '.') + str(self.seq)))
                    self.withdraw(bankName, accountNum, amount, nretries)
                else:
                    self.output('Client: maximum retry count reached for withdraw')
                    pass
                _st_label_74+=1
            else:
                super()._label('_st_label_74', block=True, timeout=self.T)
                _st_label_74-=1

    def psend(self, type, reqId, accountNum, amount, recepient):
        prob = random.random()
        if (prob >= self.dropRate):
            self._send((type, reqId, accountNum, amount), recepient)
        else:
            self.output(('Client: Dropping send message with ReqID ' + reqId))

    def _Client_handler_0(self, balance, accountNumber, outcome, reqID):
        self.responses.append((reqID, balance))
    _Client_handler_0._labels = None
    _Client_handler_0._notlabels = None

    def _Client_handler_1(self, bankName, master, head):
        self.output('Client: Head update received from master')
        bankIndex = [x for x in self.bankList if (x.name == bankName)]
        bankIndex[0].head = head
    _Client_handler_1._labels = None
    _Client_handler_1._notlabels = None

    def _Client_handler_2(self, tail, bankName):
        self.output('Client: Tail update received from master')
        bankIndex = [x for x in self.bankList if (x.name == bankName)]
        bankIndex[0].tail = tail
    _Client_handler_2._labels = None
    _Client_handler_2._notlabels = None

def main(master, fileName):
    json_data = open(fileName)
    info = json.load(json_data)
    bankList = []
    bank_client_list = []
    bank_client_dict = {}
    for bank in info['master']['banks']:
        temp = Bank(bank['bank_name'], None, None)
        bankList.append(temp)
    for bank in info['master']['banks']:
        bank_client_list = da.api.new(Client, num=bank['bank_clength'])
        i = 0
        for cli in bank_client_list:
            da.api.setup(cli, [bank['clients'][i]['client_id'], bank['bank_name'], master, bankList, bank['clients'][i]['client_total_req'], bank['clients'][i]['client_prob_getbal'], bank['clients'][i]['client_prob_dep'], bank['clients'][i]['client_prob_with'], bank['clients'][i]['client_requests'], bank['clients'][i]['client_drop_rate']])
            i+=1
        bank_client_dict[bank['bank_name']] = bank_client_list
    for bank in bank_client_dict:
        da.api.start(bank_client_dict[bank])
