import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import messagebox

def get_wp_version(url):
    try:
        if not url.startswith("http"):
            url = "http://" + url

        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Try meta tag first
        generator = soup.find("meta", attrs={"name": "generator"})
        if generator and "WordPress" in generator.get("content", ""):
            return generator["content"]

        # Try RSS feed as a backup
        feed_url = url.rstrip("/") + "/feed/"
        response = requests.get(feed_url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'xml')
        generator = soup.find("generator")
        if generator and "WordPress" in generator.text:
            return generator.text.strip()

        return "Version not found (hidden or not a WP site)"
    except Exception as e:
        return f"Error: {str(e)}"

def check_version():
    url = url_entry.get().strip()
    if not url:
        messagebox.showwarning("Input Needed", "Please enter a website URL.")
        return

    result = get_wp_version(url)
    result_label.config(text=result)

# GUI setup
root = tk.Tk()
root.title("WordPress Version Checker")
root.geometry("400x250")
root.configure(bg="#1e1e1e")

tk.Label(root, text="Enter website URL:", bg="#1e1e1e", fg="white", font=("Helvetica", 12)).pack(pady=10)

url_entry = tk.Entry(root, width=40, font=("Helvetica", 12))
url_entry.pack(pady=5)

check_button = tk.Button(root, text="Check WordPress Version", command=check_version, bg="#007acc", fg="white", font=("Helvetica", 12, "bold"))
check_button.pack(pady=15)

result_label = tk.Label(root, text="", wraplength=350, bg="#1e1e1e", fg="lightgreen", font=("Helvetica", 12))
result_label.pack(pady=10)

root.mainloop()
