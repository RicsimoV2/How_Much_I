from kivy.lang import Builder
from kivy.properties import StringProperty

from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout

from datetime import datetime, timedelta
import csv
import os
import pandas as pd


class HowMuchI(MDApp):
     
    def build(self):
        self.list_id = ['dormire','pisolino','esercizio_fisico','cacca','ridere',
                        'pianto','pianto_gioia','pianto_tristezza','pianto_rabbia',
                        'pianto_occhilucidi','sesso','pizza','amici','alcol',
                        'alcol_sobrio','alcol_brillo','alcol_devastato','videogames',
                        'stress','fumo']
        self.create_csv_file()
        self.today = datetime.today().strftime("%d %B %Y")
        self.yesterday = (datetime.today() - timedelta(days=1)).strftime("%Y-%m-%d")
        self.title_text = f"Cosa hai fatto ieri ({self.yesterday}) ?"
        self.theme_cls.primary_palette = "Purple"
        self.theme_cls.theme_style = "Dark"
        return Builder.load_file('HowMuchI.kv')
    
    def get_output(self,widget,data_name,*args):
        # try:
        #     print(data_name,widget.value)
        # except:
        #     print(data_name,widget.active)
        pass
            
    def obtain_data_vector(self, *args):
        self.data = []
        self.data.append(self.yesterday)
        for label in self.list_id:
            try:
                val = self.root.ids[label].value
            except:
                val = self.root.ids[label].active
                
            self.data.append(val)
            
        print(self.data)
        self.write_csv(self.data)
            
    
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

        print(f"Riga aggiornata o aggiunta per la data {date_to_update}.")


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
        
        # Controlla se il file esiste già
        if os.path.exists(self.filename):
            print(f"The file '{self.filename}' already exists. No action taken.")
            return
        
        # Calcola il numero di giorni nell'anno corrente
        start_date = datetime(current_year, 1, 1)
        end_date = datetime(current_year + 1, 1, 1)  # Primo giorno dell'anno successivo
        num_days = (end_date - start_date).days
        
        # Genera i dati per ogni giorno
        rows = []
        for day in range(num_days):
            date = start_date + timedelta(days=day)
            rows.append([date.strftime("%Y-%m-%d")] + [""] * (len(headers) - 1))  # Colonna della data più colonne vuote
        
        # Scrive il file CSV
        with open(self.filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(headers)
            writer.writerows(rows)
        
        print(f"CSV file '{self.filename}' with {len(headers)} columns and {num_days} rows created successfully.")
        
                
                         
HowMuchI().run()