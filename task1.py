# imports below this line
import urllib.request as request
import json

# task says: 1. access https://my-json-server.typicode.com/marcuzh/router_location_test_api/db
# i see a JSON format if i access using Chrome.

url = "https://my-json-server.typicode.com/marcuzh/router_location_test_api/db"
response = request.urlopen(url)

# 2. read data from API

data = json.loads(response.read())

# print(data) # uncomment to see the raw JSON data, for debugging

""" JSON data structure is as so:

{
    "routers": [
        {
            "id": x, (an int)
            "name": "name", (a string)
            "location_id": y (an int)
            "router_links": [
                z1, (an int belonging to another router, can be multiple in this array, see z2 and z3)
                z2,
                z3
            ]
        }
    ]
    "locations": [
        {
            "id": y, (an int)
            "postcode": "postcode", (a string)
            "name": "name" (a string)
        }
    ]
}

there can be multiple routers and locations, the above is just an example of the structure,
and i don't want to create multiple examples just to exhaustively display the structure.

and from what i see in the JSON data:
- the next id is not always the next integer, it can skip numbers,
  so i cannot assume that the id of the next router or location is always the next integer,
  which means no lazy iteration sadly.
- router_links can be empty, i did see one instance of a router with no links.
- the location_id of a router can be any integer, not necessarily the next one,
  and routers can share the same location_id.

these are just cases to account for and/or be aware of in the next bit numbered 3 below.

"""

# 3. output list of connections between locations

