import threading
import time
from Network.udp_connection_handler import UdpConnectionHandler

class GameLobby(object):

    def __init__(self) -> None:
        self._connection_handler = UdpConnectionHandler()
        self._msg_handler = None
        self._peer = None
        self._is_open = False

    def open_lobby(self, mode):
        self._is_open = True
        self._connection_handler.initialize_connection(mode)
        if mode == "host":
            self.__launch_lobby()
        elif mode == "connect":
            self.__launch_lobby()
            self.__send_msg_to_peer("JOIN REQUEST")

    def __launch_lobby(self):
        self._connection_handler.start_sender()
        self._connection_handler.start_listener()
        self._msg_handler = threading.Thread(target=self.__read_msgs)
        self._msg_handler.start()

    def close_lobby(self):
        print("Closing game lobby")
        self._is_open = False
        self._connection_handler.stop_listener()
        self._connection_handler.stop_sender()

    def __read_msgs(self):
        if not self._is_open:
            return

        while True:
            if self._connection_handler.pending_msgs():
                addr, data = self._connection_handler.pop_inbound_msg()

                match data:
                    case "JOIN REQUEST":
                        self.__process_join_request(addr)
                    case "ACCEPTED":
                        self.__accept_rdy_check(addr)
                    case "REJECTED":
                        self.__process_rejected_request(addr)
                    case "READY":
                        self.__accept_rdy_check(addr)
                    case "QUIT":
                        self._peer = None
                        return #TODO Check if it actually kills the thread cleanly
                    case _:
                        continue

    def __accept_rdy_check(self, addr):
        while True:
            print("The join request has been accepted by ", addr, ". Ready to start? (Y/N):")
            reply = input("> ")

            if reply == "Y":
                self._peer = addr
                self.__send_msg_to_peer("READY")
                break
            else:
                print("Do you want to quit ", addr, " game lobby? (Y/N):")
                reply = input("> ")

                if reply == "Y":
                    self.quit_peer_lobby(addr)
                    break

                print("take your time. You will be prompted again in 5 seconds")
                time.sleep(5)

    def quit_peer_lobby(self, addr=None):
        if addr is None:
            self.__send_msg_to_peer("QUIT", self._peer)
        else:
            self.__send_msg_to_peer("QUIT", addr)
        self._peer = None
        self.close_lobby()

    def __send_msg_to_peer(self, msg, addr=None):
        if addr is None:
            self._connection_handler.enqueue_outbound_msg(msg, self._peer)
        else:
            self._connection_handler.enqueue_outbound_msg(msg, addr)

    def __process_join_request(self, addr):
        if self._peer is not None:
            self.__send_msg_to_peer("REJECTED", addr)
            return

        print("Do you want to accept the connection from ", addr, "? (Y/N):")
        reply = input("> ")

        if reply == "Y":
            self._peer = addr
            self.__send_msg_to_peer("ACCEPTED")
        else:
            self.__send_msg_to_peer("REJECTED", addr)

    def __process_rejected_request(self, addr):
        print("The join request has been rejected by ", addr, ". Try again? (Y/N):")
        reply = input("> ")

        if reply == "Y":
            self.__send_msg_to_peer("JOIN REQUEST")
        else:
            self.close_lobby()
