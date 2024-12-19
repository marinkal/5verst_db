from datetime import datetime, timedelta


def generate_dates(start: str, format: str):
    current_d = datetime.strptime(start, format)
    end_d = datetime.today()
    while current_d < end_d:
        yield datetime.strftime(current_d, '%d.%m.%Y')
        current_d = current_d + timedelta(days=7)
