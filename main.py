from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
from kivy.graphics import Ellipse, Color, Rectangle
from kivy.uix.label import Label
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
import colorsys
import matplotlib.pyplot as plt
from kivy_garden.graph import Graph, MeshLinePlot
from color_wheel import ColorPickerApp
from circular_button import CircularButtonApp
from math import sin
import websockets
import asyncio
from send_audio import AudioStreamingService
class StickyNavBarApp(App):
    async def connect_to_websocket_server(self):
        """

        :return:
        """
        # Modify these credentials with your own
        username = "your_phone_username"
        password = "your_phone_password"

        uri = f"ws://your_server_ip:8765"  # Replace with your server details
        self.websocket = await websockets.connect(uri)

        # Send authentication credentials to the server
        await self.websocket.send(f"{username}:{password}")

        while True:
            response = await self.websocket.recv()
            # Process and handle the received data as needed
            # response will be what comes back
            # this will be what jarvis says

    def build(self):
        """

        :return: returns the boxlayout of the whole app
        """
        # Websocket stuff
        # asyncio.ensure_future(self.connect_to_websocket_server())
        self.service = AudioStreamingService('')
        self.service.start()




        # Create visual aspects of app
        self.root = BoxLayout(orientation='vertical')

        self.content_area = Label(text="Select a menu item to see content.")
        # Create the navigation bar
        nav_bar = BoxLayout(orientation='horizontal', size_hint=(1, None), height=50)
        home_button = Button(text='Home')
        home_button.bind(on_press=self.show_home_content)
        camera_button = Button(text='Camera')
        camera_button.bind(on_press=self.show_camera_content)
        services_button = Button(text='Pws')
        services_button.bind(on_press=self.show_pws_content)
        contact_button = Button(text='Color')
        contact_button.bind(on_press=self.show_color_content)
        graph_button = Button(text='Graphs')
        graph_button.bind(on_press=self.show_graph_content)

        # Create the content area
        self.content = ScrollView()
        self.content_label = self.content_area

        # Add widgets to the navigation bar
        nav_bar.add_widget(home_button)
        nav_bar.add_widget(camera_button)
        nav_bar.add_widget(services_button)
        nav_bar.add_widget(contact_button)
        nav_bar.add_widget(graph_button)

        # Add the navigation bar and content to the root layout
        self.root.add_widget(nav_bar)
        self.content.add_widget(self.content_label)
        self.root.add_widget(self.content)

        return self.root

    def show_home_content(self, instance):

        new_content_label = Label(text="Select a menu item to see content.")
        self.update_content_content_label(new_content_label)

    def show_camera_content(self, instance):
        camera_big_div = BoxLayout(orientation='vertical', size_hint=(1, None), height=1000)

        # Create the content area (text or image)
        camera_box_2 = BoxLayout(orientation='horizontal', size_hint=(1, None), height=500)
        new_content_label = Label(text="Learn more about us in the About section.", height=500)
        camera_box_2.add_widget(new_content_label)
        camera_big_div.add_widget(camera_box_2)

        # Create the buttons box
        buttons_box = BoxLayout(orientation='horizontal', size_hint=(1, None), height=200)
        save_10_min_button = Button(text='Save last 10 minutes')
        save_10_min_button.bind(on_press=self.save_10_mins_camera)
        speak_button = Button(text='Speak')
        speak_button.bind(on_press=self.speak_to_computer)
        buttons_box.add_widget(save_10_min_button)
        buttons_box.add_widget(speak_button)
        buttons_box.pos_hint = {'bottom': 1}
        camera_big_div.add_widget(buttons_box)

        # Update the content_label with the camera content
        self.update_content_content_label(camera_big_div)


    def on_stop(self):
        # Close the WebSocket connection when the app is closed
        if self.websocket:
            self.websocket.close()


    def update_content_content_label(self, new_content_label):
        # Remove the old content_label
        self.content.remove_widget(self.content_label)

        # Replace it with the new content_label
        self.content_label = new_content_label
        self.content.add_widget(self.content_label)


    def show_pws_content(self, instance):
        pws_big_div = BoxLayout(orientation='vertical', size_hint=(1, None), height=1000)

        # Create the content area (text or image)
        camera_box_2 = BoxLayout(orientation='horizontal', size_hint=(1, None), height=200)
        new_content_label = Label(text="Search box", height=200)
        camera_box_2.add_widget(new_content_label)
        pws_big_div.add_widget(camera_box_2)

        # Create the buttons box
        pws_list_box = BoxLayout(orientation='horizontal', size_hint=(1, None), height=200)

        pws_list = [{'title': 'google', 'username': 'a@a.com', 'password': 'pw', 'email': 'a@a.com', 'other_info': 'idk'}]
        for pw in pws_list:
            # pws is a dictonary with username, email, password, other info, title,
            username = pw['username']
            email = pw['email']
            password = pw['password']
            title = pw['title']
            other_info = pw['other_info']
            single_pw = Label(text=f"Title: {title}, username: {username}, email: {email}"
                                   f", password: {password}, 'other_info: {other_info}", height=200)
            pws_list_box.add_widget(single_pw)

        # buttons_box.add_widget(save_10_min_button)
        # buttons_box.add_widget(speak_button)
        # buttons_box.pos_hint = {'bottom': 1}
        pws_big_div.add_widget(pws_list_box)

        # Update the content_label with the camera content
        self.update_content_content_label(pws_big_div)

    def show_color_content(self, instance):
        color_big_div = BoxLayout(orientation='vertical', size_hint=(1, None), height=2000)

        # Create the content area (text or image)
        main_color_box = BoxLayout(orientation='horizontal', size_hint=(1, None), height=1000)
        # Create a colored background

        middle_wheel_box = ColorPickerApp()
        on_off_but = CircularButtonApp()


        color_big_div.add_widget(middle_wheel_box.build())
        color_big_div.add_widget(on_off_but.build())
        # main_color_box.add_widget(right_wheel_box)

        # Create the buttons box

        self.update_content_content_label(color_big_div)

    def create_graph_temp(self, plot_points):
        """

        :param plot_points: this will be a list of plot points
        :return: returns the object of the graph to add as a widget
        """
        graph = Graph(xlabel='Time in seconds', ylabel='Temp in C', x_ticks_minor=5,
                      x_ticks_major=30, y_ticks_major=5,
                      y_grid_label=True, x_grid_label=True, padding=5,
                      x_grid=True, y_grid=True, xmin=-0, xmax=120, ymin=0, ymax=100)
        plot = MeshLinePlot(color=[1, 0, 0, 1])
        plot.points = plot_points
        graph.add_plot(plot)
        return graph


    def create_graph_usage(self, plot_points):
        """

        :param plot_points: this will be a list of plot points
        :return: returns the object of the graph to add as a widget
        """
        graph = Graph(xlabel='Time in seconds', ylabel='Usage %', x_ticks_minor=5,
                      x_ticks_major=30, y_ticks_major=5,
                      y_grid_label=True, x_grid_label=True, padding=5,
                      x_grid=True, y_grid=True, xmin=-0, xmax=120, ymin=0, ymax=100)
        plot = MeshLinePlot(color=[1, 0, 0, 1])
        plot.points = plot_points
        graph.add_plot(plot)
        return graph


    def show_graph_content(self, instance):
        graph_big_div = BoxLayout(orientation='vertical', size_hint=(1, None), height=3000)

        cpu_data = [(i, 30 + i) for i in range(60)]  # Start at x=0, y=30 and increase x by 1 for each point

        # Ensure that the y-values (temperatures) do not exceed the maximum y-value of 100
        cpu_data = [(x, min(100, y)) for x, y in cpu_data]
        graph = self.create_graph_temp(cpu_data)
        graph_gpu_temp = self.create_graph_temp(cpu_data)
        # Create the content area (text or image)
        graph_usage = self.create_graph_usage(cpu_data)
        graph_usage_gpu = self.create_graph_usage(cpu_data)
        graph_usage_mem = self.create_graph_usage(cpu_data)
        graph_usage_net = self.create_graph_usage(cpu_data)

        cpu_usage_box = BoxLayout(orientation='vertical', size_hint=(1, None), height=500)
        cpu_usage_widg = Label(text="CPU Usage", height=50)
        cpu_usage_box.add_widget(cpu_usage_widg)
        cpu_usage_box.add_widget(graph_usage)

        gpu_usage_box = BoxLayout(orientation='vertical', size_hint=(1, None), height=500)
        gpu_usage_widg = Label(text="GPU Usage", height=50)
        gpu_usage_box.add_widget(gpu_usage_widg)
        gpu_usage_box.add_widget(graph_usage_gpu)

        mem_usage_box = BoxLayout(orientation='vertical', size_hint=(1, None), height=500)
        mem_usage_widg = Label(text="MEMORY Usage", height=50)
        mem_usage_box.add_widget(mem_usage_widg)
        mem_usage_box.add_widget(graph_usage_mem)

        net_usage_box = BoxLayout(orientation='vertical', size_hint=(1, None), height=500)
        net_usage_widg = Label(text="NETWORK Usage", height=50)
        net_usage_box.add_widget(net_usage_widg)
        net_usage_box.add_widget(graph_usage_net)

        cpu_temp_box = BoxLayout(orientation='vertical', size_hint=(1, None), height=500)
        cpu_temp_widg = Label(text="CPU Temperature", height=50)
        cpu_temp_box.add_widget(cpu_temp_widg)
        cpu_temp_box.add_widget(graph)

        gpu_temp_box = BoxLayout(orientation='vertical', size_hint=(1, None), height=500)
        gpu_temp_widg = Label(text="GPU Temperature", height=50)
        gpu_temp_box.add_widget(gpu_temp_widg)
        gpu_temp_box.add_widget(graph_gpu_temp)
        # graph_big_div.add_widget(camera_box_2)

        # Create the buttons box

        graph_big_div.add_widget(cpu_usage_box)
        graph_big_div.add_widget(gpu_usage_box)
        graph_big_div.add_widget(mem_usage_box)
        graph_big_div.add_widget(net_usage_box)
        graph_big_div.add_widget(cpu_temp_box)
        graph_big_div.add_widget(gpu_temp_box)
        # Update the content_label with the camera content
        self.update_content_content_label(graph_big_div)


    def save_10_mins_camera(self, idk):

        pass


    def speak_to_computer(self, idk):

        pass


if __name__ == '__main__':
    StickyNavBarApp().run()
