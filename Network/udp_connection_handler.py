import socket
import threading

class UdpConnectionHandler(object):
    def __init__(self, host_port, guest_port) -> None:
        self._udp_socket = None
        self.__HOST_S_PORT = host_port
        self.__GUEST_S_PORT = guest_port
        self._mode = None
        self._d_port = None
        self._receiver = None
        self._sender = None
        self._outbound_queue = []
        self._inbound_queue = []
        self._is_sending = False
        self._is_receiving = False

    def initialize_connection(self, mode):
        self._mode = mode
        self._udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        if mode == "host":
            self._udp_socket.bind((socket.gethostname(), self.__HOST_S_PORT))
            self._d_port = self.__GUEST_S_PORT
        else:
            self._udp_socket.bind((socket.gethostname(), self.__GUEST_S_PORT))
            self._d_port = self.__HOST_S_PORT

        self._udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    def stop_listener(self):
        self._is_sending = False

    def stop_sender(self):
        self._is_receiving = False

    def start_listener(self):
        self._is_receiving = True
        self._receiver = threading.Thread(target=self.__rcv_msgs)
        self._receiver.start()

    def start_sender(self):
        self._is_sending = True
        self._sender = threading.Thread(target=self.__snd_msg)
        self._sender.start()

    def __rcv_msgs(self):
        while True:
            if self._is_receiving:
                data, addr = self._udp_socket.recvfrom(1024)
                host, port = addr
                self._inbound_queue.append((host, data.decode()))
            else:
                self._inbound_queue.clear()
                return

    def __snd_msg(self):
        while True:
            if self._is_sending:
                if len(self._outbound_queue) == 0:
                    continue
                #FIXME Get message from sync next method instead of using pop
                datagram  = self._outbound_queue.pop()
                msg, addr = datagram
                self._udp_socket.sendto(msg.encode(),(addr, self._d_port))
            else:
                self._outbound_queue.clear()
                return

    def enqueue_outbound_msg(self, msg, addr=None):
        #FIXME Write to queue using sync method instead of using append
        if addr is None:
            self._outbound_queue.append((msg, '<broadcast>'))
        else:
            self._outbound_queue.append((msg, addr))

    def pop_inbound_msg(self):
        #FIXME Read from queue using sync method instead of using pop
        return self._inbound_queue.pop()

    def pending_msgs(self):
        return len(self._inbound_queue) > 0
