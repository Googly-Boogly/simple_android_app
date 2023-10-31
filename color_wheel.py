from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.colorpicker import ColorPicker
from kivy.uix.label import Label

class ColorPickerApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')

        # Create a ColorPicker widget
        color_picker = ColorPicker()
        color_picker.bind(color=self.on_color)

        # Label to display the selected color
        self.color_label = Label(text='Selected Color: [color=#000000][/color]', markup=True)

        layout.add_widget(color_picker)
        layout.add_widget(self.color_label)

        return layout

    def on_color(self, instance, value):
        # Update the label with the selected color
        hex_color = '#{0:02X}{1:02X}{2:02X}'.format(
            int(value[0] * 255),
            int(value[1] * 255),
            int(value[2] * 255)
        )
        self.color_label.text = f'Selected Color: [color={hex_color}]{hex_color}[/color]'

if __name__ == '__main__':
    ColorPickerApp().run()
