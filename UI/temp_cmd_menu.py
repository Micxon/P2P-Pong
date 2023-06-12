class CMD_Menu(object):

    def __init__(self) -> None:
        self._options = 0
        self._mode = ""

    def display(self):
        print("P2P-PONG v0.01")
        print("- 'host' to host game")
        print("- 'connect' to connect to server")
        print("- 'quit' to quit game")
        self._mode = input("> ")

    def get_mode(self) -> str:
        return self._mode
