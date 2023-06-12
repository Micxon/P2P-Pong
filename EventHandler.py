import sys
import pygame

class EventHandler:
    def __init__(self, interface_controller):
        self.interface_controller = interface_controller
        self.collision_detected = True
        self.point_scored = False

    def handle_collision(self):
        player_paddle_rect = pygame.Rect(self.interface_controller.paddle_x, self.interface_controller.paddle_y, self.interface_controller.paddle_width, self.interface_controller.paddle_height)
        enemy_paddle_rect = pygame.Rect(self.interface_controller.width - self.interface_controller.paddle_x - self.interface_controller.paddle_width, self.interface_controller.paddle_y, self.interface_controller.paddle_width, self.interface_controller.paddle_height)
        ball_rect = pygame.Rect(self.interface_controller.ball_x, self.interface_controller.ball_y, self.interface_controller.ball_size, self.interface_controller.ball_size)

        if ball_rect.colliderect(player_paddle_rect) or ball_rect.colliderect(enemy_paddle_rect):
            # La bola golpeó una de las paletas, cambia la dirección de la bola
            self.interface_controller.ball_speed_x *= -1
            self.collision_detected = True
        else:
            # La bola no golpeó ninguna paleta, se anota un punto
            if self.interface_controller.ball_x <= 0:
                # Punto para el enemigo
                self.interface_controller.enemy_score += 1
                self.interface_controller.display_notification("¡El enemigo anotó un punto!")
                if self.interface_controller.enemy_score >= 10:
                    self.interface_controller.display_notification("¡El enemigo ha ganado!")
            else:
                # Punto para el jugador
                self.interface_controller.score += 1
                self.interface_controller.display_notification("¡Has anotado un punto!")
                if self.interface_controller.score >= 10:
                    self.interface_controller.display_notification("¡Ganaste!")

            self.interface_controller.reset_ball()
            self.collision_detected = False

        if not self.collision_detected:
            self.interface_controller.update_score()

    def handle_point_scored(self):
        if self.point_scored:
            # Incrementar el puntaje del jugador
            self.interface_controller.score += 1
            self.interface_controller.update_score()  # Actualizar el puntaje en la interfaz
            self.point_scored = False

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                self.handle_keydown(event.key)

    def handle_keydown(self, key):
        if key == pygame.K_UP:
            self.interface_controller.move_paddle_up()
        elif key == pygame.K_DOWN:
            self.interface_controller.move_paddle_down()
