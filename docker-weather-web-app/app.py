
from flask import Flask, request, render_template #create the app, get user input, communicate to html
from data_processing import process_forecast_data, get_weather_data #proccess data from user and weather server
from database import store_daily_summaries, init_db # handle database things
from error_handler import handle_error # handle error when getting data from weather server
import setup # configure the app according to environment (Docker or local)


app = Flask(__name__)
db = setup.configure_app(app)
if isinstance(db, str):
    init_db()


@app.route('/', methods=['GET', 'POST'])
def weather():
    """
    core function for handling weather data requests and responses.
    serves as the main entry point for the weather-related operations.
    :return: renders html file
    """
    location = 'london'
    if request.method == 'POST':
        location = request.form.get('location')

    weather_data, error_code = get_weather_data(location)

    if weather_data:
        daily_summaries = process_forecast_data(weather_data['list'])
        store_daily_summaries(db, location, daily_summaries)

        return render_template('index.html', location=location, country=weather_data['city']['country'],
                               daily_summaries=daily_summaries)
    else:
        error_str = handle_error(error_code)
        return render_template('index.html', error_data=error_str)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
