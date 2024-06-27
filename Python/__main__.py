# Writing by Atlas
# __main__.py
import argparse
from package.server import Server
from package.common.logger import Logger
from package.client import Client
from package.server import Server

# Wireshark rule
# tcp.port == 8680 || tcp.port == 8681 || tcp.port == 8682 || tcp.port == 8683 || tcp.port == 8684 || tcp.port == 8625 || tcp.port == 8468 || tcp.port == 5682 || tcp.port == 9868

# Start Server > python.exe .\__main__.py -s -p 45859 -ip 127.0.0.1
# Start Client > python.exe .\__main__.py -c -p 45859 -ip 127.0.0.1

# TODO: Implementer le changement de port en time based
# TODO: Implementer une communication asynchrone
def setup_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="Port Hopping", description="This project is a proof-of-concept for port hopping, which dynamically changes the port on a regular basis to prevent an attacker from listening in on a port. This project also implements an encryption module to reinforce the confidentiality of exchanges.")
    parser.add_argument("-s", "--server", action="store_true", help="Server Mode, Wait connection from client")
    parser.add_argument("-c", "--client", action="store_true", help="Client Mode, Connect to server")
    parser.add_argument("-p", "--port", action="store", type=int, default=8680, help="Change default starting port")
    parser.add_argument("-ip", "--ip-address", action="store", type=str, default="127.0.0.1", help="IP to use, server : Use for binding, Client : Use ip to connect on server")
    return parser


if __name__ == "__main__":
    parser = setup_parser()
    args = parser.parse_args()
    allowed_port:list = [8680, 8681, 8682, 8683, 8684, 8625, 8468, 5682, 9868]
    # allowed_port:list = [8680]

    port:int = int(args.port)
    if port not in allowed_port:
        allowed_port.append(port)

    ip:str = str(args.ip_address)

    if args.server:
        Logger().info("Server selected")
        my_server = Server()
        my_server.main(ip=ip, port=port, allowed_ports=allowed_port)
    
    elif args.client:
        Logger().info("Client selected")
        my_client = Client(allowed_ports=allowed_port)
        my_client.main(ip=ip, port=port)

    else:
        Logger().info("Nothing selected")
        parser.print_usage()
