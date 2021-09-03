from BeautifulSoup import BeautifulSoup
import requests
import tomark

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

def extract_meta(url):
    r = requests.get(url)

    print(dir(r))
    soup = BeautifulSoup(r.text)

    meta = soup.findAll('meta')
    print(meta)

    for tag in meta:
        print(tag)

if __name__ == '__main__':
    companies = []
    with open("companies.txt", "r") as domains:
        for domain in domains:
            company = extract_meta(domain.strip())
            companies.append(company)
    with open("regtech.md", "w") as output:
        file1.write("# RegTech comapnies")
        file1.writelines(table(companies))
    
