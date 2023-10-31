from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.togglebutton import ToggleButton
from kivy.graphics import Color, Ellipse

class CircularButton(ToggleButton):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.width = 400
        self.height = 400

        # Create a circular shape for the button
        with self.canvas:
            Color(1, 1, 1)  # Color for the button's background
            self.circle = Ellipse(pos=self.pos, size=self.size)

        self.bind(pos=self.update_shape, size=self.update_shape)

    def update_shape(self, instance, value):
        self.circle.pos = self.pos
        self.circle.size = self.size

class CircularButtonApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical', spacing=10)

        # Create a circular on-off button
        button = CircularButton(text="Off")
        button.bind(on_press=self.on_button_press)
        layout.add_widget(button)

        return layout

    def on_button_press(self, instance):
        if instance.state == 'normal':
            instance.text = "On"
        else:
            instance.text = "Off"

if __name__ == '__main__':
    CircularButtonApp().run()
