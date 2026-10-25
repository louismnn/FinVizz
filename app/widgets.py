from app.check_errors import check_errors
from CTkMessagebox import CTkMessagebox
from decimal import Decimal, InvalidOperation
import customtkinter as ctk
import pandas as pd
from typing import Optional
import json


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")


class DerivativeInput():

    def __init__(self):
        self.s = 100
        self.t_a = 0.5
        self.sigma = 0.15
        self.q = 0.01
        self.r = 0.02
        self.k1 = 90
        self.k2 = 100
        self.k3 = 110
        self.k4 = 120
        self.t1 = 1.0
        self.t2 = 1.5

        self.default_values = {
            "s": self.s,
            "k": self.k1,
            "k1": self.k1,
            "k2": self.k2,
            "k3": self.k3,
            "k4": self.k4,
            "t": self.t1,
            "t1": self.t1,
            "t2": self.t2,
            "t_a": self.t_a,
            "sigma": self.sigma,
            "r": self.r,
            "q": self.q
            }

        with open(r"app\assets\database.json", "r") as file:
            datas = json.load(file)
            
            self.dict_of_derivatives = dict(datas["dict_of_derivatives"])
            self.translate_names = dict(datas["translated_name"])
            self.boll_table = pd.DataFrame(datas["bool_table"])

    def _get_type(self, derivative_type : str) -> int:
        return self.dict_of_derivatives[derivative_type]

    def _build_kwargs(self, base_params : dict) -> dict:

        params = {
            "S": base_params.get("s"),
            "K": base_params.get("k"),
            "K1": base_params.get("k1"),
            "K2": base_params.get("k2"),
            "K3": base_params.get("k3"),
            "K4": base_params.get("k4"),
            "T": base_params.get("t"),
            "T1": base_params.get("t1"),
            "T2": base_params.get("t2"),
            "t_a": base_params.get("t_a"),
            "sigma": base_params.get("sigma"),
            "q": base_params.get("q"),
            "r": base_params.get("r")
        }

        return {k: v for k, v in params.items()}
    
    def _generate_widget(self, number) -> Optional[list]:

        root = ctk.CTk()
        root.title(self.derivative_type)
        self.values = None

        self.font = ctk.CTkFont(family="Helverica", size=12, weight="bold")

        entries = {}

        for j, col_name in enumerate(self.boll_table.columns):
 
            element = self.boll_table.loc[number, col_name]

            if element:
            
                Label = ctk.CTkLabel(root, text=self.translate_names.get(col_name), font=self.font)
                Label.grid(row=j, column=0, padx=10, pady=5)

                Entry = ctk.CTkEntry(root)
                Entry.grid(row=j, column=1, padx=10, pady=5)

                value = self.default_values.get(col_name)
                Entry.insert(0, str(value))

                entries[col_name] = Entry

        def submit():

            values = {}

            for key, Entry in entries.items():
                try:
                    values[key] = Decimal(Entry.get()) if Entry.get() not in ("NaN", "nan") else Decimal("a")

                except InvalidOperation:
                    CTkMessagebox(title="Input Error", message="Inputs must be integers or floats")
                    return

            try:
                values = self._build_kwargs(values)
                values.update({"product" : self.derivative_type})
                check_errors(**values)
                values.pop("product")

            except ValueError as e:
                CTkMessagebox(title="Input Error : ", message=e)
                return

            self.values = dict()
            for k,v in values.items():
                try:
                    self.values.update({k:float(v)})
                except TypeError:
                    self.values.update({k: v})

            root.destroy()

        def cancel():
            self.values = None
            root.destroy()

        button = ctk.CTkButton(root, text="Submit", text_color="black", hover=True, fg_color= "forest green", hover_color="SpringGreen4", font=self.font, command=submit)
        button.grid(row=15, column=0, columnspan=2, pady=10)

        root.protocol("WM_DELETE_WINDOW", cancel)
        root.attributes("-topmost", True)

        root.mainloop()

        if self.values is None:
            return None

        return list(self.values.values())

    def get_data(self, derivative_type: str) -> Optional[list]:

        self.derivative_type = derivative_type
        num = self._get_type(derivative_type=self.derivative_type)

        return self._generate_widget(number = num)
