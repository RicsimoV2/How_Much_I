from kivy.lang import Builder
from kivy.properties import StringProperty

from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.dialog import (
    MDDialog,
    MDDialogIcon,
    MDDialogHeadlineText,
    MDDialogSupportingText
)
from kivymd.uix.pickers import MDModalInputDatePicker, MDModalDatePicker
from kivy.metrics import dp
from kivy.clock import Clock

from datetime import datetime, timedelta
import csv
import os
import pandas as pd
import numpy as np



class HowMuchI(MDApp):
     
    def build(self):
        self.list_id = ['dormire','pisolino','esercizio_fisico','cacca','ridere',
                        'pianto','pianto_gioia','pianto_tristezza','pianto_rabbia',
                        'pianto_occhilucidi','sesso','pizza','amici','alcol',
                        'alcol_sobrio','alcol_brillo','alcol_devastato','videogames',
                        'stress','fumo']
        self.mask_boolean = [False,True,True,False,True,True,True,True,True,True,False,True,True,True,True,True,True,True,True,False]
        self.create_csv_file()
        self.today = datetime.today().strftime("%Y-%m-%d")
        self.yesterday = (datetime.today() - timedelta(days=1)).strftime("%Y-%m-%d")
        self.theme_cls.primary_palette = "Purple"
        self.theme_cls.theme_style = "Dark"
        # Carica il layout KV
        root = Builder.load_file('HowMuchI.kv')
        
        return root
    
    
    
    
    def on_start(self):
        # Chiama load_previous_data quando la root è popolata
        self.load_previous_data(self.yesterday)
        self.count_streak()
    
    def choose_data(self,):
        pass
    
    def get_output(self,widget,data_name,*args):
        # try:
        #     print(data_name,widget.value)
        # except:
        #     print(data_name,widget.active)
        pass

    def show_date_picker(self,*args):
        date_dialog = MDModalDatePicker(   mark_today=True,
        min_date=datetime.strptime('2023-01-01', "%Y-%m-%d").date(),
        max_date=datetime.today().date()
        )
        date_dialog.bind(on_edit=self.on_edit)
        # date_dialog.bind(on_select_day=self.on_select_day)
        date_dialog.bind(on_cancel=self.on_cancel)
        date_dialog.bind(on_ok=self.on_ok)
        date_dialog.open()

    def show_modal_input_date_picker(self, *args):
        def on_edit(*args):
            date_dialog.dismiss()
            Clock.schedule_once(self.show_date_picker, 0.2)

        date_dialog = MDModalInputDatePicker()
        date_dialog.bind(on_edit=on_edit)
        date_dialog.bind(on_cancel=self.on_cancel)
        date_dialog.bind(on_ok=self.on_ok)
        date_dialog.open()

    def on_ok(self, instance_date_picker):
        instance_date_picker.dismiss()
        self.data=(instance_date_picker.get_date()[0]).strftime("%Y-%m-%d")
        self.load_previous_data(self.data)

    def on_cancel(self, instance_date_picker):
        instance_date_picker.dismiss()

    def on_edit(self, instance_date_picker):
        instance_date_picker.dismiss()
        Clock.schedule_once(self.show_modal_input_date_picker, 0.2)

    def on_select_day(self, instance_date_picker, number_day):
        instance_date_picker.dismiss()
        self.data=(instance_date_picker.get_date()[0]).strftime("%Y-%m-%d")
        self.load_previous_data(self.data)
           
    def obtain_data_vector(self, *args):
        self.values = []
        self.values.append(self.data)
        for i,label in enumerate(self.list_id):
            if self.mask_boolean[i]:
                val = self.root.ids[label].active   
            else:
                val = self.root.ids[label].value
                
            self.values.append(val)
            
        saved=True
        self.values.append(saved)    
        print(self.values)
        self.write_csv(self.values)
            
    def update_title(self,data):
        self.root.ids['title'].text = f"Cosa hai fatto il {data} ?"
        
    def write_csv(self,data_vector):
        # Nome del file CSV
        csv_file = self.filename
        
        # Carica il file CSV in un DataFrame
        df = pd.read_csv(csv_file)
        
        # Estrai la data dal vettore
        date_to_update = data_vector[0]
        
        # Controlla se la data esiste nel DataFrame
        if date_to_update in df['data'].values:
            # Aggiorna la riga corrispondente
            df.loc[df['data'] == date_to_update] = data_vector
        else:
            # Aggiungi una nuova riga
            new_row = pd.DataFrame([data_vector], columns=df.columns)
            df = pd.concat([df, new_row], ignore_index=True)
        
        # Salva il DataFrame aggiornato di nuovo nel file CSV
        df.to_csv(csv_file, index=False)
        
        self.count_streak()

        print(f"Riga aggiornata o aggiunta per la data {date_to_update}.")

    def load_previous_data(self,data):
        self.data=data
        data_object = datetime.strptime(self.data, "%Y-%m-%d")
        
        if data_object > datetime.today():
            title = 'Data non disponibile!'
            error_message = f'Il giorno {self.data} è nel futuro.'
            self.show_error_popup(title,error_message)
            csv_file = self.filename 
            df = pd.read_csv(csv_file)          
            self.data = self.yesterday
        
        else:
            if data_object.year < datetime.now().year:
                filename = f"data_{self.data_object.year}.csv"
                csv_file = filename
            else:
                csv_file = self.filename
            # Carica il file CSV in un DataFrame
            try:
                df = pd.read_csv(csv_file)
            except:
                title = 'Dati non disponibili!'
                error_message = f'Non sono stati trovati dati per il giorno {self.data}.'
                self.show_error_popup(title,error_message)
                csv_file = self.filename 
                df = pd.read_csv(csv_file)          
                self.data = self.yesterday
            
        self.update_title(self.data)    
        # Controlla se la data esiste nel DataFrame
        data_vector = df.loc[df['data'] == self.data]
        row = data_vector.iloc[0]
        for i,label in enumerate(self.list_id):
            
            if self.mask_boolean[i]:
                self.root.ids[label].active = bool(row.iloc[i+1])
            else:
                self.root.ids[label].value = float(row.iloc[i+1])
            print(f"Updating widget {label} with value {row.iloc[i+1]}")

    def show_error_popup(self, title, error_message):
        MDDialog(
            # ----------------------------Icon-----------------------------
            MDDialogIcon(
                icon="allert-circle-outline",
            ),
            # -----------------------Headline text-------------------------
            MDDialogHeadlineText(
                text=title,
            ),
            # -----------------------Supporting text-----------------------
            MDDialogSupportingText(
                text=error_message,
            )
        ).open()

    def enable_other_checkbox(self,switch,*args):
        """
        Gestisce i gruppi di checkbox separatamente.
        """
        # Gestione del primo gruppo
        if switch == self.root.ids.pianto:
            if self.root.ids.pianto.active:  # Primo checkbox del primo gruppo attivato
                self.root.ids.pianto_gioia.disabled = False
                self.root.ids.pianto_tristezza.disabled = False
                self.root.ids.pianto_rabbia.disabled = False
                self.root.ids.pianto_occhilucidi.disabled = False
            else:  # Primo checkbox del primo gruppo disattivato
                self.root.ids.pianto_gioia.disabled = True
                self.root.ids.pianto_gioia.active = False
                self.root.ids.pianto_tristezza.disabled = True
                self.root.ids.pianto_tristezza.active = False                
                self.root.ids.pianto_rabbia.disabled = True                
                self.root.ids.pianto_rabbia.active = False
                self.root.ids.pianto_occhilucidi.disabled = True
                self.root.ids.pianto_occhilucidi.active = False   

        elif switch == self.root.ids.alcol:
            if self.root.ids.alcol.active:  # Primo checkbox del primo gruppo attivato
                self.root.ids.alcol_sobrio.disabled = False
                self.root.ids.alcol_brillo.disabled = False
                self.root.ids.alcol_devastato.disabled = False
            else:  # Primo checkbox del primo gruppo disattivato
                self.root.ids.alcol_sobrio.disabled = True
                self.root.ids.alcol_sobrio.active = False
                self.root.ids.alcol_brillo.disabled = True
                self.root.ids.alcol_brillo.active = False                
                self.root.ids.alcol_devastato.disabled = True                
                self.root.ids.alcol_devastato.active = False
                
    def create_csv_file(self):
        # Nome del file basato sull'anno corrente
        current_year = datetime.now().year 
        self.filename = f"data_{current_year}.csv"

        # Intestazioni delle colonne
        headers = ['data']
        headers += self.list_id
        headers += ['saved']

        # Controlla se il file esiste già
        if os.path.exists(self.filename):
            print(f"The file '{self.filename}' already exists. No action taken.")
            return

        # Calcola il numero di giorni nell'anno corrente
        start_date = datetime(current_year, 1, 1)
        end_date = datetime(current_year + 1, 1, 1)  # Primo giorno dell'anno successivo
        num_days = (end_date - start_date).days

        # Valori predefiniti per le colonne
        default_values = [0., 'False', 'False', 0., 'False', 'False', 'False', 'False', 'False', 'False', 0., 'False', 'False', 'False', 'False', 'False', 'False', 'False', 'False', 0.,'False']

        # Genera i dati per ogni giorno
        rows = []
        for day in range(num_days):
            date = start_date + timedelta(days=day)
            rows.append([date.strftime("%Y-%m-%d")] + default_values)

        # Scrive il file CSV
        with open(self.filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(headers)
            writer.writerows(rows)

        print(f"CSV file '{self.filename}' with {len(headers)} columns and {num_days} rows created successfully.")

    def count_streak(self):
        csv_file = self.filename 
        df = pd.read_csv(csv_file)
        saves = df.iloc[:, -1].to_numpy()
        yesterday = datetime.strptime(self.yesterday, "%Y-%m-%d")
        numero_giorno = int(( yesterday- datetime(yesterday.year, 1, 1)).days)
        i = numero_giorno
        streak = 0
        while saves[i] and i<=numero_giorno:
            streak += 1
            i -=1
        self.root.ids['streak_salvataggi_numero'].text = str(streak)
                         
HowMuchI().run()