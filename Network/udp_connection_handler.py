import socket
import threading

class UdpConnectionHandler(object):
    __HOST_S_PORT = 45585
    __GUEST_S_PORT = 45584

    def __init__(self) -> None:
        self._udp_socket = None
        self._mode = None
        self._d_addr = None
        self._d_port = None
        self._receiver = None
        self._sender = None
        self._outbound_queue = []

    def initialize_connection(self, mode):
        self._mode = mode
        self._udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        if mode == "host":
            self._udp_socket.bind((socket.gethostname(), UdpConnectionHandler.__HOST_S_PORT))
            self._d_port = UdpConnectionHandler.__GUEST_S_PORT
        else:
            self._udp_socket.bind((socket.gethostname(), UdpConnectionHandler.__GUEST_S_PORT))
            self._d_port = UdpConnectionHandler.__HOST_S_PORT

        self._udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    def start_listener(self):
        self._receiver = threading.Thread(target=self.__rcv_msgs)
        print("waiting for peer to join")
        self._receiver.start()

    def start_sender(self):
        self._sender = threading.Thread(target=self.__snd_msg)
        print("sending connection request")
        self._sender.start()

    def __rcv_msgs(self):
        while True:
            data, addr = self._udp_socket.recvfrom(1024)
            print("[Received message] {}: {}".format(addr, data.decode()))

    def __snd_msg(self):
        while True:
            if len(self._outbound_queue) == 0:
                continue
            #FIXME Get message from sync next method instead of using pop
            msg = self._outbound_queue.pop()
            if self._d_addr is  None:
                self._udp_socket.sendto(msg.encode(),('<broadcast>', self._d_port))
            else:
                self._udp_socket.sendto(msg.encode(),(self._d_addr, self._d_port))

    def enqueue_msg(self, msg):
        #FIXME Write to queue using sync method instead of using insert
        self._outbound_queue.append(msg)
