# Saudi-Arabia-COVID-19-Dashboard-Scraping
Scraping the data from the [COVID 19 Dashboard: Saudi Arabia](https://covid19.moh.gov.sa/) using Selenium and BeautifulSoup. 

## Usage

1. Install dependencies via pip:

    ```shell
    $ pip install -r requirements.txt
    ```
2. Install [Google Chrome](https://www.googleadservices.com/pagead/aclk?sa=L&ai=DChcSEwjO2fHJofToAhUNsO0KHRPcA88YABABGgJkZw&ohost=www.google.com&cid=CAESQOD2m7uj-RcgXhC03F2o8snI-YTPdGb9ruXgoJ5_nBbk3NQCRv0fxAmaI-98FxteASPMarkIn7JCjWW1c8vigoE&sig=AOD64_2t4_J7iqTcnTuJBUAS-SVo4Ar1rw&adurl=&q=&ved=2ahUKEwi8y-nJofToAhXVtHEKHXj9DUkQqyQoAHoECBUQBw).
3. Download [ChromeDriver](http://chromedriver.chromium.org/downloads), the ChromeDriver version has to match the Google Chrome version you have installed, and place the file in the program directory.
4. Run the program:
    ```shell
    $ python dashboard_scraper.py
    ```
5. Make sure that the page is fully loaded before it automatically closes, otherwise there might be some data missing.
6. Find the data in ksa_covid19.xlsx


## License
[Apache License 2.0](https://choosealicense.com/licenses/apache-2.0/)
