# Writing by Atlas
# server.py

from package.common.common import Common
from socket import socket, AF_INET, SOCK_STREAM, SHUT_RDWR, IPPROTO_IP, IP_TOS
from package.socket_class import SocketClass
from package.common.logger import Logger
import subprocess
from time import sleep
import package.common.constants as Constant
import logging

# Faire une class avec un stdout et stdin en pipe, en thread
class Server(SocketClass):
    def __init__(self):
        super().__init__()
        self.my_socket:socket = socket(AF_INET, SOCK_STREAM)
        self.my_socket.setsockopt(IPPROTO_IP, IP_TOS, 16)
    
    def bind(self, ip:str="127.0.0.1", port: int= 8680) -> None:
        self.port: int= int(port)
        self.my_socket.bind((ip, self.port))

    def listen(self) -> None:
        self.my_socket.listen(5)

    def accept(self) -> tuple:
        (client_socket, client_address) = self.my_socket.accept()
        return (client_socket, client_address)

    def rebind_port(self, ip:str, port:int) -> bool:
        try:
            self.my_socket:socket = socket(AF_INET, SOCK_STREAM)
            self.bind(ip=ip, port=port)
            self.my_socket.settimeout(Constant.SOCKET_SERVER_TIMEOUT)
            return True
        except:
            return False

    def main(self, ip:str, port:int, allowed_ports:list) -> None:
        self.bind(ip=ip, port=port)
        is_continue = True
        self.port = port
        new_port = port
        i=0
        while is_continue:
            Logger().info(f"Server port : {self.port}")
            try:
                self.listen()
                sock = self.accept()
                while new_port == self.port:
                    Logger().info(f"I : {i}")
                    client_socket = SocketClass(sock[0])
                    try:
                        command = client_socket.secure_receive(self.port).decode("utf-8")
                        Logger().info(f"{sock[1][0]}:{sock[1][1]} say > {command}, {type(command)}")

                        if command.upper() == "Q":
                            is_continue = False
                            client_socket.secure_send("Q".encode("utf-8"), self.port)
                            Logger().warning(f"Reading quit command : {command}")
                            break
                        else:
                            client_socket.secure_send("OK".encode("utf-8"), self.port)

                    except KeyboardInterrupt:
                        exit()
                    except Exception as e:
                        Logger().warning(f"Error during reading or sending data")
                        Logger().error(f"{e}")
                        Logger().print_traceback(logging.ERROR)
                        exit()

                    new_port = Common.calcul_next_port(self.port, allowed_ports=allowed_ports)

                # self.secure_send(client_socket, "CHANGE_PORT".encode("utf-8"), self.port)
                client_socket.shutdown()
                client_socket.close()
                self.my_socket.close()
                # while self.rebind_port(ip=ip, port=new_port):
                #     new_port = Common.calcul_next_port(self.port, allowed_ports=allowed_ports)
                self.rebind_port(ip=ip, port=new_port)
                i += 1

            except KeyboardInterrupt:
                Logger().print_traceback(logging.WARNING)
                exit()

            except TimeoutError:
                Logger().warning("Timeout reached")
                Logger().print_traceback(logging.WARNING)
                
            except:
                Logger().warning(f"Error port probably already used")
                Logger().print_traceback()
                temp_port = 0
                while new_port != temp_port:
                    sleep(1)
                    temp_port = Common.calcul_next_port(self.port, allowed_ports=allowed_ports)
                    new_port = temp_port  if self.rebind_port(ip=ip, port=temp_port) else 0
                

        self.my_socket.close()
