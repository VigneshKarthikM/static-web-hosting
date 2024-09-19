import requests

def fetch_and_save_html(url, filename='index.html'):
    try:
        # Make the GET request
        response = requests.get(url)

        # Check if the request was successful
        if response.status_code == 200:
            # Save the HTML content to the specified file
            with open(filename, 'w', encoding='utf-8') as file:
                file.write(response.text)
            print(f'HTML content saved to {filename}')
        else:
            print(f'Error: Received status code {response.status_code}')

    except requests.exceptions.RequestException as e:
        print(f'Request failed due to: {e}')
