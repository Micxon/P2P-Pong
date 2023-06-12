from Lobby.game_lobby import GameLobby
from UI.temp_cmd_menu import CMD_Menu


def main():
    active_lobby = GameLobby()
    main_menu = CMD_Menu()
    main_menu.display()

    active_lobby.configure_lobby(main_menu.get_mode())
    
if __name__ == "__main__":
    main()