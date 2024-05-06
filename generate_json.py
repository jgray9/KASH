import requests, json
from bs4 import BeautifulSoup
from collections import defaultdict
from urllib.parse import  urljoin

# iterate through every link on https://www.va.gov/directory/guide/allstate.asp
# return list of tuples (state name, state link)
def get_states():
    url = 'https://www.va.gov/directory/guide/allstate.asp'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    states = []
    for a in soup.findAll('a', class_='reglink'):
        state_name = a.text
        state_url = urljoin(url, a['href'])
        states.append((state_name, state_url))
    return states

# scrapes the page of a state and returns dictionary organized as:
# "department": {
#     "subdepartment": [
#         {
#             "name": facility name,
#             "url": facility link
#         }
#     ]
# }
# departments are: VHA, VBA, and NCA
# subdepartments vary depending on page
def parse_state_page(state_url):
    state_data = defaultdict(dict)
    page = requests.get(state_url)
    soup = BeautifulSoup(page.content, "html.parser")

    department = ''
    subdepartment = ''
    # all data is organized in a table element
    # first two rows of table don't contain useful info
    for td in soup.findAll('td')[2:]:
        # usually the first <td> of each row has a class, but sometimes the class is in a <span> inside of the <td>
        cl = td['class'][0] if td.has_attr('class') else td.find('span')['class'][0] if td.find('span') != None else None

        # <td> contains the title of a department (VHA, VBA or NCA)
        # following rows will contain info pertaining to that department until next 'stitle'
        if cl == 'stitle':
            department = td.text
            state_data[department] = {}
        # <td> contains title of a subdepartment (text has an indent that must be removed)
        # following rows will contain facilities in that subdepartment until next 'sreptitle'
        elif cl == 'sreptitle':
            subdepartment = td.text.replace('\xa0','')
            state_data[department][subdepartment] = []
        # <td> contains title of a facility
        # the title of the <a> element is more descriptive so that is used instead
        elif cl == 'reglink':
            a = td.parent.find('a') # link always in same row as <td class='reglink'>
            state_data[department][subdepartment].append({
                'name': a.text,
                'url': urljoin(state_url, a['href'])
            })
    return state_data

# generate dictionary object organized as:
# "department": {
#     "state name": {
#         "subdepartment": [
#             {
#                 "name": facility name,
#                 "url": facility link
#             }
#         ]
#     }
# }
def parse_all():
    data = {
        'VHA': {},
        'VBA': {},
        'NCA': {}
    }
    for state_name, state_url in get_states():
        print(f'Loading {state_name}...')
        state_data = parse_state_page(state_url)
        # get data for each department
        vha_data = state_data['Veterans Health Administration']
        vba_data = state_data['Veterans Benefits Administration']
        nca_data = state_data['National Cemetery Administration']
        # put data for each department in proper state
        data['VHA'][state_name] = vha_data
        data['VBA'][state_name] = vba_data
        data['NCA'][state_name] = nca_data
    return data

# create json file
with open('test.json', '+w') as file:
    json.dump( parse_all(), file )