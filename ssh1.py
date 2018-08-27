#!/usr/bin/python
import paramiko
import time

try:
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.WarningPolicy())

    client.connect("192.168.1.66", port="22", username="shaomin", password="abcd")

    #stdin, stdout, stderr = client.exec_command("ls -1")
    stdin, stdout, stderr = client.exec_command("python3 nonstop.py &")
    print("aaaaaaaaaaaaaaaaa")
    time.sleep(10)
    client.close()
    print(stdout.read().decode("utf-8"))
    print(stderr.read().decode("utf-8"))
finally:
    client.close()

print("done.")
