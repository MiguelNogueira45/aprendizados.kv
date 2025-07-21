from kivy.uix.button import Button
import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse, Line

class MeuPaintWidget(Widget):
    def on_touch_down(self, touch):
        with self.canvas:
            Color(1, 1, 0)
            d = 30.
            Ellipse(pos=(touch.x - d / 2, touch.y - d /2 ), size=(d, d))
            touch.ud['line'] = Line(points=(touch.x, touch.y))  
            
            
    def on_touch_move(self, touch):
        touch.ud['line'].points += [touch.x, touch.y]

class MeuPaintApp(App):
    def build(self):
        parent  = Widget()
        self.painter = MeuPaintWidget()
        clearbtn = Button(text='apagar')
        clearbtn.bind (on_release=self.clear_canvas)
        parent.add_widget(self.painter)
        parent.add_widget(clearbtn)
        return parent
    
    def clear_canvas(self, obj):
        
        self.painter.canvas.clear()
    
MeuPaintApp().run()