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

""" 
important excerpt from instructions:

Output should be one line per location, in the format [location name] <-> [location
name], e.g.:
Adastral <-> London
London <-> Birmingham
Birmingham <-> Adastral
Order is not important, but you should only output one row for each connected pair of
locations.

my derived requirements from this:
- no duplicates of connections, because A <-> B is basically the same as B <-> A
- only output connections between locations that are directly linked by routers
- has to be printed line by line in the terminal as <location name> <-> <location name>

to find a connection between locations, locations have routers, routers connect to each others,
and this is how locations are linked.
Like: London has router 1, and Birmingham has router 2. Router 1 connects to Router 2.
Then London and Birmingham are connected and must be printed as London <-> Birmingham.
"""

# convert JSON to an object Python can work with
routers = data.get("routers", [])
locations = data.get("locations", [])

# set of connections
connections = set()

# find all connections between locations
# do not add if given A and B, B <-> A exists in connections
# the cities must be distinct, cannot be a city into itself, so A must not equal B ("London <-> London" is wrong)

router_id_to_location_id = {}
location_id_to_name = {}

for router in routers:
    router_id_to_location_id[router["id"]] = router["location_id"]

for location in locations:
    location_id_to_name[location["id"]] = location["name"]

for router in routers:
    current_location_id = router["location_id"]
    current_location_name = location_id_to_name.get(current_location_id)
    
    if not current_location_name:
        continue
    
    for linked_router_id in router.get("router_links", []):
        linked_location_id = router_id_to_location_id.get(linked_router_id)
        if linked_location_id is None:
            continue
            
        linked_location_name = location_id_to_name.get(linked_location_id)
        if not linked_location_name:
            continue
        
        # no self-connections
        if current_location_name == linked_location_name:
            continue
        
        # ensure consistent ordering to avoid duplicates
        # always put alphabetically first location first (for no particular reason)
        if current_location_name < linked_location_name:
            connection = f"{current_location_name} <-> {linked_location_name}"
        else:
            connection = f"{linked_location_name} <-> {current_location_name}"
        
        connections.add(connection)

# print connections
for conn in connections:
    print(conn)
