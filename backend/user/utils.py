from pathlib import Path
import os
import re
import base64

from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import check_password
from django.conf import settings
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

from .models import User


def get_user_by_account(account):
    """
    根据account查询用户
    :param account: 用户名/手机号/邮箱
    :return: user
    """
    try:
        if re.match('^1[3-9]\d{9}$', account):
            # 手机号登录
            user = User.objects.get(phone=account)
        elif re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', account):
            # 邮箱登录
            user = User.objects.get(email=account)
        else:
            # 用户名登录
            user = User.objects.get(userName=account)
    except User.DoesNotExist:
        return None
    else:
        return user
    
class MultiFieldAuthBackend(ModelBackend):
    """自定义用户认证后端"""
    def authenticate(self, request=None, username=None, password=None, **kwargs):
        """
        重写认证方法，实现多账号登录
        :param username: 用户名
        :param password: 密码
        :param kwargs: 其他参数
        :return: user
        """
        print(username)
        user = get_user_by_account(username)
       
        if user and check_password(password, user.password):
            return user
        

def decrypt(e: str, cryptojs_key: str) -> str:
    """
    AES-ECB 解密函数，模拟原 JavaScript 代码功能
    
    Args:
        e: 加密的字符串
        cryptojs_key: 密钥
    
    Returns:
        解密后的字符串
    """
    # 1. 替换字符（同JS中的 replace）
    t = e.replace("-", "+").replace("_", "/")
    
    # 2. 对密钥进行UTF-8编码
    key = cryptojs_key.encode('utf-8')
    
    # 3. Base64解码加密数据
    encrypted_data = base64.b64decode(t)
    
    # 4. 创建AES解密器 (ECB模式)
    cipher = AES.new(key, AES.MODE_ECB)
    
    # 5. 解密
    decrypted = cipher.decrypt(encrypted_data)
    
    # 6. 移除PKCS7填充
    unpadded = unpad(decrypted, AES.block_size, style='pkcs7')
    
    # 7. 返回UTF-8字符串
    return unpadded.decode('utf-8')



# 使用示例
if __name__ == "__main__":
    cryptojs_key = getattr(settings, 'CRYPTOJS_KEY', 'aaaabbbbccccdddd')
    
    # 假设这是加密后的字符串
    encrypted_string = "HpQOJYk1fZ9ADAOzMVQF8g=="
    
    try:
        result = decrypt(encrypted_string, cryptojs_key)
        print(f"解密结果: {result}")
    except Exception as e:
        print(f"解密失败: {e}")