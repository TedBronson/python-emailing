import requests
import smtplib

def get_emails():
    emails = {}

    try:
        email_file = open('emails2.txt', 'r')

        for line in email_file:
            (email, name) = line.split(',')
            emails[email] = name.strip()
                
    except FileNotFoundError as err:
        print(err)

    return emails

def get_schedule():
    try:
        schedule_file = open('schedule.txt', 'r')

        schedule = schedule_file.read()

    except FileNotFoundError as err:
        print(err)

    return schedule

def get_weather_forecast():
    url = 'http://api.openweathermap.org/data/2.5/weather?q=Kharkiv&units=metric&APPID=cbae6355a16c9ab4e4526a0bcb30395d'
    weather_request = requests.get(url)
    weather_json = weather_request.json()

    description = weather_json['weather'][0]['description']
    temp_min = weather_json['main']['temp_min']
    temp_max = weather_json['main']['temp_max']

    forecast = 'The Circus forecast for today is a '
    forecast += description + ' with a high of ' + str(temp_max)
    forecast += ' and a low of ' + str(temp_min) + '.'

    return forecast

def send_emails(emails, schedule, forecast):
    # connect to the smtp server
    server = smtplib.SMTP('smtp.gmail.com', '587')
    server.starttls()

    #Login
    password = input('What is your password?')
    from_email = 'tedbronson0@gmail.com'
    server.login(from_email, password)


    for to_email, name in emails.items():
        message = 'Subject: Welcome \n'
        message += 'Hi ' + name + '!\n\n'
        message += forecast + '\n\n'
        message += schedule
        server.sendmail(from_email, to_email, message)
    
    server.quit()
    

def main():
    emails = get_emails()
    print(emails)

    schedule = get_schedule()
    print(schedule)

    forecast = get_weather_forecast()
    print(forecast)

    send_emails(emails, schedule, forecast)

main()
