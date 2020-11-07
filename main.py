import tkinter as tk
from tkinter import messagebox,filedialog
from threading import Thread, Event

from data import Reader

root = tk.Tk()
root.title('스토어 리뷰 크롤러')
root.geometry('250x150')

#var
limit = tk.IntVar()
no_limit = tk.IntVar()
delay_pages = tk.IntVar()
delay_time = tk.DoubleVar()
FILENAME = []

#command
def add_file():
    filename = filedialog.askopenfilename(initialdir='./list', title='파일 탐색', filetypes=[("text files", "*.txt")])
    filename_label.config(text=f"{filename.split('/')[-1]}")
    FILENAME.append(filename)
    

class Controller(object):
    def __init__(self):
        self.thread = None
        self.stop_thread = Event()

    def scraping(self):
        Reader(self.stop_thread, FILENAME[-1], limit=limit.get(), delay_time=delay_time.get())
        print('크롤링 완료!')
    
    def start(self):
        self.stop_thread.clear()
        self.thread = Thread(target = self.scraping)
        self.thread.start()
        
    def stop(self):
        self.stop_thread.set()
        self.thread.join()
        self.thread = None
        messagebox.showinfo('info', '크롤링 완료!')

#label
filename_label = tk.Label(root, text="")
filename_label.grid(row=0, column=1)

request_label = tk.Label(root, text='요청 파일명:')
request_label.grid(row=0, column=0)

limit_label = tk.Label(root, text='최소 수량')
limit_label.grid(row=1, column=0)

delay_time_label = tk.Label(root, text="딜레이 (초)")
delay_time_label.grid(row=2, column=0)

#entry
limit_entry = tk.Entry(root, width=7, textvariable=limit)
limit_entry.grid(row=1, column=1)

delay_time_entry = tk.Entry(root, width=7, textvariable=delay_time)
delay_time_entry.grid(row=2, column=1)

#button
control = Controller()
search_btn = tk.Button(root, text='파일 탐색', command=add_file)
search_btn.grid(row=0, column=2)
start_btn = tk.Button(root, text='시작', command=control.start)
start_btn.grid(row=2, column=2)
stop_btn = tk.Button(root, text='중지', command=control.stop)
stop_btn.grid(row=3, column=2)

root.mainloop()
