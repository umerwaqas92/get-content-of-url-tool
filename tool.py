import threading
import tkinter as tk
import requests
from bs4 import BeautifulSoup

class URLTextRetriever:
    def __init__(self, master):
        self.master = master
        master.title("URL Text Retriever")

        # Create input label and entry box
        self.url_label = tk.Label(master, text="Enter a URL:")
        self.url_label.pack()
        self.url_entry = tk.Entry(master, width=50)
        self.url_entry.pack()

        # Create submit button
        self.submit_button = tk.Button(master, text="Submit", command=self.submit)
        self.submit_button.pack()

        # Create output label, text box, and copy button
        self.output_label = tk.Label(master, text="Result:")
        self.output_label.pack()
        self.output_text = tk.Text(master, height=20, width=50)
        self.output_text.pack()
        self.copy_button = tk.Button(master, text="Copy", command=self.copy_to_clipboard)
        self.copy_button.pack()

    def submit(self):
        url = self.url_entry.get()
        self.output_text.delete("1.0", tk.END) # clear previous output

        # Create a new thread to run the URL retrieval in the background
        retrieval_thread = threading.Thread(target=self.retrieve_url, args=(url,))
        retrieval_thread.start()

    def retrieve_url(self, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        content = soup.get_text().strip()  # remove trailing whitespace

        # Update the output text box with the retrieved content
        self.master.after(0, self.output_text.insert, tk.END, content)

    def copy_to_clipboard(self):
        self.master.clipboard_clear()
        self.master.clipboard_append(self.output_text.get("1.0", tk.END))

root = tk.Tk()
app = URLTextRetriever(root)
root.mainloop()
