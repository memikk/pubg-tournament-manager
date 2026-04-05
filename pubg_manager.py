import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import csv

class TournamentManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PUBG Tournament Manager")
        self.root.geometry("1000x800")
        
        # Data
        self.match_count = 0
        self.current_match = 1
        self.teams_list = [] # List of 16 Team Names
        self.matches_data = [] # List of results
        
        self.setup_styles()
        self.root.configure(bg="#1e1e1e") # Dark BG for root
        self.show_main_menu()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam') # 'clam' allows easier color customization
        
        # Colors
        BG_DARK = "#1e1e1e"
        BG_LIGHT = "#2d2d2d"
        FG_WHITE = "#ffffff"
        ACCENT = "#f2a900" # PUBG Yellow/Orange
        
        # General Frame
        style.configure("TFrame", background=BG_DARK)
        
        # Labels
        style.configure("Header.TLabel", font=("Segoe UI", 24, "bold"), background=BG_DARK, foreground=ACCENT)
        style.configure("SubHeader.TLabel", font=("Segoe UI", 16, "bold"), background=BG_DARK, foreground=FG_WHITE)
        style.configure("TLabel", font=("Segoe UI", 11), background=BG_DARK, foreground=FG_WHITE)
        
        # Buttons
        style.configure("TButton", font=("Segoe UI", 11, "bold"), padding=8, background=ACCENT, foreground="black", borderwidth=0)
        style.map("TButton", background=[("active", "#d49200")])
        
        # Entry
        style.configure("TEntry", fieldbackground=BG_LIGHT, foreground=FG_WHITE, padding=5, insertcolor=FG_WHITE)
        
        # Combobox
        style.configure("TCombobox", fieldbackground=BG_LIGHT, background=BG_LIGHT, foreground=FG_WHITE, arrowcolor=ACCENT)
        style.map("TCombobox", fieldbackground=[("readonly", BG_LIGHT)], background=[("readonly", BG_LIGHT)], foreground=[("readonly", FG_WHITE)])
        
        # Treeview
        style.configure("Treeview", background="#252525", foreground=FG_WHITE, fieldbackground="#252525", rowheight=30, font=("Segoe UI", 11))
        style.configure("Treeview.Heading", font=("Segoe UI", 12, "bold"), background="#333", foreground=ACCENT)
        style.map("Treeview", background=[("selected", ACCENT)], foreground=[("selected", "black")])

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    # --- 1. MAIN MENU ---
    def show_main_menu(self):
        self.clear_window()
        frame = ttk.Frame(self.root, padding=40)
        frame.pack(expand=True, fill="both")
        
        # Center Content
        content = ttk.Frame(frame)
        content.place(relx=0.5, rely=0.5, anchor="center")
        
        ttk.Label(content, text="PUBG TOURNAMENT MANAGER", style="Header.TLabel", justify="center").pack(pady=40)
        
        btn_frame = ttk.Frame(content)
        btn_frame.pack(pady=20)
        
        ttk.Button(btn_frame, text="Create New Tournament", command=self.setup_tournament, width=30).pack(pady=15)
        ttk.Button(btn_frame, text="Help", command=self.show_help, width=30).pack(pady=15)
        ttk.Button(btn_frame, text="Exit", command=self.root.quit, width=30).pack(pady=15)

    def show_help(self):
        msg = ("1. Enter number of matches.\n"
               "2. Paste or Enter the names of the 16 Teams.\n"
               "3. For each match, assign the Team to their Rank and enter Kills.\n"
               "4. Export final Leaderboard.\n\n"
               "Tip: Use TAB key to move quickly between fields!")
        messagebox.showinfo("Help", msg)

    # --- 2. SETUP TOURNAMENT (Matches & Teams) ---
    def setup_tournament(self):
        self.clear_window()
        frame = ttk.Frame(self.root, padding=20)
        frame.pack(expand=True, fill="both")
        
        header_frame = ttk.Frame(frame)
        header_frame.pack(fill="x", pady=10)
        ttk.Label(header_frame, text="Step 1: Tournament Setup", style="Header.TLabel").pack(side="left")
        
        # Match Count
        inputs_frame = ttk.Frame(frame, padding=10)
        inputs_frame.pack(fill="x", pady=10)
        ttk.Label(inputs_frame, text="Number of Matches:", style="SubHeader.TLabel").pack(side="left", padx=(0,10))
        self.match_var = tk.StringVar(value="4")
        match_entry = ttk.Entry(inputs_frame, textvariable=self.match_var, width=5, font=("Segoe UI", 14))
        match_entry.pack(side="left")
        
        # Team Names Entry
        ttk.Label(frame, text="TEAMS LIST (16 Teams)", style="SubHeader.TLabel", foreground="#f2a900").pack(pady=(20, 10))
        
        self.team_vars = []
        
        teams_frame = ttk.Frame(frame)
        teams_frame.pack(expand=True, fill="both", padx=20)
        
        # Grid of 4 columns, 4 rows for better density
        for i in range(16):
            r = i % 4
            c = i // 4
            
            f = ttk.Frame(teams_frame, padding=5)
            f.grid(row=r, column=c, padx=10, pady=5, sticky="ew")
            
            lbl = ttk.Label(f, text=f"Team {i+1}", font=("Segoe UI", 9, "bold"), foreground="grey")
            lbl.pack(anchor="w")
            
            var = tk.StringVar(value=f"Team {i+1}")
            entry = ttk.Entry(f, textvariable=var, width=20)
            entry.pack(fill="x")
            self.team_vars.append(var)
        
        teams_frame.columnconfigure(0, weight=1)
        teams_frame.columnconfigure(1, weight=1)
        teams_frame.columnconfigure(2, weight=1)
        teams_frame.columnconfigure(3, weight=1)

        btn_frame = ttk.Frame(frame)
        btn_frame.pack(pady=30, fill="x")
        
        # Center buttons
        center_btn = ttk.Frame(btn_frame)
        center_btn.pack(anchor="center")
        
        ttk.Button(center_btn, text="Start Tournament", command=self.start_matches).pack(side="left", padx=10)
        ttk.Button(center_btn, text="Paste Clipboard", command=self.paste_teams).pack(side="left", padx=10)
        ttk.Button(center_btn, text="Clear", command=self.clear_teams).pack(side="left", padx=10)
        ttk.Button(center_btn, text="Back", command=self.show_main_menu).pack(side="left", padx=10)
        
        # Auto-load previous teams if available
        self.load_saved_teams()

    def paste_teams(self):
        try:
            # Get text from clipboard
            content = self.root.clipboard_get()
            # Split by lines
            lines = [line.strip() for line in content.split('\n') if line.strip()]
            
            # Fill inputs
            for i, line in enumerate(lines):
                if i < 16:
                    self.team_vars[i].set(line)
                    
            messagebox.showinfo("Success", f"Pasted {min(len(lines), 16)} teams.")
        except Exception:
            messagebox.showerror("Error", "Clipboard is empty or invalid.")

    def clear_teams(self):
        for var in self.team_vars:
            var.set("")

    def load_saved_teams(self):
        # Check if saved file exists
        import os
        if os.path.exists("saved_teams.txt"):
            try:
                with open("saved_teams.txt", "r", encoding="utf-8") as f:
                    lines = [l.strip() for l in f.readlines()]
                    for i, line in enumerate(lines):
                        if i < 16:
                            self.team_vars[i].set(line)
            except:
                pass

    def start_matches(self):
        try:
            count = int(self.match_var.get())
            if count < 1: raise ValueError
        except:
            messagebox.showerror("Error", "Invalid number of matches.")
            return

        # Save teams to variables
        self.teams_list = [v.get().strip() for v in self.team_vars]
        if any(not t for t in self.teams_list):
            messagebox.showerror("Error", "All team names must be filled.")
            return
            
        # SAVE to file for next time
        try:
            with open("saved_teams.txt", "w", encoding="utf-8") as f:
                for t in self.teams_list:
                    f.write(t + "\n")
        except:
            pass

        self.match_count = count
        self.current_match = 1
        self.matches_data = [] # Reset data
        
        self.show_match_entry()

    # --- 3. MATCH ENTRY SCREEN ---
    def show_match_entry(self):
        self.clear_window()
        frame = ttk.Frame(self.root, padding=20)
        frame.pack(expand=True, fill="both")
        
        # Header
        top_bar = ttk.Frame(frame)
        top_bar.pack(fill="x", pady=(0, 20))
        ttk.Label(top_bar, text=f"MATCH {self.current_match} RESULTS", style="Header.TLabel").pack(side="left")
        ttk.Label(top_bar, text=f"Entry for {self.match_count} matches", style="TLabel", foreground="grey").pack(side="left", padx=20, pady=10)
        
        # Main Grid Area (Scrollable)
        canvas = tk.Canvas(frame, bg="#1e1e1e", highlightthickness=0)
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        grid_frame = ttk.Frame(canvas)
        
        grid_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas_window = canvas.create_window((0, 0), window=grid_frame, anchor="nw")
        
        # Ensure full width
        def configure_width(event):
            canvas.itemconfig(canvas_window, width=event.width)
        canvas.bind("<Configure>", configure_width)
        
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True, padx=(0, 10))
        scrollbar.pack(side="right", fill="y")
        
        # We will split 16 ranks into 2 Columns (Rank 1-8, Rank 9-16)
        
        left_col = ttk.Frame(grid_frame)
        left_col.pack(side="left", fill="both", expand=True, padx=(0, 20))
        
        right_col = ttk.Frame(grid_frame)
        right_col.pack(side="left", fill="both", expand=True)
        
        self.rank_entries = []
        sorted_teams = sorted(self.teams_list)

        for i in range(16):
            rank = i + 1
            parent = left_col if rank <= 8 else right_col
            
            # Row Container
            row_frame = ttk.Frame(parent, padding=(0, 5))
            row_frame.pack(fill="x")
            
            # Rank Number styling
            rank_color = "#f2a900" if rank <= 3 else "#ffffff" # Gold for Top 3
            rank_font = ("Segoe UI", 14, "bold") if rank <= 3 else ("Segoe UI", 12)
            
            lbl_rank = ttk.Label(row_frame, text=f"#{rank}", width=4, font=rank_font, foreground=rank_color, anchor="center")
            lbl_rank.pack(side="left")
            
            # Team Dropdown
            default_val = self.teams_list[rank-1] if rank <= len(self.teams_list) else ""
            team_var = tk.StringVar(value=default_val)
            
            # Style Combobox as "Entry-like"
            cb = ttk.Combobox(row_frame, textvariable=team_var, values=self.teams_list, state="readonly", width=25, font=("Segoe UI", 11))
            cb.pack(side="left", fill="x", expand=True, padx=5)
            
            # Kills
            ttk.Label(row_frame, text="Kills:", foreground="grey", font=("Segoe UI", 9)).pack(side="left")
            kill_var = tk.StringVar(value="0")
            ke = ttk.Entry(row_frame, textvariable=kill_var, width=5, justify="center", font=("Segoe UI", 11))
            ke.pack(side="left", padx=(5, 0))
            
            self.rank_entries.append({
                "rank": rank,
                "team_var": team_var,
                "kill_var": kill_var
            })

        # Bottom Buttons
        btn_frame = ttk.Frame(frame, padding=20)
        btn_frame.pack(fill="x")
        
        ttk.Button(btn_frame, text="NEXT MATCH >>", command=self.save_match, width=20).pack(side="right")

    def save_match(self):
        # Validate
        results = []
        used_teams = set()
        
        try:
            for entry in self.rank_entries:
                rank = entry['rank']
                team = entry['team_var'].get()
                k_str = entry['kill_var'].get()
                
                if not team:
                    raise ValueError(f"Rank {rank} has no team selected.")
                if team in used_teams:
                    raise ValueError(f"Team '{team}' is selected multiple times.")
                used_teams.add(team)
                
                if not k_str.isdigit():
                    raise ValueError(f"Invalid kills for Rank {rank}.")
                
                results.append({
                    "rank": rank,
                    "team": team,
                    "kills": int(k_str)
                })
                
            # Save
            self.matches_data.append(results)
            messagebox.showinfo("Success", f"Match {self.current_match} saved.")
            
            self.current_match += 1
            if self.current_match > self.match_count:
                self.show_results()
            else:
                self.show_match_entry()
                
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    # --- 4. FINAL RESULTS ---
    def show_results(self):
        self.clear_window()
        frame = ttk.Frame(self.root, padding=20)
        frame.pack(expand=True, fill="both")
        
        ttk.Label(frame, text="FINAL LEADERBOARD", style="Header.TLabel").pack(pady=10)
        
        # Calculate
        final_scores, match_cols = self.calculate_scores()
        
        # Treeview Stats
        # Rank, Team, [Match 1, Match 2...], Wins, Kills, Total
        cols = ["Rank", "Team"] + match_cols + ["Wins", "Total Kills", "Total Score"]
        
        tree = ttk.Treeview(frame, columns=cols, show="headings", height=20)
        
        # Configure columns
        tree.column("Rank", width=50, anchor="center")
        tree.column("Team", width=200, anchor="w")
        for mc in match_cols:
            tree.column(mc, width=80, anchor="center")
        tree.column("Wins", width=60, anchor="center")
        tree.column("Total Kills", width=80, anchor="center")
        tree.column("Total Score", width=100, anchor="center")
        
        for c in cols:
            tree.heading(c, text=c)
            
        # Striped Tags
        tree.tag_configure('odd', background='#252525')
        tree.tag_configure('even', background='#2d2d2d')
        tree.tag_configure('top1', background='#ffd700', foreground='black') # Gold
        
        for idx, item in enumerate(final_scores):
            # Row Values
            row_vals = [idx+1, item['Team']]
            # Add Per-Match Scores
            for mc in match_cols:
                row_vals.append(item.get(mc, 0))
                
            row_vals.extend([item['Wins'], item['Total Kills'], item['Total Score']])
            
            # Tags
            tag = 'odd' if idx % 2 == 0 else 'even'
            if idx == 0: tag = 'top1'
            
            tree.insert("", "end", values=row_vals, tags=(tag,))
            
        tree.pack(expand=True, fill="both")
        
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(pady=20)
        ttk.Button(btn_frame, text="Export CSV", command=lambda: self.export_csv(final_scores, cols)).pack(side="left", padx=10)
        ttk.Button(btn_frame, text="New Tournament", command=self.show_main_menu).pack(side="left", padx=10)
        ttk.Button(btn_frame, text="Exit", command=self.root.quit).pack(side="left", padx=10)

    def calculate_scores(self):
        # Initial Aggregation
        agg = {name: {'Team': name, 'Wins': 0, 'Total Kills': 0, 'Total Score': 0} 
               for name in self.teams_list}
        
        match_columns = []
        
        for m_idx, match in enumerate(self.matches_data):
            m_label = f"M{m_idx+1}"
            match_columns.append(m_label)
            
            for row in match:
                t = row['team']
                rank = row['rank']
                kills = row['kills']
                
                # Placement Points
                p_pts = 0
                if rank == 1: p_pts = 10
                elif rank == 2: p_pts = 6
                elif rank == 3: p_pts = 5
                elif rank == 4: p_pts = 4
                elif rank == 5: p_pts = 3
                elif 6 <= rank <= 10: p_pts = 2
                elif 11 <= rank <= 16: p_pts = 1
                
                match_score = p_pts + kills
                
                # Update Agg
                if rank == 1: agg[t]['Wins'] += 1
                agg[t]['Total Kills'] += kills
                agg[t]['Total Score'] += match_score
                
                # Store Match Score
                agg[t][m_label] = match_score
                
        # Sort
        result = list(agg.values())
        result.sort(key=lambda x: x['Total Score'], reverse=True)
        return result, match_columns

    def export_csv(self, data, fieldnames):
        path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV", "*.csv")])
        if path:
            try:
                with open(path, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(data)
                messagebox.showinfo("Success", "Saved.")
            except Exception as e:
                messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = TournamentManagerApp(root)
    root.mainloop()
