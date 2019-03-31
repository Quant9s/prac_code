# file = open('key.key', 'rb')

# key = file.read()
# file.close()

# print(type(key))

a = "b'gAAAAABcf_6WNbSe4J6ptaJ8tdCbuchSU105Ih79QRaoJhwaFuWmIe0ZYu-a2-RTi8DC-qGvo8vNcrZfYVjqOnRgqQesb0Q1eg=='"
print(a)
print(type(a))

print(a.decode())

# -*- coding: utf-8 -*-
import win32com.client
import pythoncom
import os
from getpass import getpass
import xalogger
import xaconfig
import xaparser
import sys

import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC



log = xalogger.XALogger(__name__)

class _XASessionEvent:
    def __init__(self):
        self.code   = -1
        self.msg    = None
    
    def OnLogin(self, code, msg):
        self.code   = str(code)
        self.msg    = str(msg)

    def OnLogout(self):
        pass

    def OnDisconnect(self):
        pass

class Session:
    """COM XASession객체의 파이썬 확장 클래스

        ::
            session = Session()
    """
    def __init__(self):
        self.session = win32com.client.DispatchWithEvents("XA_Session.XASession", _XASessionEvent)
        self.config_file = os.path.join(os.path.expanduser("~"),'xingpy','login_config.ini') # 자동 로그인 설정 파일 위치 예) C:\Users\jay\xingpy\login_config.ini
        self.key_file = os.path.join(os.path.expanduser("~"),'xingpy','key.key')

    def login(self, auto=True):
        """서버 연결을 요청한다

        ::
            session = Session()
            # 자동 로그인 설정 파일을 이용시
            session.login()
            
            # 수동 로그인 커맨드 라인 인풋 로그인 시
            session.login(auto=False)
        """

        # 서버 연결 및 로그인 후 응답을 기다리는 함수
        def connect_and_login(server, user):
            key = self._read_key_config(self.key_file)
            F_key = Fernet(key)

            self.session.ConnectServer(server['ip'], server['port'])
            self.session.Login(str(F_key.decrypt(user['id']).decode()), 
                               str(F_key.decrypt(user['pw']).decode()), 
                               str(F_key.decrypt(user['cert_pw']).decode()), 
                               str(user['server_type']), 
                               str(user['show_error']))
            while self.session.code == -1:
                pythoncom.PumpWaitingMessages()

        # 자동로그인
        if auto:
            try:
                server  = self._get_server_info_from_config(self.config_file)
                user    = self._get_user_info_from_config(self.config_file)
                
                connect_and_login(server, user)
                log.info('자동 로그인 시도')
            except:
                log.error('자동 로그인 실패. 수동로그인 으로 전환.')
                auto = False

        # 수동로그인
        if not auto:
            try:
                self._write_key_config(self.key_file)
                key = self._read_key_config(self.key_file)

                server  = self._get_server_info_from_input()
                user    = self._get_user_info_from_input(key)
                if self._ask_create_config():
                    self._create_config_from_input(self.config_file, server['ip'], server['port'], 
                        user['id'], user['pw'], user['cert_pw'])
                    log.info('자동 로그인용 config_file을 생성. {} 에서 확인가능'.format(self.config_file))
                connect_and_login(server, user)
                log.info('수동 로그인 입력값 으로 접속 및 로그인 시도')
            except:
                log.error('수동 로그인 실패. 서버 연결 상태 및 입력 정보 확인.')
        
        # 로그인상태 확인
        if self.session.code == "0000":
            log.info('{}(코드 {}: {})'.format(self.session.msg, self.session.code, xaparser.parse_error(self.session.code)))
        else:
            log.critical('{}(코드 {}: {})'.format(self.session.msg.strip(), self.session.code, xaparser.parse_error(self.session.code)))

    def logout(self):
        """서버와의 연결을 끊는다.
            ::
                session.logout()
        """
        self.session.DisconnectServer()
        if not self.session.IsConnected():
            log.info('정상 로그아웃 되었습니다')

    def account(self):
        """계좌 정보를 반환한다.
            :return: 계좌 정보를 반환한다.
            :rtype: object {no:"계좌번호",name:"계좌이름",detailName:"계좌상세이름"}
            ::
                session.account()
        """
        accounts = []
        total_accounts = self.session.GetAccountListCount()
        for n in range(total_accounts):
            accounts.append({
                "account_number"        : self.session.GetAccountList(n),
                "account_name"          : self.session.GetAccountName(n),
                "account_detail_name"   : self.session.GetAcctDetailName(n),
                "account_nick_name"     : self.session.GetAcctNickname(n),
            })
        log.info('계좌정보조회')
        return accounts

    def heartbeat(self):
        pass

    ##############################
    ### 내부에서만 사용하는 함수 ###
    ##############################

    @staticmethod
    def _get_server_info_from_input():
        server = {
            'ip'          : str(input('server ip (엔터시 기본값: hts.ebestsec.co.kr): ') or "hts.ebestsec.co.kr"),
            'port'        : str(input('server port (엔터시 기본값: 20001): ') or "20001")}
        return server
        
    @staticmethod
    def _get_user_info_from_input(key):
        F_key = Fernet(key)
        user = {
            'id'          : bytes(F_key.encrypt(input('user id: ').encode())),
            'pw'          : bytes(F_key.encrypt(getpass('user pw: ').encode())),
            'cert_pw'     : bytes(F_key.encrypt(getpass('user cert_pw: ').encode())),
            'server_type' : 0,
            'show_error'  : 0}
        return user
    
    def _ask_create_config(self):
        answer = str(input('자동로그인을 위한 설정파일을 만드시겠습니까? (y/n): ') or "y")
        if answer is 'y': return True
        else: return False

    @staticmethod
    def _create_config_from_input(
        config_file, ip, port, id, pw, cert_pw):
        config = xaconfig.XAConfig(config_file)
        config.set_server(ip, port)
        config.set_user(id, pw, cert_pw)
        config.create()

    @staticmethod
    def _get_server_info_from_config(config_file):
        if not os.path.isfile(config_file): 
            log.error('다음 위치에 자동 로그인 설정 파일이 존재하지 않습니다: {}'.format(config_file))
        config  = xaconfig.XAConfig(config_file)
        server  = config.get_server()
        return server

    @staticmethod
    def _get_user_info_from_config(config_file):
        if not os.path.isfile(config_file): 
            log.error('다음 위치에 자동 로그인 설정 파일이 존재하지 않습니다: {}'.format(config_file))
        config  = xaconfig.XAConfig(config_file)
        users   = config.get_user()

        user = {
            'id'          : bytes(users['id'].replace("b'","").replace("'","").encode()),
            'pw'          : bytes(users['pw'].replace("b'","").replace("'","").encode()),
            'cert_pw'     : bytes(users['cert_pw'].replace("b'","").replace("'","").encode()),
            'server_type' : users['server_type'],
            'show_error'  : users['show_error']}

        return user

    @staticmethod
    def _write_key_config(key_file):
        key_pw_provided ="bluekey"
        key_pw = key_pw_provided.encode()

        salt = os.urandom(16) # key_pw와 salt로 조합하여 암호화 키를 만든다.
        kdf = PBKDF2HMAC (
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend(),
        )

        key = base64.urlsafe_b64encode(kdf.derive(key_pw))
        file = open(key_file,'wb')
        file.write(key)
        file.close
        
    @staticmethod
    def _read_key_config(key_file):
        file = open(key_file,'rb')

        key = file.read()
        file.close()

        return key

        
if __name__ == "__main__":
    session = Session()
    session.login(auto=True)
    session.account()
    session.logout()

