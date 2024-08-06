import requests
from bs4 import BeautifulSoup


def fetch_google_doc(url):
    response = requests.get(url)
    return response.text


def parse_data(html_data):
    soup = BeautifulSoup(html_data, 'html.parser')
    table = soup.find('table')
    parsed_data = []

    rows = table.find_all('tr')[1:]
    for row in rows:
        cells = row.find_all('td')
        if len(cells) == 3:
            try:
                x = int(cells[0].text.strip())
                char = cells[1].text.strip()
                y = int(cells[2].text.strip())
                parsed_data.append((char, x, y))
            except ValueError:
                continue
    print(parsed_data)
    return parsed_data


def create_grid(parsed_data):
    if not parsed_data:
        raise ValueError("No valid data")
    max_x = max(item[1] for item in parsed_data)
    max_y = max(item[2] for item in parsed_data)
    grid = [[' ' for _ in range(max_x + 1)] for _ in range(max_y + 1)]

    for char, x, y in parsed_data:
        grid[y][x] = char
    print(grid)
    return grid


def print_grid(grid):
    for row in grid:
        print(''.join(row))


def decode_secret_message(url):
    html_data = fetch_google_doc(url)
    parsed_data = parse_data(html_data)
    grid = create_grid(parsed_data)
    print_grid(grid)


url = "https://docs.google.com/document/d/e/2PACX-1vSHesOf9hv2sPOntssYrEdubmMQm8lwjfwv6NPjjmIRYs_FOYXtqrYgjh85jBUebK9swPXh_a5TJ5Kl/pub"
decode_secret_message(url)
