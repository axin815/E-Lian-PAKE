def key_padding(byte_data: bytes) -> bytes:
    """
    检查字节数据长度是否为 128 位（16 字节），如果不足，使用 'a' 到 'z' 的字母字节按顺序补齐。

    参数:
    byte_data (bytes): 输入的字节数据。

    返回:
    bytes: 补齐到 128 位（16 字节）的字节数据。
    """
    target_length = 32  # 128 位即 16 字节
    letter_bytes = b'abcdefghijklmnopqrstuvwxyz0123456789'  # 26个字母的字节表示

    # 检查字节数据的长度是否超过 32 字节
    if len(byte_data) > target_length:
        # raise ValueError("输入数据超过 256 位（32 字节）。")
        byte_data = byte_data[:32]
    # 如果长度不足 32 字节，按顺序补齐字母字节
    if len(byte_data) < target_length:
        padding_length = target_length - len(byte_data)
        byte_data += letter_bytes[:padding_length]  # 用字母字节补齐

    return byte_data


# # 示例
# input_data = b'\x01\x02\x03'  # 示例字节数据
# padded_data = pad_to_128_bits_with_digits(input_data)
# print(f"补齐后的数据: {padded_data}")
# print(f"数据长度: {len(padded_data)} 字节")
