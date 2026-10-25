import blackscholes as bs
import app.functions as fn
import pandas as pd
import numpy as np
import inspect
import json
from functools import lru_cache



with open(r"app\assets\database.json", "r") as file:
    datas = json.load(file)

    list_of_derivatives = dict(datas["list_of_derivatives"])


def return_class(classe: str):
    file_name, class_name = classe.split(".", maxsplit=1)

    if file_name == "fn":
        return getattr(fn, class_name)

    if file_name == "bs":
        return getattr(bs, class_name)

    raise ValueError(f"Unsupported derivative module: {file_name}")


@lru_cache(maxsize=1)
def get_derivative_metadata() -> tuple[dict[str, type], dict[str, set[str]]]:
    derivative_classes = {
        name: return_class(path) for name, path in list_of_derivatives.items()
    }
    allowed_params = {
        name: set(inspect.signature(cls.__init__).parameters)
        for name, cls in derivative_classes.items()
    }
    return derivative_classes, allowed_params


class File():

    def __init__(self):

        self._param_columns = ["S", "K", "K1", "K2", "K3", "K4", "T", "T1", "T2", "t_a", "sigma", "q", "r"]
        self.number = 0

        self.S = np.arange(1,250,1)
        self.R = np.arange(-0.05, 0.697, 0.003)

        self.derivatives_types = [None] * 10

        self.deltas = np.zeros((10, 249))
        self.vegas = np.zeros((10, 249))
        self.rhos = np.zeros((10, 249))
        self.gammas = np.zeros((10, 249))
        self.thetas = np.zeros((10, 249))
        self.overall = np.zeros((5, 249))

        self.datas = pd.DataFrame(columns=self._param_columns, index=[n for n in range(10)])

        self._derivative_classes, self.allowed_params = get_derivative_metadata()

    def _build_kwargs(self, base_params: dict, variable: int | float, derivative_type: str, vector_type: str = "s") -> dict:

        params = {
            "S": variable if vector_type == 's' else base_params["S"],
            "K": base_params["K"],
            "K1": base_params["K1"],
            "K2": base_params["K2"],
            "K3": base_params["K3"],
            "K4": base_params["K4"],
            "T": base_params["T"],
            "T1": base_params["T1"],
            "T2": base_params["T2"],
            "t_a": base_params["t_a"],
            "sigma": base_params["sigma"],
            "q": base_params["q"],
            "r": variable if vector_type == 'r' else base_params["r"]
        }

        allowed_params = self.allowed_params[derivative_type]
        return {k: v for k, v in params.items() if k in allowed_params and v is not None}

    def _compute_greek(self, derivative_type : str, i : int, greek : str, ) -> np.array:

        my_class = self._derivative_classes[derivative_type]
        row = self.datas.iloc[i].to_dict()

        my_vector = self.R if greek == "Rho" else self.S
        vec_ty = "r" if greek == "Rho" else "s"

        return np.array([
            getattr(my_class(**self._build_kwargs(row, el, derivative_type, vec_ty)), greek.lower())()
            for el in my_vector
        ])

    def _compute_greeks(self, derivative_type: str, base_params: dict) -> dict[str, np.ndarray]:
        derivative_class = self._derivative_classes[derivative_type]
        greeks = {
            name: np.empty(self.S.size, dtype=float)
            for name in ("delta", "gamma", "vega", "theta")
        }
        spot_kwargs = self._build_kwargs(
            base_params, base_params["S"], derivative_type, vector_type="s"
        )

        for index, spot in enumerate(self.S):
            spot_kwargs["S"] = spot
            derivative = derivative_class(**spot_kwargs)
            for name in greeks:
                greeks[name][index] = getattr(derivative, name)()

        rho = np.empty(self.R.size, dtype=float)
        rate_kwargs = self._build_kwargs(
            base_params, base_params["r"], derivative_type, vector_type="r"
        )
        for index, rate in enumerate(self.R):
            rate_kwargs["r"] = rate
            rho[index] = derivative_class(**rate_kwargs).rho()

        greeks["rho"] = rho
        return greeks

    def _compute_portfolio(self) -> None:

        all_greeks = [self.deltas, self.gammas, self.vegas, self.thetas, self.rhos]

        for m, greek_matrix in enumerate(all_greeks):
            self.overall[m] = greek_matrix.sum(axis=0)

    def add_element(self, derivative_type : str, data : list) -> None:

        self.datas.loc[self.number] = data
        self.derivatives_types[self.number] = derivative_type
        base_params = dict(zip(self._param_columns, data))

        greeks = self._compute_greeks(derivative_type, base_params)
        self.deltas[self.number] = greeks["delta"]
        self.gammas[self.number] = greeks["gamma"]
        self.vegas[self.number] = greeks["vega"]
        self.thetas[self.number] = greeks["theta"]
        self.rhos[self.number] = greeks["rho"]

        if self.number == 9:
            self.number = 0
        else:
            self.number += 1

        self._compute_portfolio()
