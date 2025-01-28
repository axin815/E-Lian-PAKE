# 加密函数
import pickle

from Crypto.Cipher import AES


def encrypt(key, message):
    plaintext = pickle.dumps(message)  # 将message的元组修改为字节类型
    cipher = AES.new(key, AES.MODE_GCM)  # 创建一个加密对象
    nonce = cipher.nonce  # 创建一次性数字，用于保证在密钥和明文相同的情况下，加密的结果不一致
    ciphertext, tag = cipher.encrypt_and_digest(plaintext)  # ciphertext是密文，tag是认证标签，保证密文的完整性和真实性
    return ciphertext, nonce, tag


# 解密函数
def decrypt(key, ciphertext, nonce, tag):
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    t = cipher.decrypt(ciphertext)  # 解密，结果为字节
    plaintext = pickle.loads(t)  # 将解密后的明文修转化为元组
    try:
        cipher.verify(tag)  # 验证tag是否相同，相同则未被修改
        return plaintext[0], plaintext[1], plaintext[2]  # 将元组中的数据拿出，在此代码中为加密后的数据XB、YB、TB等值
    except ValueError:
        print("key is not valid")
        return False