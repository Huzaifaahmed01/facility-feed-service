# SQL query to retrieve facility details from the 'facility' table.
# The query selects specific columns and orders the results by 'id'.
# It uses OFFSET and LIMIT for pagination,
# where $1 and $2 are placeholders for offset and limit values.
# The query is designed for use with PostgreSQL.
GET_FACILITIES_QUERY = """
    SELECT id, name, phone, url, latitude, longitude, country, locality, region, postal_code, street_address 
    FROM facility
    ORDER BY id
    OFFSET $1 LIMIT $2;
"""
