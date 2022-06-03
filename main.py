import requests
import config
from _color import color as c

with open("log.txt", "w") as f:
    f.write("")
    f.close()

def log(message):
    print(message)

    with open("log.txt", "a") as f:
        f.write(message + "\n")
        f.close()
step = 500

individual = 0

for i in range(0, config.LAUNCHPAD_AMOUNT, step):
    
    collections = requests.get(f"http://api-mainnet.magiceden.dev/v2/collections?offset={i}&limit={step}").json()

    for collection in collections:
        individual += 1

        dcollection = dict(collection)

        keys = dcollection.keys()

        log(c.BOLD + c.UNDERLINE + c.rand() + f"project #{individual}  |  " + collection["name"] + c.END)
                            
        step = 20

        listings = []

        log("obtaining listings for collection...")

        for u in range(0, 10000, step):
            symbol = dcollection["symbol"]

            short_listings = requests.get(f"http://api-mainnet.magiceden.dev/v2/collections/{symbol}/listings?offset={u}&limit={step}")

            try:
                short_listings = short_listings.json()

                for item in short_listings:
                    ditem = dict(item)

                    listings.append(ditem)
            except:
                break

        print("getting best trade...")

        sorted_listings = sorted(listings, key=lambda x: x["price"])

        if len(sorted_listings) > 0:
            listing_1 = sorted_listings[0]
            listing_2 = sorted_listings[1]

            l1p = float(listing_1["price"])
            l2p = float(listing_2["price"])

            diff = l2p - l1p

            flip_value = diff * config.SOL_PRICE

            print("flipping value = " + (c.GREEN + str(round(flip_value, 2)) + "gbp" + c.END) if flip_value > config.VALUE_TRADE else (c.RED + str(round(flip_value, 2)) + "gbp" + c.END))

            if flip_value > config.VALUE_TRADE:
                print(c.GREEN + "FOUND FLIP" + c.END + "\n")

                with open("output.txt", "a") as f:
                    f.write("\n" + dcollection["name"])
                    f.close()
            
            else:
                print(c.RED + "flip value too low :P" + c.END + "\n")

        else:
            print(c.PURPLE + "project has no listings" + c.END + "\n")

    if len(collections) < step:
        break