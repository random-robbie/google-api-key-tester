import urllib.request
import json
import ssl
import time
import argparse
from collections import defaultdict

# URL for the Google API Discovery Service
DISCOVERY_URL = "https://www.googleapis.com/discovery/v1/apis"

def test_api_endpoint(session, api_name, base_url, key, results):
    """Tests a generic request to the API's base URL and categorizes the response."""
    url = f"{base_url}?key={key}"
    try:
        with session.open(url, timeout=10) as response:
            status_code = response.getcode()
            # Any successful response is noteworthy
            if 200 <= status_code < 300:
                results['accessible'].append(f"{api_name}")
            else:
                results['other_errors'].append(f"{api_name}: Responded with unexpected HTTP {status_code}")

    except urllib.error.HTTPError as e:
        status_code = e.code
        try:
            body = e.read().decode('utf-8', errors='ignore')
            error_json = json.loads(body)
            message = error_json.get('error', {}).get('message', 'No error message.')

            if "API has not been used" in message or "is disabled" in message:
                project_id = 'Unknown'
                try:
                    project_id = message.split('project: ')[-1].split(' ')[0]
                except IndexError: pass
                results['informative_denials'].append(f"{api_name} (Project: {project_id})")
            elif "API key not valid" in message:
                results['key_invalid_for_api'].append(f"{api_name}")
            elif "API keys are not supported" in message:
                results['requires_oauth'].append(f"{api_name}")
            else:
                results['other_errors'].append(f"{api_name}: FAILED (HTTP {status_code}): {message}")
        except (json.JSONDecodeError, AttributeError):
            results['other_errors'].append(f"{api_name}: FAILED (HTTP {status_code}): {e.reason}")
    except Exception as e:
        results['other_errors'].append(f"{api_name}: ERROR ({type(e).__name__})")

def format_results(results):
    """Formats the collected results into a readable string."""
    output = []
    output.append("--- Google API Key Scan Report ---")

    if results['accessible']:
        output.append("\n[+] ACCESSIBLE APIS")
        output.append("="*20)
        output.append("The key has some level of access to the following APIs:")
        for item in sorted(results['accessible']):
            output.append(f"  - {item}")
    
    if results['informative_denials']:
        output.append("\n[*] ACTIONABLE INTELLIGENCE: INFORMATIVE DENIALS")
        output.append("="*50)
        output.append("The key was denied, but the error messages reveal the key's associated project ID and that the following APIs could potentially be enabled:")
        for item in sorted(results['informative_denials']):
            output.append(f"  - {item}")

    if results['key_invalid_for_api']:
        output.append("\n[-] DENIED: API KEY INVALID")
        output.append("="*28)
        output.append("The key was explicitly rejected by these APIs.")
        for item in sorted(results['key_invalid_for_api']):
            output.append(f"  - {item}")

    if results['requires_oauth']:
        output.append("\n[*] INFO: REQUIRES OAUTH2")
        output.append("="*25)
        output.append("These APIs do not support API keys for authentication and require OAuth2.")
        for item in sorted(results['requires_oauth']):
            output.append(f"  - {item}")

    output.append("\nScan complete.")
    return "\n".join(output)

def main():
    parser = argparse.ArgumentParser(description="Scan all discoverable Google APIs with a given key to check for permissions.")
    parser.add_argument("-k", "--key", required=True, help="The Google API key to test.")
    parser.add_argument("-o", "--output", help="Optional path to save the report to a text file.")
    args = parser.parse_args()

    api_key = args.key

    print(f"\nStarting full API discovery scan for key ending in '...{api_key[-4:]}'")
    print("Step 1: Fetching list of all discoverable APIs from Google...")

    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    opener = urllib.request.build_opener(urllib.request.HTTPSHandler(context=ctx))

    try:
        with opener.open(DISCOVERY_URL) as response:
            if response.getcode() == 200:
                discovery_data = json.loads(response.read().decode())
                apis = discovery_data.get('items', [])
                print(f"Found {len(apis)} APIs to test. This may take a few minutes...")
            else:
                print(f"Failed to fetch API list: HTTP {response.getcode()}")
                return
    except Exception as e:
        print(f"Failed to fetch API list: {e}")
        return

    results = defaultdict(list)
    
    print("\nStep 2: Testing each API...")
    for i, api in enumerate(apis):
        name = api.get('title', api.get('name'))
        base_url = api.get('baseUrl', api.get('rootUrl'))
        if not base_url:
            continue
        
        print(f"({i+1}/{len(apis)}) Testing: {name}", end='\r')
        test_api_endpoint(opener, name, base_url, api_key, results)
        time.sleep(0.05) # Be a good citizen

    print("\n\nStep 3: Generating report...")
    report = format_results(results)
    print(report)

    if args.output:
        print(f"\nSaving report to {args.output}...")
        with open(args.output, 'w') as f:
            f.write(report)
        print("Done.")

if __name__ == "__main__":
    main()