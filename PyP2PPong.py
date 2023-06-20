import sys
from Lobby.game_lobby import GameLobby
from UI.temp_cmd_menu import CMD_Menu
#from p2pong_game_control import P2PongGameControl

def main():
    active_lobby = GameLobby()
    main_menu = CMD_Menu()
    main_menu.display()

    if main_menu.get_mode() == "host" or main_menu.get_mode() == "join":
       #active_lobby.open_lobby(main_menu.get_mode())
       active_lobby.open_vpn_lobby(main_menu.get_mode())
    else:
        print("Invalid selection, exiting program")
        sys.exit()

    while active_lobby.is_open():
        if active_lobby.is_ready():
            print("Game is ready to start!")
            break
        continue

    print("Game lobby has been closed. Exiting game")
    sys.exit()
#    game_controller = P2PongGameControl()
#    game_controller.launch_game()

if __name__ == "__main__":
    main()

