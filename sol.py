from pwn import *
from binascii import hexlify, unhexlify
import typing

AES_BLOCK_SIZE = 16
context.log_level = 'error'


def send_msg_to_server_and_get_res(msg: bytes) -> str:
    server = process(['/usr/bin/python2', './challenge/pkcs7.py'])
    welcome_text = server.recvuntil(b'What is your cookie?\n').decode()
    server.sendline(hexlify(msg))
    result_msg = server.recv()
    server.close()
    return result_msg.decode()


def is_valid_padding(msg: bytes) -> bool:
    server_res = send_msg_to_server_and_get_res(msg)

    if 'invalid padding' in server_res:
        return False
    elif 'cookie2decoded = decrypt(cookie2[:-1])' in server_res:
        print(msg)
        raise("bad PADDING error !!!!!!!!!!!!!!!!!!!")

    return True


def find_block_zeroer_IV(enc_block: bytes = b'B' * 16) -> bytes:
    block_zeroers = list()
    
    for cur_byte_index in range(1, AES_BLOCK_SIZE +1):
        print(f"\t[+] Working on byte number {cur_byte_index}")
        
        for byte_option_i in range(256):
            IV = b'A' * (AES_BLOCK_SIZE - cur_byte_index)
            IV += byte_option_i.to_bytes(1, byteorder='big')
            
            for zeroer in block_zeroers:
                IV += (zeroer ^ cur_byte_index).to_bytes(1, byteorder='big')
            
            block_payload = IV + enc_block

            if is_valid_padding(block_payload) == True:
                # this byte will zero byte number (cur_byte) in the decrypted text
                zeroer = byte_option_i ^ cur_byte_index
                print(f"\t\t[+] FOUND ZEROER BYTE! {hex(zeroer)}")
                block_zeroers.insert(0, zeroer)
                break
            
    zeroer_str = bytes()
    for zeroer in block_zeroers:
        zeroer_str += (zeroer).to_bytes(1, byteorder='big')
    
    return hexlify(zeroer_str)
    
    
def byte_xor(ba1: bytes, ba2: bytes) -> bytes:
    return bytes([_a ^ _b for _a, _b in zip(ba1, ba2)])
    
    
def find_str_encrypted_payload(wanted_dec_msg: bytes) -> None:
    # spit the message into AES_BLOCK_SIZE sized chunks
    blocks_arr = [wanted_dec_msg[i:i+AES_BLOCK_SIZE] for i in range(0, len(wanted_dec_msg), AES_BLOCK_SIZE)]
    blocks_arr = list(reversed(blocks_arr))
    
    # pad last string chunk if needed
    padded_block = blocks_arr[0]
    if len(padded_block) != AES_BLOCK_SIZE:
        needed_padding = AES_BLOCK_SIZE - len(blocks_arr[0]) % AES_BLOCK_SIZE
        padded_block += needed_padding * chr(needed_padding).encode()
        blocks_arr.pop(0)
        blocks_arr.insert(0, padded_block)
        
    final_payload = bytes()    
    last_ptbs_iv = None
    
    for i, block in enumerate(blocks_arr):
        print(f"[+] Started block number {i}/{len(blocks_arr)-1}")
        
        if i == 0:
            zeroer_iv = unhexlify(find_block_zeroer_IV(b'A' * 16))
            last_ptbs_iv = byte_xor(zeroer_iv, block)
            final_payload += hexlify(last_ptbs_iv) + hexlify(b'A' * 16)
        else:
            zeroer_iv = unhexlify(find_block_zeroer_IV(last_ptbs_iv))
            last_ptbs_iv = byte_xor(zeroer_iv, block)
            final_payload = hexlify(last_ptbs_iv) + final_payload
            
    print("final payload is:")
    print(final_payload)


def main():
    wanted_dec_msg = b'{"username":"admin","expires":"3017-01-01","is_admin":"true"}'
    find_str_encrypted_payload(wanted_dec_msg)


if __name__ == "__main__":
    main()