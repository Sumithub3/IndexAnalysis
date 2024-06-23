import os
import shutil
import pickle
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
from AnalyseNSEData import AnalyseCSVData


class GetCSVDataFromNSE:
    def __init__(self):
        self.download_path = r'D:\IndexDataAnalysisAutomation\NSE_Data'
        self.DownloadCSVDataFromNSE(self.download_path)
        self.data = self.output_data()
    def DownloadCSVDataFromNSE(self, download_path):
        # Set Chrome WebDriver options
        chrome_options = Options()
        chrome_options.add_experimental_option('prefs', {
            'download.default_directory': download_path,
            'download.prompt_for_download': False,
            'download.directory_upgrade': True,
            'safebrowsing.enabled': True,
            'profile.default_content_setting_values.automatic_downloads': 1  # Allow automatic download
        })


        # Clear the download directory before starting the script
        clear_download_directory(download_path)

        chrome_options.add_argument("--disable-geolocation")
        chrome_options.add_argument("--disable-popup-blocking")
        chrome_options.add_argument("--disable-notifications")


        # Initialize Chrome WebDriver with options
        driver = webdriver.Chrome(options=chrome_options)

        # Navigate to the website
        driver.get("https://www.nseindia.com/option-chain?type=gsec")

        # Clear cookies
        driver.delete_all_cookies()
        # Find and click the download button
        try:
            equity_page = driver.find_element("id", "Equity_Stock_pg")
            equity_page.click()
            time.sleep(10)
            secTable = driver.find_element("id", "downloadOCTable")
            time.sleep(10)
            download_button = secTable.find_element("id", "download_csv")
            print("Element found and clickable")
            # Perform further actions like clicking the button
            download_button.click()
        except:
            print("Element not found or not clickable")


        # Wait for the download to complete (you may need to adjust the sleep time based on the file size and internet speed)
        time.sleep(10)

        # Close the WebDriver
        driver.quit()

    def output_data(self):
        response = AnalyseCSVData(self.download_path)
        with open(r"D:\IndexDataAnalysisAutomation\AnalysisData.pkl", "wb") as f:
            pickle.dump(response.export_output_data, f)
            print("data dump successfully.....")



# Function to clear the download directory
def clear_download_directory(path):
    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path)
# Set the download directory path
if __name__ == "__main__":
    # IP :: 192.168.1.5
    # port :: 816

    def recursive_function():
        print("Function called....... ")
        GetCSVDataFromNSE()
        # Wait for 5 minutes (300 seconds)
        time.sleep(2 * 60)   # 5 minutes
        # Call itself recursively

        recursive_function()


    recursive_function()


