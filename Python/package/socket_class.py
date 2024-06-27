# Writing by Atlas
# socket_class.py

from package.common.logger import Logger
from socket import socket
from socket import socket, SHUT_RDWR

class SocketClass:
    __my_socket_verbose:bool = True

    def __init__(self, socket:socket = None) -> None:
        self.my_socket:socket = socket
    
    def shutdown(self) -> None:
        self.my_socket.shutdown(SHUT_RDWR)

    def close(self) -> None:
        self.my_socket.close()

    def secure_send(self, data:bytes, seed:int) -> None:
        self.__send(data=data)

    def __send(self, data:bytes) -> None:
        len_data = len(data)
        data_size = str(str(len_data) + "\n").encode("utf-8")

        self.my_socket.send(data_size)
        Logger().debug(f"Send : len_data {len_data}") if SocketClass.__my_socket_verbose else None

        self.my_socket.send(data)
        Logger().debug(f"Send : data {data}") if SocketClass.__my_socket_verbose else None


    def __receive_lenght_data(self) -> int:
        buffer:str = ""
        temp = ""
        while temp != "\n":
            temp = self.my_socket.recv(1).decode("utf-8")
            buffer += temp

        try:
            buffer_length:int = int(buffer)
            return buffer_length

        except Exception as e:
            Logger().error(f"Buffer length cannot be convert to int : {buffer}")
            raise e

    def secure_receive(self, seed:int) -> bytes:
        text_received:bytes = self.__receive()
        return text_received

    def __receive(self) -> bytes:
        buffer_length:int = self.__receive_lenght_data()
        Logger().debug(f"Length data to receive : {buffer_length}") if SocketClass.__my_socket_verbose else None
        temp_len:int = 0
        chunks:bytes = b''
        while temp_len < buffer_length:
            chunk:bytes = self.my_socket.recv(buffer_length - temp_len)
            temp_len += len(chunk)
            chunks = chunks + chunk
            Logger().debug(f"Data received ({temp_len}*{100}/{buffer_length} = {(temp_len*100)/buffer_length}%): {chunk}") if SocketClass.__my_socket_verbose else None
        Logger().debug(f"Data complete : {chunks}") if SocketClass.__my_socket_verbose else None
        return chunks