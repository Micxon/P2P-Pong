import pygame

class GameLogic:
    def __init__(self, interface_controller):
        self.interface_controller = interface_controller

    def update_game(self):
        self.move_ball()
        self.handle_collisions()
        self.update_score()
        self.check_winner()

    def move_ball(self):
        self.interface_controller.ball_x += self.interface_controller.ball_speed_x
        self.interface_controller.ball_y += self.interface_controller.ball_speed_y

        # Verificar si la bola ha alcanzado los bordes horizontales
        if (self.interface_controller.ball_x <= 0) or (
                self.interface_controller.ball_x >= self.interface_controller.width - self.interface_controller.ball_size):
            self.interface_controller.ball_speed_x *= -1

        # Verificar si la bola ha alcanzado los bordes verticales
        if (self.interface_controller.ball_y <= 0) or (
                self.interface_controller.ball_y >= self.interface_controller.height - self.interface_controller.ball_size):
            self.interface_controller.ball_speed_y *= -1

    def handle_collisions(self):
        ball_rect = pygame.Rect(self.interface_controller.ball_x, self.interface_controller.ball_y,
                                self.interface_controller.ball_size, self.interface_controller.ball_size)
        paddle_rect = pygame.Rect(self.interface_controller.paddle_x, self.interface_controller.paddle_y,
                                  self.interface_controller.paddle_width, self.interface_controller.paddle_height)

        if ball_rect.colliderect(paddle_rect):
            self.interface_controller.ball_speed_x *= -1

    def update_score(self):
        if self.interface_controller.event_handler.point_scored:
            self.interface_controller.event_handler.point_scored = False
            self.interface_controller.update_score()

        if self.interface_controller.ball_x <= 0:
            self.interface_controller.enemy_score += 1
            self.interface_controller.display_notification("¡El enemigo anotó un punto!")

            if self.interface_controller.enemy_score >= 10:
                self.interface_controller.display_notification("¡El enemigo ha ganado!")

            self.interface_controller.reset_ball()

    def check_winner(self):
        if self.interface_controller.score >= 10:
            self.interface_controller.display_notification("¡Ganador!")
            self.interface_controller.reset_game()
