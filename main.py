from tkinter import ttk, filedialog, messagebox
import tkinter as tk
import sv_ttk, os, time, zipfile, threading

root = tk.Tk()
root.geometry('700x630')
root.title('SV Mods Manager')
sv_ttk.set_theme("dark")


def findSVFolder():
    paths=[ 'C:\Program Files (x86)\Steam\steamapps\common\Stardew Valley',
            'C:\Program Files (x86)\Steam\steamapps\common\Stardew Valley',
            'C:\Program Files (x86)\Steam\steamapps\common\Stardew Valley',
            'D:\SteamLibrary\steamapps\common\Stardew Valley'
            'E:\SteamLibrary\steamapps\common\Stardew Valley'
    ]
    for path in paths:
        if os.path.exists(f'{path}\smapi-internal') == True:
            svFolder.config(state='normal')
            svFolder.delete(0, 'end')
            svFolder.insert(0, f'{path}\Mods')
            svFolder.configure(state='disabled')

            consoleTextBox.config(state='normal')
            consoleTextBox.delete('1.0', 'end')
            consoleTextBox.insert('1.0', f'Found {path}')
            consoleTextBox.config(state='disable')
            break



def selectSVFolder():
    Folder = filedialog.askdirectory(title='Select Stardew Valley folder...')
    if Folder != '':
        svFolder.config(state='normal')
        svFolder.delete(0, 'end')
        svFolder.insert(0, f'{Folder}\Mods')
        svFolder.configure(state='disabled')
        if os.path.exists(f'{Folder}\smapi-internal') != True:
            messagebox.showinfo('Info', 'It looks like the directory you just selected does not currently have SMAPI installed. Just a reminder.')

def selectInputFile():
    global num_mods
    if 'num_mods' not in globals():
        num_mods = 0
    Files = filedialog.askopenfilenames(title='Select file(s)...', filetypes = (("Zip files","*.zip"),("All files","*.*")))
    for File in Files:
        num_mods+=1
        modLstBox.insert('', 'end', iid=num_mods, values=(num_mods, os.path.split(File)[1], File))

def installMods():
    modLstInstallButton.config(state='disable')
    selectsvFolderButton.config(state='disable')
    browserFile.config(state='disable')

    def installModsProcess():
        for order_num in range(1,num_mods+1):
            modLstBox.selection_set(order_num)
            select_item = modLstBox.selection()

            consoleTextBox.config(state='normal')
            consoleTextBox.delete('1.0', 'end')
            consoleTextBox.insert('1.0', f'Installing {modLstBox.item(select_item).get("values")[1]}')
            consoleTextBox.config(state='disable')

            with zipfile.ZipFile(modLstBox.item(select_item).get("values")[2]) as zip_ref:
                zip_ref.extractall(svFolder.get())
            
            time.sleep(1)
            
            #Temp Print
            #print(modLstBox.item(select_item).get("values")[2])
            #Temp Print
        modLstBox.selection_remove(order_num)
        consoleTextBox.config(state='normal')
        consoleTextBox.delete('1.0', 'end')
        consoleTextBox.insert('1.0', 'Done!')
        consoleTextBox.config(state='disable')

        messagebox.showinfo('Info', 'Done.')

        modLstInstallButton.config(state='normal')
        selectsvFolderButton.config(state='normal')
        browserFile.config(state='normal')

    threading.Thread(target=installModsProcess).start()

tab_control = ttk.Notebook(root)

svFolderFrame = ttk.LabelFrame(root, text='Stardew Valley mods folder')
svFolderFrame.pack(fill='x', padx=10, pady=10)
svFolder = ttk.Entry(svFolderFrame, state='disable')
svFolder.pack(side='left', fill='x',expand='True', padx=10, pady=10)

#================Installer================#
installerTab = ttk.Frame(tab_control)
tab_control.add(installerTab, text='Install Mods')

selectsvFolderButton = ttk.Button(svFolderFrame, text='Select SV folder...', command=selectSVFolder)
selectsvFolderButton.pack(side='left', fill='x', padx=10, pady=10)


browserFile = ttk.Button(installerTab, text="Select Zip...", command=selectInputFile)
browserFile.pack(fill='x', expand='False', padx=10, pady=10)

columns = ('stt', 'file_name', 'file_location')

modLstBox = ttk.Treeview(installerTab, columns=columns, show='headings', selectmode='none')

modLstBox.heading('stt', text='STT')
modLstBox.column('stt', minwidth=10, width=40, stretch=False, anchor='center')
modLstBox.heading('file_name', text="Mod file's name")
modLstBox.heading('file_location', text='Location')

modLstBox.pack(fill='x', padx=10, pady=10)

modLstInstallButton = ttk.Button(installerTab, text='Install!', command=installMods)
modLstInstallButton.pack(fill='x', expand='False', padx=10, pady=10)

statusLog = ttk.LabelFrame(installerTab, text='Status')
statusLog.pack(fill='both', expand='False', padx=10, pady=10)
consoleTextBox = tk.Text(statusLog, state="disabled")
consoleTextBox.pack(fill='x', padx=10, pady=10)
consoleTextBox.config(state='normal')
consoleTextBox.insert('1.0', 'Stopped')
consoleTextBox.config(state='disable')

findSVFolder()

#================Manager================#
managerTab = ttk.Frame(tab_control)
tab_control.add(managerTab, text='Manage Mods')

tab_control.pack(fill='both', padx='10', pady='10')

root.mainloop()

