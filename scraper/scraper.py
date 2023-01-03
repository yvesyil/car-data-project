import aiohttp
import asyncio
import time
import aiohttp
import bs4
import os
import sys
import logging
import pandas as pd

from utils import compile_url, decompile_url


logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    stream=sys.stdout,
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

csv_filename_template = 'data/cars-ie-page{}.csv'


# writes a list or a list of list to given csv file with ';' as a seperator
def write_to_csv(filename: str, all_items: list[list[str]]):
    with open(filename, 'a') as f:
        if type(all_items[0]) != type([]):
            for item in all_items[:-1]:
                f.write(item.strip() + ';')
            f.write(all_items[-1].strip() + '\n')
            return

        for items in all_items:
            for item in items[:-1]:
                f.write(item.strip() + ';')
            f.write(items[-1].strip() + '\n')


# writes header fields to given csv file
def initialise_csv(filename: str):
    if os.path.isfile(filename):
        os.remove(filename)

    # head
    head = [
        'Title',
        'Description',
        'Price',
        'Odometer',
        'Fuel Type',
        'Colour',
        'Engine Size',
        'Transmission',
        'Body Type',
        'Owners',
        'Doors',
        'Tax Expiry',
        'NCT Expiry',
        #'Dealer',
        #'Address',
        #'Phone',
        #'Franchise',
        #'Website'
    ]
    write_to_csv(filename, head)


# retrieves each car url present in the page
def get_car_urls_in_page(base: str, raw_page: str) -> list[str]:
    soup = bs4.BeautifulSoup(raw_page, 'html.parser')
    # car title
    h3s = soup.find_all('h3', {'class': 'greenText'})

    # car details
    car_urls = list()
    for div in soup.find_all('div', {'class': 'car-listing-header'}):
        car_urls.append(base + div.find('a').get('href').replace('/used-cars', ''))
    return car_urls


# sends requests to each car url and returns a list containing all cars' info
async def scrape_car_urls(session: aiohttp.ClientSession, urls: list[str], headers: dict) -> tuple[list[int], list[list[str]]]:
    resp_codes = list()
    cars = list()
    for url in urls:
        logger.info('scraping for {}'.format(url))
        resp = await session.get(url, headers=headers)
        resp_content = None
        try:
            resp_content = await resp.read()
        except Exception as e:
            logger.error(e)
            exit(69)

        resp_codes.append(resp.status)

        car_detail_soup = bs4.BeautifulSoup(resp_content, 'html.parser')
        try:
            car_title = car_detail_soup.find('h3')
            car_desc = car_detail_soup.find('div', {'class': 'col-sm-12'}).find('p')
            car_price = car_detail_soup.find('div', {'class': 'col-xs-6 text-right greenText large-text'}).find('strong')
            stripped_table = car_detail_soup.find_all('div', {'class': 'stripped-table'})[-1]
        except Exception as e:
            continue
        # body
        body = list()
        body.append(''.join(car_title.contents))
        body.append(''.join(car_desc.contents))
        body.append(''.join(car_price.contents))
        for d in stripped_table.find_all('div', {'class': 'col-xs-6'})[1::2]:
            body.append(''.join([i.get_text().strip('\t\n') for i in d.contents]))
        cars.append(body)
        logger.info('done {}'.format(url))

    return resp_codes, cars


# asynchronous worker for fetching each url (page)
async def fetch_with_aiohttp(session: aiohttp.ClientSession, url: str, headers: dict, timeout: int = 30) -> list[int]:
    _, params = decompile_url(url)
    page_num = params['page']
    filename = csv_filename_template.format(page_num)
    logger.info('started scraping url = {}'.format(url))
    resp = await session.get(url=url, headers=headers, timeout=timeout)

    resp_content = None
    try:
        resp_content = await resp.read()
    except Exception as e:
        logger.error(e)
        exit(31)

    base_url, _ = decompile_url(url)
    car_urls_in_page = get_car_urls_in_page(base_url, resp_content)
    resp_codes, cars_list = await scrape_car_urls(session, car_urls_in_page, headers)
    initialise_csv(filename)
    write_to_csv(filename, cars_list)

    logger.info('finished scraping url = {}'.format(url))
    return resp_codes
 

# scrape each page asynchronously
async def fetch_all_parallel(session: aiohttp.ClientSession, url_list: list[str], headers: dict, timeout: int = 200) -> list[tuple[int, dict[str, any], bytes]]:
    t1 = time.time()
    results = await asyncio.gather(*[fetch_with_aiohttp(session, url, headers, timeout) for url in url_list])
    t2 = time.time()
    t = t2 - t1
    logger.info('finished scraping all {} pages in {:0.2f} seconds'.format(len(url_list), t))
    return results
    

# check if the data is already scraped, if not determine which pages to scrape
def check_data_present(page_count) -> tuple[int, list[int]]:
    missing_files = list()
    count = 0

    for i in range(1, page_count+1):
        if not os.path.isfile(csv_filename_template.format(i)):
            missing_files.append(i)
        else:
            count += 1

    return count, missing_files


# merge all the files into one file
def merge_dataframes(page_count):
    final_filename = 'data/cars-ie-all-cars.csv'

    dfs = list()
    for i in range(1, page_count+1):
        dfs.append(pd.read_csv(csv_filename_template.format(i), delimiter=';'))

    final_df = pd.concat(dfs, ignore_index=True)

    final_df.to_csv(final_filename, sep=';')


async def main():
    page_count = int(sys.argv[1])

    scraped_file_count, to_scrape = check_data_present(page_count)
    if scraped_file_count == page_count: 
        logger.info('all first {} pages already scraped, returning...'.format(page_count))
        return
    
    if scraped_file_count == 0:
        logger.info('scraping first {} pages...'.format(page_count))
    else:
        logger.info('from {} pages, {} are missing...'.format(page_count, page_count - scraped_file_count))

    base_url = 'https://www.cars.ie/used-cars'
    url_params = {
        "page": 0
    }
    # act like real user
    headers = ({'User-Agent':
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit\
    /537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'})
    
    url_list = list()
    for i in to_scrape:
        url_params['page'] = i
        url_list.append(compile_url(base_url, url_params))

    async with aiohttp.ClientSession() as sess:
        await fetch_all_parallel(sess, url_list, headers=headers, timeout=5 * 60)
    
    merge_dataframes(page_count)
            

if __name__ == "__main__":
    asyncio.run(main())