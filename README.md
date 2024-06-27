# README

## Description

This application serves as a Proof of Concept (POC) for research and educational purposes only, aimed at testing the viability of Port Hopping, a method that involves establishing a network communication and dynamically switching the port. I am currently pursuing my M1 at ESIEE-IT, and this project is a part of my coursework. It is not intended for any malicious activities.

## How to Start the Application

To start the application, you need to start both the server and the client.

### Start Server

Use the following command to start the server:

```bash
python.exe .\__main__.py -s -p 45859 -ip 127.0.0.1
```

### Start Client

Use the following command to start the client:

```bash
python.exe .\__main__.py -c -p 45859 -ip 127.0.0.1
```

## Wireshark Rule

To monitor the network traffic, you can use the following Wireshark rule:

```bash
tcp.port == 8680 || tcp.port == 8681 || tcp.port == 8682 || tcp.port == 8683 || tcp.port == 8684 || tcp.port == 8625 || tcp.port == 8468 || tcp.port == 5682 || tcp.port == 9868
```

## Arguments

The application accepts the following arguments:

- `-s`, `--server`: Start the application in server mode. The server will wait for a connection from a client.
- `-c`, `--client`: Start the application in client mode. The client will connect to the server.
- `-p`, `--port`: Change the default starting port. The default port is `8680`.
- `-ip`, `--ip-address`: Specify the IP address to use. In server mode, this IP address is used for binding. In client mode, this IP address is used to connect to the server. The default IP address is `127.0.0.1`.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)