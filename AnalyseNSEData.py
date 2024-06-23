import datetime
import json
import os

import pandas as pd

from WriteSpreadsheet import ExportToSreadsheet
class AnalyseCSVData:
    def __init__(self, csv_file_path):
        files = os.listdir(csv_file_path)
        file = [file for file in files if 'option-chain' in file and str(file).endswith('.csv')][0]
        self.file_path = os.path.join(csv_file_path, file)
        calls_data, strikes, puts_data = self.read_csv(self.file_path)
        self.calls_data = calls_data
        self.strikes = strikes
        self.puts_data = puts_data
        self.PCR_value = self.calculatePCR()
        self.Puts_Total_Volume = self.Volume("Puts")
        self.Calls_Total_Volume = self.Volume("Calls")
        self.Calls_Bid_Ask_Spread_Volume_Prediction = self.Bid_Ask_Spread_Volume_Prediction("Calls")
        self.Puts_Bid_Ask_Spread_Volume_Prediction = self.Bid_Ask_Spread_Volume_Prediction("Puts")
        export_data = self.ExportDataToWrite()
        export_data = ExportToSreadsheet(export_data)
        self.export_output_data = export_data.export_data
    @staticmethod
    def read_csv(file_path):
        # Read the CSV file into a pandas DataFrame
        df = pd.read_csv(file_path, skiprows=1)

        # Separate the DataFrame into CALLS, STRIKE, and PUTS
        calls_data = df.iloc[:, :df.columns.get_loc('STRIKE')]
        strikes = df['STRIKE']
        puts_data = df.iloc[:, df.columns.get_loc('STRIKE') + 1:]

        # Remove columns with all NaN values from calls_data and puts_data
        calls_data = calls_data.dropna(axis=1, how='all')
        puts_data = puts_data.dropna(axis=1, how='all')

        return calls_data, strikes, puts_data

    def calculatePCR(self):
        """
        PCR = Total Put Open Interest / Total Put Open Interest
        """
        calls_oi = self.sum_column_data(self.calls_data, 'OI')
        puts_oi = self.sum_column_data(self.puts_data, 'OI.1')

        totalPCR = puts_oi/calls_oi
        return totalPCR
    @staticmethod
    def simplify_column(data, column_name):
        try:
            column = data[column_name]
            column_numeric = pd.to_numeric(column.apply(lambda x: 0 if x == "-"
            else x.replace(',', '')))
            return column_numeric
        except Exception as e:
            return -1
    @staticmethod
    def sum_column_data(data, column_name):
        try:
            column_numeric = AnalyseCSVData.simplify_column(data, column_name)
            return column_numeric.sum()
        except KeyError:
            # Handle the case where the column does not exist
            print(f"Column '{column_name}' does not exist in the DataFrame.")
            return 0
    def Volume(self, volume_to_calculate):
        total_volume = 0
        if volume_to_calculate == "Calls":
            total_volume = self.sum_column_data(self.calls_data, 'VOLUME')
        if volume_to_calculate == "Puts":
            total_volume = self.sum_column_data(self.puts_data, 'VOLUME.1')
        return total_volume
    @staticmethod
    def get_max_value_and_index(data, column_name, top=0):
        "Get highest index according to top default is 0'th"
        simplified_column = AnalyseCSVData.simplify_column(data, column_name)
        sorted_indices = simplified_column.sort_values(ascending=False).index
        return sorted_indices[top], simplified_column[sorted_indices[top]]

    def get_data_by_column_index(self, data, column_name, index):
        column = self.simplify_column(data, column_name)
        return column[index]
    def Bid_Ask_Spread_Volume_Prediction(self, call_put):
        data = None
        column_nm = ''
        bidQty = ""
        bid = ""
        ask = ""
        askQty = ""
        index_of_high_volume = 0
        if call_put == "Calls":
            data = self.calls_data
            column_nm = "VOLUME"
            bidQty = "BID QTY"
            bid = "BID"
            ask = "ASK"
            askQty = "ASK QTY"
            self.call_index_of_high_volume, self.call_high_volume_value = self.get_max_value_and_index(data, column_nm)
            index_of_high_volume = self.call_index_of_high_volume
        if call_put == "Puts":
            data = self.puts_data
            column_nm = "VOLUME.1"
            bidQty = "BID QTY.1"
            bid = "BID.1"
            ask = "ASK.1"
            askQty = "ASK QTY.1"
            self.put_index_of_high_volume, self.put_high_volume_value = self.get_max_value_and_index(data, column_nm)
            index_of_high_volume = self.put_index_of_high_volume


        bid_volume_column = list(self.simplify_column(data, bidQty))
        bid_column = list(self.simplify_column(data, bid))
        ask_column = list(self.simplify_column(data, ask))
        ask_volume_column = list(self.simplify_column(data, askQty))

        self.bid_ask_Spread = ask_column[index_of_high_volume] - bid_column[index_of_high_volume]
        self.bid_ask_volume_ratio = ask_volume_column[index_of_high_volume] / bid_volume_column[index_of_high_volume]

        if self.bid_ask_Spread > 10 and self.bid_ask_volume_ratio > 1.1:
            return "Super Bullish"
        elif self.bid_ask_Spread < 0 and self.bid_ask_volume_ratio > 1.1:
            return "Super Bearish"
        elif self.bid_ask_Spread < 5 and self.bid_ask_volume_ratio < 1.0:
            return "Bearish"
        elif self.bid_ask_Spread < 0 and self.bid_ask_volume_ratio < 1.0:
            return "Neutral"
        else:
            return "Choppy"

    def ExportDataToWrite(self):
        """
        [[Date, Strike_Price, Call_Current_Change, Call_Open_Interest, Call_Bid_Ask_Analysis,
        Call_Volume, Call_Total_Volume, PCR, Put_Current_Change, Put_Open_Interest,
        Put_Bid_Ask_Analysis, Put_Volume, Put_Total_Volume]]
        """
        data_serializable = {
            "Date": str(datetime.datetime.utcnow()),
            "Strike_Price": float(self.strikes[self.call_index_of_high_volume].replace(',','')),
            "Call_Current_Change": int(self.get_data_by_column_index(self.calls_data, "CHNG IN OI", self.call_index_of_high_volume)),
            "Call_Open_Interest":int(self.get_data_by_column_index(self.calls_data, "OI", self.call_index_of_high_volume)),
            "Call_Bid_Ask_Analysis": str(self.Calls_Bid_Ask_Spread_Volume_Prediction),
            "Call_Volume": int(self.call_high_volume_value),
            "Call_Total_Volume": int(self.Calls_Total_Volume),
            "PCR": float(self.PCR_value),
            "Put_Current_Change": int(self.get_data_by_column_index(self.puts_data, "CHNG IN OI.1", self.put_index_of_high_volume)),
            "Put_Open_Interest": int(self.get_data_by_column_index(self.puts_data, "OI.1", self.put_index_of_high_volume)),
            "Put_Bid_Ask_Analysis": str(self.Puts_Bid_Ask_Spread_Volume_Prediction),
            "Put_Volume": int(self.put_high_volume_value),
            "Put_Total_Volume": int(self.Puts_Total_Volume)
        }
        # Serialize the data to JSON
        # json_data_str = json.dumps(data_serializable)
        return data_serializable
    def analyse_output_data(self):
        response = self.ExportDataToWrite
        return response

def main():
    # Specify the path to your CSV file
    file_path = r'D:\IndexDataAnalysisAutomation\NSE_Data'  # Change this to the actual path of your CSV file

    # Read the CSV data
    data = AnalyseCSVData(file_path)

    # Print the CSV data
    print("CALLS Data:")
    print(data.calls_data)
    print("\nSTRIKES:")
    print(data.strikes)
    print("\nPUTS Data:")
    print(data.puts_data)
    print("\nPCR Value :: ")
    print(data.PCR_value)
    print("\nCAlls Volume :: ")
    print(data.Calls_Total_Volume)
    print("\nPuts Volume :: ")
    print(data.Puts_Total_Volume)
    print("\nCAlls BID/ASK :: ")
    print(data.Calls_Bid_Ask_Spread_Volume_Prediction)
    print("\nPuts BID/ASK :: ")
    print(data.Puts_Bid_Ask_Spread_Volume_Prediction)

if __name__ == "__main__":
    main()
