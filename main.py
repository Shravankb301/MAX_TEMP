import tkinter as tk
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import norm
import os

class TemperatureAnalysisGUI:
    def __init__(self, master):
        self.master = master
        master.title("Temperature Analysis")
        master.configure(bg='white')

        # Create the input label and entry widget
        self.input_label = tk.Label(master, text="Enter the path to the CSV file:", font=('Arial', 12), padx=10, pady=10)
        self.input_label.pack()
        self.input_entry = tk.Entry(master, width=50, font=('Arial', 12))
        self.input_entry.pack()

        # Create the submit button
        self.submit_button = tk.Button(master, text="Submit", command=self.submit, font=('Arial', 12), padx=10, pady=10, bg='white', fg='black', relief='raised', cursor='hand2')

        self.submit_button.pack()

        # Create the output text widget
        self.output_text = tk.Text(master, height=10, width=50, font=('Arial', 12), padx=10, pady=10)
        self.output_text.pack()

    def submit(self):
        # Get the CSV file path from the input entry widget
        csv_path = self.input_entry.get()

        # Check if file exists
        if not os.path.exists(csv_path):
            self.output_text.insert(tk.END, f"{csv_path} does not exist\n")
            return

        try:
            # Load data from the CSV file
            data = pd.read_csv(csv_path, parse_dates=['Year'], index_col=['Year'])
        except:
            self.output_text.insert(tk.END, "Invalid CSV file format\n")
            return

        # Check that the data contains the expected columns
        expected_columns = ['Maximum temperature']
        if not set(expected_columns).issubset(set(data.columns)):
            self.output_text.insert(tk.END, f"CSV file must contain columns {expected_columns}\n")
            return

        # Filter data to include only January dates
        data = data.loc[data.index.month == 1]

        # Calculate mean and standard deviation
        mean_temp = data['Maximum temperature'].mean()
        std_temp = data['Maximum temperature'].std()

        # Calculate Tmax at 95th percentile using the normal distribution
        tmax_95 = norm.ppf(0.95, loc=mean_temp, scale=std_temp)

        # Plot histogram of daily maximum temperature
        plt.hist(data['Maximum temperature'], bins=15)
        plt.title('Histogram of Daily Maximum Temperature in January at Melbourne Airport', fontdict={'fontsize': 14})
        plt.xlabel('Temperature (°C)', fontdict={'fontsize': 12})
        plt.ylabel('Frequency', fontdict={'fontsize': 12})
        plt.show()

        # Print mean, standard deviation, and Tmax at 95th percentile
        output_str = f"Mean temperature: {round(mean_temp, 2)} °C\n" \
                     f"Standard deviation: {round(std_temp, 2)} °C\n" \
                     f"Tmax at 95th percentile: {round(tmax_95, 2)} °C\n"
        self.output_text.insert(tk.END, output_str)

root = tk.Tk()
gui = TemperatureAnalysisGUI(root)
root.mainloop()



