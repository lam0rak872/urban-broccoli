import tkinter as tk
from tkinter import ttk, messagebox
import requests
import json
import os
import re

FAVORITES_FILE = "favorites.json"
GITHUB_API_URL = "https://api.github.com/search/users"


def load_favorites():
    if os.path.exists(FAVORITES_FILE):
        with open(FAVORITES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def save_favorites(favorites):
    with open(FAVORITES_FILE, "w", encoding="utf-8") as f:
        json.dump(favorites, f, ensure_ascii=False, indent=4)


class GitHubUserFinder:
    def __init__(self, root):
        self.root = root
        self.root.title("GitHub User Finder")
        self.root.geometry("600x500")
        self.root.minsize(400, 300)

        self.favorites = load_favorites()
        self.search_results = []

        self.create_widgets()

    def create_widgets(self):
        # Search frame
        search_frame = ttk.Frame(self.root, padding="10")
        search_frame.pack(fill="x")

        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(search_frame, textvariable=self.search_var)
        self.search_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))
        self.search_entry.bind("<Return>", lambda e: self.search_users())

        self.search_btn = ttk.Button(
            search_frame, text="Search", command=self.search_users
        )
        self.search_btn.pack(side="left")

        self.fav_btn = ttk.Button(
            search_frame, text="Show Favorites", command=self.show_favorites
        )
        self.fav_btn.pack(side="left", padx=(5, 0))

        # Notebook (tabs)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=5)

        # Results tab
        self.results_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.results_frame, text="Search Results")

        self.results_listbox = tk.Listbox(self.results_frame)
        self.results_listbox.pack(fill="both", expand=True, side="left")
        self.results_listbox.bind("<<ListboxSelect>>", self.on_result_select)

        results_scrollbar = ttk.Scrollbar(
            self.results_frame, orient="vertical", command=self.results_listbox.yview
        )
        results_scrollbar.pack(fill="y", side="right")
        self.results_listbox.config(yscrollcommand=results_scrollbar.set)

        self.add_fav_btn = ttk.Button(
            self.results_frame, text="Add to Favorites", command=self.add_to_favorites
        )
        self.add_fav_btn.pack(pady=5)

        # Favorites tab
        self.favorites_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.favorites_frame, text="Favorites")

        self.favorites_listbox = tk.Listbox(self.favorites_frame)
        self.favorites_listbox.pack(fill="both", expand=True, side="left")

        fav_scrollbar = ttk.Scrollbar(
            self.favorites_frame,
            orient="vertical",
            command=self.favorites_listbox.yview,
        )
        fav_scrollbar.pack(fill="y", side="right")
        self.favorites_listbox.config(yscrollcommand=fav_scrollbar.set)

        self.remove_fav_btn = ttk.Button(
            self.favorites_frame,
            text="Remove from Favorites",
            command=self.remove_from_favorites,
        )
        self.remove_fav_btn.pack(pady=5)

        # Details frame
        self.details_frame = ttk.LabelFrame(
            self.root, text="User Details", padding="10"
        )
        self.details_frame.pack(fill="x", padx=10, pady=5)

        self.details_label = ttk.Label(
            self.details_frame,
            text="Select a user to view details.",
            anchor="w",
            justify="left",
        )
        self.details_label.pack(fill="x")

    def search_users(self):
        query = self.search_var.get().strip()
        if not query:
            messagebox.showwarning(
                "Validation Error", "Search field must not be empty!"
            )
            return

        try:
            params = {"q": query, "per_page": 10}
            response = requests.get(GITHUB_API_URL, params=params, timeout=15)
            response.raise_for_status()
            data = response.json()
            self.search_results = data.get("items", [])

            self.results_listbox.delete(0, tk.END)
            if not self.search_results:
                self.results_listbox.insert(tk.END, "No users found.")
                self.search_results = []
                return

            for user in self.search_results:
                self.results_listbox.insert(tk.END, user["login"])
        except requests.RequestException as e:
            messagebox.showerror("Error", f"Failed to fetch data from GitHub API:\n{e}")

    def on_result_select(self, event):
        selection = self.results_listbox.curselection()
        if not selection or not self.search_results:
            return
        index = selection[0]
        if index >= len(self.search_results):
            return
        user = self.search_results[index]
        self.show_user_details(user)

    def show_user_details(self, user):
        details = (
            f"Username: {user.get('login', 'N/A')}\n"
            f"Profile URL: {user.get('html_url', 'N/A')}\n"
            f"Avatar URL: {user.get('avatar_url', 'N/A')}\n"
            f"Type: {user.get('type', 'N/A')}\n"
            f"Score: {user.get('score', 'N/A')}\n"
        )
        self.details_label.config(text=details)

    def add_to_favorites(self):
        selection = self.results_listbox.curselection()
        if not selection or not self.search_results:
            messagebox.showinfo("Info", "Please select a user from search results.")
            return
        index = selection[0]
        if index >= len(self.search_results):
            return
        user = self.search_results[index]
        login = user["login"]

        if any(fav["login"] == login for fav in self.favorites):
            messagebox.showinfo("Info", f'User "{login}" is already in favorites.')
            return

        self.favorites.append(user)
        save_favorites(self.favorites)
        self.update_favorites_listbox()
        messagebox.showinfo("Success", f'User "{login}" added to favorites.')

    def remove_from_favorites(self):
        selection = self.favorites_listbox.curselection()
        if not selection:
            messagebox.showinfo("Info", "Please select a user from favorites.")
            return
        index = selection[0]
        if index >= len(self.favorites):
            return
        user = self.favorites.pop(index)
        save_favorites(self.favorites)
        self.update_favorites_listbox()
        messagebox.showinfo(
            "Success", f'User "{user["login"]}" removed from favorites.'
        )

    def update_favorites_listbox(self):
        self.favorites_listbox.delete(0, tk.END)
        for user in self.favorites:
            self.favorites_listbox.insert(tk.END, user["login"])

    def show_favorites(self):
        self.notebook.select(self.favorites_frame)
        self.update_favorites_listbox()


def main():
    root = tk.Tk()
    app = GitHubUserFinder(root)
    root.mainloop()


if __name__ == "__main__":
    main()
