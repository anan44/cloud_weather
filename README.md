# Weather polling solution

## Installation
* Make sure you are using Python version 3.6.4 or higher.
* It is recommended to use virtual environment since the package versions used might differ from your local installation.
* After setting up virtual environment of your choice run pip install -r requirements.txt to install all the packages used in this project.
* Running tests requires [OpenWeatherMAP](https://openweathermap.org/) API key to be set to file as instructed in How to use section.

## How to use?
* Make a copy from config_template.json with the name config.json.
* Fill in the configurations using the same formula as the template file.
* Add [OpenWeatherMap](https://openweathermap.org/) API key to designated field.
    * API key might take up to 10min to be activate.
* Execute the program by running main.py.
* Application will ignore locations that are not being supported by OpenWeatherMap
* Read results from ./logs/weather_log.txt.


## Config fields
In config file there is few fields which are quite self explanatory. Regardless of that they are also explained below:
* Location
	* name: Name of city to check weather from
	* low_limit: Low temperature threshold for temperature alerts
	* high_limit: High temperature threshold for temperature alerts
* pollin_interval_in_minutes: number of minutes between between queries done to the API. There is no hard limit on value, but it is advisable to avoid intervals smaller than 10min
* api_key: API key to [OpenWeatherMap](https://openweathermap.org/) API. Free keys available from the website
* days_checked: Number of days check on each round of polling the API. For example input value 5 will check weather for present day following 4 days.

## Limitations
* Days checked is limited to values between 1-15 days. Please avoid using
values outside the range.
* Number of locations should be limited to 30 due to OpenWeatherMapAPI
limitations
* Polling intervals lower than 1min should be avoided to avoid overloading the
OpenWeatherMap API
