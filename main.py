from bs4 import BeautifulSoup
import requests
import tomark
from datetime import datetime

# a proof of concept to create a market review by a list of company domains


def table(listOfDicts):
    """Loop through a list of dicts and return a markdown table as a multi-line string.
    listOfDicts -- A list of dictionaries, each dict is a row
    """
    markdowntable = ""
    # Make a string of all the keys in the first dict with pipes before after and between each key
    markdownheader = '| ' + ' | '.join(map(str, listOfDicts[0].keys())) + ' |'
    # Make a header separator line with dashes instead of key names
    markdownheaderseparator = '|-----' * len(listOfDicts[0].keys()) + '|'
    # Add the header row and separator to the table
    markdowntable += markdownheader + '\n'
    markdowntable += markdownheaderseparator + '\n'
    # Loop through the list of dictionaries outputting the rows
    for row in listOfDicts:
        markdownrow = ""
        for key, col in row.items():
            markdownrow += '| ' + str(col) + ' '
        markdowntable += markdownrow + '|' + '\n'
    return markdowntable

def extract_meta(domain):
    url = f'http://{domain}'
    print(url)
    data = dict()
    data['company'] = f'[{domain}]({url})'

    try:
       r = requests.get(url, allow_redirects=True)
       soup = BeautifulSoup(r.text)
    except Exception:
       return data


    try:
       title = soup.find('meta', attrs={'name':'og:title'}) or soup.find('meta', attrs={'property':'title'}) or soup.find('meta', attrs={'name':'title'}) or soup.find('title')
       data['title'] = title.get('content') or title.text
    except Exception:
       data['title'] = 'N/A'
    
    data['title'] = data['title'].replace('\n', '').replace('\r', '').replace('\t', '')

    try:
       description = soup.find('meta', attrs={'name':'og:description'}) or soup.find('meta', attrs={'property':'description'}) or soup.find('meta', attrs={'name':'description'})
       data['description'] = description.get('content')
    except AttributeError:
       data['description'] = 'N/A'

    data['description'] = data['description'].replace('\n', '').replace('\r', '').replace('\t', '')

    print(data)
    return data


if __name__ == '__main__':
    companies = []
    with open("companies.txt", "r") as domains:
        for domain in domains:
            company = extract_meta(domain.strip())
            companies.append(company)


    with open("Readme.md", "w", encoding="utf-8") as output:
        output.write(f"# RegTech landscape in the EU\n[EBA RegTech study in the EU financial sector, that Gartner conducted](https://www.eba.europa.eu/eba-assesses-benefits-challenges-and-risks-regtech-use-eu-and-puts-forward-steps-be-taken-support)\n\n")
        output.writelines(table(companies))
    
