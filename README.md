Project overview (problem, audience, value)
- Problem: Airbnb renters are being mislead due to a lack of information easily accessible
- Audience: People looking for AirBnB's in popular US cities
- Value: Increasing transparency for potential airbnb guests on statistics such location, price, and crime to allow them to make a more informed decision


How to run (local + deploy notes)
- render link
- git link for repos

Data sources & data dictionary
- Bootswatch LUX style
- https://insideairbnb.com/get-the-data/
- https://lasd.org/transparency/part1and2crimedata/
- https://jsonformatter.curiousconcept.com/#
- https://www.nyc.gov/site/nypd/stats/crime-statistics/park-crime-stats.page
Data Dictionary:
    -Airbnb Listings
        -'room_type' : Types of airbnb rooms (Ex: Shared room)
        - 'price': List pricing
        - 'neighbourhood': Neighborhood name
    -Neighborhoods GeoJSON
        -'properties.neighbourhood': Name of neighbourhood
    -NYC Shooting Incididents
        -'OCCUR_DATE': Date of shooting
        -'OCCUR_TIME': TIme of shooting
        -'Latitude': Latitude coordinates
        -'Longitude': Longitude coordinates
        -'PRECINCT': Police precinct
        -'LOCATION_DESC': Description of the location
    -LA Crime Data
        -'UNIT_NAME': Neighborhood or reporting district
        -'CATEGORY': Category of crime committed
        -'STAT_DESC': Description of crime committed
        -'LATITUDE': Latitude coordinates
        -'LONGITUDE': Longitude coordinates

AI Usage Appendix
- Tools Used: Microsoft Copilot (Within VS code)
- Prompts/snippets (high-level):
    - Can you explain why there is an error with my chart display code on page1 and highlight steps I can take to fix it?
    - How can I import a bootswatch template to style my dash home page, page1, and page2?
    - What is currently wrong with my graph titles?
- Where AI output was used: AI was used to fill gaps within our code that produced errors and portion of data dictionary
- What you verified/edited: We verified that all code assistance from AI was correct and properly ran. If the code was incorrect or would not run, we made sure to make edits before finalizing