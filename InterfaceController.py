import pygame
from EventHandler import EventHandler
from GameLogic import GameLogic

class InterfaceController:
    def __init__(self):
        # Dimensiones de la ventana
        self.width = 800
        self.height = 600

        self.score = 0
        self.enemy_score = 0

        # Inicializar Pygame y configurar la ventana
        pygame.init()
        self.window = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Juego Pong")

        self.event_handler = EventHandler(self)
        
        self.game_logic = GameLogic(self)

        # Colores
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)

        # Posición y tamaño de las paletas
        self.paddle_width = 10
        self.paddle_height = 80
        self.paddle_x = 20
        self.paddle_y = self.height // 2 - self.paddle_height // 2
        self.paddle_speed = 1.1

        # Posición y tamaño de la bola
        self.ball_size = 10
        self.ball_x = self.width // 2 - self.ball_size // 2
        self.ball_y = self.height // 2 - self.ball_size // 2
        self.ball_speed_x = 0.9
        self.ball_speed_y = 0.9

    def display_menu(self):
        # Configuración de la fuente
        font = pygame.font.Font(None, 24)

        # Variables para el campo de entrada y las opciones del menú
        username = ""
        selected_option = None

        while selected_option is None:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if create_room_button.collidepoint(mouse_pos):
                        selected_option = "Crear sala" if len(username) > 0 else None
                    elif join_room_button.collidepoint(mouse_pos):
                        selected_option = "Unirse a sala"
                    elif exit_button.collidepoint(mouse_pos):
                        selected_option = "Salir"

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        username = username[:-1]
                    else:
                        username += event.unicode

            # Dibujar el fondo y el menú
            self.window.fill(self.BLACK)
            menu_text = font.render("Bienvenido al juego Pong", True, self.WHITE)
            text_rect = menu_text.get_rect(center=(self.width // 2, self.height // 4))
            self.window.blit(menu_text, text_rect)

            username_text = font.render("Ingresa tu nombre de usuario:", True, self.WHITE)
            username_rect = username_text.get_rect(center=(self.width // 2, self.height // 2))
            self.window.blit(username_text, username_rect)

            input_text = font.render(username, True, self.WHITE)
            input_rect = input_text.get_rect(midtop=(self.width // 2, self.height // 2 + 30))
            pygame.draw.rect(self.window, self.BLACK, pygame.Rect(input_rect.left - 5, input_rect.top - 5, input_rect.width + 10, input_rect.height + 10))
            self.window.blit(input_text, input_rect)

            create_room_button = pygame.draw.rect(self.window, self.WHITE, pygame.Rect(self.width // 2 - 100, self.height // 2 + 80, 200, 30))
            create_room_text = font.render("Crear sala", True, self.BLACK)
            create_room_text_rect = create_room_text.get_rect(center=create_room_button.center)
            self.window.blit(create_room_text, create_room_text_rect)

            join_room_button = pygame.draw.rect(self.window, self.WHITE, pygame.Rect(self.width // 2 - 100, self.height // 2 + 120, 200, 30))
            join_room_text = font.render("Unirse a sala", True, self.BLACK)
            join_room_text_rect = join_room_text.get_rect(center=join_room_button.center)
            self.window.blit(join_room_text, join_room_text_rect)

            exit_button = pygame.draw.rect(self.window, self.WHITE, pygame.Rect(self.width // 2 - 100, self.height // 2 + 160, 200, 30))
            exit_text = font.render("Salir", True, self.BLACK)
            exit_text_rect = exit_text.get_rect(center=exit_button.center)
            self.window.blit(exit_text, exit_text_rect)

            pygame.display.flip()

        print(username)
        return selected_option, username


    def display_notification(self, message):
        # Configuración de la fuente
        font = pygame.font.Font(None, 24)

        # Tiempo de duración de la notificación (en milisegundos)
        notification_duration = 2000  # 2 segundos

        # Obtener el tiempo actual
        current_time = pygame.time.get_ticks()

        # Calcular el tiempo de expiración de la notificación
        expiration_time = current_time + notification_duration

        while pygame.time.get_ticks() < expiration_time:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

            # Dibujar el fondo y el mensaje de la notificación
            self.window.fill(self.BLACK)
            notification_text = font.render(message, True, self.WHITE)
            text_rect = notification_text.get_rect(center=(self.width // 2, self.height // 2))
            self.window.blit(notification_text, text_rect)

            pygame.display.update()

    def move_paddle_up(self):
        if self.paddle_y > 0:
            self.paddle_y -= self.paddle_speed

    def move_paddle_down(self):
        if self.paddle_y < self.height - self.paddle_height:
            self.paddle_y += self.paddle_speed

    def update_score(self):
        # Configuración de la fuente
        font = pygame.font.Font(None, 24)

        # Crear el texto del puntaje
        score_text = font.render("Puntaje: " + str(self.score), True, self.WHITE)

        # Posicionar el texto en la ventana
        score_rect = score_text.get_rect(topright=(self.width - 10, 10))

        # Dibujar el texto en la ventana
        self.window.blit(score_text, score_rect)

        # Crear el texto del puntaje del enemigo
        enemy_score_text = font.render("Puntaje enemigo: " + str(self.enemy_score), True, self.WHITE)

        # Posicionar el texto en la ventana
        enemy_score_rect = enemy_score_text.get_rect(topright=(self.width - 10, 40))

        # Dibujar el texto en la ventana
        self.window.blit(enemy_score_text, enemy_score_rect)

    def reset_ball(self):
        self.ball_x = self.width // 2 - self.ball_size // 2
        self.ball_y = self.height // 2 - self.ball_size // 2

    def reset_game(self):
        self.score = 0
        self.enemy_score = 0
        self.reset_ball()

    def run_game(self):
        # Bucle principal del juego
        running = True
        game_logic = GameLogic(self)
        while running:
            self.event_handler.handle_events()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Lógica del juego 
            game_logic.update_game()            

            # Actualizar la posición de las paletas
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:
                self.move_paddle_up()
            if keys[pygame.K_DOWN]:
                self.move_paddle_down()

            # Actualizar la posición de la bola
            self.ball_x += self.ball_speed_x
            self.ball_y += self.ball_speed_y

            # Verificar si la bola ha alcanzado los bordes horizontales
            if (self.ball_x <= 0) or (self.ball_x >= self.width - self.ball_size):
                self.ball_speed_x *= -1

            # Verificar si la bola ha alcanzado los bordes verticales
            if (self.ball_y <= 0) or (self.ball_y >= self.height - self.ball_size):
                self.ball_speed_y *= -1

            # Renderizar los cambios en la ventana

            # Dibujar el fondo
            self.window.fill(self.BLACK)

            # Dibujar las paletas
            pygame.draw.rect(self.window, self.WHITE, (self.paddle_x, self.paddle_y, self.paddle_width, self.paddle_height))
            pygame.draw.rect(self.window, self.WHITE, (self.width - self.paddle_x - self.paddle_width, self.paddle_y, self.paddle_width, self.paddle_height))

            # Dibujar la bola
            pygame.draw.rect(self.window, self.WHITE, (self.ball_x, self.ball_y, self.ball_size, self.ball_size))

            # Actualizar el puntaje en la interfaz
            self.update_score()

            # Actualizar la ventana
            pygame.display.update()


        pygame.quit()

# Crear una instancia de la clase InterfaceController y ejecutar el juego
game = InterfaceController()
#game.display_notification("Jaja soy yo de nuevo!!")
#game.display_menu()
game.run_game()
