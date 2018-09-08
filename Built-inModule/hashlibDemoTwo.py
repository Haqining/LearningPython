
'可以说是一个登录注册的小样板了'

import random
import hashlib

db = {}


def get_md5(s):
    return hashlib.md5(s.encode('utf-8')).hexdigest()


class User():
    def __init__(self, username, password):
        self.username = username
        self.password = password
        # 这里不对salt做操作是要让它只被生成一次，不然会疯狂爆炸
        self.salt = ''

    def register(self):
        if self.username in db:
            print('The username "%s" is used.' % self.username)
            return False
        else:
            # chr() 用一个范围在 range（256）内的（就是0～255）整数作参数，返回一个对应的字符
            self.salt = ''.join([chr(random.randint(48, 122))
                                 for i in range(20)])
            self.password = get_md5(self.password + self.salt)
            self.__addUserToDB()
            print('Register success.')
            return True

    def login(self):
        userInfo = self.__getUserFromDB()
        if userInfo != None:
            if get_md5(self.password + userInfo['salt']) != userInfo['password']:
                print('Password error.')
                return False
            else:
                print('Login success.')
                return True
        else:
            print('The user "%d" is not found, please register.' % self.username)
            return False

    def __addUserToDB(self):
        # self.__dict__ =>就是属性和值的键值对
        db[self.username] = self.__dict__

    def __getUserFromDB(self):
        if self.username in db:
            return db[self.username]
        else:
            return None


def register(username, password):
    return User(username, password).register()


def login(username, password):
    return User(username, password).login()


# 测试:
assert register('michael', '123456')
assert register('bob', 'abc999')
assert register('alice', 'alice2008')
assert login('michael', '123456')
assert login('bob', 'abc999')
assert login('alice', 'alice2008')
assert not login('michael', '1234567')
assert not login('bob', '123456')
assert not login('alice', 'Alice2008')
print('ok')
