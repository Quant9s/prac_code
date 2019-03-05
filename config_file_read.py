from configparser import ConfigParser

parser = ConfigParser()
parser.read('dev.ini')

# parser 종류이름 가져오기
print(parser.sections()) # ['settings','db','files']
# perser setting 안에 secret_key 가져오기
print(parser.get('setting','secret_key')) # abc123
# parser seting 안에 option을 가져오기
print(parser.options('setting')) # ['debug','secret_key','log_path']

# db라는 것이 parser 안에 있는지 보기
print('db' in parser) # True

# db.db_port 값을 가져오고, 그것의 타입을 본다
print(parser.get('db','db_port'), type(parser.get('db','db_port'))) # 8889 <class 'str'>
# db.db_port 값을 integer로 가져온다
print(int(parser.get('db','db_port'))) # 8889 (as int)
# db.db_defalut_port fallback = 3306
print(parser.getint('db','db_default_port', fallback=3306)) # 3306

print(parser.getboolean('setting','debug',fallback=False)) # True