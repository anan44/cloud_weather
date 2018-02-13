# Weather polling solution

## How to use?
* Make a copy from config_template.json with name config.json.
* Fill the file using the same formula as the template file.
* Add OpenWeatherApi API key to designated field.
* Execute the program by running main.py.
* Read results from ./logs/weather_log.txt.

## Limitations
* Days checked is limited to values between 1-15 days. Please avoid using
values outside the range.
* Number of locations should be limited to 30 due to OpenWeatherMapAPI
limitations.
* Polling intervals lower than 1min should be avoided to avoid overloading the
OpenWeatherMap API.
