def pass_change(s):
    result = []
    for char in s:
        if char.isalpha():  # 判断字符是否为字母
            # 将字母转换为字母表中的顺序，`ord('a')` 返回 97
            number = ord(char.lower()) - ord('a') + 1
            result.append(str(number))  # 转换为字符串并加入结果列表
    number_string = ''.join(result)  # 将结果拼接成一个字符串
    return int(number_string)  # 将拼接后的字符串转换为整数

# 测试
# input_string = "KFsNi3s5Tk8jhx0V"
# output_integer = letters_to_numbers_as_int(input_string)
# print(output_integer,type(output_integer))  # 输出 123242526
