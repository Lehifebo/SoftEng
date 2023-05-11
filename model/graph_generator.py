import pandas as pd
import matplotlib.pyplot as plt


class GraphGenerator:
    def __init__(self, maybe_path):
        self.maybe_path = maybe_path

    def fix_date(self, data):
        # Convert the 'Date' column to a datetime object
        data['Date'] = pd.to_datetime(data['Date'])
        data['Date'] = data['Date'].dt.strftime('%m-%d')
        # Set the 'Date' column as the index
        data.set_index('Date', inplace=True)
        return data

    def team_graph(self):
        # pathing needs to be fixed
        data = pd.read_csv("../historical_data/Config0001_data.csv")
        data = self.fix_date(data)
        # Create a figure and axis object
        fig, ax = plt.subplots()
        issues = ['Compliance result ID',
                  'Vulnerability ID', 'Total Vulnerability ID']
        for issue in issues:
            data[issue].plot(ax=ax, label=issue)

        # Set the title, legend, and axis labels
        ax.set_title('Issues for team x')
        ax.legend()
        ax.set_xlabel('Date')
        ax.set_ylabel('Count')

        # Show the plot
        plt.show()

    def get_data_tuples(self):
        datasets = []
        for x in range(1, 11):
            config_name = "Config{:04d}".format(x)
            historical_data = pd.read_csv("../historical_data/" + config_name + "_data.csv")
            historical_data = self.fix_date(historical_data)
            datasets.append((config_name, historical_data))
        return datasets

    def issue_graph(self, issue):
        # issue = 'Vulnerability ID'
        datasets = self.get_data_tuples()
        for config, data in datasets:
            # plot the 'y' column from both dataframes on the same graph
            plt.plot(data[issue], label=config)
            # add labels and legend
        plt.xlabel('Date')
        plt.ylabel(issue)
        plt.legend()

        # show the graph
        plt.show()

    def everything_graphs(self):
        datasets = self.get_data_tuples()
        issues = ['Compliance result ID',
                  'Vulnerability ID', 'Total Vulnerability ID']
        fig, axs = plt.subplots(nrows=1, ncols=3, figsize=(20, 8))
        for index, issue in enumerate(issues):
            # maybe here could use issue function but difference with axs
            for config, data in datasets:
                # plot the 'y' column from both dataframes on the same graph
                axs[index].plot(data[issue], label=config)
                # add labels and legend
            plt.xlabel('Date')
            plt.ylabel(issue)
            plt.legend()

            # show the graph
        plt.show()


if __name__ == "__main__":
    gg = GraphGenerator("idk")
    gg.team_graph()
