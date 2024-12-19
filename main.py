from kivy.lang import Builder
from kivy.properties import StringProperty

from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from datetime import datetime



class HowMuchI(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Purple"
        self.theme_cls.theme_style = "Dark"
        return Builder.load_file('HowMuchI.kv')

    def on_save_pressed(self, ):
        pass
    
    def on_checkbox_active(self, checkbox,value):
        if value:
            print(f'The {str(self.root.ids.esercizio)} is active')
        else:
            print('The checkbox', checkbox, 'is inactive')
        
    def on_complex_checkbox_active(self,checkbox,question):
        pass
HowMuchI().run()