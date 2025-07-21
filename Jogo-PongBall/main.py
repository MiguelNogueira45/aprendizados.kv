from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.core.window import Window
from random import randint

class PongBall(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos

    def bounce_paddle(self, paddle):
        if self.collide_widget(paddle):
            offset = (self.center_y - paddle.center_y) / (paddle.height / 2)
            bounced = Vector(-1 * self.velocity_x, self.velocity_y)
            self.velocity = bounced * 1.1  # Aumenta a velocidade após cada rebatida
            self.velocity_y += offset * 2  # Ângulo varia conforme o local do impacto

    def bounce_wall(self):
        self.velocity_y *= -1

class PongPaddle(Widget):
    score = NumericProperty(0)
    velocity = NumericProperty(0)  # Nova propriedade para controle por teclado

    def bounce_ball(self, ball):
        if self.collide_widget(ball):
            ball.bounce_paddle(self)
    
    def move(self):
        self.y += self.velocity
        # Limita o movimento para não sair da tela
        if self.y < 0:
            self.y = 0
        if self.top > self.parent.height:
            self.top = self.parent.height

class PongGame(Widget):
    ball = ObjectProperty(None)
    player1 = ObjectProperty(None)
    player2 = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(PongGame, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        self._keyboard.bind(on_key_up=self._on_keyboard_up)

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard.unbind(on_key_up=self._on_keyboard_up)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        # Jogador 1 (esquerda) - W/S
        if keycode[1] == 'w':
            self.player1.velocity = 5
        elif keycode[1] == 's':
            self.player1.velocity = -5
        
        # Jogador 2 (direita) - Setas ↑/↓
        elif keycode[1] == 'up':
            self.player2.velocity = 5
        elif keycode[1] == 'down':
            self.player2.velocity = -5
        return True

    def _on_keyboard_up(self, keyboard, keycode):
        # Para o movimento quando a tecla é solta
        if keycode[1] in ('w', 's'):
            self.player1.velocity = 0
        elif keycode[1] in ('up', 'down'):
            self.player2.velocity = 0
        return True

    def serve_ball(self, vel=(4, 0)):
        self.ball.center = self.center
        self.ball.velocity = Vector(vel[0], vel[1]).rotate(randint(-30, 30))

    def update(self, dt):
        # Atualiza o movimento das raquetes
        self.player1.move()
        self.player2.move()
        
        self.ball.move()

        # Rebate no topo e na base
        if (self.ball.y < 0) or (self.ball.top > self.height):
            self.ball.bounce_wall()

        # Rebate nas raquetes
        self.player1.bounce_ball(self.ball)
        self.player2.bounce_ball(self.ball)

        # Pontuação
        if self.ball.x < self.x:
            self.player2.score += 1
            self.serve_ball(vel=(4, 0))
        elif self.ball.right > self.width:
            self.player1.score += 1
            self.serve_ball(vel=(-4, 0))

    def on_touch_move(self, touch):
        # Controle das raquetes por toque (mantido para compatibilidade)
        if touch.x < self.width / 3:
            self.player1.center_y = touch.y
        if touch.x > self.width - self.width / 3:
            self.player2.center_y = touch.y

class PongApp(App):
    def build(self):
        game = PongGame()
        game.serve_ball()
        Clock.schedule_interval(game.update, 1.0 / 120.0)  # 60 FPS
        return game

if __name__ == '__main__':
    PongApp().run()
    