import pandas as pd
import random
import tkinter as tk
from tkinter import filedialog, messagebox, ttk


class TeamGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Header Heeler Selector")
        self.root.geometry("1280x720")
        self.file_path = ""
        self.teams = []

        tk.Label(root, text="Header Heeler Selector", font=("Arial", 16, "bold")).pack(pady=10)
        self.btn_select = tk.Button(root, text="Select The Excel File", command=self.select_file)
        self.btn_select.pack(pady=5)

        self.lbl_file = tk.Label(root, text="No file selected", fg="gray")
        self.lbl_file.pack(pady=5)

        self.btn_generate = tk.Button(root, text="Create Teams", command=self.generate_teams, state=tk.DISABLED)
        self.btn_generate.pack(pady=10)

        columns = ("Team", "Header", "Heeler")
        self.tree = ttk.Treeview(root, columns=columns, show="headings")
        self.tree.heading("Team", text="Team #")
        self.tree.heading("Header", text="Header")
        self.tree.heading("Heeler", text="Heeler")
        self.tree.pack(pady=10, fill=tk.BOTH, expand=True)

        self.tree.column("Team", width=70, anchor="center")
        self.tree.column("Header", width=180, anchor="center")
        self.tree.column("Heeler", width=180, anchor="center")

        self.btn_save = tk.Button(root, text="Save Results to Excel", command=self.save_file, state=tk.DISABLED)
        self.btn_save.pack(pady=10)

    def select_file(self):
        filePath = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")])
        if filePath:
            self.file_path = filePath
            self.lbl_file.config(text=f"Selected: {filePath.split('/')[-1]}", fg="green")
            self.btn_generate.config(state=tk.NORMAL)

    def save_file(self):
        if not self.teams:
            return

        save_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
        if save_path:
            df = pd.DataFrame(self.teams, columns=["Header", "Heeler"])
            df.to_excel(save_path, index=False)
            messagebox.showinfo("Saved", f"File saved successfully to {save_path.split('/')[-1]}")

    def generate_teams(self):
        try:
            data = pd.read_excel(self.file_path)
            headers = []
            heelers = []
            data = data.reset_index()
            for i, row in data.iterrows():
                headers.append(row.iloc[1])
                heelers.append(row.iloc[2])

            if len(headers) != len(heelers):
                messagebox.showerror("Error", "Headers and Heelers lists must have equal lengths.")
                return

            MAX_COUNT = 5000
            count = 0

            while True:
                redo = False
                random.shuffle(headers)
                random.shuffle(heelers)

                for i, j in zip(headers, heelers):
                    if i == j:
                        redo = True
                        break

                if redo:
                    count += 1
                    if count >= MAX_COUNT:
                        break
                    continue

                for i in range(len(headers) - 2):
                    team1 = {headers[i], heelers[i]}
                    team2 = {headers[i + 1], heelers[i + 1]}
                    team3 = {headers[i + 2], heelers[i + 2]}

                    if team1 & team2 & team3:
                        redo = True
                        break

                count += 1
                if redo:
                    if count >= MAX_COUNT:
                        break
                    continue
                break

            if count >= MAX_COUNT:
                messagebox.showerror("Error","Could not find a valid combination for the names, try a different list")


            for row in self.tree.get_children():
                self.tree.delete(row)
            for team, (header, heeler) in enumerate(zip(headers, heelers), start = 1):
                self.tree.insert("", tk.END, values=(team, header, heeler))
            self.btn_save.config(state=tk.NORMAL)
            self.teams = list(zip(headers, heelers))
        except Exception as error:
            messagebox.showerror("Error", f"Failed to process file: {str(error)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = TeamGeneratorApp(root)
    root.mainloop()