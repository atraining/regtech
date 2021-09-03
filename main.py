from bs4 import BeautifulSoup
import requests
import tomark
from datetime import datetime


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
       title = soup.find('meta', attrs={'name':'og:title'}) or soup.find('meta', attrs={'property':'title'}) or soup.find('meta', attrs={'name':'title'}) or soup.find('title')
       data['title'] = title.get('content').replace('\n', '') or title.text.replace('\n', '')
    except Exception:
       data['title'] = 'No title on homepage.'

    try:
       description = soup.find('meta', attrs={'name':'og:description'}) or soup.find('meta', attrs={'property':'description'}) or soup.find('meta', attrs={'name':'description'})
       data['description'] = description.get('content').replace('\n', '')
    except Exception:
       data['description'] = 'No desciption on homepage.'

    print(data)
    return data


if __name__ == '__main__':
    companies = []
    with open("companies.txt", "r") as domains:
        for domain in domains:
            company = extract_meta(domain.strip())
            companies.append(company)


    with open("Readme.md", "w", encoding="utf-8") as output:
        output.write(f"# EU RegTech comapnies - Status: {datetime.today().strftime('%Y-%m-%d')}\n\n")
        output.writelines(table(companies))
    
