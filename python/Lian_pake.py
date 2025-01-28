import random
import time

import gmpy2

from function import id_generate, pass_generate, key_padding
from function.enc_dec import encrypt, decrypt
from function import prime_generate,pake_hash

SECURITY_PARAMETER = 1024
g = 2
PRIME = prime_generate.generate_large_prime(SECURITY_PARAMETER)

# 生成id
id_A = id_generate.id_generate(SECURITY_PARAMETER)  # int类型
id_B = id_generate.id_generate(SECURITY_PARAMETER)  # int类型

# 生成口令
pw_A = pass_generate.pass_generate(g, PRIME)
pw_B = pw_A

def intToByte(message):
    result = message.to_bytes((message.bit_length() + 7) // 8, byteorder='big')
    return result

def H(data):  # 任意长度的字符映射为p(k)长度的字符，此处p(k)=2*k，输出为int类型
    return pake_hash.h_fun(data, SECURITY_PARAMETER)


def H1(data):
    return pake_hash.h1_fun(data, PRIME)  # 输出值为int类型，将任意长度的比特值或整数映射到模 q 的非零整数群 (Z_q*) 中


def H2(data):
    return pake_hash.h2_fun(data)  # 输出值为int类型，线性哈希函数


def H3(data):
    return pake_hash.h3_fun(data, PRIME)  # 输出值为int类型，将生成的包含字母和数字的口令值映射到一个阶为 q 的乘法循环群 G，并最终映射到阶为 q 的非零整数群 Z_q*


def rand():
    return random.randint(1, PRIME)  # 从1-prime中随机选取一个值

# 时间戳验证
def timestamp_is_fresh(timestamp):
    now = time.perf_counter()
    if now - timestamp > 600:  # 60s内皆为新鲜
        return False
    else:
        return True


# 生成hw D
def generate_password_file(password, idd):
    s = rand()
    hw = H1(password) ^ s
    D = H2(s) ^ idd
    # print(hw,D)
    return hw, D

def session():
    # 激活A实例---A
    rA = rand()
    hwA, DA = generate_password_file(pw_A, id_A)
    XA = H2(hwA) ^ H2(rA)
    YA = gmpy2.powmod(g, rA, PRIME)
    TA = time.time()
    # 将（XA、YA、TA）发送给B实例---B
    rB = rand()
    hwB, DB = generate_password_file(pw_B, id_B)
    XB = H2(hwB) ^ H2(rB)
    YB = gmpy2.powmod(g, rB, PRIME)
    # 接收到（XA、YA、TA）---B
    if not timestamp_is_fresh(TA):
        print("TA has expired")
    else:
        tkB = XA ^ DB ^ id_B ^ H2(rB) ^ H2(H3(gmpy2.powmod(YA, rB, PRIME)))
        tkB_byte = intToByte(tkB)
        # 补齐字节，共128位
        tkB_byte = key_padding.key_padding(tkB_byte)
        TB = time.time()
        CB, nonce, tag = encrypt(tkB_byte, (TB, hwB, rB))

        # B将XB、YB、CB、TB发送给A  ---A
        if not timestamp_is_fresh(TB):
            print("TB has expired")
        else:
            tkA = XB ^ DA ^ id_A ^ H2(rA) ^ H2(H3(gmpy2.powmod(YB, rA, PRIME)))
            # 共20位，差4位 用0补齐
            tkA_byte = intToByte(tkA)
            # 补齐字节，共128位
            tkA_byte = key_padding.key_padding(tkA_byte)
            dec_TB, dec_hwB, dec_rB = decrypt(tkA_byte, CB, nonce, tag)
            if dec_TB != TB:
                print("dec_TB does not match TB, is not valid")
            else:
                if YB != gmpy2.powmod(g, dec_rB, PRIME) or XB != H2(dec_hwB) ^ H2(dec_rB):
                    print("YB does not match or XB does not match")
                else:
                    CA, nonce_CA, tag_CA = encrypt(tkA_byte, (TA, hwA, rA))
                    sidA = str(XA) + str(YA) + str(XB) + str(YB)  # XA、YA、XB、YB都是经过哈希或者幂运算的，都是int类型
                    KA = H(str(tkA) + str(sidA))
                    # A把CA发送给B ---B
                    dec_TA, dec_hwA, dec_rA = decrypt(tkB_byte, CA, nonce_CA, tag_CA)
                    if dec_TA != TA:
                        print("dec_TA does not match, is not valid")
                    else:
                        if YA != gmpy2.powmod(g, dec_rA, PRIME) or XA != H2(dec_hwA) ^ H2(dec_rA):
                            print("YA does not match or XA does not match")
                        else:
                            sidB = str(XA) + str(YA) + str(XB) + str(YB)  # XA、YA、XB、YB都是经过哈希或者幂运算的，都是int类型
                            KB = H(str(tkB) + str(sidB))
                            return KA, KB

if __name__ == '__main__':
    # 计算运行10000次平均的消耗的时间
    i = 0
    m = 100000
    sum_time = 0
    while i < m:
        start_time = time.perf_counter()
        KA, KB = session()
        assert KA == KB, "Session keys do not match!"
        print('KA=', KA,len(KA))
        print('KB=', KB,len(KB))
        print("第" + str(i + 1) + "次Key exchange successful!")
        end_time = time.perf_counter()
        run_time = end_time - start_time
        print("第" + str(i + 1) + "运行时间：", run_time)
        sum_time += run_time
        i = i + 1
    print("运行" + str(m) + "次的时间：", sum_time)
    print("运行" + str(m) + "次的平均时间：", sum_time / m)