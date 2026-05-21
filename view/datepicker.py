import customtkinter as ctk
import tkinter as tk
from datetime import datetime, date

try:
    from tkcalendar import DateEntry
    TKCALENDAR_DISPO = True
except ImportError:
    TKCALENDAR_DISPO = False


class DatePickerWidget(ctk.CTkFrame):
    """Widget sélecteur de date : utilise tkcalendar si dispo, sinon 3 spinbox JJ/MM/AAAA."""
    def __init__(self, parent, **kwargs):
        super().__init__(parent, fg_color="transparent")
        self._var = ctk.StringVar()

        if TKCALENDAR_DISPO:
            self._entry = DateEntry(
                self, textvariable=self._var, date_pattern="dd/mm/yyyy",
                background="#313244", foreground="white", selectbackground="#89b4fa",
                selectforeground="black", normalbackground="#1e1e2e", normalforeground="white",
                headersbackground="#313244", headersforeground="#89b4fa", weekendforeground="#f38ba8",
                othermonthforeground="#6c7086", font=("Segoe UI", 11), width=14, borderwidth=0,
            )
            self._entry.grid(row=0, column=0, sticky="w")  # Grid instead of pack
        else:
            today = date.today()
            self._jour = tk.IntVar(value=today.day)
            self._mois = tk.IntVar(value=today.month)
            self._annee = tk.IntVar(value=today.year)

            tk.Spinbox(self, from_=1, to=31, textvariable=self._jour, width=3,
                       font=("Segoe UI", 11), bg="#313244", fg="white",
                       buttonbackground="#45475a").grid(row=0, column=0, padx=(0, 2))
            ctk.CTkLabel(self, text="/", font=("Segoe UI", 11)).grid(row=0, column=1)
            tk.Spinbox(self, from_=1, to=12, textvariable=self._mois, width=3,
                       font=("Segoe UI", 11), bg="#313244", fg="white",
                       buttonbackground="#45475a").grid(row=0, column=2, padx=(0, 2))
            ctk.CTkLabel(self, text="/", font=("Segoe UI", 11)).grid(row=0, column=3)
            tk.Spinbox(self, from_=1900, to=2100, textvariable=self._annee, width=5,
                       font=("Segoe UI", 11), bg="#313244", fg="white",
                       buttonbackground="#45475a").grid(row=0, column=4)

    def get(self) -> str:
        if TKCALENDAR_DISPO:
            return self._var.get()
        return f"{self._jour.get():02d}/{self._mois.get():02d}/{self._annee.get():04d}"

    def set(self, valeur: str):
        if not valeur:
            return
        for fmt in ("%d/%m/%Y", "%Y-%m-%d", "%Y-%m-%d %H:%M:%S"):
            try:
                d = datetime.strptime(str(valeur).strip(), fmt).date()
                if TKCALENDAR_DISPO:
                    self._entry.set_date(d)
                else:
                    self._jour.set(d.day)
                    self._mois.set(d.month)
                    self._annee.set(d.year)
                return
            except ValueError:
                continue

    def reset(self):
        today = date.today()
        if TKCALENDAR_DISPO:
            self._entry.set_date(today)
        else:
            self._jour.set(today.day)
            self._mois.set(today.month)
            self._annee.set(today.year)
