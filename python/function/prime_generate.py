import random


def is_prime(n, k=100):
    """
    使用Miller-Rabin测试判断n是否为素数
    :param n: 需要测试的数字
    :param k: 测试次数，次数越多准确性越高
    :return: 如果是素数返回True，否则返回False
    """
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0:
        return False

    # 将n-1表示为d*2^r
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2

    # k次测试
    for _ in range(k):
        # 随机选择一个a
        a = random.randint(2, n - 2)
        x = pow(a, d, n)

        if x == 1 or x == n - 1:
            continue

        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True


def generate_large_prime(bits):
    """
    生成指定位数的素数
    :param bits: 素数的位数
    :return: 生成的素数
    """
    while True:
        # 随机生成一个指定位数的奇数
        prime_candidate = random.getrandbits(bits) | 1  # 确保是奇数

        # 检查候选素数是否为素数
        if is_prime(prime_candidate):
            return prime_candidate


# def main():
#     bits = 1024  # 生成512位的素数
#     prime = generate_large_prime(bits)
#     print(f"Generated prime: {prime}")
#
#
# if __name__ == "__main__":
#     main()
