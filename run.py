import requests
from bs4 import BeautifulSoup


entry = domain + '/'
pages = set()
checked_links = set()
with_errors = set()


def get_page_content(url: str) -> str:
    """Should be splitted in two methods"""
    r = requests.get(url)
    if r.status_code in [400, 401, 402, 403, 404, 500, 501, 502]:
        with_errors.add(url)
    return r.text


def populate_links(html_content: str) -> list:
    soup = BeautifulSoup(html_content)
    return soup.findAll('a')


def filter_links(links: list) -> list:
    filtered_links = set()
    for link in links:
        if link.startswith('#'):
            continue
        if link.startswith('tel'):
            continue
        if link.startswith('javascript'):
            continue
        if link.startswith('http') and not link.startswith(domain):
            continue
        if link == '':
            continue
        if link.startswith('/'):
            link = domain + link
        if not link.startswith('http'):
            print('WARNING: ', link)
            continue
        if link.startswith(domain + '/news/'):
            continue

        skip = False
        for el in ['.zip', '.pdf', '.png', '.jpg', '.gif', '.svg']:
            if el in link:
                print('WARNING: skipping ', link)
                skip = True
                break

        if not skip:
            filtered_links.add(link)

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
    to_check = list(pages - checked_links)
    for link in to_check:
        check(link)


print('Checked')
for page in list(sorted(list(checked_links))):
    print(page)

print('Error')
for page in list(with_errors):
    print(page)

