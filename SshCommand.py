#!/usr/bin/python
import paramiko
import traceback
import socket
import logging


log = logging.getLogger(__name__)
logging.basicConfig(level="DEBUG")
logging.getLogger('paramiko').setLevel(logging.INFO)

class SshCommand:
    """ execute a command on a remote host """
    def __init__(self, command, verifier):
        self.command = command
        self.verifier = verifier
       
    def verify_result(self, stdout, stderr):
        log.debug("stdout: %s" % stdout)
        log.debug("stderr: %s" % stderr)
        if stderr != "":
            return False
        else:
            return self.verifier(stdout)
            
class SshClient:
    """a SSHClient using paramiko"""
        
    def __init__(self, username, password, host, port=22):
        self.client = paramiko.SSHClient()
        self.client.load_system_host_keys()
        self.client.set_missing_host_key_policy(paramiko.WarningPolicy())

        try:
            self.client.connect(host, port, username, password)
        except paramiko.BadHostKeyException:
            log.error("BadHostKeyException ... ")
            log.error(traceback.format_exc())
            exit(1)
        except paramiko.AuthenticationException:
            log.error("AuthenticationException ... ")
            log.error(traceback.format_exc())
            exit(1)
        except paramiko.SSHException:
            log.error("SSHException ...")
            log.error(traceback.format_exc())
            exit(1)
        except socket.error:
            log.error("socket.error ...")
            log.error(traceback.format_exc())
            exit(1)
            
    def execute(self, ssh_command):
        try:
            stdin, stdout, stderr = self.client.exec_command(ssh_command.command)
            output = stdout.read().decode("utf-8")
            error = stderr.read().decode("utf-8")
            return (output, error)
        except paramiko.SSHException:
            log.error(traceback.format_exc())
            return ("", "error")
        
    def close(self):
        self.client.close()

class Service:
    def __init__(self, name, ssh_command, hosts, username, password):
        self.name = name
        self.ssh_command = ssh_command
        self.hosts = hosts
        self.username = username
        self.password = password

    def __start_service_on_host(self, host):
        client = SshClient(host=host, username=self.username, password=self.password)
        try:
            stdout, stderr = client.execute(self.ssh_command)
            result = command.verify_result(stdout, stderr)
            log.info("%s - command '%s' on host: %s" % (result and 'Success' or 'Fail', self.ssh_command.command, host))
            return result
        finally:
            client.close()
            
    def start_service(self):
        results = [self.__start_service_on_host(host) for host in hosts]
         
        return (False not in results)
               
        

username = 'shaomin'
password = 'abcd'
hosts = ['192.168.1.66', '192.168.1.66']

if __name__ == "__main__":
    command = SshCommand("ls -l", lambda stdout: "words.txt" in stdout)
    service = Service("list directory", command, hosts, username, password)
    result = service.start_service()
    log.info("%s - start service %s on hosts: %s" % (result and 'Success' or 'Fail', service.name, hosts))

#     try:
#         client = SshClient(host="192.168.1.66", username="shaomin", password="abcd")
#         try:
#             command = SshCommand("ls -l", lambda stdout: "words.txt" in stdout)
#             stdout, stderr = client.execute(command)
#             if command.verify_result(stdout, stderr):
#                 print("success")
#             else:
#                 print("fail")
#         finally:
#             client.client.close()
#     except Exception: 
#         print(traceback.format_exc())
#         print("cannot create the client")

