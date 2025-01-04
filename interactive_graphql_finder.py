import requests
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urljoin

# Define common GraphQL paths to check
GRAPHQL_ENDPOINTS = [
    "/graphql", "/graphiql", "/graphql/v1", "/api/graphql",
    "/api/v1/graphql", "/v1/graphql"
]

def check_graphql(domain):
    """
    Check if a domain has a GraphQL endpoint.
    """
    headers = {
        "User-Agent": "AdvancedGraphQLFinder/1.0",
        # Add more headers here if required for authentication
    }
    results = []
    for endpoint in GRAPHQL_ENDPOINTS:
        url = urljoin(domain, endpoint)
        try:
            response = requests.get(url, headers=headers, timeout=5)
            if response.status_code == 200 and (
                "graphql" in response.text.lower() or "application/json" in response.headers.get("Content-Type", "")
            ):
                results.append(f"✅ {url} - GraphQL Found!")
        except requests.exceptions.RequestException:
            results.append(f"❌ {url} - No response")
    return results

def scan_domain(domain):
    """
    Scan a single domain for GraphQL endpoints.
    """
    domain = domain.strip()
    if not domain.startswith("http"):
        domain = "http://" + domain  # Add protocol if missing
    return check_graphql(domain)

def main():
    # Ask for domain file name
    input_file = input("Enter the domain file name (e.g., domain.txt): ").strip()
    output_file = "graphql_advanced_results.txt"

    try:
        # Read domains from the specified file
        with open(input_file, "r") as file:
            domains = file.readlines()
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found!")
        return

    results = []
    print("[*] Starting GraphQL discovery...")

    # Use ThreadPoolExecutor for concurrent scanning
    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_domain = {executor.submit(scan_domain, domain): domain for domain in domains}
        for future in future_to_domain:
            domain_results = future.result()
            results.extend(domain_results)

    # Save results to output file
    with open(output_file, "w") as file:
        file.write("\n".join(results))

    print(f"[+] Scanning completed. Results saved in {output_file}")

if __name__ == "__main__":
    main()
