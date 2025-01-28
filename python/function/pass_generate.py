import random
import string


def pass_generate(generator: int, q: int, length: int = 16) -> str:
    """
    自动生成一个包含字母和数字的口令值，口令值属于阶为素数 q 的乘法循环群 G 中。

    参数:
    generator (int): 乘法循环群的生成元 g。
    q (int): 一个素数，表示循环群 G 的阶。
    length (int): 口令的长度。默认值为 8。

    返回:
    str: 一个包含字母和数字的口令值。
    """

    # Base62 字符集：包含数字、大小写字母
    charset = string.ascii_letters + string.digits  # 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'

    # 验证生成元的合法性
    if pow(generator, q - 1, q) != 1:
        raise ValueError("生成元不合法，必须在该群中生成所有非零元素")

    # 在 1 到 q-1 之间随机生成一个指数 i
    exponent = random.randint(1, q - 1)

    # 计算 g^i mod q，确保结果在群 G 中
    group_element = pow(generator, exponent, q)

    # 将群元素转换为 Base62 字符串
    password_value = ""
    while group_element > 0:
        password_value = charset[group_element % 62] + password_value
        group_element //= 62

    # 如果生成的口令值长度不足，填充随机字符至指定长度
    if len(password_value) < length:
        password_value = ''.join(random.choice(charset) for _ in range(length - len(password_value))) + password_value

    return password_value[:length]  # 截断到指定长度

# a=pass_generate(3,99991)
# print(a,type(a))
