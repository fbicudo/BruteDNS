import socket
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
import sys


def resolve_dns(domain):
    """
    Resolve a single DNS name to its corresponding IP address.
    
    :param domain: Domain name to resolve.
    :return: Tuple containing the domain name and its resolved IP address or error message.
    """
    try:
        ip_address = socket.gethostbyname(domain)
        return domain, ip_address
    except socket.gaierror as e:
        pass

def resolve_dns_names_concurrently(domains, pb, max_workers=10):
    """
    Resolve a list of DNS names to their corresponding IP addresses using threads.

    :param domains: List of domain names to resolve.
    :param max_workers: Maximum number of threads to use.
    :return: Dictionary with domain names as keys and IP addresses (or error messages) as values.
    """
    results = {}
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_domain = {executor.submit(resolve_dns, domain): domain for domain in domains}
        for future in as_completed(future_to_domain):
            domain = future_to_domain[future]
            try:
                domain, ip_address = future.result()
                results[domain] = ip_address
                print(f"\nDomain {domain} is valid")
                pb.update(1)
            except Exception as e:
                pb.update(1)
    return results

if __name__ == "__main__":
    
    tld = input("Enter the domain to brute force (ex. \"dnsdomain.com\"): ")
    if tld.strip() == "":
        print("Error: Domain cannot be empty")
        sys.exit()
    dic_bf = input("Enter the dictionary file name: ")
    tld = tld.strip()
    dic_bf = dic_bf.strip()


    try:
        with open(dic_bf, 'r') as file:
            hosts = file.readlines()

        domain_list = []


        for h in hosts:
            # print(h)
            domain_list.append(f"{h.strip('\n')}.{tld}")

        
        with tqdm(total=len(domain_list), unit=" hosts") as progress_bar:

            # Resolve DNS names concurrently
            resolved_results = resolve_dns_names_concurrently(domain_list, progress_bar, max_workers=10)
        
        # Write results to a file and print to the screen
        with open('valid_domains.txt','w') as file:
            print("\nDNS Resolution Results:")
            for domain, ip in resolved_results.items():
                file.write(f"{domain}: {ip}\n")
                print(f"{domain}: {ip}")

    except Exception as e:
        print(e.args)


