import requests

def get_earth_position_vector(date):
    base_url = "https://ssd.jpl.nasa.gov/horizons_batch.cgi"
    
    # Set up parameters for the API request
    params = {
        'batch': '1',
        'COMMAND': "399",
        'CENTER': "'@0'",
        'COORD_TYPE': "'RECT'",
        'SITE_COORD': "'0,0,0'",
        'MAKE_EPHEM': "'YES'",
        'TABLE_TYPE': "'VECTORS'",
        'OUT_UNITS': "'KM-S'",
        'REF_PLANE': "'ECLIPTIC'",
        'VEC_LABELS': "'NO'",
        'VEC_DELTA_T': "'YES'",
        'TARGET': "'10'",
        'START_TIME': f"'{date} 00:00:00'",
        'STOP_TIME': f"'{date} 23:00:00'",
        'STEP_SIZE': "'1d'",
        'CSV_FORMAT': "'YES'"
    }
    
    # Make the API request
    response = requests.get(base_url, params=params)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the response and extract the position vector
        lines = response.text.split('\n')

        # this was merely here to count the lines :P
        #for idx_l, l in enumerate(lines):
        #    print(str(idx_l) + ":" + l)
        data_line = lines[54]
        values = data_line.split(',')
        
        # Extract x, y, z coordinates from the response
        x, y, z = map(float, values[3:6])
        
        # Return the position vector (km)
        return [x, y, z]
        # return {'x': x, 'y': y, 'z': z}
    else:
        print(f"Error: Unable to fetch data. Status code: {response.status_code}")
        return None

