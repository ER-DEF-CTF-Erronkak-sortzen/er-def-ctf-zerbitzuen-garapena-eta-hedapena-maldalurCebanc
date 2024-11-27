#!/usr/bin/env python3

from ctf_gameserver import checkerlib
import logging
import http.client
import socket
import paramiko
import hashlib
PORT_WEB = 80
PORT_DB = 3306
def ssh_connect():
    def decorator(func):
        def wrapper(*args, **kwargs):
            # SSH connection setup
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            rsa_key = paramiko.RSAKey.from_private_key_file(f'/keys/team{args[0].team}-sshkey')
            client.connect(args[0].ip, username = 'root', pkey=rsa_key)

            # Call the decorated function with the client parameter
            args[0].client = client
            result = func(*args, **kwargs)

            # SSH connection cleanup
            client.close()
            return result
        return wrapper
    return decorator

class MyChecker(checkerlib.BaseChecker):

    def __init__(self, ip, team):
        checkerlib.BaseChecker.__init__(self, ip, team)
        self._baseurl = f'http://[{self.ip}]:{PORT_WEB}'
        logging.info(f"URL: {self._baseurl}")

    @ssh_connect()
    def place_flag(self, tick):
        # DB Flag
        logging.info('creating db flag')
        flag = checkerlib.get_flag(tick)
        creds = self._add_new_flag(self.client, flag)
        if not creds:
            return checkerlib.CheckResult.FAULTY
        logging.info('created db flag')
        checkerlib.store_state(str(tick), creds)
        checkerlib.set_flagid(str(tick))
        return checkerlib.CheckResult.OK

    def check_service(self):
        # check if ports are open
        if not self._check_port_web(self.ip, PORT_WEB):
            return checkerlib.CheckResult.DOWN
        # check if dev1 user exists in pasapasa_ssh docker
        if not self._check_ssh_user('dev1'):
            return checkerlib.CheckResult.FAULTY
        # check if server is Apache 2.4.50
        if not self._check_php_version():
            return checkerlib.CheckResult.FAULTY
        # check if dev1 user exists in webdatubasea_ssh docker
        if not self._check_db_user('root'):
            return checkerlib.CheckResult.FAULTY
        if not self._check_db_user('dev1'):
            return checkerlib.CheckResult.FAULTY
        file_path_web = '/var/www/html/index.html'
        # check if index.hmtl from webdatubasea_web has been changed by comparing its hash with the hash of the original file
        if not self._check_web_integrity(file_path_web):
            return checkerlib.CheckResult.FAULTY        
        file_path_ssh = '/etc/ssh/sshd_config'
        if not self._check_web_integrity(file_path_ssh):
            return checkerlib.CheckResult.FAULTY                      
        return checkerlib.CheckResult.OK        
    
    def check_flag(self, tick):
        if not self.check_service():
            return checkerlib.CheckResult.DOWN
        flag = checkerlib.get_flag(tick)
        #creds = checkerlib.load_state("flag_" + str(tick))
        # if not creds:
        #     logging.error(f"Cannot find creds for tick {tick}")
        #     return checkerlib.CheckResult.FLAG_NOT_FOUND
        flag_present = self._check_flag_present(flag)
        if not flag_present:
            logging.info('db flag not found')
            return checkerlib.CheckResult.FLAG_NOT_FOUND
        return checkerlib.CheckResult.OK
    
    @ssh_connect()
    #Function to check if an user exists
    def _check_ssh_user(self, username):
        ssh_session = self.client
        command = f"docker exec webdatubasea_web_1 sh -c 'id {username}'"
        stdin, stdout, stderr = ssh_session.exec_command(command)
        if stderr.channel.recv_exit_status() != 0:
            return False
        return True
        
    @ssh_connect()
    def _check_php_version(self):
        ssh_session = self.client
        command = f"docker exec webdatubasea_web_1 sh -c 'php -v | grep \"PHP 8.3.13\"'"
        stdin, stdout, stderr = ssh_session.exec_command(command)

        if stdout:
            return True
        else:
            return False
        
    @ssh_connect()
    #Function to check if an user exists
    def _check_db_user(self, username):
        ssh_session = self.client
        command = (
            f"docker exec webdatubasea_web_1 sh -c "
            f"\"mysql -h db -u root -proot_password -e \\\"SELECT User FROM mysql.user WHERE User = '{username}';\\\"\""
        )
        stdin, stdout, stderr = ssh_session.exec_command(command)
        output = stdout.read().decode()

        if username in output:
            return True
        return False
      
    @ssh_connect()
    def _check_web_integrity(self, path):
        ssh_session = self.client
        command = f"docker exec webdatubasea_web_1 sh -c 'cat {path}'"
        stdin, stdout, stderr = ssh_session.exec_command(command)
        if stderr.channel.recv_exit_status() != 0:
            return False
        
        output = stdout.read().decode().strip()
        print(hashlib.md5(output.encode()).hexdigest())
        return hashlib.md5(output.encode()).hexdigest() == '99a0004b63ced8dfef0d63de1c1955e9'
    
    @ssh_connect()
    def _check_xss_integrity(self, path):
        ssh_session = self.client
        command = f"docker exec webdatubasea_xss_1 sh -c 'cat {path}'"
        stdin, stdout, stderr = ssh_session.exec_command(command)
        if stderr.channel.recv_exit_status() != 0:
            return False
        output = stdout.read().decode().strip()
        print (hashlib.md5(output.encode()).hexdigest())
        return hashlib.md5(output.encode()).hexdigest() == '234c06b516486f37ef4c9550c249e279'

    # Private Funcs - Return False if error
    def _add_new_flag(self, ssh_session, flag):
        # Escapar el valor de la bandera para evitar inyección SQL
        escaped_flag = flag.replace("'", "\\'")  # Escapar comillas simples

        # Comando completo para ejecutar dentro del contenedor
        command = (
            f"docker exec webdatubasea_web_1 sh -c "
            f"\"mysql -h db -u root -proot_password -e \\\""
            f"USE faulty_db; INSERT INTO flags (flag) VALUES ('{escaped_flag}');\\\"\""
        )

        # Ejecutar el comando en el contenedor a través de SSH
        stdin, stdout, stderr = ssh_session.exec_command(command)

        # Comprobar el estado de salida del comando
        exit_status = stdout.channel.recv_exit_status()

        if exit_status != 0:
            # Registrar el error para depuración
            error_message = stderr.read().decode()
            print(f"Error ejecutando comando: {error_message}")
            return False

        # Return the result
        return {'flag': flag}
    
    @ssh_connect()
    def _check_flag_present(self, flag):
        ssh_session = self.client
        command = (
            f"docker exec webdatubasea_db_1 sh -c "
            f"\"mysql -h db -u root -proot_password -sse "
            f"\\\"USE faulty_db; "
            f"SELECT flag FROM flags WHERE flag = '{flag}' ORDER BY id DESC LIMIT 1;\\\"\""
        )
        stdin, stdout, stderr = ssh_session.exec_command(command)
        output = stdout.read().decode().strip()
        if output != flag:
            return False

        
        return flag == output
    
    def _check_port_db(self, ip, port):
        try:
            conn = http.client.HTTPConnection(ip, port, timeout=5)
            conn.request("GET", "/")
            response = conn.getresponse()
            return response.status == 200
        except (http.client.HTTPException, socket.error) as e:
            print(f"Exception: {e}")
            return False
        finally:
            if conn:
                conn.close()

    def _check_port_web(self, ip, port):
        try:
            conn = http.client.HTTPConnection(ip, port, timeout=5)
            conn.request("GET", "/")
            response = conn.getresponse()
            return response.status == 200
        except (http.client.HTTPException, socket.error) as e:
            print(f"Exception: {e}")
            return False
        finally:
            if conn:
                conn.close()

    def _check_port_xss(self, ip, port):
        try:
            conn = http.client.HTTPConnection(ip, port, timeout=5)
            conn.request("GET", "/")
            response = conn.getresponse()
            return response.status == 200
        except (http.client.HTTPException, socket.error) as e:
            print(f"Exception: {e}")
            return False
        finally:
            if conn:
                conn.close()

  
if __name__ == '__main__':
    checkerlib.run_check(MyChecker)




