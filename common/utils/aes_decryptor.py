from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex
import string
import random
import requests



class Prpcrypt():
    def __init__(self):
        self.key = 'eCcGFZQj6PNoSSma31LR39rTzTbLkU8E'.encode('utf-8')
        self.mode = AES.MODE_CBC

    # 加密函数，如果text不足16位就用空格补足为16位，
    # 如果大于16当时不是16的倍数，那就补足为16的倍数。
    def encrypt(self, text):
        cryptor = AES.new(self.key, self.mode, b'0000000000000000')
        # 这里密钥key 长度必须为16（AES-128）,
        # 24（AES-192）,或者32 （AES-256）Bytes 长度
        # 目前AES-128 足够目前使用
        length = 16
        count = len(text)
        if count < length:
            add = (length - count)
            # \0 backspace
            text = text + ('\0' * add)
        elif count > length:
            add = (length - (count % length))
            text = text + ('\0' * add)
        self.ciphertext = cryptor.encrypt(text.encode('utf-8'))
        # 因为AES加密时候得到的字符串不一定是ascii字符集的，输出到终端或者保存时候可能存在问题
        # 所以这里统一把加密后的字符串转化为16进制字符串
        return b2a_hex(self.ciphertext).decode(encoding='utf-8')

    # 解密后，去掉补足的空格用strip() 去掉
    def decrypt(self, text):
        cryptor = AES.new(self.key, self.mode, b'0000000000000000')
        plain_text = cryptor.decrypt(a2b_hex(text))
        return plain_text.decode().rstrip('\0')


'''
$#!^等特殊字符，在shell下的mysql命令行里面不识别
#特殊字符，在java下不识别
$特殊字符，在php下不识别
'''
SPECIAL_CHARS = '~%&*-_'
PASSWORD_CHARS = string.ascii_letters + string.digits + SPECIAL_CHARS


def generate_random_password(password_length=32):
    """
    生成指定长度的密码字符串，当密码长度超过3时，密码中至少包含：
    1个大写字母+1个小写字母+1个特殊字符
    :param password_length:密码字符串的长度
    :return:密码字符串
    """
    char_list = list()
    char_list.extend(random.sample(string.ascii_uppercase,1))
    char_list.extend(random.sample(string.digits,1))
    char_list.extend(random.sample(string.ascii_lowercase,1))
    char_list.extend(random.sample(SPECIAL_CHARS,1))
    char_list = random.sample(PASSWORD_CHARS,4)
    # char_list = [
    #     random.choice(string.ascii_lowercase),
    #     random.choice(string.ascii_uppercase),
    #     random.choice(SPECIAL_CHARS),
    # ]
    if password_length > 8:
        # random.choice 方法返回一个列表，元组或字符串的随机项
        # (x for x in range(N))返回一个Generator对象
        # [x for x in range(N)] 返回List对象
        char_list.extend([random.choice(PASSWORD_CHARS) for _ in range(password_length - 8)])
    # 使用random.shuffle来将list中元素打乱
    random.shuffle(char_list)
    return ''.join(char_list[0:password_length])


def get_out_ip() :
    url = r'http://www.trackip.net/'
    r = requests.get(url)
    txt = r.text
    ip = txt[txt.find('title')+6:txt.find('/title')-1]
    return ip


if __name__ == '__main__':
    pc = Prpcrypt()  # 初始化密钥
    e = pc.encrypt('123456')  # 加密
    d = pc.decrypt(e)  # 解密
    print("加密:", str(e))
    print("解密:", str(d))
