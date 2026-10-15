import tkinter as tk
from tkinter import messagebox, ttk

from circular_doubly_linked_list import CircularDoublyLinkedList
from horse import Horse


class HorseManagerApp:
    def __init__(self):
        self.horses = CircularDoublyLinkedList()
        self.root = tk.Tk()
        self.root.title("HorseManager | Stable Management")
        self.root.geometry("1050x700")
        self.root.minsize(900, 620)
        self.root.configure(bg="#f3f0e7")

        self.colors = {
            "green": "#183d32",
            "green_light": "#245747",
            "gold": "#d3a84f",
            "cream": "#f3f0e7",
            "white": "#ffffff",
            "text": "#20332c",
            "muted": "#6b776f",
            "red": "#b7463d",
        }
        self._configure_styles()
        self._build_ui()
        self._load_sample_data()
        self._refresh_view()

    def _configure_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Treeview",
            background=self.colors["white"],
            foreground=self.colors["text"],
            fieldbackground=self.colors["white"],
            rowheight=30,
            font=("Segoe UI", 10),
        )
        style.configure(
            "Treeview.Heading",
            background=self.colors["green"],
            foreground=self.colors["white"],
            font=("Segoe UI", 10, "bold"),
            padding=8,
        )
        style.map("Treeview", background=[("selected", "#dce9df")],
                  foreground=[("selected", self.colors["text"])])

    def _build_ui(self):
        header = tk.Frame(self.root, bg=self.colors["green"], height=105)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header, text="HORSEMANAGER", bg=self.colors["green"],
            fg=self.colors["white"], font=("Segoe UI", 24, "bold")
        ).pack(anchor="w", padx=28, pady=(17, 0))
        tk.Label(
            header, text="Stable management system  |  Circular doubly linked list",
            bg=self.colors["green"], fg="#dce7df", font=("Segoe UI", 10)
        ).pack(anchor="w", padx=30, pady=(2, 0))

        content = tk.Frame(self.root, bg=self.colors["cream"])
        content.pack(fill="both", expand=True, padx=22, pady=18)

        left = tk.Frame(content, bg=self.colors["white"], highlightbackground="#deded5",
                        highlightthickness=1)
        left.pack(side="left", fill="y", padx=(0, 16))
        left.configure(width=320)
        left.pack_propagate(False)

        tk.Label(left, text="HORSE DETAILS", bg=self.colors["white"],
                 fg=self.colors["green"], font=("Segoe UI", 13, "bold")).pack(
                     anchor="w", padx=18, pady=(18, 12))

        self.fields = {}
        field_specs = [
            ("Horse ID", "horse_id"),
            ("Name", "name"),
            ("Breed", "breed"),
            ("Age", "age"),
        ]
        for label, key in field_specs:
            tk.Label(left, text=label, bg=self.colors["white"], fg=self.colors["muted"],
                     font=("Segoe UI", 9, "bold")).pack(anchor="w", padx=18, pady=(5, 3))
            entry = tk.Entry(left, font=("Segoe UI", 10), relief="solid", bd=1)
            entry.pack(fill="x", padx=18, ipady=6)
            self.fields[key] = entry

        tk.Label(left, text="Health status", bg=self.colors["white"],
                 fg=self.colors["muted"], font=("Segoe UI", 9, "bold")).pack(
                     anchor="w", padx=18, pady=(10, 3))
        self.health_var = tk.StringVar(value="Healthy")
        ttk.Combobox(left, textvariable=self.health_var, state="readonly",
                     values=("Healthy", "Under treatment", "Needs checkup")).pack(
                         fill="x", padx=18, ipady=4)

        tk.Label(left, text="Activity", bg=self.colors["white"],
                 fg=self.colors["muted"], font=("Segoe UI", 9, "bold")).pack(
                     anchor="w", padx=18, pady=(10, 3))
        self.activity_var = tk.StringVar(value="Training")
        ttk.Combobox(left, textvariable=self.activity_var, state="readonly",
                     values=("Training", "Riding", "Breeding", "Resting", "Competition")).pack(
                         fill="x", padx=18, ipady=4)

        button_frame = tk.Frame(left, bg=self.colors["white"])
        button_frame.pack(fill="x", padx=18, pady=(18, 8))
        self._button(button_frame, "Add horse", self._add_horse, self.colors["green"]).pack(
            fill="x", pady=3)
        self._button(button_frame, "Update selected", self._update_horse,
                     self.colors["green_light"]).pack(fill="x", pady=3)
        self._button(button_frame, "Delete selected", self._delete_horse,
                     self.colors["red"]).pack(fill="x", pady=3)
        self._button(button_frame, "Clear form", self._clear_form, "#727d75").pack(
            fill="x", pady=3)

        right = tk.Frame(content, bg=self.colors["cream"])
        right.pack(side="left", fill="both", expand=True)

        self.card = tk.Frame(right, bg=self.colors["green"], height=190)
        self.card.pack(fill="x")
        self.card.pack_propagate(False)

        tk.Label(self.card, text="CURRENT HORSE", bg=self.colors["green"],
                 fg=self.colors["gold"], font=("Segoe UI", 9, "bold")).pack(
                     anchor="w", padx=22, pady=(17, 4))
        self.current_name = tk.Label(self.card, text="No horse selected",
                                     bg=self.colors["green"], fg=self.colors["white"],
                                     font=("Segoe UI", 22, "bold"))
        self.current_name.pack(anchor="w", padx=22)
        self.current_details = tk.Label(self.card, text="Add a horse to get started.",
                                        bg=self.colors["green"], fg="#dce7df",
                                        font=("Segoe UI", 10), justify="left")
        self.current_details.pack(anchor="w", padx=22, pady=(5, 8))

        navigation = tk.Frame(right, bg=self.colors["cream"])
        navigation.pack(fill="x", pady=10)
        self._button(navigation, "← Previous", self._previous_horse,
                     self.colors["green"]).pack(side="left", padx=(0, 8))
        self._button(navigation, "Next →", self._next_horse,
                     self.colors["green"]).pack(side="left", padx=(0, 8))
        self._button(navigation, "Search by ID or name", self._search_horse,
                     self.colors["gold"], fg=self.colors["text"]).pack(side="left")

        self.counter = tk.Label(navigation, text="0 horses", bg=self.colors["cream"],
                                fg=self.colors["muted"], font=("Segoe UI", 10, "bold"))
        self.counter.pack(side="right", padx=4)

        list_header = tk.Frame(right, bg=self.colors["cream"])
        list_header.pack(fill="x", pady=(5, 7))
        tk.Label(list_header, text="REGISTERED HORSES", bg=self.colors["cream"],
                 fg=self.colors["green"], font=("Segoe UI", 12, "bold")).pack(side="left")

        columns = ("horse_id", "name", "breed", "age", "health", "activity")
        self.tree = ttk.Treeview(right, columns=columns, show="headings", height=9)
        headings = {
            "horse_id": "ID", "name": "Name", "breed": "Breed",
            "age": "Age", "health": "Health", "activity": "Activity",
        }
        widths = {"horse_id": 70, "name": 105, "breed": 100, "age": 45,
                  "health": 110, "activity": 95}
        for column in columns:
            self.tree.heading(column, text=headings[column])
            self.tree.column(column, width=widths[column], anchor="w")
        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<<TreeviewSelect>>", self._on_tree_select)

        tk.Label(
            right,
            text="Circular behavior: Next from the last horse returns to the first; Previous from the first returns to the last.",
            bg=self.colors["cream"], fg=self.colors["muted"],
            font=("Segoe UI", 9), wraplength=680, justify="left"
        ).pack(anchor="w", pady=(9, 0))

    def _button(self, parent, text, command, bg, fg="white"):
        return tk.Button(
            parent, text=text, command=command, bg=bg, fg=fg,
            activebackground=self.colors["gold"], activeforeground=self.colors["text"],
            relief="flat", cursor="hand2", font=("Segoe UI", 9, "bold"),
            padx=10, pady=8
        )

    def _load_sample_data(self):
        samples = [
            ("H001", "Thunder", "Andalusian", 6, "Healthy", "Training"),
            ("H002", "Spirit", "Mustang", 5, "Healthy", "Riding"),
            ("H003", "Shadow", "Arabian", 8, "Needs checkup", "Resting"),
        ]
        for horse_id, name, breed, age, health, activity in samples:
            self.horses.add(Horse(horse_id, name, breed, age, health, activity))

    def _form_values(self, include_id=True):
        horse_id = self.fields["horse_id"].get().strip()
        name = self.fields["name"].get().strip()
        breed = self.fields["breed"].get().strip()
        age_text = self.fields["age"].get().strip()

        if not name or not breed or not age_text or (include_id and not horse_id):
            raise ValueError("Please complete all fields.")
        try:
            age = int(age_text)
        except ValueError:
            raise ValueError("Age must be a whole number.")
        if age < 0 or age > 100:
            raise ValueError("Age must be between 0 and 100.")
        return horse_id, name, breed, age, self.health_var.get(), self.activity_var.get()

    def _add_horse(self):
        try:
            horse_id, name, breed, age, health, activity = self._form_values()
            if self.horses.find_node(horse_id) is not None:
                messagebox.showerror("Duplicate ID", "A horse with this ID already exists.")
                return
            self.horses.add(Horse(horse_id, name, breed, age, health, activity))
            self.horses.set_current(horse_id)
            self._refresh_view()
            self._clear_form()
            messagebox.showinfo("Success", "Horse added successfully.")
        except ValueError as error:
            messagebox.showerror("Invalid data", str(error))

    def _update_horse(self):
        selected = self._selected_horse()
        if selected is None:
            messagebox.showwarning("No selection", "Select a horse from the table first.")
            return
        try:
            _, name, breed, age, health, activity = self._form_values(include_id=False)
            selected.update(name, breed, age, health, activity)
            self._refresh_view()
            messagebox.showinfo("Success", "Horse updated successfully.")
        except ValueError as error:
            messagebox.showerror("Invalid data", str(error))

    def _delete_horse(self):
        selected = self._selected_horse()
        if selected is None:
            messagebox.showwarning("No selection", "Select a horse from the table first.")
            return
        if messagebox.askyesno("Confirm deletion", f"Delete {selected.name}?"):
            self.horses.remove(selected.horse_id)
            self._refresh_view()
            self._clear_form()

    def _selected_horse(self):
        selection = self.tree.selection()
        if not selection:
            return None
        return self.horses.find_node(selection[0]).horse if self.horses.find_node(selection[0]) else None

    def _on_tree_select(self, _event=None):
        horse = self._selected_horse()
        if horse:
            self.horses.set_current(horse.horse_id)
            self._show_horse(horse)
            self._fill_form(horse)

    def _fill_form(self, horse):
        values = {
            "horse_id": horse.horse_id, "name": horse.name,
            "breed": horse.breed, "age": str(horse.age),
        }
        for key, value in values.items():
            self.fields[key].delete(0, tk.END)
            self.fields[key].insert(0, value)
        self.health_var.set(horse.health_status)
        self.activity_var.set(horse.activity)

    def _clear_form(self):
        for entry in self.fields.values():
            entry.delete(0, tk.END)
        self.health_var.set("Healthy")
        self.activity_var.set("Training")
        self.tree.selection_remove(self.tree.selection())

    def _show_horse(self, horse):
        self.current_name.config(text=f"{horse.name}  ·  {horse.horse_id}")
        self.current_details.config(
            text=f"Breed: {horse.breed}     Age: {horse.age}\n"
                 f"Health: {horse.health_status}     Activity: {horse.activity}"
        )

    def _refresh_view(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for horse in self.horses.get_all():
            self.tree.insert("", "end", iid=horse.horse_id, values=(
                horse.horse_id, horse.name, horse.breed, horse.age,
                horse.health_status, horse.activity
            ))
        self.counter.config(text=f"{self.horses.size} horse(s)")
        current = self.horses.current.horse if self.horses.current else None
        if current:
            self._show_horse(current)
            if self.tree.exists(current.horse_id):
                self.tree.selection_set(current.horse_id)
                self.tree.focus(current.horse_id)
        else:
            self.current_name.config(text="No horse selected")
            self.current_details.config(text="Add a horse to get started.")

    def _next_horse(self):
        horse = self.horses.next_horse()
        if horse:
            self._refresh_view()

    def _previous_horse(self):
        horse = self.horses.previous_horse()
        if horse:
            self._refresh_view()

    def _search_horse(self):
        from tkinter.simpledialog import askstring
        query = askstring("Search horse", "Enter a horse ID or name:")
        if query is None or not query.strip():
            return
        horse = self.horses.set_current(query)
        if horse:
            self._refresh_view()
            self._fill_form(horse)
        else:
            messagebox.showinfo("Not found", "No horse matched your search.")

    def run(self):
        self.root.mainloop()
