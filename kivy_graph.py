from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.graphics import Line, Color

class GraphWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.points = []

    def on_touch_down(self, touch):
        self.points.append(touch.pos)
        self.draw_graph()

    def draw_graph(self):
        with self.canvas:
            self.canvas.clear()
            Color(0.1, 0.6, 0.3)  # Set line color (RGB values)
            Line(points=self.points, width=2)

class GraphApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')

        # Add the graph widget to the layout
        graph_widget = GraphWidget()
        layout.add_widget(graph_widget)

        # Add a button to clear the graph
        clear_button = Button(text='Clear Graph')
        clear_button.bind(on_release=self.clear_graph)
        layout.add_widget(clear_button)

        return layout

    def clear_graph(self, instance):
        # Clear the graph by resetting the points list
        graph_widget = self.root.children[0]  # Get the first child (the graph widget)
        graph_widget.points = []
        graph_widget.canvas.clear()

if __name__ == '__main__':
    GraphApp().run()
