import threading
from InterfaceController import InterfaceController
from Lobby.game_lobby import GameLobby
from Network.udp_connection_handler import UdpConnectionHandler

class P2PongGameControl(object):

    def __init__(self) -> None:
        self._connection_handler = UdpConnectionHandler(55585, 55584)
        self._ui_control = InterfaceController()
        self.active_lobby = GameLobby()
        self._remote_event_handler = None
        self.mode = None
        self._peer = None
        self._is_active = False

    def launch_game(self):
        self.mode = self._ui_control.display_menu2()
        self._is_active = True
        self._connection_handler.initialize_connection(self.mode)
        self.active_lobby.open_lobby(self.mode)
        self._connection_handler.start_sender()
        self._connection_handler.start_listener()
        self._remote_event_handler = threading.Thread(target=self.__process_remote_event)
        self._remote_event_handler.start()
        self._ui_control.run_game()

    def __process_remote_event(self):
        if not self._is_active:
            return #TODO Check if it actually kills the thread cleanly

        while True:
            if self._connection_handler.pending_msgs():
                addr, data = self._connection_handler.pop_inbound_msg()

                match data:
                    case "PIVOT":
                        pass
                    case "SCORE":
                        pass
                    case "REJECTED":
                        pass
                    case "READY":
                        pass
                    case "QUIT":
                        pass
                    case _:
                        continue