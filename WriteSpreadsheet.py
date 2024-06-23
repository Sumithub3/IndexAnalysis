import requests
import json

class ExportToSreadsheet:
    def __init__(self, data):
        self.data = data
        self.print_response(data)
        self.spreadsheet_url = "https://script.google.com/macros/s/AKfycbw-PQgS8mx23gB55fpOdVEwkdqwZM4nP_khyiF8r0yF/dev"
        self.export_data = self.export_output_data()
        # self.write_data_to_spreadsheet(self.spreadsheet_url)
    def print_response(self, response):
        print(response)
    def write_data_to_spreadsheet(self, spreadsheet_url):
        """
        https://script.google.com/macros/s/your-web-app-id/exec?action=write&data={"Date":"2024-06-02T12:50:15.088Z","Strike_Price":"22600.00","Call_Current_Change":31941,"Call_Open_Interest":85649,"Call_Bid_Ask_Analysis":"Choppy","Call_Volume":1412968,"Call_Total_Volume":15181211,"PCR":0.7628777509650102,"Put_Current_Change":37451,"Put_Open_Interest":117459,"Put_Bid_Ask_Analysis":"Bearish","Put_Volume":1388151,"Put_Total_Volume":12222559}
        """

        try:
            # Define the JSON data


            # Convert data to JSON string
            json_data_str = json.dumps(self.data)

            # Construct the full URL
            # full_url = f"{spreadsheet_url}/exec?action=write&data={json_data_str}"
            response = requests.post(spreadsheet_url+'/exec', params={"action": "write", "data": json_data_str})

            # Send the GET request
            # response = requests.get(full_url)

            # Check the response
            if response.status_code == 200:
                self.print_response("Data posted successfully.")
                self.print_response("Response:" + response.text)
            else:
                self.print_response("Failed to post data.")
                self.print_response("Response Code:" + response.status_code)
                self.print_response("Response:" + response.text)

        except Exception as e:
            print(e)
    def export_output_data(self):
        return self.data

    def update_data_to_spreadsheet(self):
        """
        https://script.google.com/macros/s/your-web-app-id/exec?action=update

        """
        pass
    def get_data_from_spreadsheet(self):
        """
        https://script.google.com/macros/s/your-web-app-id/exec?action=read

        """
        pass

