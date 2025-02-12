import socket

def check_port(host, port, is_udp=False):
    if is_udp:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    else:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(3)
    try:
        sock.connect((host, port))
        print(f"Port {port} is open on {host}")
    except Exception as e:
        print(f"Port {port} is closed or blocked: {e}")
    finally:
        sock.close()

host = "heygenstream-lnczb0yw.livekit.cloud"

# Check TCP 7880
check_port(host, 7880)

# Check UDP 7882 and 7883
check_port(host, 7882, is_udp=True)
check_port(host, 7883, is_udp=True)
