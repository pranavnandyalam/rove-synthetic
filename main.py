from reference import *



#Extracting flight route data
routes = [
    ("JFK", "ORD", "NYC to Chicago"),
    ("SAN", "DFW", "San Diego to Dallas"),
    ("MIA", "CLT", "Miami to Charlotte"),
    ("SEA", "LAX", "Seattle to Los Angeles"),
    ("BOS", "MSY", "Boston to New Orleans")
]

for route in routes:
    for i in range(1, 3):
        if i < 10:
            day = "0" + str(i)
        else:
            day = i
        offers = simplify_offers(search_flights(route[0], route[1], f"2025-09-{day}", 1, 5))

        # save_flights_to_db(offers, routes[3])


