
# Google API Key Scanner

A powerful Python script to audit a Google API key against all discoverable Google Cloud services to determine its permissions and exposure.

This tool helps security professionals and developers understand the exact scope of an API key, highlighting which services are accessible and revealing the associated Google Cloud Project ID.

## Features

- **Comprehensive Scanning:** Tests the key against all 490+ APIs listed in the Google API Discovery Service.
- **Actionable Intelligence:** Identifies not just what a key *can* access, but also what it *could* access if services were enabled. The output reveals the associated Project ID, which is critical for remediation.
- **Clear Categorization:** Results are neatly grouped into:
    - `ACCESSIBLE APIS`: Services the key can interact with.
    - `INFORMATIVE DENIALS`: Services that are disabled but reveal the Project ID.
    - `REQUIRES OAUTH2`: Services that correctly reject API keys in favor of OAuth2.
- **File Output:** Easily save the detailed report to a text file for documentation and analysis.
- **No Dependencies:** Uses only standard Python libraries.

## Usage

1.  Clone the repository or download `google-api-key-tester.py`.
2.  Navigate to the tool's directory.

### Basic Scan

Provide the API key using the `-k` or `--key` argument.

```bash
python3 google-api-key-tester.py -k YOUR_API_KEY_HERE
```

### Save Report to File

Use the `-o` or `--output` argument to specify a file path for the report.

```bash
python3 google-api-key-tester.py --key YOUR_API_KEY_HERE --output scan_report.txt
```

## Interpreting the Output

- **`[+] ACCESSIBLE APIS`**: This is the most critical section. It lists all the services where the API key was accepted. If you see services here that you don't expect, it indicates the key is overly permissive.

- **`[*] ACTIONABLE INTELLIGENCE: INFORMATIVE DENIALS`**: This section is key for security auditing. It lists APIs that denied the key but returned an error message containing the **Google Cloud Project ID**. This tells you exactly which project the key belongs to, allowing you to track it down and remediate it. It also shows which powerful APIs could be enabled in that project, indicating the potential for future misuse.

- **`[*] INFO: REQUIRES OAUTH2`**: This is a good sign. It means these APIs are following best practices by disallowing the use of simple API keys for authentication.

## Disclaimer

This tool is intended for authorized security auditing and educational purposes only. Do not use it to test API keys that you do not own. The user is responsible for any and all actions performed using this tool.
