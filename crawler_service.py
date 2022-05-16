import logging
import statistics
import time

import requests
from bs4 import BeautifulSoup as soup

from config.chain_constant import Chain

logger = logging.getLogger('Crawl Service')
logger.setLevel(logging.INFO)

HOLDER_NATIVE = {
    Chain.ethereum_chain_id: 130843778,
    Chain.bsc_chain_id: 15499309,
    Chain.polygon_chain_id: 433546,
    Chain.ftm_chain_id: 755491,
}


class TokenHolderStats:
    # time throttle limit the minimum time per token
    @staticmethod
    def time_throttling(start_time, end_time, time_throttle):
        if time_throttle > (end_time - start_time):
            time.sleep(time_throttle - end_time + start_time)

    # Possible error value
    INVALID_ADDRESS = "Contract address  is invalid"
    CAPTCHA_REQUIRED = "Captcha required"
    TRAP_ADDRESS = "Possibly a trap address"
    NO_HOLDERS = "Cannot get holders/There are no holders"
    NO_STATS = "Cannot get token's stat/There are no stats"
    NO_ERRORS = None

    def __init__(self, chain_id, soup_calls_limit=25, sleep_time=10):
        # Number of consecutive calls
        self.get_url_soup_calls = 1
        # Number of consecutive calls before sleep
        self.soup_calls_limit = soup_calls_limit
        # Sleep time
        self.sleep_time = sleep_time

        self.chain_id = chain_id

        self.end_fix_urls = {
            "https://bitbitgo.xyz/token": "&__cpo=aHR0cHM6Ly9ldGhlcnNjYW4uaW8",
            "https://etherscan-io.translate.goog/token": "&_x_tr_sl=en&_x_tr_tl=en&_x_tr_hl=en-US&_x_tr_pto=nui,op,elem",
        }
        base_urls = {
            '0x38': [
                'https://bscscan.com/token',
                'https://bscscan-com.translate.goog/token'
            ],
            '0x89': [
                'https://polygonscan.com/token',
                'https://polygonscan-com.translate.goog/token'
            ],
            '0x1': [
                # 'http://165.22.53.97:2808/proxy/?url=https://etherscan.io/token',
                # 'https://translate.google.com/translate?hl=&sl=en&tl=vi&u=https://etherscan.io/token',
                'https://etherscan-io.translate.goog/token',
                'https://etherscan.io/token',
            ],
            '0xfa': [
                # 'http://0.0.0.0:2808/proxy/?url=https://ftmscan.com/token',
                'https://ftmscan.com/token',
                'https://ftmscan-com.translate.goog/token'
            ],
            '0xa': [
                'https://optimistic.etherscan.io/token',
                'https://optimistic.etherscan.io.translate.goog/token',
            ],
            
            '0xa4b1': [
              'https://arbiscan.io/token/',
              'https://arbiscan.io.translate.goog/token/',
            ],
            '0x504': [
              'https://moonscan.io/token/',
              'https://moonscan.io.translate.goog/token/',
            ],
            '0x505': [
              'https://moonriver.moonscan.io/token/',
              'https://moonriver.moonscan.io.translate.goog/token/',
            ]
        }

        self.base_urls = base_urls[chain_id]

    def __get_url_soup(self, url):
        # Read the html of the page
        logger.debug(f"get_url_soup_calls: {self.get_url_soup_calls}")
        if self.get_url_soup_calls <= self.soup_calls_limit:
            self.get_url_soup_calls += 1
        else:
            logger.debug(f"Limit exceeded, continue in {self.sleep_time}s")
            time.sleep(self.sleep_time)
            # Reset get_url_soup_calls
            self.get_url_soup_calls = 1
            logger.debug(f"get_url_soup_calls: 1")

        logger.debug(f"Getting {url} soup")
        # headers = {
        #     # 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
        #     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
        #     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        #     'Accept-Encoding': 'gzip',
        #     'Accept-Language': 'en-US,en;q=0.9,es;q=0.8',
        #     'Upgrade - Insecure - Requests': '1',
        #     'Referer': f'{self.base_url}s'
        # }
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
        }

        # proxies = {
        #     "http": "http://78.128.45.132:5678",
        # }
        # logger.debug(headers)
        start = time.time()
        response = requests.get(url, headers=headers, verify=False)
        # scraper = cloudscraper.create_scraper(
        # browser={
        #     'browser': 'firefox',
        #     'platform': 'windows',
        #     'mobile': False
        # }
        # )
        #
        # response = scraper.get(url, headers=headers,proxies=proxies,verify=False)
        logger.debug(f"Get response take {time.time() - start}s")
        status = response.status_code
        content = response.text

        logger.debug(f"Parsing {url} soup content")
        page_soup = soup(content, "html.parser")
        # Check errors
        title = str(page_soup.title)
        # if "Error" in title:
        #     error_code = page_soup.find("p", {"class": "mb-0"}).text
        #     raise ValueError(error_code)
        # If ip is blocked
        if "Attention" in title:
            raise ConnectionError("Captcha")

        # Check if there are any result
        error_col = page_soup.find("div", {"class": "col-md-12"})
        if error_col is not None:
            if "Sorry" in error_col.text:
                raise ValueError("Invalid address")

        logger.debug(f"Finished getting {url} soup content")
        return page_soup, status

    def get_stats(self, contract_address, time_throttle=1, holders_range=500):
        start_time = time.time()
        stats = {}
        if str(contract_address).lower() == "0x":
            stats = {
                "total_holders": HOLDER_NATIVE.get(self.chain_id),
                "percentage_mean": 0.1,
                "percentage_stdev": 0.01,
                "error": None,
            }
            return stats

        err = None
        page_soup = None
        try:
            for base_url in self.base_urls:
                logger.debug(f" Try with base url {base_url}")
                self.end_fix = ""
                if self.end_fix_urls.get(base_url):
                    self.end_fix = self.end_fix_urls.get(base_url)

                tail_url = f"/tokenholderchart/{contract_address}?range={holders_range}" + self.end_fix
                if base_url.startswith("https://proxysite.cloud"):
                    tail_url = tail_url.replace("/", "%2F") + "#"
                    # tail_url = tail_url.replace("?", "%3F")
                    # tail_url = tail_url.replace("=", "%3D")
                elif base_url.startswith("https://translate.google.com/"):
                    tail_url = tail_url + "&anno=2&sandbox=1"
                url = base_url + tail_url

                status = 500
                try:
                    page_soup, status = self.__get_url_soup(url)
                    holders = page_soup.findAll("span", {"class": "text-nowrap"})[1].text
                    retry = False
                except ValueError:
                    err = TokenHolderStats.INVALID_ADDRESS
                    retry = False
                except ConnectionError:
                    err = TokenHolderStats.CAPTCHA_REQUIRED
                    time.sleep(3)
                    retry = True
                except Exception as ex:
                    err = type(ex).__name__
                    retry = True
                if 200 <= status <= 299 and not retry:
                    break
        except ValueError:
            logger.debug(f"{contract_address} is invalid")
            stats['total_holders'] = 0
            stats['percentage_mean'] = 0
            stats['percentage_stdev'] = 0
            stats['quantity_mean'] = 0
            stats['quantity_stdev'] = 0
            stats['error'] = TokenHolderStats.INVALID_ADDRESS

            # Make sure each request take at least time throttle
            end_time = time.time()
            TokenHolderStats.time_throttling(start_time=start_time, end_time=end_time, time_throttle=time_throttle)
            return stats
        except ConnectionError as ex:
            logger.debug(f"Captcha is required")
            time.sleep(10)
            raise ex

        except PermissionError:
            logger.debug(f"{contract_address} is possibly a Trap")
            stats['total_holders'] = 0
            stats['percentage_mean'] = 0
            stats['percentage_stdev'] = 0
            stats['quantity_mean'] = 0
            stats['quantity_stdev'] = 0
            stats['error'] = TokenHolderStats.TRAP_ADDRESS

            # Make sure each request take at least time throttle
            end_time = time.time()
            TokenHolderStats.time_throttling(start_time=start_time, end_time=end_time, time_throttle=time_throttle)
            return stats

        # Total holders info
        if err == TokenHolderStats.INVALID_ADDRESS:
            logger.debug(f"{contract_address} is invalid")
            stats['total_holders'] = 0
            stats['percentage_mean'] = 0
            stats['percentage_stdev'] = 0
            stats['quantity_mean'] = 0
            stats['quantity_stdev'] = 0
            stats['error'] = TokenHolderStats.NO_ERRORS
            logger.info(f'{contract_address} stats: {stats}')
            return stats

        try:
            holders = page_soup.findAll("span", {"class": "text-nowrap"})[1].text
            holders = int(holders.replace("Token Holders: ", "").replace(",", ""))
            logger.debug(f"{contract_address} total holders: {holders}")
            stats['total_holders'] = holders
        except (IndexError, AttributeError):
            stats['total_holders'] = 0
            stats['percentage_mean'] = 0
            stats['percentage_stdev'] = 0
            stats['quantity_mean'] = 0
            stats['quantity_stdev'] = 0
            stats['error'] = err or TokenHolderStats.NO_HOLDERS

            # Make sure each request take at least time throttle
            end_time = time.time()
            TokenHolderStats.time_throttling(start_time=start_time, end_time=end_time, time_throttle=time_throttle)
            return stats

        # Percentage & Quantity info in side holders range
        logger.debug(f"Getting {contract_address} quantity and percentage info")

        table_rows = page_soup.findAll("tr")
        if len(table_rows) > 1:
            percentage_list = []
            quantity_list = []
            number_of_rows = min(501, len(table_rows))
            for i in range(1, number_of_rows):
                row = table_rows[i].findAll("td")
                # holder = row[1].find("span").text
                if len(row) >= 4:
                    quantity = float(row[2].text.replace(",", ""))
                    percentage = float(row[3].text.replace("%", "").replace(",", ""))
                else:
                    quantity = 0
                    percentage = 0
                quantity_list.append(quantity)
                percentage_list.append(percentage)
                # logger.info(f"{holder} quantity: {quantity}")
                # logger.info(f"{holder} percentage: {percentage}")

            stats['percentage_mean'] = statistics.mean(percentage_list)
            stats['percentage_stdev'] = statistics.stdev(percentage_list) if len(percentage_list) > 1 else 100
            stats['quantity_mean'] = statistics.mean(quantity_list)
            stats['quantity_stdev'] = statistics.stdev(quantity_list) if len(quantity_list) > 1 else 0
            stats['error'] = TokenHolderStats.NO_ERRORS
        else:
            stats['percentage_mean'] = 0
            stats['percentage_stdev'] = 0
            stats['quantity_mean'] = 0
            stats['quantity_stdev'] = 0
            stats['error'] = TokenHolderStats.NO_STATS

        logger.info(f'{contract_address} stats: {stats}')
        # print(f'{contract_address} stats: {stats}')
        # Make sure each request take at least time throttle
        end_time = time.time()
        TokenHolderStats.time_throttling(start_time=start_time, end_time=end_time, time_throttle=time_throttle)
        return stats

    def get_holder(self, contract_address, time_throttle=1, holders_range=500):
        start_time = time.time()
        stats = {}
        if str(contract_address).lower() == "0x":
            stats = {
                "total_holders": HOLDER_NATIVE.get(self.chain_id),
                "error": None,
            }
            return stats

        err = None
        page_soup = None
        try:
            for base_url in self.base_urls:
                logger.debug(f" Try with base url {base_url}")
                self.end_fix = ""
                if self.end_fix_urls.get(base_url):
                    self.end_fix = self.end_fix_urls.get(base_url)

                tail_url = f"/tokenholderchart/{contract_address}?range={holders_range}" + self.end_fix
                if base_url.startswith("https://proxysite.cloud"):
                    tail_url = tail_url.replace("/", "%2F") + "#"
                    # tail_url = tail_url.replace("?", "%3F")
                    # tail_url = tail_url.replace("=", "%3D")
                elif base_url.startswith("https://translate.google.com/"):
                    tail_url = tail_url + "&anno=2&sandbox=1"
                url = base_url + tail_url

                status = 500
                try:
                    page_soup, status = self.__get_url_soup(url)
                    holders = page_soup.findAll("span", {"class": "text-nowrap"})[1].text
                    retry = False
                except ValueError:
                    err = TokenHolderStats.INVALID_ADDRESS
                    retry = False
                except ConnectionError:
                    err = TokenHolderStats.CAPTCHA_REQUIRED
                    time.sleep(3)
                    retry = True
                except Exception as ex:
                    err = type(ex).__name__
                    retry = True
                if 200 <= status <= 299 and not retry:
                    break
        except ValueError:
            logger.debug(f"{contract_address} is invalid")
            stats['total_holders'] = 0
            stats['error'] = TokenHolderStats.INVALID_ADDRESS

            # Make sure each request take at least time throttle
            end_time = time.time()
            TokenHolderStats.time_throttling(start_time=start_time, end_time=end_time, time_throttle=time_throttle)
            return stats
        except ConnectionError as ex:
            logger.debug(f"Captcha is required")
            time.sleep(10)
            raise ex

        except PermissionError:
            logger.debug(f"{contract_address} is possibly a Trap")
            stats['total_holders'] = 0
            stats['error'] = TokenHolderStats.TRAP_ADDRESS

            # Make sure each request take at least time throttle
            end_time = time.time()
            TokenHolderStats.time_throttling(start_time=start_time, end_time=end_time, time_throttle=time_throttle)
            return stats

        # Total holders info
        if err == TokenHolderStats.INVALID_ADDRESS:
            logger.debug(f"{contract_address} is invalid")
            stats['total_holders'] = 0
            stats['error'] = TokenHolderStats.NO_ERRORS
            logger.info(f'{contract_address} stats: {stats}')
            return stats

        try:
            holders = page_soup.findAll("span", {"class": "text-nowrap"})[1].text
            holders = int(holders.replace("Token Holders: ", "").replace(",", ""))
            logger.debug(f"{contract_address} total holders: {holders}")
            stats['total_holders'] = holders
        except (IndexError, AttributeError):
            stats['total_holders'] = 0
            stats['error'] = err or TokenHolderStats.NO_HOLDERS

            # Make sure each request take at least time throttle
            end_time = time.time()
            TokenHolderStats.time_throttling(start_time=start_time, end_time=end_time, time_throttle=time_throttle)
            return stats

        # Percentage & Quantity info in side holders range
        logger.debug(f"Getting {contract_address} quantity and percentage info")

        stats['error'] = TokenHolderStats.NO_ERRORS
        logger.info(f'{contract_address} stats: {stats}')
        # print(f'{contract_address} stats: {stats}')
        # Make sure each request take at least time throttle
        end_time = time.time()
        TokenHolderStats.time_throttling(start_time=start_time, end_time=end_time, time_throttle=time_throttle)
        return stats
  


if __name__ == "__main__":
    polygon = TokenHolderStats(chain_id='0x1')
    stat = polygon.get_holder("")
    
    print(stat)
