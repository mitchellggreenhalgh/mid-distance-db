import sqlite3
import os
import pandas as pd
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from glob import glob
from datetime import date, datetime, timedelta
from shutil import copyfile


class MidDistanceDB:

    def __init__(self, title, db_name = 'middistanceDB_master.db'):
        self.title = title
        self.db_name = db_name


    def launch_app(self):
        """Set up and launch a tkinter notebook widget"""

        root = Tk()
        root.title(self.title)

        # Create or backup the database
        try:
            self.maintain_db()
        except:
            messagebox.showinfo(title = 'Something is wrong lmao', message = 'If this shows up you\'re fucked')
        
        # Create Notebook widget
        nb = ttk.Notebook(root)
        nb.pack(fill='both', expand=1)
    
        # region <800m Frame>
        frame_800 = ttk.Frame(nb, padding = '3 3 12 12')

        def upload_file_800(db_name = self.db_name):
            filename = filedialog.askopenfilename()
            upload_confirmation_800.set(f'Selected file: {filename}')

            data = pd.read_csv(filename)
            

            for row in range(len(data)):
                try:    
                    insert_data = tuple(data.iloc[row])

                    insert_query = '''
                        INSERT INTO splits_800m (
                            athlete,
                            first_400,
                            second_400,
                            total_time_sec,
                            split_ratio
                        ) VALUES (?, ?, ?, ?, ?)
                        '''
                    
                    mid_distance_db = sqlite3.connect(self.db_name)
                    cursor = mid_distance_db.cursor()
                    cursor.execute(insert_query, insert_data)
                    mid_distance_db.commit()
                    mid_distance_db.close()
                    
                except:
                    mid_distance_db.close()
                
            else:
                submit_confirmation_800.set(f'Successfully submitted {filename} to {db_name}')


        ttk.Button(frame_800, text = 'Upload File', command = upload_file_800).grid(column = 1, row = 0, sticky = (W, E))

        upload_confirmation_800 = StringVar()
        ttk.Label(frame_800, textvariable = upload_confirmation_800).grid(column = 1, row = 1, sticky = (N, S, E, W))

        submit_confirmation_800 = StringVar()
        ttk.Label(frame_800, textvariable = submit_confirmation_800).grid(column = 1, row = 2, sticky = (N, S, E, W))

        # endregion

        # region <400m frame>

        frame_400 = ttk.Frame(nb, padding = '3 3 12 12')

        def upload_file_400(db_name = self.db_name):
            filename = filedialog.askopenfilename()
            upload_confirmation_400.set(f'Selected file: {filename}')

            data = pd.read_csv(filename)
            

            for row in range(len(data)):
                try:    
                    insert_data = tuple(data.iloc[row])

                    insert_query = '''
                        INSERT INTO splits_400m (
                            athlete,
                            first_200,
                            second_200,
                            total_time_sec,
                            split_ratio
                        ) VALUES (?, ?, ?, ?, ?)
                        '''
                    
                    mid_distance_db = sqlite3.connect(self.db_name)
                    cursor = mid_distance_db.cursor()
                    cursor.execute(insert_query, insert_data)
                    mid_distance_db.commit()
                    mid_distance_db.close()
                    
                except:
                    mid_distance_db.close()
                
            else:
                submit_confirmation_400.set(f'Successfully submitted {filename} to {db_name}')


        ttk.Button(frame_400, text = 'Upload File', command = upload_file_400).grid(column = 1, row = 0, sticky = (W, E))

        upload_confirmation_400 = StringVar()
        ttk.Label(frame_400, textvariable = upload_confirmation_400).grid(column = 1, row = 1, sticky = (N, S, E, W))

        submit_confirmation_400 = StringVar()
        ttk.Label(frame_400, textvariable = submit_confirmation_400).grid(column = 1, row = 2, sticky = (N, S, E, W))

        # endregion

        nb.add(frame_800, text = '800m Database')
        nb.add(frame_400, text = '400m Database')

        root.mainloop()
        

    def maintain_db(self):
        """Create a database or back up the current database"""

        files = glob('*.db')

        # If there's no existing db, make one, else backup the existing one
        if len(files) == 0:
            self.create_db()
        else:
            self.backup_db()


    def create_db(self):
        """Create a new MidDistance DB if there isn't one in the working directory"""

        new_db = sqlite3.connect(self.db_name)
        new_connection = new_db.cursor()

        # TODO: 800m table
        new_connection.execute('''
                            CREATE TABLE splits_800m (
                               athlete TEXT,
                               first_400 REAL,
                               second_400 REAL,
                               total_time_sec REAL,
                               split_ratio REAL,
                               PRIMARY KEY (athlete, first_400, second_400, total_time_sec, split_ratio)
                               )
                            ''')
        
        new_connection.execute('''
                               CREATE TABLE splits_400m (
                                athlete TEXT,
                               first_200 REAL,
                               second_200 REAL,
                               total_time_sec REAL,
                               split_ratio REAL,
                               PRIMARY KEY (athlete, first_200, second_200, total_time_sec, split_ratio)
                               )
                               ''')
        
        new_db.commit()
        new_db.close()
    

    def backup_db(self):
        """Create a backup of an exiting DB if there hasn't been a backup made in the last 30 days"""

        current_db = self.db_name
        now = datetime.now()
        
        backup_files = glob('backup_DBs/backup*.db')
        backup_period = timedelta(days = 30)
        backup_db_name = 'backup_DBs/backup_middistanceDB_' + str(date.today()) + '.db'
        
        timestamps = [datetime.fromtimestamp(os.path.getctime(db)) for db in backup_files]
        time_since_backup = [now - tmstmp for tmstmp in timestamps]

        if not any(time < backup_period for time in time_since_backup):
            copyfile(current_db, backup_db_name)
            messagebox.showinfo(title = 'Database Maintenance', message = 'New backup created.')
        else:
            messagebox.showinfo(title = 'Database Maintenance', message = 'Recent backup found.')


if __name__ == '__main__':
    MidDistanceDB(title = 'Mid-Distance Database Entry Tool').launch_app()

