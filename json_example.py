#!/usr/bin/env python3

import requests
import json

def retrieve_records(url):
    """Http call to retrieve the published records from provided API endpoint"""

    # Basic try and except logic since we are dealing with an HTTP request
    # Responses may vary depending on network health or server health
    try:
        print("Retrieving records from:\n"
              f"{url}...")
        response = requests.get(f"{url}")

        if response.status_code == 200:
            print("Success!\n")
        else:
            e = response.status_code
            print(f"HTTP Error {e}")
            raise Exception

    except Exception as e:
        print("Something went wrong", e,"\n")
        quit()

    return response

def generate_report(todo_data, user_data):
    """Response payload is passed into here. We need to
    loop through the response and manipulate the data into
     the report requirements"""

    report_dict = {}
    report_list = []

    todo_json = json.loads(todo_data.content)
    users_json = json.loads(user_data.content)

    for user in users_json:

        todo_total_count = 0
        todo_true_count = 0

        for todo in todo_json:

            if user['id'] == todo['userId']:
                todo_total_count += 1

                if todo['completed'] is True:
                    todo_true_count += 1

        report_dict = {
            "user": user['username'],
            "total assigned": f"{todo_total_count}",
            "total completed": f"{todo_true_count}"
        }

        report_list.append(report_dict)

    return report_list

def report_calculator(total, completed):
    """Pass your values into here and returns percentage"""

    quotient = completed / total
    percent = quotient * 100
    percent = round(percent, 2)

    return percent

def main():

    # Set our URLs
    todo_url = "https://jsonplaceholder.typicode.com/todos"
    users_url = "https://jsonplaceholder.typicode.com/users"

    # Receive responses from each url
    todo_response = retrieve_records(url=todo_url)
    user_response = retrieve_records(url=users_url)

    # Correlate the two responses and generate a list of values we need
    report_list = generate_report(todo_data=todo_response, user_data=user_response)

    # Report list is returned, we just need to loop through the list and print the values
    for report in report_list:

        total = int(report['total assigned'])
        completed = int(report['total completed'])
        user = report['user']

        # Just need to figure out the percentage quick
        percent = report_calculator(total, completed)

        print(f"{user} has {total} to-dos, {completed} of which are completed giving the individual"
              f" a completion percentage of {percent}%.")

if __name__ == "__main__":
    main()