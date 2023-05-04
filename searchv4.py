import os
import tkinter as tk
from tkinter import filedialog
from shutil import copy
from tkinter import messagebox
import subprocess
from tkinter import ttk
import tkinter.font as tkFont


search_folder = ""
copy_folder = ""
result_list = []
i = 0

def search_files():
    i = 0
    

    global search_folder, copy_folder, result_list, filename, file_path, keyword
    os.chdir(search_folder)
    keyword = keyword_entry.get().upper()
    # result_text.delete(1.0, tk.END)  # Clear the previous search result
    found = False

    for root, dirs, files in os.walk(search_folder):
        for filename in files:
            # Check if the file is a text file
            
            if filename.endswith('.txt'):
                
            # Open the file for reading
                file_path = os.path.join(root, filename)
                with open((file_path), 'r') as f:
                    # Read the contents of the file
                    
                    contents = f.read()
                    
                    # Check if the string exists in the contents
                    if keyword in contents:
                        found = True
                        with open(file_path, 'r') as source_file:
                            for line in source_file:
                                if keyword in line:

                                    result_list.append(line)
                                    
                  
                if found:
                    break
            if found:
                break
    if not found:
        result_text.insert(tk.END, f"No records were found.\n")  
    
    if found:
        result_text.insert(tk.END, f"Records found, please check in new window.\n")        
        result_view()
        result_list = []


def copy_file(file):
    global copy_folder
    if not copy_folder:
        return
    os.makedirs(copy_folder, exist_ok=True)
    dest = os.path.join(copy_folder, os.path.basename(file))
    fileformat = "txt"
    if os.path.exists(os.path.join(copy_folder, os.path.basename(file))):
        if messagebox.askyesno("File Found", f"File name: {file} already exists. Do you want to overwrite the file?"):
            copy(file, dest)
    copy(file, dest)

description = ("""To use the program: 
               1. Select the source folder. This is where the files to be searched are found.
               2. Select the folder where the working file is to be stored. The filename will be "Combine"
               3. Type the name of the record being searched.
               4. Once you hit search, you will be prompted to write the item to the combined document.
               5. Once you have set the Output folder, you can open the text document.

               This is a work in progress. There will be errors.
""")


root = tk.Tk()
root.title("Search Text Files")
root.geometry("600x800")


desc_label = tk.Label(root, text=description)
desc_label.pack()

def update_gui():
    # update the GUI
    root.update_idletasks()







search_folder_label = tk.Label(root, text="Search Folder:")
search_folder_label.pack()

search_folder_text = tk.Text(root, height=1)
search_folder_text.pack()

def browse_folder():
    global search_folder
    search_folder = filedialog.askdirectory(title="Select Folder")
    search_folder_text.delete(1.0, tk.END)
    search_folder_text.insert(tk.END, search_folder)

browse_folder_button = tk.Button(root, text="Select Search Folder", command=browse_folder)
browse_folder_button.pack(padx= 10, pady= 10)

copy_folder_label = tk.Label(root, text="Output Location:")
copy_folder_label.pack()

copy_folder_text = tk.Text(root, height=1)
copy_folder_text.pack()

def browse_copy_folder():
    global copy_folder
    copy_folder = filedialog.askdirectory(title="Select Folder to Copy Files")
    copy_folder_text.delete(1.0, tk.END)
    copy_folder_text.insert(tk.END, copy_folder)
    if copy_folder:
        open_file_button.config(state='normal')
        # Do something with the folder path
    else:
        open_file_button.config(state='disabled')

browse_copy_folder_button = tk.Button(root, text="Set Output Folder", command=browse_copy_folder)
browse_copy_folder_button.pack(padx= 10, pady= 5)

def open_file():
    filename = os.path.join(copy_folder, os.path.basename("combine.txt"))
    if filename:
        subprocess.Popen(['notepad.exe', filename])

open_file_button = tk.Button(root, text="Open File", command= open_file, state='disabled')
open_file_button.pack(padx= 10, pady= 10)

# Frame for Search Box
keyword_label = tk.Label(root, text="Keyword to Search:")
keyword_label.pack()

frame = tk.Frame(root)
frame.pack(side=tk.TOP)
keyword_entry = tk.Entry(frame)
search_button = tk.Button(frame, text="Search", command=search_files)
keyword_entry.pack(side=tk.LEFT)
search_button.pack(side=tk.LEFT, padx= 5)
keyword_entry.bind('<Return>', lambda event: search_files())

def add_record(item):
     if messagebox.askyesno("File Found", f"Record found in {filename}. Do you want to copy the record?"):
        
        
        if not os.path.exists(os.path.join(copy_folder, os.path.basename("combine.txt"))):
            with open(os.path.join(copy_folder, os.path.basename("combine.txt")), 'a') as f:
                f.write('ACCOUNT_REF,SURNAME,FORENAME,TRN,CR_CONTRACT_NUMBER,DB_CONTRACT_NUMBER,TRANSACTION_TYPE,TRANSACTION_DATE,SETTLEMENT_DATE, CR_ISIN_CODE,DB_ISIN_CODE,CR_ISIN_PRICE,DB_ISIN_PRICE,CR_CASH_OBLIGATION,DB_CASH_OBLIGATION,CR_NOMINAL_VALUE,DB_NOMINAL_VALUE, CR_SECURITY_MARKET_VALUE,DB_SECURITY_MARKET_VALUE,CR_MARGIN,DB_MARGIN,CASH_CURRENCY,EXCHANGE_RATE,INTEREST_RATE,MATURITY_DATE,REMARKS\n')
        
        if os.path.exists(os.path.join(copy_folder, os.path.basename("combine.txt"))):
            with open(os.path.join(copy_folder, os.path.basename("combine.txt")), 'a') as destination_file:
                
                destination_file.write(item)
                result_text.insert(tk.END, f"Record successfully added: {keyword}\n")
                result_text.insert(tk.END, f"---------------------------------------\n")
                result_window.destroy()

            # newname = keyword
            # copy_file(filename)
        else:
            result_text.insert(tk.END, f"---------------------------------------\n")        
                


def result_view():
    
    # create a new button
    global result_window
    result_window = tk.Toplevel(root)
    result_window.title("Search Results")  
    result_window.geometry("700x400")

    update_gui()
    

    data = [
    ["ITEM", "ACCOUNT_REF", "SURNAME" ,"FORENAME","TRN","CR_CONTRACT_NUMBER","DB_CONTRACT_NUMBER","TRANSACTION_TYPE","TRANSACTION_DATE","SETTLEMENT_DATE", "CR_ISIN_CODE","DB_ISIN_CODE","CR_ISIN_PRICE","DB_ISIN_PRICE","CR_CASH_OBLIGATION","DB_CASH_OBLIGATION","CR_NOMINAL_VALUE","DB_NOMINAL_VALUE", "CR_SECURITY_MARKET_VALUE","DB_SECURITY_MARKET_VALUE","CR_MARGIN","DB_MARGIN","CASH_CURRENCY","EXCHANGE_RATE","INTEREST_RATE","MATURITY_DATE","REMARKS"],
    
]
    tree = ttk.Treeview(result_window, columns=data[0], show="headings")
    
    


    for col in data[0]:
        tree.heading(col, text=col)

        tree.column(col, width=tkFont.Font().measure(col))

        
    itemlist = []
    i = 0
    c = 0
    # add the data rows
    for x in result_list:
        i+=1
        value = x.split(",")
        value.insert(0, i)
        tree.insert("", tk.END, values=value)
        itemlist.append(x)


    btnframe = tk.Frame(result_window)
    btnframe.pack(side=tk.TOP)
    for n in itemlist:
        c += 1
        btn_name = "Record " + str(c)
        button = tk.Button(btnframe, text= btn_name, command = lambda v = n : add_record(v) )
        button.pack(side=tk.LEFT, padx= 2, pady= 5)



    for p, col in enumerate(tree["columns"]):
        tree.column(col, width=150)

    tree.column('ITEM', width=40)


    # pack the treeview widget

    # Create a Treeview widget

    hscrollbar = ttk.Scrollbar(result_window, orient='horizontal', command=tree.xview)
    hscrollbar.pack(side='bottom', fill='x')
    tree.configure(xscrollcommand=hscrollbar.set)


    # Display the table
    tree.pack(fill="both", expand=True)


    root.after(100, update_gui)  
    result_window.after(100, update_gui)



# clear_button = tk.Button(root, text="View", command=result_view)
# clear_button.pack(padx= 10, pady= 20)

def clear_result():
    result_text.delete(1.0, tk.END)  # Clear the previous search result

clear_button = tk.Button(root, text="Clear Results Screen", command=clear_result)
clear_button.pack(padx= 10, pady= 20)

result_label = tk.Label(root, text="Search Result:")
result_label.pack()

result_text = tk.Text(root)
result_text.pack()



root.mainloop()
