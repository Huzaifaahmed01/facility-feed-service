DROP TABLE IF EXISTS facility;

CREATE TABLE facility (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    phone TEXT,
    url TEXT,
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION,
    country TEXT,
    locality TEXT,
    region TEXT,
    postal_code TEXT,
    street_address TEXT
);

-- Insert dummy data into the facility table
INSERT INTO facility (name, phone, url, latitude, longitude, country, locality, region, postal_code, street_address)
SELECT
    'Facility ' || g,
    '+1-800-55' || LPAD(g::TEXT, 2, '0'),
    'https://modified-facility' || g || '.example.com',
    40.0 + random(),
    -75.0 + random(),
    'CA',
    'City ' || (g % 15),
    'Region ' || (g % 7),
    'MZIP' || LPAD((80000 + g)::TEXT, 5, '0'),
    (200 + g) || ' Modified St'
FROM generate_series(1, 1000) AS g;