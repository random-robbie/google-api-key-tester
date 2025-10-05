# Google API Key Tester

A script to test a Google API key against all discoverable Google Cloud services.

## Description

This script tests a Google API key against all discoverable Google Cloud services to determine which services are accessible. It provides a report of accessible APIs, APIs that are disabled but reveal the project ID, and APIs that require OAuth2.

## Features

-   Tests against all discoverable Google Cloud services.
-   Categorizes results into accessible APIs, informative denials, and APIs requiring OAuth2.
-   Identifies the Google Cloud Project ID associated with the API key.
-   No external dependencies.

## Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/random-robbie/google-api-key-tester.git
    ```
2.  Navigate to the project directory:
    ```bash
    cd google-api-key-tester
    ```

## Usage

Run the script with your Google API key:

```bash
python3 google-api-key-tester.py -k YOUR_API_KEY
```

You can also save the output to a file:

```bash
python3 google-api-key-tester.py -k YOUR_API_KEY -o report.txt
```

## Interpreting the Results

-   **ACCESSIBLE APIS**: The API key has some level of access to these APIs.
-   **ACTIONABLE INTELLIGENCE: INFORMATIVE DENIALS**: The API key was denied, but the error messages reveal the key's associated project ID and that the following APIs could potentially be enabled.
-   **INFO: REQUIRES OAUTH2**: These APIs do not support API keys for authentication and require OAuth2.

## Disclaimer

This tool is for educational purposes only. Do not use it to test API keys that you do not own.

## License

This project is licensed under the MIT License.