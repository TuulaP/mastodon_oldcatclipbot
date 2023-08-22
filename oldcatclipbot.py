
# Goal , post a random cat clipping to Mastodon as a bot.

import random
import requests
from simplemasto import post_to_mastodon


baseserver = "https://digi.kansalliskirjasto.fi"
## local = "http://localhost:9090"

api_url = baseserver + "/rest/article-search/search-by-type?offset=0&count=22"


headers = {'Content-type': 'application/json', 'Accept': 'application/json'}

data = {
    "keywords": ['kissa']
}


r = requests.post(url=api_url, json=data, headers=headers)  

##print("Status:", r.status_code)


# We got data from webystem A
if (r.status_code == 200):

    response = r.json() 

    totalResults = response['totalResults']
    allResults = response['rows']
    randomOne = random.choice(allResults)


    # Grab data of the clipping.
    # Generate post contents

    articleTitle = randomOne['title']
    previewImageUrl = baseserver + randomOne['previewImageUrl']
    bindingTitle = randomOne['bindingTitle']
    bindingDate = randomOne['bindingDate']
    fullUrl = baseserver + randomOne['url']


    tootText = articleTitle + "\nFrom:" + bindingTitle  \
        + "\nPublished originally on: " + bindingDate

    tootText += "\nSee full image at: "+fullUrl

    ## print(tootText)

    # Post to mastodon
    postresult = post_to_mastodon(tootText)

    

#print("All done, bye!")






