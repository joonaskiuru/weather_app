from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import customtkinter as ctk

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Simple Weather App")
        self.geometry("500x290")
        self.minsize(500,290)

        # create 2x2 grid system
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure((0, 1), weight=1)

        self.cityEntry = ctk.CTkEntry(master=self,placeholder_text="Enter a City")
        self.cityEntry.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        self.button = ctk.CTkButton(master=self, command=self.get_report, text="Get Weather")
        self.button.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        self.label1 = ctk.CTkLabel(master=self,bg_color="#303030",text="URL Status")
        self.label1.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

        self.textbox = ctk.CTkTextbox(master=self)
        self.textbox.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

    def get_report(self):
        # set options to browser
        browser = webdriver.Chrome(options=self.set_options())

        city = self.cityEntry.get().capitalize()
        url, valid = self.validate_url(city)

        # If url is valid, continue
        if valid:
            html = self.get_html(browser, url)
            report = self.get_soup(html)
            self.print_report(report, city)

    # Set Chromedriver Options
    def set_options(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('headless')
        chrome_options.add_experimental_option('excludeSwitches',['enable-logging'])
        return chrome_options

    # Validate Url
    def validate_url(self,city):
        valid = False
        url = "https://www.foreca.fi/Finland/" + city
        req = requests.get(url)
        if req.status_code == 200:
            self.label1.configure(text=f"Getting the weather from: {url}",text_color="green")
            valid = True
        else:
            msg = (f'Error: Url "{url}" is unreachable.')
            self.label1.configure(text=msg,text_color="red")
        return url, valid

    # Get the weather report from the url
    def get_soup(self,html):
        soup = BeautifulSoup(html, "html.parser")
        all_div = soup.find("div",{"id":"mg-hover-info"})
        report = all_div.text.split("  ")
        report = [i for i in report if i]
        report = "\n".join(report)
        return report

    # Print the report into the textbox
    def print_report(self,report,city):
        weather_info = f'Kaupunki: {city} \nTämän päivän sää:\n{report}'
        self.textbox.insert("0.0", weather_info)
        return

    def get_html(self, browser, url):
        browser.get(url)
        html = browser.page_source
        browser.quit()
        return html

if __name__ == '__main__':
    # Dark Mode
    ctk.set_appearance_mode("dark")
    app = App()
    app.mainloop()
