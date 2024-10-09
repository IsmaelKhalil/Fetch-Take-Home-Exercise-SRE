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
    method = endpoint.get('method', 'GET').upper()  # Default method is GET if not provided
    headers = endpoint.get('headers', {})  # Defaults to empty headers
    body = endpoint.get('body', None)  # Defaults to no body for the request

    try:
        # Starts a timer to measure response latency
        start_time = time.time()
        
        # Send the request based on the specified HTTP method
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

        # Calculates the response latency in milliseconds
        latency = (time.time() - start_time) * 1000

        # Determine if the endpoint is UP or DOWN based on status code and latency
        if 200 <= response.status_code < 300 and latency < 500:
            return 'UP', latency
        else:
            return 'DOWN', latency

    except requests.RequestException as e:
        print(f"Error checking health of {name}: {e}")
        return 'DOWN', 0

# Logs the cumulative availability percentage of each domain to the console.
def log_availability(domain_availability):
    for domain, data in domain_availability.items():
        total_requests = data['total']
        up_requests = data['up']
        availability = round(100 * (up_requests / total_requests)) if total_requests > 0 else 0
        print(f"{domain} has {availability}% availability percentage")

# Runs health checks for all endpoints every 15 seconds and prints results to the console.
def run_health_checks(endpoints):
    # Dictionary to keep track of domain availability statistics
    domain_availability = defaultdict(lambda: {'total': 0, 'up': 0})

    try:
        while True:
            # For each endpoint, check its health and update the availability statistics
            for endpoint in endpoints:
                domain = endpoint['url'].split('/')[2]  # Extract the domain from the URL
                status, latency = check_health(endpoint)

                # Update the count of total and UP requests for each domain
                domain_availability[domain]['total'] += 1
                if status == 'UP':
                    domain_availability[domain]['up'] += 1

                # Log the status and latency of each request
                print(f"Endpoint: \"{endpoint['name']}\" - Status: {status}; Latency: {latency} ms")

            # Log the overall availability percentages after each 15-second cycle
            log_availability(domain_availability)

            # Wait for 15 seconds and run again
            time.sleep(15)

    except KeyboardInterrupt:
        # Gracefully exit the program when the user interrupts (e.g., CTRL+C)
        print("Program exited by user.")

# Main function that accepts user input and runs the health check process.
def main():
    # Use input() to ask the user for the YAML configuration file path
    config_file_path = input("Please enter the path to the configuration file: ")

    # Load the YAML configuration file
    endpoints = read_yml(config_file_path)

    # Start the health check process for the endpoints
    run_health_checks(endpoints)

if __name__ == "__main__":
    main()