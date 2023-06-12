from Network.udp_connection_handler import UdpConnectionHandler

class GameLobby(object):

    def __init__(self) -> None:
        self._connection_handler = UdpConnectionHandler()

    def configure_lobby(self, mode):
        self._connection_handler.initialize_connection(mode)
        if mode == "host":
            self.host_lobby()
        elif mode == "connect":
            self.join_lobby()

    def host_lobby(self):
        self._connection_handler.start_listener()

    def join_lobby(self):
        self._connection_handler.start_sender()
        self.__send_msg_to_peer("JOIN REQUEST")

    def __send_msg_to_peer(self, msg):
        self._connection_handler.enqueue_msg(msg)
