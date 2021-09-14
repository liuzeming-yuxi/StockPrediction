import numpy as np
import pandas as pd
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, ConstantKernel as C

import data_handler


class Wrapper:
    company_data = None
    quarters = None
    alpha = None
    iterations = None
    kernels = None
    gp = None

    def __init__(self, company_name: str):
        self.company_data = data_handler.CsvHandler(company_name)
        self.quarters = self.company_data.quarters
        self.years = self.company_data.years

        kernel = C(1.0, (1e-3, 1e3)) * RBF(10, (1e-2, 1e2))
        self.alpha = 0.5
        self.iterations = 10
        self.kernels = [kernel]
        self.gp = GaussianProcessRegressor(kernel=self.kernels[0], alpha=self.alpha, n_restarts_optimizer=self.iterations)

    def get_eval_model(self, start_year, end_year, prices):
        num = prices.shape[0]
        X = np.atleast_2d(np.linspace(0, num - 1, num)).T
        x = np.linspace(0, num - 1, num*10)
        x_prec = np.atleast_2d(x).T
        y = np.asarray(prices.loc[:, 'Adj Close'])

        self.gp.fit(X, y)
        y_pred, sigma = self.gp.predict(x_prec, return_cov=True)

        return x, y_pred, sigma

    def get_kernels(self):
        return self.__kernels
