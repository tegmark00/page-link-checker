import requests
from bs4 import BeautifulSoup

domain = 'http://127.0.0.1:8000'
entry = domain + '/'

pages = set()
checked_links = set()
with_errors = set()
skipped = set()


def get_page_content(url: str) -> str:
    """Should be splitted in two methods"""
    r = requests.get(url)
    if r.status_code != 200:
        with_errors.add(url)
    return r.text


def populate_links(html_content: str) -> list:
    soup = BeautifulSoup(html_content)
    return soup.findAll('a')


def filter_links(links: list) -> list:
    filtered_links = set()
    for link in links:
        skip = False
        if link.startswith('#'):
            skip = True
        if link.startswith('tel'):
            skip = True
        if link.startswith('javascript'):
            skip = True
        if link.startswith('http') and not link.startswith(domain):
            skip = True
        if link == '':
            skip = True
        if link.startswith('/'):
            link = domain + link
        if not link.startswith('http'):
            # print('WARNING: ', link)
            skip = True
        if link.startswith(domain + '/news/'):
            skip = True

        for el in ['.zip', '.pdf', '.png', '.jpg', '.gif', '.svg']:
            if el in link:
                # print('WARNING: skipping ', link)
                skip = True
                break

        if not skip:
            filtered_links.add(link)
        else:
            skipped.add(link)

    return list(filtered_links)


def check(url):
    print('Checking url: ', url)
    content = get_page_content(url)
    links = populate_links(content)
    links = [link.attrs['href'] for link in links]
    links = filter_links(links)
    checked_links.add(url)
    pages.update(links)


check(entry)

while pages - checked_links:
    print('ERRORS: ', with_errors)
    to_check = pages - checked_links
    for link in to_check:
        check(link)


print('Checked')
for page in sorted(checked_links):
    print(page)

print('Skipped')
for page in skipped:
    print(page)

print('Error')
for page in with_errors:
    print(page)
