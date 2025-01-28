import hashlib


def h_fun(value, k):
    """
    将输入值转换为字节，并映射为由 k 决定的固定位数的十六进制字符串。

    参数:
    value: 需要映射的值，可以是整数或字符串。
    k: 控制映射位数的参数，位数为 2^k 字节长度。

    返回:
    映射后的十六进制字符串。
    """
    # 计算目标字节长度（位数为 2^k 字节长度）
    bit =  k

    # 根据输入类型将其转换为字节形式
    if isinstance(value, int):
        # 将整数转换为字节，使用大端字节序，确保不丢失信息
        value_bytes = value.to_bytes((value.bit_length() + 7) // 8, byteorder='big')
    elif isinstance(value, str):
        # 将字符串转换为字节，假设使用 utf-8 编码
        value_bytes = value.encode('utf-8')
    else:
        raise TypeError("Unsupported type for value. Must be an integer or string.")

    # 创建一个 SHAKE256 哈希对象
    shake256 = hashlib.shake_256()

    # 这里可以添加需要哈希的数据
    shake256.update(value_bytes)
    # 生成指定长度的哈希值
    # k 是二进制位数，我们需要将其转换为字节长度，因为每个字节包含8位
    digest_size = bit // 8
    digest = shake256.digest(digest_size)

    # 将二进制的哈希值转换为十六进制表示
    hex_digest = digest.hex()

    return hex_digest

def h1_fun(value, q: int) -> int:
    """
    将任意长度的比特值或整数映射到模 q 的非零整数群 (Z_q*) 中。

    参数:
    value (str or int): 输入的比特值，可以是二进制字符串或整数。
    q (int): 一个素数，表示整数群 Z_q 的阶。

    返回:
    int: 映射到 Z_q* 的一个整数。
    """

    # 如果输入是字符串类型，则直接转为字节，直接进行哈希映射
    if isinstance(value,str):
        hashed_int = int(hashlib.sha256(value.encode()).hexdigest(),16)
    elif isinstance(value,int):  # 如果是int类型，则转为字节，进行哈希映射
        hashed_int = int(hashlib.sha256(value.to_bytes((value.bit_length() + 7) // 8, byteorder='big')).hexdigest(),16)
    else:
        raise ValueError("输入必须是二进制字符串或整数类型")

    # 对哈希值进行模运算以确保落在 Z_q 的范围内，并且不等于 0
    result = hashed_int % q

    # 确保结果落在 Z_q* 中，即不为 0
    if result == 0:
        result = 1

    return result

def h2_fun(data):
    # 检查输入的数据类型是否为整数
    if isinstance(data, int):
        # 如果是整数，即为原值
        data = data
    # 检查输入的数据类型是否为字符串
    elif isinstance(data, str):
        # 如果是字符串，将其编码为字节数组
        data_byte = data.encode()
        data = int.from_bytes(data_byte, byteorder='big')

    hash_obj = data ^ (data >> 16) ^ (data >> 8)
    return hash_obj


# 以下为H3哈希函数的内容
def is_in_group(value: int, q: int) -> bool:
    """
    检查值是否在阶为 q 的乘法循环群 G 中。

    参数:
    value (int): 需要检查的整数值。
    q (int): 群的阶，必须是素数。

    返回:
    bool: 如果值在群中返回 True，否则返回 False。
    """
    return 1 <= value < q


def map_to_z_q_star(value: int, q: int) -> int:
    """
    将整数值映射到阶为 q 的乘法循环群 Z_q* 中的值。

    参数:
    value (int): 需要映射的整数值。
    q (int): 群的阶，必须是素数。

    返回:
    int: 映射后的 Z_q* 中的整数值。
    """
    # if not isprime(q):
    #     raise ValueError("q 必须是一个素数")

    # 计算模 q
    mod_value = value % q

    # 确保结果不为零
    if mod_value == 0:
        mod_value = 1  # 可以选择其他非零值

    return mod_value


def h3_fun(value: int, q: int) -> int:
    """
    根据输入值是否在阶为 q 的乘法循环群 G 中进行不同的映射。

    参数:
    value (int): 需要处理的整数值。
    q (int): 群的阶，必须是素数。

    返回:
    int: 映射后的 Z_q* 中的整数值。
    """
    # if not isprime(q):
    #     raise ValueError("q 必须是一个素数")

    # 检查输入值是否在群 G 中
    if is_in_group(value, q):
        # 已经在群 G 中，直接映射到 Z_q* 中
        return map_to_z_q_star(value, q)
    else:
        # 不在群 G 中，先映射到 G，再映射到 Z_q*
        v = value % q
        return map_to_z_q_star(v, q)