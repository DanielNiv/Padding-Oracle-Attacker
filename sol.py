from pwn import *
from binascii import hexlify
import typing

AES_BLOCK_SIZE = 16
context.log_level = 'error'

# TODO: MAKE IT MORE GENERIC !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
WANTED_ENCRYPTED_BLOCKS = [
    b'7b22757365726e616d65223a20226164',
    b'6d696e222c202265787069726573223a',
    b'2022333031372d30312d3031222c2022',
    b'69735f61646d696e223a202274727565',
    b'227d'
]


def send_msg_to_server_and_get_res(msg: bytes):
    server = process(['/usr/bin/python2', 'pkcs7.py'])
    welcome_text = server.recvuntil(b'What is your cookie?\n').decode()
    #print(f"sending {hexlify(msg)}")
    server.sendline(hexlify(msg))
    result_msg = server.recv()
    
    server.close()
    #result_msg = server.recv().decode()
    #print(f"ANS::::: {result_msg}")
    return result_msg.decode()


def is_valid_padding(msg: bytes) -> bool:
    server_res = send_msg_to_server_and_get_res(msg)
    #return False if 'invalid padding' in server_res else True
    #print(f"#################\n{server_res}$$$$$$$$$$$$$$$$")
    if 'invalid padding' in server_res:
        return False
    elif 'cookie2decoded = decrypt(cookie2[:-1])' in server_res:
        print(msg)
        raise("bad PADDING error !!!!!!!!!!!!!!!!!!!")

    #print(hexlify(msg))
    return True


def find_block_zeroer_IV(enc_block=b'B' * 16):
    block_zeroers = list()
    
    for cur_byte_index in range(1, AES_BLOCK_SIZE +1):
        
        print(f"[+] Started byte number {cur_byte_index}")
        
        for byte_option_i in range(256):
            IV = b'A' * (AES_BLOCK_SIZE - cur_byte_index)
            IV += byte_option_i.to_bytes(1, byteorder='big')
            
            for zeroer in block_zeroers:
                IV += (zeroer ^ cur_byte_index).to_bytes(1, byteorder='big')
            
            first_block = b'B' * AES_BLOCK_SIZE
            block_payload = IV + first_block

            if is_valid_padding(block_payload) == True:
                # this byte will zero byte number (cur_byte) in the decrypted text
                zeroer = byte_option_i ^ cur_byte_index
                print(f"FOUND ZEROER BYTE! {hex(zeroer)}")
                block_zeroers.insert(0, zeroer)
                break
            
    print(f"FINISHED BLOCK !!!!!!!!!!!!!!")
    
    zeroer_str = b""
    for zeroer in block_zeroers:
        zeroer_str += (zeroer).to_bytes(1, byteorder='big')
    
    zeroer_str += b'B' * AES_BLOCK_SIZE
    print(hexlify(zeroer_str))
    
    
# TODO: ADD TYPES
def find_blocks_encrypted_payload(blocks_arr):
    for block in blocks_arr:
        if len(block) != AES_BLOCK_SIZE and :
            


def main():
    find_block_zeroer_IV(enc_block=b"C"*16)


if __name__ == "__main__":
    main()