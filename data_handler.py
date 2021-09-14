import pandas as pd
import numpy as np


class CsvHandler:
    df = None
    quarters = None
    years = None

    def __init__(self, csv_name: str):
        self.__load_data(csv_name)
        self.years = list(self.df.Date)
        self.years = list({self.years[i].year for i in range(0, len(self.years))})
        self.df['Quarter'] = self.__add_quarters(self.df)

    def get_year_data(self, year: int):
        if year not in self.years:
            raise ValueError('\n' +
                             'Input year: {} not in available years: {}'.format(year, self.years))

        prices = (self.df.loc[self.df['Date'].dt.year == year])

        return np.asarray(prices.loc[:, 'Adj Close'])

    def get_whole_prices(self, start_year: int, end_year: int):
        if start_year < self.years[0] or end_year > self.years[-1]:
            raise ValueError('\n' +
                             'Input years out of available range! \n' +
                             'Max range available: {}-{}\n'.format(self.years[0], self.years[-1]) +
                             'Was: {}-{}'.format(start_year, end_year))

        df = (self.df.loc[(self.df['Date'].dt.year >= start_year) & (self.df['Date'].dt.year <= end_year)])
        df = df.loc[:, ['Date', 'Adj Close']]

        return df

    def show(self, max_rows=None, max_columns=None):
        with pd.option_context('display.max_rows', max_rows, 'display.max_columns', max_columns):
            print(self.df)

    def __load_data(self, csv_name: str):
        self.df = pd.read_csv('Data/' + csv_name + '.csv')
        self.df = self.df.iloc[:, [0, 5]]
        self.df = self.df.dropna()
        self.df.Date = pd.to_datetime(self.df.Date)
        self.quarters = ['Q' + str(i) for i in range(1, 5)]

    def __add_quarters(self, df):
        quarters = pd.DataFrame()

        for i in range(0, len(self.years)):
            dates = list((df.loc[df['Date'].dt.year == self.years[i]]).iloc[:, 0])
            dates = pd.DataFrame([self.__get_quarter(dates[i].month) for i in range(0, len(dates))])
            quarters = quarters.append(dates, ignore_index=True)

        return quarters

    def __get_quarter(self, month: int):
        return self.quarters[(month - 1) // 3]