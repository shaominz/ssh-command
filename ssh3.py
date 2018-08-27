#!/usr/bin/python
import time
import paramiko


#http://chamilad.github.io/blog/2015/11/26/timing-out-of-long-running-methods-in-python/
def long_function():
    try:
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.WarningPolicy())
     
        client.connect("192.168.1.66", port="22", username="shaomin", password="abcd")
        channel = client.get_transport().open_session()
        #channel.exec_command("ls -l")
        channel.exec_command("python3 nonstop.py")
    
        start = time.time()
        PERIOD_OF_TIME = 5 # 5min

        while True:
            print("aaaaaaaaaaaa")
            if channel.exit_status_ready():
                print("eeeeeeeeeeeeeeeeee")
                break
            #rl, wl, xl = select.select([channel], [], [], 0.0)
            if channel.recv_ready():
                print("bbbbbbbbbbbbbbbbbbbbb")
                print(channel.recv(1024))
    
            if channel.recv_stderr_ready():
                print("cccccccccccccccc")
                print(channel.recv_stderr(1024))
            time.sleep(2)
            if time.time() > start + PERIOD_OF_TIME : break
    finally:
        client.close()
     
    print("done.")

     
long_function()