import ast
from json import JSONDecodeError
import json
import math
from threading import Thread
import time
import requests
import config
from _color import color as c

with open("log.txt", "w") as f:
    f.write("")
    f.close()

with open("output.txt", "w") as f:
    f.write("")
    f.close()

def log(message):
    print(message)

    with open("log.txt", "a") as f:
        try:
            f.write(message + "\n")
        except UnicodeEncodeError as e:
            pass
        
        f.close()

def loop():
    step = 500

    individual = 0

    collections = []

    for _ in range(10):
        collections.append([])

    log(c.YELLOW + "obtaining list of collections... this could take a while\n" + c.END)

    for i in range(0, config.LAUNCHPAD_AMOUNT, step):
        try:
            short_collections = requests.get(f"http://api-mainnet.magiceden.dev/v2/collections?offset={i}&limit={step}").json()

            for index, collection in enumerate(short_collections):
                individual += 1

                pool = math.floor(index / 50)

                collections[pool].append(collection)

            if len(short_collections) < step:
                break
        except:
            time.sleep(1)

            short_collections = requests.get(f"http://api-mainnet.magiceden.dev/v2/collections?offset={i}&limit={step}").json()

            for index, collection in enumerate(short_collections):
                individual += 1

                if index < len(collections):
                    collections[index].append(collection)
                else:
                    collections[math.floor(index / 50)].append(collection)

            if len(short_collections) < step:
                break
        
    def proc(pool):
        individual = 0

        for collection in pool:
            individual += 1
            dcollection = collection

            keys = dcollection.keys()

            log(c.BOLD + c.UNDERLINE + c.rand() + f"project #{individual}/{len(pool)}  |  " + collection["name"] + c.END)
                                
            step = 20

            listings = []

            log(c.YELLOW + "obtaining listings for collection..." + c.END)

            for u in range(0, 10000, step):
                symbol = dcollection["symbol"]

                short_listings = requests.get(f"http://api-mainnet.magiceden.dev/v2/collections/{symbol}/listings?offset={u}&limit={step}")

                try:
                    short_listings = short_listings.json()

                    if len(short_listings) > 0:
                        for item in short_listings:
                            ditem = dict(item)

                            listings.append(ditem)
                    
                    else:
                        if len(short_listings) < step:
                            break

                except JSONDecodeError as e:
                    time.sleep(1)

                    short_listings = short_listings.json()

                    if len(short_listings) > 0:
                        for item in short_listings:
                            ditem = dict(item)

                            listings.append(ditem)
                    
                    else:
                        if len(short_listings) < step:
                            break
                    
            sorted_listings = sorted(listings, key=lambda x: x["price"])

            if len(sorted_listings) > 1:
                listing_1 = sorted_listings[0]
                listing_2 = sorted_listings[1]

                l1p = float(listing_1["price"])
                l2p = float(listing_2["price"])

                diff = l2p - l1p

                flip_value = diff * config.SOL_PRICE

                print(c.GREEN + "flipping value " + str(round(flip_value, 2)) + "gbp\n" + c.END if flip_value >= config.VALUE_TRADE else c.RED + "flipping value " + str(round(flip_value, 2)) + "gbp\n" + c.END)

                if flip_value > config.VALUE_TRADE:
                    with open("output.txt", "a") as f:
                        f.write("\n" + dcollection["name"])
                        f.close()
            else:
                print(c.PURPLE + "project has no listings" + c.END + "\n")

    # for pool in collections:

    print(len(collections))

    thr = Thread(target=proc, args=(collections[0],))
    thr.start()

    # loop()
loop()
