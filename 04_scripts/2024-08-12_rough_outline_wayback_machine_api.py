# Using WaybackPy to bulk archive URLs

# Code copied liberally from pypi

# import package
from waybackpy import WaybackMachineSaveAPI


url = "https://library.carr.org/"
user_agent = "emily"

save_api = WaybackMachineSaveAPI(url, user_agent)
a = save_api.save()

save_api.cached_save

save_api.timestamp()


test = WaybackMachineSaveAPI('http://www.harvard.edu/', 'emily')
test.save()

from waybackpy import WaybackMachineCDXServerAPI
test = WaybackMachineCDXServerAPI('http://www.harvard.edu/', 'emily')
test.oldest()


# pseudo code for how to make this work


# import stuff
# assign the variable names for the auth stuff

# import .txt file with the list of URLs
# if extant - import .csv file with timestamps

# some kind of merge to reconcile the txt and the csv
# anything that ONLY appears on the txt, add to csv as a new row

# isolate only the rows of the csv (now a df) that do not
#   # have a timestamp in the timestamp column
# leave the rows that do have a timestamp alone
# for the isolated rows
#   # archive them (code above)
#   # retrieve their archival timestamp and put it in that column
#   # save the output URL to its own column (later we can import the data from this column!)

# when complete, save new a new copy of the csv













