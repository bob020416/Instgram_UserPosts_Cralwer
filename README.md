# Instgram_UserPosts_Cralwer
Tool designed to scrape Instagram account details using the Smart Proxy API. This tool will gather posts, captions, likes, comments, and other relevant information, exporting the data into a CSV file and saving images to a specified directory on Windows.
### Introduction to Instagram_UserPosts_Crawler

In the realm of social media analytics and research, the ability to efficiently gather detailed information from Instagram accounts is invaluable. The Instagram_UserPosts_Crawler is designed with this need in mind, offering a powerful tool for scraping comprehensive details from Instagram profiles. Utilizing the Smart Proxy API, this tool can bypass common scraping challenges, enabling users to collect a wide array of data including posts, captions, the number of likes, top comments, and other pertinent account information.

The crawler is engineered for simplicity and efficiency, allowing users to save the scraped data into a structured CSV file and download all images from the targeted accounts directly into a specified Windows directory. This functionality not only serves researchers and marketers looking to analyze Instagram data but also provides a resource for developers interested in creating data-driven applications.

**Example of scrapping ferragamo accounts csv and all images:**
![ferragamo_posts - Excel 2024_2_12 下午 07_30_17](https://github.com/bob020416/Instgram_UserPosts_Cralwer-/assets/82202284/ba0164d7-bb37-48a2-b30a-1740c885fa0e)

![images 2024_2_12 下午 07_30_55](https://github.com/bob020416/Instgram_UserPosts_Cralwer-/assets/82202284/1bd89e62-0811-4367-aa78-f6d7d45c3407)

Key Features:
- **Comprehensive Data Collection:** From detailed post analytics to capturing visual content, gather all the essential data from Instagram accounts.
- **Efficient Proxy Utilization:** Leverage Smart Proxy API for reliable data access, minimizing the risk of IP bans or rate limiting.
- **User-Friendly Output:** Organize scraped data into CSV files for easy analysis and store images systematically in a local directory.

### Prerequisites for Using Instagram_UserPosts_Crawler

Before diving into the capabilities of the Instagram_UserPosts_Crawler, it's essential to ensure you have the necessary tools and accounts set up. This preparation will facilitate a smooth installation process and enable you to start scraping Instagram data efficiently.

#### Required Tools and Accounts:

1. **Python Installation:**
   - The crawler is built on Python, making it mandatory to have Python installed on your system. Ensure you have Python 3.6 or later versions for optimal compatibility. Visit the [official Python website](https://www.python.org/downloads/) for download and installation instructions.

2. **Smart Proxy API Account:**
   - Given the tool's reliance on Smart Proxy for accessing Instagram data, you'll need an active Smart Proxy API account. This account will provide you with the necessary API keys to configure the crawler. Sign up or log in to your account on the [Smart Proxy website](https://smartproxy.com/) to retrieve your API credentials.

3. **Git (Optional):**
   - While not strictly necessary, having Git installed will simplify the process of cloning the repository to your local machine. If you prefer not to use Git, you can download the repository as a ZIP file from GitHub.

Given your clarification, let's revise the configuration instructions to align with the actual setup process involving `scrap.py` and the method for specifying Smart Proxy API credentials and Instagram account names directly within the script.

### Revised Configuration

To configure the Instagram_UserPosts_Crawler for use with your Smart Proxy API and to target specific Instagram accounts, you'll need to make modifications directly in the `scrap.py` script. This approach allows for a streamlined setup process, ensuring your API credentials are securely entered and the desired Instagram accounts are specified for scraping.

#### Smart Proxy API Configuration in `scrap.py`

1. **Modify API Credentials:**
   - Open `scrap.py` in a text editor or IDE of your choice.
   - Locate the section of the script where Smart Proxy API credentials are defined. It will have placeholder values for the username and password. Replace these placeholders with your actual Smart Proxy API username and password. The modification should look something like this:
     ```python
     # Smart Proxy API Credentials
     proxy_username = 'your_smart_proxy_username'
     proxy_password = 'your_smart_proxy_password'
     ```
   - Ensure you save the changes to the `scrap.py` file after entering your credentials.

#### Specifying Instagram Accounts to Scrape

2. **Input Account Names in the Account List:**
   - Within `scrap.py`, find the list or array designated for Instagram account names. If it's not predefined, you may need to create it following the syntax:
     ```python
     # List of Instagram accounts to scrape
     account_list = ['account_name_1', 'account_name_2', 'account_name_3']
     ```
   - Replace `'account_name_1'`, `'account_name_2'`, `'account_name_3'` with the actual usernames of the Instagram accounts you wish to scrape. You can add or remove account names as needed, depending on how many accounts you're targeting.

### Usage

After successfully configuring the Instagram_UserPosts_Crawler with your Smart Proxy API credentials and specifying the Instagram accounts you wish to scrape, you're now ready to execute the script and collect data. This section outlines the steps to run `scrap.py`, detailing the command-line arguments and what to expect in terms of output.

#### Running the `scrap.py` Script

To start the data collection process, follow these steps:

1. **Open Your Command Line Interface:**
   - Navigate to the directory where your `scrap.py` script is located using the command line or terminal.

2. **Execute the Script:**
   - Run the script by entering the following command:
     ```shell
     python scrap.py
     ```
   - This command initiates the scraping process, where `scrap.py` will use the specified Smart Proxy API credentials to access Instagram and begin collecting data from the accounts listed in your `account_list`.

#### Command-Line Arguments

- The current setup does not require any additional command-line arguments, as the script uses the internal configurations (API credentials and account list) you've set up. However, if you modify the script in the future to accept arguments, you could run it with additional options for flexibility, such as specifying different accounts or output directories directly from the command line.

#### Output Handling = Find the file of the output filed called "Results" in user directory 

- **CSV File Creation:** The script will generate a CSV file containing all scraped data, including captions, the number of likes, top comments, and other relevant information for each post from the targeted Instagram accounts. This file will be saved in the specified output directory within your project folder.

- **Image Downloading:** Alongside textual data, `scrap.py` will download all images from the posts of the specified accounts. These images will be stored in a separate folder within your output directory, organized by account name for easy navigation.

