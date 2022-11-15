import csv
from datetime import datetime

DEGREE_SYBMOL = "\N{DEGREE SIGN}C"


def format_temperature(temp) -> str:
    """Takes a temperature and returns it in string format with the degrees
        and celcius symbols.

    Args:
        temp: A string representing a temperature.
    Returns:
        A string contain the temperature and "degrees celcius."
    """
    return f"{temp}{DEGREE_SYBMOL}"


def convert_date(iso_string: str) -> str:
    """Converts and ISO formatted date into a human readable format.

    Args:
        iso_string: An ISO date string..
    Returns:
        A date formatted like: Weekday Date Month Year e.g. Tuesday 06 July 2021
    """
    dt = datetime.fromisoformat(iso_string)
    return dt.strftime("%A %d %B %Y")


def convert_f_to_c(temp_in_farenheit: float) -> float:
    """Converts an temperature from farenheit to celcius.

    Args:
        temp_in_farenheit: float representing a temperature.
    Returns:
        A float representing a temperature in degrees celcius, rounded to 1dp.
    """
    return round((float(temp_in_farenheit) - 32) * 5 / 9, 1)


def calculate_mean(weather_data: list[int | float]) -> float:
    """Calculates the mean value from a list of numbers.

    Args:
        weather_data: a list of numbers.
    Returns:
        A float representing the mean value.
    """
    # not using sum
    total = 0
    for x in weather_data:
        total += float(x)
    return total / len(weather_data)


def load_data_from_csv(csv_file: str) -> list[list]:
    """Reads a csv file and stores the data in a list.

    Args:
        csv_file: a string representing the file path to a csv file.
    Returns:
        A list of lists, where each sublist is a (non-empty) line in the csv file.
    """

    def is_iso_format(iso_str: str) -> bool:
        """Takes a string, checks if its iso format."""
        try:
            datetime.fromisoformat(iso_str)
            return True
        except Exception as e:
            return False

    def number_or_string(num_str: str) -> str | int | float:
        try:
            return int(num_str)
        except ValueError:
            pass
        try:
            return float(num_str)
        except ValueError:
            pass
        return num_str

    output_list = []
    with open(csv_file) as f:
        csv_reader = csv.reader(f)
        for row in csv_reader:
            if len(row) == 3:  # if the length of the row is three
                date, min, max = row  # split the row into variable names
                if is_iso_format(date):  # check the date is a date
                    output_list.append(
                        [date, number_or_string(min), number_or_string(max)]
                    )  # put values on list
    return output_list


def find_min(weather_data: list[float | int]) -> None | tuple[float, int]:
    """Calculates the minimum value in a list of numbers.

    Args:
        weather_data: A list of numbers.
    Returns:
        The minium value and it's position in the list.
    """
    # without using min
    found_id = None
    found_val = None
    for idx, val in enumerate(weather_data):
        if not found_val or float(val) <= found_val:
            found_id = idx
            found_val = float(val)
    if found_id is None:
        return ()
    return found_val, found_id


def find_max(weather_data: list[float | int]) -> tuple[float, int]:
    """Calculates the maximum value in a list of numbers.

    Args:
        weather_data: A list of numbers.
    Returns:
        The maximum value and it's position in the list.
    """
    found_id = None
    found_val = None
    for idx, val in enumerate(weather_data):
        if not found_val or float(val) >= found_val:
            found_id = idx
            found_val = float(val)
    if found_id is None:
        return ()
    return found_val, found_id


def generate_summary(weather_data: list[list]) -> str:
    """Outputs a summary for the given weather data.

    Args:
        weather_data: A list of lists, where each sublist represents a day of weather data.
    Returns:
        A string containing the summary information.
    """
    date_list = [x[0] for x in weather_data]
    min_list = [x[1] for x in weather_data]
    max_list = [x[2] for x in weather_data]
    low_val, low_id = find_min(min_list)
    high_val, high_id = find_max(max_list)
    high_avg = calculate_mean(max_list)
    low_avg = calculate_mean(min_list)
    return f"""{len(weather_data)} Day Overview
  The lowest temperature will be {format_temperature(convert_f_to_c(low_val))}, and will occur on {convert_date(date_list[low_id])}.
  The highest temperature will be {format_temperature(convert_f_to_c(high_val))}, and will occur on {convert_date(date_list[high_id])}.
  The average low this week is {format_temperature(convert_f_to_c(low_avg))}.
  The average high this week is {format_temperature(convert_f_to_c(high_avg))}.
"""


def generate_daily_summary(weather_data: list[list]) -> str:
    """Outputs a daily summary for the given weather data.

    Args:
        weather_data: A list of lists, where each sublist represents a day of weather data.
    Returns:
        A string containing the summary information.
    """
    output = ""
    for day in weather_data:
        date_str, min_val, max_val = day
        output += f"""---- {convert_date(date_str)} ----
  Minimum Temperature: {format_temperature(convert_f_to_c(min_val))}
  Maximum Temperature: {format_temperature(convert_f_to_c(max_val))}

"""

    return output
