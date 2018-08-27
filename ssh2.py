# import paramiko
# import select
# 
# client = paramiko.SSHClient()
# client.load_system_host_keys()
# client.connect('host.example.com')
# channel = client.get_transport().open_session()
# channel.exec_command("tail -f /var/log/everything/current")
# while True:
#     if channel.exit_status_ready():
#         break
#     rl, wl, xl = select.select([channel], [], [], 0.0)
#     if len(rl) > 0:
#         print channel.recv(1024)


#!/usr/bin/python
import paramiko
import time
import select
 
try:
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.WarningPolicy())
 
    client.connect("192.168.1.66", port="22", username="shaomin", password="abcd")
    channel = client.get_transport().open_session()
    channel.exec_command("ls -l")
#    channel.exec_command("python3 nonstop.py &")

    while True:
        print("aaaaaaaaaaaa")
        if channel.exit_status_ready():
            print("eeeeeeeeeeeeeeeeee")
            break
        #rl, wl, xl = select.select([channel], [], [], 0.0)
        if channel.recv_ready():
            print("bbbbbbbbbbbbbbbbbbbbb")
            print(channel.recv(10))
        #time.sleep(2)
finally:
    client.close()
 
print("done.")
