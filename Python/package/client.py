# Writing by Atlas
# client.py

from package.socket_class import SocketClass
from package.common.common import Common
from socket import socket, AF_INET, SOCK_STREAM, SHUT_RDWR, IPPROTO_IP, IP_TOS
from package.common.logger import Logger
import random
import package.common.constants as Constant
from time import sleep, time
from queue import Queue
import statistics

class Client(SocketClass):
    def __init__(self, allowed_ports:[] = [8680]):
        super().__init__()
        self.my_socket:socket = socket(AF_INET, SOCK_STREAM)
        self.my_socket.setsockopt(IPPROTO_IP, IP_TOS, 16)
        self.std_out:Queue = Queue()
        self.std_in:Queue = Queue()
        self.allowed_ports:[] = allowed_ports
        self.allowed_ports:[] = allowed_ports
        self.messages_sent = 0
        self.messages_received = 0
        self.start_time = time()
        self.last_send_time = time()
        self.send_times = []
        self.timeout_reached = 0
        self.fail_reading_sending = 0

    def connect(self, ip:str="127.0.0.1", port:int=8680) -> bool:
        try:
            self.port = port
            self.my_socket.connect((ip, port))
            self.my_socket.settimeout(Constant.SOCKET_CLIENT_TIMEOUT)
            return True
        except:
            return False

    def rebind_port(self, port:int) -> None:
        self.my_socket:socket = socket(AF_INET, SOCK_STREAM)
        self.port:int = int(port)
    
    def change_port(self) -> None:
        new_port = Common.calcul_next_port(self.port, allowed_ports=self.allowed_ports)
        if new_port != self.port:
            self.rebind_port(self, new_port)


    def main(self, ip:str, port:int) -> None:
        self.port = int(port)
        
        list_send_text:list = ["Hello World!", "My name is Bob", "I send message to Alfred", "How did you do?", "If ... then ... else ...", "Input Output", "Nope", "Yep", "This is a file", "This is a code", "To be or not to be", "C is a best language ever", "bash ipconfig", "bash ping 127.0.0.1 -n 2"]
        is_continue:bool = True
        i = 0
        self.port = port
        new_port = port

        while is_continue:
            Logger().info(f"Client port : {self.port}")
            try:
                if not self.connect(ip=ip, port=self.port):
                    Logger().warning("Not connected")
                    new_port = Common.calcul_next_port(self.port, allowed_ports=self.allowed_ports)
                    self.rebind_port(port=new_port)
                    continue
                is_next = 0
                while new_port == self.port or is_next <= 1:
                    Logger().info(f"I : {i}")
                    try:
                        if i >= 5000:
                            self.secure_send("Q".encode("utf-8"), self.port)
                            Logger().info(f"Sending Quit Command")
                        else:
                            text_to_send:str = random.choice(list_send_text)
                            self.secure_send(text_to_send.encode("utf-8"), self.port)
                            self.messages_sent += 1
                            self.last_send_time = time()
                            current_time = time()
                            messages_per_second = self.messages_sent / (current_time - self.start_time)
                            Logger().info(f"Messages sent: {self.messages_sent}")
                            Logger().info(f"Messages per second: {messages_per_second}")

                        text = self.secure_receive(self.port)

                        self.messages_received += 1
                        time_since_last_send = time() - self.last_send_time
                        self.send_times.append(time_since_last_send)
                        mean_send_time = statistics.mean(self.send_times)
                        median_send_time = statistics.median(self.send_times)
                        Logger().info(f"Messages received: {self.messages_received}")
                        Logger().info(f"Time since last send: {time_since_last_send}")
                        Logger().info(f"Mean send time: {mean_send_time}")
                        Logger().info(f"Median send time: {median_send_time}")

                        text_clear = ""
                        try:
                            text_clear = text.decode("utf-8")
                        except:
                            try:
                                text_clear = text.decode("ascii")
                            except:
                                try:
                                    text_clear = text.decode("ansi")
                                except:
                                    text_clear = text
                        Logger().info(f"Server say > {text_clear}")

                        if type(text_clear) == str:
                            if text_clear.upper() == "Q":
                                Logger().warning(f"Quit Command Received")
                                is_continue = False
                                break

                        Logger().info(f"Command execute > {text_clear}")

                    except TimeoutError:
                        Logger().warn("Timeout Reached")
                        self.timeout_reached += 1

                    except Exception as e:
                        self.fail_reading_sending += 1
                        Logger().warning(f"Error during reading or sending data")
                        Logger().error(f"{e}")
                        sleep(1)

                    new_port = Common.calcul_next_port(self.port, allowed_ports=self.allowed_ports)
                    if new_port != self.port:
                        is_next += 1
                        Logger().debug(f"Iter : {is_next}, {new_port} == {self.port} or {is_next} <= 1 : {new_port == self.port or is_next <= 1}")

                    i+=1
                
                self.my_socket.shutdown(SHUT_RDWR)
                self.my_socket.close()

                self.rebind_port(port=new_port)

            except Exception as e:
                Logger().warning(f"Error during connection")
                Logger().error(f"{e}")
            mean_send_time = statistics.mean(self.send_times)
            median_send_time = statistics.median(self.send_times)
            Logger().info(f"Messages received: {self.messages_received}")
            Logger().info(f"Time since last send: {time_since_last_send}")
            Logger().info(f"Mean send time: {mean_send_time}")
            Logger().info(f"Median send time: {median_send_time}")
            Logger().info(f"reached timeout: {self.timeout_reached}")
            Logger().info(f"fail reading sending: {self.fail_reading_sending}")