import tkinter as tk
from tkinter import messagebox
import json
import os
from datetime import datetime

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.tasks = []
        self.setup_ui()
        self.load_tasks()
        
    def setup_ui(self):
        self.root.title("✅ My To-Do List")
        self.root.geometry("500x600")
        self.root.config(bg="#A746A7")
        
        # Title
        title_label = tk.Label(
            self.root,
            text="📝 My To-Do List",
            font=("Segoe UI", 24, "bold"),
            bg="#DB6B8D",
            fg="#C5578E"
        )
        title_label.pack(pady=20)
        
        
        self.stats_frame = tk.Frame(self.root, bg="#A746A7")
        self.stats_frame.pack(pady=5)
        
        self.stats_label = tk.Label(
            self.stats_frame,
            text="Total: 0 | Completed: 0 | Pending: 0",
            font=("Segoe UI", 10),
            bg="#A746A7",
            fg="white"
        )
        self.stats_label.pack()
        
        
        entry_frame = tk.Frame(self.root, bg="#222831")
        entry_frame.pack(pady=15)
        
        self.entry = tk.Entry(
            entry_frame,
            font=("Segoe UI", 13),
            width=28,
            bg="white",
            fg="black",
            insertbackground="black",
            bd=0,
            relief="solid"
        )
        self.entry.grid(row=0, column=0, padx=10, ipady=8)
        self.entry.bind('<Return>', lambda e: self.add_task())
        
        add_btn = tk.Button(
            entry_frame,
            text="➕ Add Task",
            bg="#C04272",
            fg="white",
            font=("Segoe UI", 11, "bold"),
            width=12,
            relief="flat",
            cursor="hand2",
            command=self.add_task
        )
        add_btn.grid(row=0, column=1)
        
        
        priority_frame = tk.Frame(self.root, bg="#A746A7")
        priority_frame.pack(pady=5)
        
        tk.Label(
            priority_frame,
            text="Priority:",
            font=("Segoe UI", 10),
            bg="#A746A7",
            fg="white"
        ).pack(side=tk.LEFT, padx=5)
        
        self.priority_var = tk.StringVar(value="Medium")
        priorities = ["Low", "Medium", "High"]
        
        for priority in priorities:
            rb = tk.Radiobutton(
                priority_frame,
                text=priority,
                variable=self.priority_var,
                value=priority,
                font=("Segoe UI", 9),
                bg="#A746A7",
                fg="white",
                selectcolor="#C04272",
                activebackground="#A746A7",
                activeforeground="white"
            )
            rb.pack(side=tk.LEFT, padx=5)
        
        
        list_frame = tk.Frame(self.root, bg="#C798DA")
        list_frame.pack(pady=15, padx=20, fill=tk.BOTH, expand=True)
        
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.listbox = tk.Listbox(
            list_frame,
            font=("Consolas", 11),
            bg="#BE1887",
            fg="white",
            selectbackground="#CE7DBA",
            selectforeground="black",
            yscrollcommand=scrollbar.set,
            bd=0,
            relief="flat",
            highlightthickness=0
        )
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.listbox.yview)
        
       
        btn_frame = tk.Frame(self.root, bg="#530440")
        btn_frame.pack(pady=15)
        
        buttons = [
            ("✓ Complete", "#66054E", self.mark_done),
            ("✎ Edit", "#881E46", self.edit_task),
            ("🗑 Delete", "#66054E", self.delete_task),
            ("↻ Clear Done", "#881E46", self.clear_completed)
        ]
        
        for i, (text, color, cmd) in enumerate(buttons):
            btn = tk.Button(
                btn_frame,
                text=text,
                bg=color,
                fg="white",
                font=("Segoe UI", 10, "bold"),
                width=12,
                relief="flat",
                cursor="hand2",
                command=cmd
            )
            btn.grid(row=i//2, column=i%2, padx=8, pady=5)
        
       
        footer = tk.Label(
            self.root,
            text="💪 Stay productive! Press Enter to add tasks quickly",
            bg="#881E46",
            fg="#AAAAAA",
            font=("Segoe UI", 9)
        )
        footer.pack(side=tk.BOTTOM, pady=15)
    
    def add_task(self):
        task_text = self.entry.get().strip()
        if task_text:
            task = {
                "text": task_text,
                "completed": False,
                "priority": self.priority_var.get(),
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M")
            }
            self.tasks.append(task)
            self.entry.delete(0, tk.END)
            self.update_listbox()
            self.save_tasks()
        else:
            messagebox.showwarning("⚠ Warning", "Please enter a task first!")
    
    def delete_task(self):
        try:
            index = self.listbox.curselection()[0]
            actual_index = self.index_map[index]
            task = self.tasks[actual_index]
            if messagebox.askyesno("Confirm", f"Delete task: '{task['text']}'?"):
                self.tasks.pop(actual_index)
                self.update_listbox()
                self.save_tasks()
        except IndexError:
            messagebox.showwarning("⚠ Warning", "Select a task to delete!")
    
    def mark_done(self):
        try:
            index = self.listbox.curselection()[0]
            actual_index = self.index_map[index]
            self.tasks[actual_index]["completed"] = not self.tasks[actual_index]["completed"]
            self.update_listbox()
            self.save_tasks()
        except IndexError:
            messagebox.showwarning("⚠ Warning", "Select a task to mark done!")
    
    def edit_task(self):
        try:
            index = self.listbox.curselection()[0]
            actual_index = self.index_map[index]
            task = self.tasks[actual_index]
            
            # Create edit dialog
            edit_window = tk.Toplevel(self.root)
            edit_window.title("Edit Task")
            edit_window.geometry("400x150")
            edit_window.config(bg="#A746A7")
            edit_window.transient(self.root)
            edit_window.grab_set()
            
            tk.Label(
                edit_window,
                text="Edit Task:",
                font=("Segoe UI", 12),
                bg="#A746A7",
                fg="white"
            ).pack(pady=10)
            
            edit_entry = tk.Entry(
                edit_window,
                font=("Segoe UI", 12),
                width=35,
                bg="white",
                fg="black",
                insertbackground="black"
            )
            edit_entry.pack(pady=10, ipady=5)
            edit_entry.insert(0, task["text"])
            edit_entry.focus()
            
            def save_edit():
                new_text = edit_entry.get().strip()
                if new_text:
                    self.tasks[actual_index]["text"] = new_text
                    self.update_listbox()
                    self.save_tasks()
                    edit_window.destroy()
            
            edit_entry.bind('<Return>', lambda e: save_edit())
            
            tk.Button(
                edit_window,
                text="Save",
                bg="#66054E",
                fg="white",
                font=("Segoe UI", 10, "bold"),
                width=15,
                command=save_edit
            ).pack(pady=10)
            
        except IndexError:
            messagebox.showwarning("⚠ Warning", "Select a task to edit!")
    
    def clear_completed(self):
        completed_count = sum(1 for task in self.tasks if task["completed"])
        if completed_count > 0:
            if messagebox.askyesno("Confirm", f"Clear {completed_count} completed task(s)?"):
                self.tasks = [task for task in self.tasks if not task["completed"]]
                self.update_listbox()
                self.save_tasks()
        else:
            messagebox.showinfo("Info", "No completed tasks to clear!")
    
    def update_listbox(self):
        self.listbox.delete(0, tk.END)
        self.index_map = {}
        
        # sort by priority 
        priority_order = {"High": 0, "Medium": 1, "Low": 2}
        sorted_tasks = sorted(
            enumerate(self.tasks),
            key=lambda x: (x[1]["completed"], priority_order[x[1]["priority"]])
        )
        
        for display_index, (original_index, task) in enumerate(sorted_tasks):
            status = "✓" if task["completed"] else "○"
            priority_emoji = {"High": "🔴", "Medium": "🟡", "Low": "🟢"}[task["priority"]]
            display_text = f"{status} {priority_emoji} {task['text']}"
            
            self.listbox.insert(tk.END, display_text)
            self.index_map[display_index] = original_index
            
         
            if task["completed"]:
                self.listbox.itemconfig(tk.END, fg="#CE7DBA")
        
        self.update_stats()
    
    def update_stats(self):
        total = len(self.tasks)
        completed = sum(1 for task in self.tasks if task["completed"])
        pending = total - completed
        self.stats_label.config(text=f"Total: {total} | Completed: {completed} | Pending: {pending}")
    
    def save_tasks(self):
        with open("tasks.json", "w", encoding="utf-8") as file:
            json.dump(self.tasks, file, indent=2, ensure_ascii=False)
    
    def load_tasks(self):
        if os.path.exists("tasks.json"):
            try:
                with open("tasks.json", "r", encoding="utf-8") as file:
                    self.tasks = json.load(file)
                self.update_listbox()
            except json.JSONDecodeError:
                self.tasks = []

if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()