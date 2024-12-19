from kivy.lang import Builder
from kivymd.app import MDApp

KV = '''
<Check@MDCheckbox>:
    group: 'group'
    size_hint: None, None
    size: dp(48), dp(48)
    on_active: app.enable_other_checkbox(self, *args)

MDFloatLayout:

    # Primo gruppo
    Check:
        id: first_check
        active: False
        disabled: False
        pos_hint: {'center_x': .3, 'center_y': .7}

    MDCheckbox:
        id: second_check
        active: False
        disabled: True
        size_hint: None, None
        pos_hint: {'center_x': .5, 'center_y': .7}
        size: "48dp", "48dp"

    # Secondo gruppo
    Check:
        id: first_check_2
        active: False
        disabled: False
        pos_hint: {'center_x': .3, 'center_y': .5}

    MDCheckbox:
        id: second_check_2
        active: False
        disabled: True
        size_hint: None, None
        pos_hint: {'center_x': .5, 'center_y': .5}
        size: "48dp", "48dp"
'''

class Example(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Green"
        self.theme_cls.theme_style = "Dark"
        return Builder.load_string(KV)

    def enable_other_checkbox(self, checkbox, value, *args):
        """
        Gestisce i gruppi di checkbox separatamente.
        """
        # Gestione del primo gruppo
        if checkbox == self.root.ids.first_check:
            if self.root.ids.first_check.active:  # Primo checkbox del primo gruppo attivato
                print("First checkbox of first group activated!")
                self.root.ids.second_check.disabled = False
            else:  # Primo checkbox del primo gruppo disattivato
                print("First checkbox of first group deactivated!")
                self.root.ids.second_check.disabled = True
                self.root.ids.second_check.active = False

        # Gestione del secondo gruppo
        if checkbox == self.root.ids.first_check_2:
            if self.root.ids.second_check.active:  # Primo checkbox del secondo gruppo attivato
                print("First checkbox of second group activated!")
                self.root.ids.second_check_2.disabled = False
            else:  # Primo checkbox del secondo gruppo disattivato
                print("First checkbox of second group deactivated!")
                self.root.ids.second_check_2.disabled = True
                self.root.ids.second_check_2.active = False

Example().run()
