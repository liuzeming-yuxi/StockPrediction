import matplotlib.pyplot as plt
plt.ion()
import matplotlib.dates as mdates
import numpy as np
import data_handler
import gpr_wrapper


class Plotter:
    company_name = None
    company_handler = None
    quarters = None
    years = None
    gpr = None
    extreme = []

    def __init__(self, company_name: str):
        self.company_name = company_name
        self.company_handler = data_handler.CsvHandler(company_name)
        self.quarters = self.company_handler.quarters
        self.years = self.company_handler.years
        self.gpr = gpr_wrapper.Wrapper(company_name)

    def show_gpr(self, train_start: int, train_end: int):
        self.validate_dates(start_year=train_start, end_year=train_end)

        prices = self.company_handler.get_whole_prices(train_start, train_end)
        prices = prices[prices.iloc[:].notnull()]

        fig = plt.figure(num=self.company_name + ' prediction')
        ax = plt.gca()
        fig.set_size_inches(12, 6)
        x_obs = np.linspace(0, prices.shape[0] - 1, prices.shape[0])

        x, y_mean, y_cov = self.gpr.get_eval_model(train_start, train_end, prices)

        y_lower = y_mean - np.sqrt(np.diag(y_cov))
        y_upper = y_mean + np.sqrt(np.diag(y_cov))
        y_max = max(y_upper) * 1.1
        ax.set_ylim(bottom=0, top=y_max)

        x_min, x_max = x_obs[0], x_obs[-1]
        ax.set_xlim(left=x_min, right=x_max)

        plt.plot(x_obs, prices.loc[:, 'Adj Close'], color='#006699', alpha=.95, label=u'Observations ', zorder=10)
        plt.plot(x, y_mean, color='#ff0066', linestyle='--', label=u'Prediction')
        plt.fill_between(x, y_lower, y_upper, alpha=.25, label='95% confidence', color='#ff0066')

        handles, labels = plt.gca().get_legend_handles_labels()
        new_labels, new_handles = [], []
        for handle, label in zip(handles, labels):
            if label not in new_labels:
                new_labels.append(label)
                new_handles.append(handle)
        plt.legend(new_handles, new_labels, bbox_to_anchor=(0.01, 0.02), loc='lower left', borderaxespad=0.)

        plt.grid(True, alpha=.25)
        plt.title(self.company_name)
        plt.xlabel('Days\n')
        plt.ylabel('Price')

        plt.tight_layout()

        fname = '{}_{}__{}prediction.png'.format(self.company_name, train_start, train_end)
        fig.savefig(fname, dpi=fig.dpi)
        plt.clf()
        return x, y_mean

    def show_whole_time_series(self, intermediate: bool = False):
        self.show_time_series(start_year=self.years[0], end_year=self.years[-1], intermediate=intermediate)

    def show_time_series(self, start_year: int, end_year: int):
        self.validate_dates(start_year=start_year, end_year=end_year)

        prices_data = self.company_handler.get_whole_prices(start_year=start_year, end_year=end_year)

        fig = plt.figure(num=self.company_name + ' prices')
        fig.set_size_inches(12, 6)
        plt.plot(prices_data.iloc[:, 0], prices_data.iloc[:, 1], color='#006699', alpha=.95,
                 label=u'Observations ' + str(start_year) + '-' + str(end_year), zorder=10)
        ax = plt.gca()

        x_ticks = []
        for year in range(start_year, end_year + 2):
            if year == end_year + 1:
                current_date = prices_data[prices_data['Date'].dt.year == end_year].iloc[-1, 0]
            else:
                current_date = prices_data[prices_data['Date'].dt.year == year].iloc[0, 0]
            x_ticks.append(current_date)
        x_formatter = mdates.DateFormatter('%Y-%m-%d')
        ax.xaxis.set_major_formatter(x_formatter)
        ax.set_xticks(x_ticks)
        plt.xticks(rotation=20)
        y_min, y_max = ax.get_ylim()
        x_min, x_max = ax.get_xlim()
        ax.set_ylim(bottom=y_min, top=y_max)
        ax.set_xlim(left=x_min, right=x_max)

        for i in range(0, len(x_ticks)):
            plt.vlines(x=x_ticks[i], ymin=y_min, ymax=y_max, color='black', linestyles='--', alpha=.6,
                       zorder=-1)

        plt.grid(True, alpha=0.25)
        plt.legend()
        plt.title(self.company_name)
        plt.ylabel('Price')

        plt.tight_layout()

        fname = '{}_{}_{}_prices.png'.format(self.company_name, start_year, end_year)
        fig.savefig(fname, dpi=fig.dpi)
        plt.clf()

    def validate_dates(self, start_year: int, end_year: int):
        if start_year < self.years[0] or end_year > self.years[-1]:
            raise ValueError('\n' +
                             'Input years out of available range! \n' +
                             'Max range available: {}-{}\n'.format(self.__years[0], self.__years[-1]) +
                             'Was: {}-{}'.format(start_year, end_year))

    def update(self, X, Y):
        self.extreme = []
        if X.shape[0] != Y.shape[0]:
            raise ValueError('\n' +
                             'The shape of X and Y is not equal }' + '\n')
        if(X.shape[0] == 0):
            return
        self.extreme.append([X[0], Y[0]])
        for i in range(1,X.shape[0]-1):
            if Y[i] >= Y[i-1] and Y[i] >= Y[i+1] or Y[i] <= Y[i-1] and Y[i] <= Y[i+1]:
                self.extreme.append([X[i], Y[i]])
        self.extreme.append([X[-1], Y[-1]])