import os
import data_plotter
import mode_match

companies = []
modematch = None
plotters = {}



def init_data():
    for company in os.listdir('Data'):
        current_company = company.split('.')[0]
        companies.append(current_company)
        plotters[current_company] = (data_plotter.Plotter(company_name=current_company))


if __name__ == "__main__":
    init_data()
    for company in companies:
        plotter = plotters[company]
        end_year = plotter.years[-1]
        start_year = max(plotter.years[0], end_year - 1)
        plotter.show_time_series(start_year, end_year)
        x, y = plotter.show_gpr(train_start=start_year, train_end=end_year)
        plotter.update(x, y)
        modematch = mode_match.ModeMatch(0.8, 0.2)
        modematch.fit(plotter.extreme)
        print(modematch.predict_w())
        print(modematch.predict_m())
        print(modematch.cal_error())