#!/usr/bin/env python
# MassRDAP - developed by acidvegas (https://git.acid.vegas/massrdap)

import asyncio
import logging
import json
import re
import os, random
from datetime import datetime

import modin.pandas as pd
# import dask.dataframe as pd
from DataRecorder import Recorder
from dbhelper import *

# try:
#     import aiofiles
# except ImportError:
#     raise ImportError('missing required aiofiles library (pip install aiofiles)')

try:
    import aiohttp
except ImportError:
    raise ImportError("missing required aiohttp library (pip install aiohttp)")
import aiohttp
import asyncio
from contextlib import asynccontextmanager
import aiohttp_socks

from loguru import logger
import ray

# Replace this with your actual test URL
test_url = "http://example.com"
# ray.shutdown()
# ray.init()

# Replace this with your actual outfile object and method for adding data
# outfile = YourOutfileClass()
# Color codes
BLUE = "\033[1;34m"
CYAN = "\033[1;36m"
GREEN = "\033[1;32m"
GREY = "\033[1;90m"
PINK = "\033[1;95m"
PURPLE = "\033[0;35m"
RED = "\033[1;31m"
YELLOW = "\033[1;33m"
RESET = "\033[0m"

MAX_RETRIES = 3
INITIAL_DELAY = 1
MAX_DELAY = 10

# Setup basic logging
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
)

# Global variable to store RDAP servers
RDAP_SERVERS = {}



from bs4 import BeautifulSoup
import asyncio
import aiohttp
import time

# Semaphore to control concurrency
semaphore = asyncio.Semaphore(100)  # Allow up to 50 concurrent tasks
# db_manager = DatabaseManager()


filename='./tranco_Z377G'

folder_path='.'
inputfilepath=filename + ".csv"
# logger.add(f"{folder_path}/domain-index-ai.log")
# print(domains)

outfilepath=inputfilepath.replace('.csv','-rank.csv')
outfilepath='top-domains-1m-in.csv'

outfile = Recorder(folder_path+'/'+outfilepath, cache_size=200)
outfileerror = Recorder(folder_path+'/'+outfilepath.replace('.csv','-error.csv'), cache_size=10)



async def get_proxy():
    proxy=None
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get('http://demo.spiderpy.cn/get') as response:
                data = await response.json()
                proxy=data['proxy']
                return proxy
        except:
            pass
async def get_proxy_proxypool():
    async with aiohttp.ClientSession() as session:

        try:
            async with session.get('https://proxypool.scrape.center/random') as response:
                proxy = await response.text()
                return proxy
        except:
            return None


def get_tld(domain: str):
    """Extracts the top-level domain from a domain name."""
    parts = domain.split(".")
    return ".".join(parts[1:]) if len(parts) > 1 else parts[0]



def save_data_to_csv(data, csv_filename):
  # Load JSON data

  # Extract domain and ranks
  domain = data['domain']
  ranks = data['ranks']

  # Save to CSV
  with open(csv_filename, 'a', newline='', encoding='utf-8') as csvfile:
      writer = csv.writer(csvfile)
      
      if csvfile.tell() == 0:
          # Write header if file is empty
          writer.writerow(['date', 'rank'])

      for entry in ranks:
          writer.writerow([entry['date'], entry['rank']])

  print(f"Saved data to CSV: {csv_filename}")
def save_data_to_mongodb(data):
    # Extract domain and ranks
    domain = data['domain']
    ranks = data['ranks']

    # Save to MongoDB
    client = MongoClient('mongodb://localhost:27017/')
    db = client['rank_database']
    collection = db['rank_collection']

    # Check if domain exists in MongoDB
    existing_entry = collection.find_one({'domain': domain})

    if existing_entry:
        # Append new dates to existing dates in MongoDB
        existing_dates = existing_entry['dates']
        new_dates = [(entry['date'], entry['rank']) for entry in ranks]

        updated_dates = existing_dates + new_dates

        # Update the document in MongoDB
        collection.update_one(
            {'domain': domain},
            {'$set': {'dates': updated_dates}}
        )

        print(f"Updated MongoDB document for domain: {domain}")
    else:
        # Insert new document if domain does not exist
        dates = [(entry['date'], entry['rank']) for entry in ranks]
        document = {
            'domain': domain,
            'dates': dates
        }

        collection.insert_one(document)

        print(f"Inserted new MongoDB document for domain: {domain}")

    # Close MongoDB connection
    client.close()
async def extract_rank(response,domain):
    try:
        date='unk'
        data = await response.json()        
        # Specify CSV file path
        csv_file = 'rank_timeseries.csv'
        save_data_to_csv(data,csv_file)


        return True
    except Exception as e:
        logger.error(f'parse index date error for:{e}')
            # Domain=
            # new_domain = db_manager.Domain(
            #     url=domain,tld=get_tld(domain),
            # title=None,
            # indexat=r[-1] or None,
            # des=None,
            # bornat=None)
            # db_manager.add_domain(new_domain)
        return False


# Function to simulate a task asynchronously
async def get_rank(domain):
    async with semaphore:
        url = f'https://tranco-list.eu/ranks/domain/{domain}'
        retries = 3
        for attempt in range(1, retries + 1):
            try:
                proxy_url = "socks5://127.0.0.1:1080"  # Example SOCKS5 proxy URL
                if attempt>1:
                    # proxy_url=await get_proxy_proxypool()
                    proxy_url = "socks5://127.0.0.1:1080"  # Example SOCKS5 proxy URL


                # proxy_url = "socks5://127.0.0.1:9050"  # Example SOCKS5 proxy URL
                connector = aiohttp_socks.ProxyConnector.from_url(proxy_url) if proxy_url and proxy_url.startswith("socks") else None
                proxy=proxy_url if proxy_url and 'http' in proxy_url else None
                print('===proxy',proxy,domain)
                async with aiohttp.ClientSession(connector=connector) as session:                
                    async with session.get(url,proxy=proxy) as response:
                        if response.status == 200:
                            data = await extract_rank(response,domain)
                            # print('data',data)
                            if data:
                                print(f"Task {url} completed on attempt {attempt}. Data: {data}")
                                return
                        else:
                            print(f"Task {url} failed on attempt {attempt}. Status code: {response.status}")
            except aiohttp.ClientConnectionError:
                if attempt < retries:
                    print(f"Task {url} failed on attempt {attempt}. Retrying...")
                else:
                    print(f"Task {url} failed on all {retries} attempts. Skipping.")
                    outfileerror.add_data([domain])

            except Exception:
                if attempt < retries:
                    print(f"Task {url} failed on attempt {attempt}. Retrying...")
                else:
                    print(f"Task {url} failed on all {retries} attempts. Skipping.")
                    outfileerror.add_data([domain])


# To run the async function, you would do the following in your main code or script:
# asyncio.run(test_proxy('your_proxy_url_here'))
def cleandomain(domain):
    if isinstance(domain,str)==False:
        domain=str(domain)
    domain=domain.strip()
    if "https://" in domain:
        domain = domain.replace("https://", "")
    if "http://" in domain:
        domain = domain.replace("http://", "")
    if "www." in domain:
        domain = domain.replace("www.", "")
    if domain.endswith("/"):
        domain = domain.rstrip("/")
    return domain

# Function to run tasks asynchronously with specific concurrency
async def run_async_tasks():
    tasks = []

    df = pd.read_csv(inputfilepath,
                    #  , encoding="ISO-8859-1"
                    usecols=['domain']
                     )
    domains=df['domain'].to_list()
    print(f'load domains:{len(domains)}')

    try:
        # dbdata=db_manager.read_domain_all()

        # for i in dbdata:
        #     if i.indexat is not None:
        #         donedomains.append(i.url)    
        pass    
    except Exception as e:
        print(f'query error: {e}')
    alldonedomains=[]

    # if os.path.exists(outfilepath):
        # df=pd.read_csv(outfilepath)
        # filtered_df = df[df['indexdate'] != 'unk']
        # print(df.head(50))
        # alldonedomains=df['domain'].to_list()
    # else:
    #     df=pd.read_csv('top-domains-1m.csv')

    #     donedomains=df['domain'].to_list()
    # donedomains=list(set(donedomains))


    # 使用chunksize读取数据，返回一个可迭代的TextFileReader对象
    chunk_iter = pd.read_csv(outfilepath, chunksize=100000)

    # 初始化一个空列表来收集所有域
    alldonedomains = []

    # 逐个处理每个数据块
    for chunk in chunk_iter:
        # 将当前块的'domain'列转换为列表并添加到all_done_domains中
        alldonedomains.extend(chunk['domain'].dropna().unique().tolist())

    alldonedomains=set(alldonedomains)

    print(f'load alldonedomains:{len(list(alldonedomains))}')

    donedomains=[element for element in domains if element  in alldonedomains]

    print(f'load done domains {len(donedomains)}')

    tododomains=list(set([cleandomain(i) for i in domains])-set(donedomains))

    print(f'to be done {len(tododomains)}')
    time.sleep(30)
    for domain in tododomains:


        domain=cleandomain(domain)
        # print(domain)
        if  domain not in donedomains:
            print('add domain',domain)
            task = asyncio.create_task(get_rank(domain))
            tasks.append(task)
            if len(tasks) >= 100:
                # Wait for the current batch of tasks to complete
                await asyncio.gather(*tasks)
                tasks = []            
    await asyncio.gather(*tasks)

# Example usage: Main coroutine
async def main():
    start_time = time.time()
    await run_async_tasks()
    print(f"Time taken for asynchronous execution with concurrency limited by semaphore: {time.time() - start_time} seconds")

# Manually manage the event loop in Jupyter Notebook or other environments
if __name__ == "__main__":

    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    finally:
        loop.close()
    outfile.record()
    outfileerror.record()
    ray.shutdown()
