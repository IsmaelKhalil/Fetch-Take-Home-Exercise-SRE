import time
import yaml
import requests
from collections import defaultdict

def read_yml(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def check_health(endpoint):
    name = endpoint.get('name')
    url = endpoint.get('url')
    method = endpoint.get('method', 'GET').upper()
    headers = endpoint.get('headers', {})
    body = endpoint.get('body', None)

    try:
        start_time = time.time()
        
        if method == 'GET':
            response = requests.get(url, headers=headers)
        elif method == 'POST':
            response = requests.post(url, headers=headers, json=body)
        elif method == 'PUT':
            response = requests.put(url, headers=headers, json=body)
        elif method == 'DELETE':
            response = requests.delete(url, headers=headers)
        else:
            print(f"Unsupported HTTP method: {method}")
            return 'DOWN', 0

        latency = (time.time() - start_time) * 1000

        if 200 <= response.status_code < 300 and latency < 500:
            return 'UP', latency
        else:
            return 'DOWN', latency

    except requests.RequestException as e:
        print(f"Error checking health of {name}: {e}")
        return 'DOWN', 0

def log_availability(domain_availability):
    for domain, data in domain_availability.items():
        total_requests = data['total']
        up_requests = data['up']
        availability = round(100 * (up_requests / total_requests)) if total_requests > 0 else 0
        print(f"{domain} has {availability}% availability percentage")

def run_health_checks(endpoints):
    domain_availability = defaultdict(lambda: {'total': 0, 'up': 0})

    try:
        while True:
            for endpoint in endpoints:
                domain = endpoint['url'].split('/')[2]  # Extract the domain from the URL
                status, latency = check_health(endpoint)

                domain_availability[domain]['total'] += 1
                if status == 'UP':
                    domain_availability[domain]['up'] += 1

                print(f"Endpoint: \"{endpoint['name']}\" - Status: {status}; Latency: {latency} ms")

            log_availability(domain_availability)

            time.sleep(15)

    except KeyboardInterrupt:
        print("Program exited by user.")

def main():
    config_file_path = input("Please enter the path to the configuration file: ")

    endpoints = read_yml(config_file_path)

    run_health_checks(endpoints)

if __name__ == "__main__":
    main()