import socket
import json

localIP = "127.0.0.1"
localPort = 53533
bufferSize = 2048

msgFromServer = "Hello UDP Client"

bytesToSend = str.encode(msgFromServer)

# Create a datagram socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Bind to address and ip

UDPServerSocket.bind((localIP, localPort))

print("UDP server up and listening")

# Listen for incoming datagrams

while (True):
    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    message = bytesAddressPair[0]
    sender = bytesAddressPair[1]
    print(message)
    print(sender)
    request = json.loads(message.decode())

    if len(request) == 2:
        print("dns query")
        with open("record.json", "r") as dns:
            dns_dict = json.load(dns)
        resp = dns_dict[request["NAME"]]
        data = json.dumps(resp)
        UDPServerSocket.sendto(data.encode(), sender)
    elif len(request) == 4:
        print("register")
        print(request)
        data = {request["NAME"]: sender[0]}
        print(data)
        data = json.dumps(data)
        with open("record.json", "w") as dns:
            dns.write(data)
        UDPServerSocket.sendto(str(201).encode(), sender)
    else:
        UDPServerSocket.sendto(str(500).encode(), sender)

    UDPServerSocket.sendto(bytesToSend, sender)