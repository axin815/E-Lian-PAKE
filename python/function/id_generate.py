# 生成k位的字符串（用于生成ID）

import secrets
import string


def id_generate(k):
    # 可能的字符集合
    characters = string.ascii_letters + string.digits

    # 计算字节数，因为1字节 = 8比特
    bytes_length = k // 8

    # 生成一个k比特的随机字符串
    random_string = ''.join(secrets.choice(characters) for _ in range(bytes_length))

    # 将字符串转换为字节
    result_byte = random_string.encode('UTF-8')

    # 将字节转换为int
    result = int.from_bytes(result_byte, byteorder='big')
    # print('id=',result)
    return result

# print(id_generate(25))
