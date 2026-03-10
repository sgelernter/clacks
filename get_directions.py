import requests

ROUTES_API_ENDPOINT="https://routes.googleapis.com/directions/v2:computeRoutes"

def _get_coordinates_for_address(address: str, maps_api_key: str):
    res = requests.get(f'https://maps.googleapis.com/maps/api/geocode/json', params={"address": address, "key": maps_api_key})
    location = res.json()['results'][0]['geometry']['location']
    return {"location": {"latLng": {"latitude": location['lat'], "longitude": location['lng']}}}

def _parse_steps(steps: dict):
    parsed_steps = []
    i = 0
    for step in steps:
        if "distanceMeters" in step: 
            i += 1
            step_str = f'{i} - {step["travelMode"] if "travelMode" in step else ""} {step["distanceMeters"]}m\n'
            if "navigationInstruction" in step:
                if "maneuver" in step['navigationInstruction']:
                    step_str += step['navigationInstruction']['maneuver']
                if "instructions" in step['navigationInstruction']:
                    step_str += f' {step["navigationInstruction"]["instructions"]}'
            parsed_steps.append(step_str)
    return '\n'.join(parsed_steps)

def get_route_steps(origin_address: str, destination_address: str, maps_api_key: str, mask_values: list[str] = ["routes.legs"]):
    origin, destination = _get_coordinates_for_address(origin_address, maps_api_key), _get_coordinates_for_address(destination_address, maps_api_key)
    headers = {
        "X-Goog-FieldMask": "*" if mask_values is None else ','.join(mask_values),
        "X-Goog-Api-Key": maps_api_key
    }
    res = requests.post(ROUTES_API_ENDPOINT, headers=headers, json={"origin": origin, "destination": destination, "travelMode": "TRANSIT"})
    steps = res.json()['routes'][0]['legs'][0]['steps']
    return _parse_steps(steps)

