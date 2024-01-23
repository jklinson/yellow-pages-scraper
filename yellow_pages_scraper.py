import requests
from bs4 import BeautifulSoup
import pandas as pd

def fetch_yellow_pages_data():
    base_url = "https://www.yellowpages.com.au/search/listings?clue=Business&locationClue=Greater+Melbourne%2C+VIC"  # Replace with the actual API endpoint
    
    # Parameters for the API request
    payload = {}

    headers = {
        'User-Agent': 'PostmanRuntime/7.36.1',
        'Cookie': 'clue=Business; locationClue="Greater Melbourne, VIC"; yellow-guid=22eec8fa-622f-49c9-949c-1b2a629fd014'
    }

    # Make the request to the API
    response = requests.get(base_url, headers=headers, data=payload)

    if response.status_code == 200:
        data = response.text
        return data
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        return None


def scrape_yellow_pages():
    yellow_pages_data = fetch_yellow_pages_data()
    print('Here 1')

    soup = BeautifulSoup(yellow_pages_data, 'html.parser')
    print('Here 2')
    # Extract business details
    business_list = []
    for listing_div in soup.find_all('div', class_='Box__Div-sc-dws99b-0 iOfhmk MuiPaper-root MuiCard-root PaidListing MuiPaper-elevation1 MuiPaper-rounded'):
        business_name = listing_div.find('h3', class_='MuiTypography-root jss376 MuiTypography-h3 MuiTypography-displayBlock').text.strip()
        business_address = listing_div.find('p', class_='MuiTypography-root jss377 MuiTypography-body2 MuiTypography-colorTextSecondary').text.strip()
        
        additional_details = [detail.text.strip() for detail in listing_div.find_all('div', class_='Box__Div-sc-dws99b-0 bKFqNV true')]
        
        business_list.append({'Business Name': business_name, 'Business Address': business_address, 'Additional Details': additional_details})

    return business_list


def save_to_excel(data, file_name='business_list.xlsx'):
    df = pd.DataFrame(data)
    df.to_excel(file_name, index=False)
    print(f'Data has been saved to {file_name}')

def save_to_text_file(data, file_name='yellow_pages_data.txt'):
    with open(file_name, 'w') as file:
        file.write(data)
    print(f'Data has been saved to {file_name}')

if __name__ == "__main__":
    business_list_data = scrape_yellow_pages()
    if business_list_data:
        save_to_text_file(business_list_data)
