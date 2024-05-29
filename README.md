# LINE Bot with Selenium

This project integrates a LINE Bot with Selenium to fetch bus information.

## Setup

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/your-repository-name.git
    cd your-repository-name
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Ensure `chromedriver` is in the `drivers` directory.

4. Set environment variables:
    ```bash
    export LINE_CHANNEL_ACCESS_TOKEN=your_line_channel_access_token
    export LINE_CHANNEL_SECRET=your_line_channel_secret
    ```

5. Run the application:
    ```bash
    python app.py
    ```

## Usage

Send "557公車" or "300公車" to the LINE bot to get bus information.
