import cefpython3 as cef
import tkinter as tk
from tkinter import ttk

# URLs for Google Finance
nasdaq_url = "https://www.google.com/finance/quote/.IXIC:INDEXNASDAQ?window=5D"
sp500_url = "https://www.google.com/finance/quote/.INX:INDEXSP?window=5D"

class BrowserFrame(tk.Frame):
    def __init__(self, master, url):
        super().__init__(master)
        self.browser = None
        self.url = url
        self.create_widgets()

    def create_widgets(self):
        self.browser = cef.CreateBrowserSync(window_info=cef.WindowInfo(self.winfo_id()), url=self.url)
        self.bind("<Configure>", self.on_configure)

    def on_configure(self, event):
        if self.browser:
            self.browser.SetBounds(0, 0, event.width, event.height)

def main():
    root = tk.Tk()
    root.geometry("800x600")
    root.title("Google Finance Viewer")

    notebook = ttk.Notebook(root)
    notebook.pack(fill=tk.BOTH, expand=True)

    nasdaq_frame = BrowserFrame(notebook, nasdaq_url)
    sp500_frame = BrowserFrame(notebook, sp500_url)

    notebook.add(nasdaq_frame, text="NASDAQ")
    notebook.add(sp500_frame, text="S&P 500")

    cef.Initialize()
    root.mainloop()
    cef.Shutdown()

if __name__ == "__main__":
    main()