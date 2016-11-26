import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askdirectory
from time import sleep
import os
import re
from pathlib import Path
from FindErrors import find_errors


class Main(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Find Errors")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        mainframe = ttk.Frame(self, padding="10")
        mainframe.grid(sticky=(tk.N, tk.W, tk.E, tk.S))
        mainframe.rowconfigure(1, weight=1, pad=5, minsize=50)
        mainframe.rowconfigure(3, pad=10)
        mainframe.columnconfigure(0, minsize=200)
        mainframe.columnconfigure(2, pad=5)

        self.count = 0
        self.process = tk.StringVar()
        self.process.set('None')
        self.bit_change = tk.IntVar()
        self.bit_depth = tk.IntVar()
        self.bit_var = 0
        self.otsu = tk.IntVar()
        self.high = tk.StringVar()
        self.low = tk.StringVar()
        self.high.set(.9)
        self.low.set(.4)
        self.otsu.set(1)

        tk.Label(mainframe, text="Processing:").grid(row=2, column=0, sticky=(tk.W, tk.S))
        tk.Label(mainframe, textvariable=self.process).grid(row=2, column=1, sticky=tk.S)

        self.files = []
        tk.Button(mainframe, text="Select Directory", command=self.change_directory).grid(row=0, column=0, sticky=tk.W)

        tk.Button(mainframe, text="Options", command=self.pref).grid(row=0, column=1, sticky=tk.E)

        outerframe = tk.Frame(mainframe)
        outerframe.grid(row=1, column=0, columnspan=2, sticky=(tk.N, tk.W, tk.S, tk.E))

        self.canvas = tk.Canvas(outerframe, borderwidth=0)
        self.frame = tk.Frame(self.canvas)
        self.vsb = tk.Scrollbar(outerframe, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)

        self.vsb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((4, 4), window=self.frame, anchor="nw",
                                  tags="self.frame")

        self.frame.bind("<Configure>", self.onFrameConfigure)

        tk.Button(mainframe, text="Run", command=self.go).grid(row=1, column=2)

        self.to_display = []
        self.images = []

        self.progress = tk.ttk.Progressbar(mainframe, orient=tk.HORIZONTAL, mode='determinate')
        self.progress.grid(row=3, column=0, columnspan=5, sticky=(tk.E, tk.W))

    def onFrameConfigure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def change_directory(self):
        self.files = []
        folder = askdirectory()
        if folder:
            for f in self.frame.winfo_children():
                f.destroy()
            for f in os.listdir(folder):
                if re.search('(?i)\.jpg', f):
                    self.files.append(str(Path(folder+"\\"+f).resolve()))
            for x, f in enumerate(self.files):
                tk.Label(self.frame, text=f).grid(row=x, column=0)
            self.count = 0

    def go(self):
        self.progress['maximum'] = len(self.files)
        self.progress['value'] = 0
        self.to_display = []
        total = len(self.files)
        for n, f in enumerate(self.files):
            self.process.set(f)
            self.update_idletasks()
            sleep(1)
            self.to_display.append([])
            try:
                self.to_display[n].append(find_errors(f, self.bit_var, self.otsu.get(), float(self.high.get()),
                                                      float(self.low.get())))
            except:
                raise
            print('--')
            self.progress['value'] += 1
        self.process.set('Done')
        self.count = 1

    def pref(self):
        pref_win = tk.Toplevel()
        pref_win.transient(self)
        pref_win.grab_set()
        pref_frame = tk.Frame(pref_win, padding="10")
        pref_frame.grid(sticky=(tk.N, tk.W, tk.E, tk.S))
        bit_spin = tk.Spinbox(pref_frame, from_=1, to=16, textvariable=self.bit_depth, command=self.bit_var_change)
        if not self.bit_change.get():
            bit_spin['state'] = tk.DISABLED
        bit_spin.grid(row=0, column=1, columnspan=2)
        tk.Checkbutton(pref_frame, text="Reduce bit depth by a factor of", variable=self.bit_change,
                        command=lambda: self.swap_state(bit_spin)).grid(row=0, column=0, sticky=tk.W)
        tk.Radiobutton(pref_frame, text="Use Otsu's method to determine\nCanny thresholds (ratio between 0 - 1)",
                        variable=self.otsu, value=1).grid(row=1, column=0, sticky=tk.W)
        tk.Radiobutton(pref_frame, text="Set Canny thresholds manually (0 - 255)",
                        variable=self.otsu, value=0).grid(row=2, column=0, sticky=tk.W)
        self.otsu.set(1)
        tk.Label(pref_frame, text='Upper threshold').grid(row=1, column=1, sticky=tk.W)
        tk.Entry(pref_frame, width=3, textvariable=self.high).grid(row=1, column=2, sticky=tk.W)
        tk.Label(pref_frame, text='Lower threshold').grid(row=2, column=1, sticky=tk.W)
        tk.Entry(pref_frame, width=3, textvariable=self.low).grid(row=2, column=2, sticky=tk.W)

    def bit_var_change(self):
        self.bit_var = self.bit_depth.get()

    def swap_state(self, widget):
        if widget['state'] == tk.NORMAL:
            widget['state'] = tk.DISABLED
            self.bit_var = 0
        else:
            widget['state'] = tk.NORMAL
            self.bit_var = self.bit_depth.get()


if __name__ == "__main__":
    Main().mainloop()
