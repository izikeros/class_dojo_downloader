# class_dojo_downloader

Download all ClassDojo photos and videos in your timeline.

> NOTE: The original author is unknown. The docstring mention: kecebongsoft
> >
> This version has several features not present in the original version:
> - add group name to the downloaded files (useful for multiple children
> - create classdojo directory in the current directory if it does not exist
> - use .env file for storing session cookies
> - updated README extended on e.g. instructions on how to get session cookies

## Prerequisites
- create virtual environment with `requests` and `python-dotenv` packages. You can use `pdm` or just pure Python:

```sh
# create venv
python3 -m venv venv

# activate
source venv/bin/activate

# install dependencies
pip install requests python-dotenv
```

## Usage
1. Use the `.env_template` to create `.env` file with session cookie values. Check your session cookie by opening ClassDojo in the browser and copy the following cookies:
   - `dojo_log_session_id`,
   - `dojo_login.sid`,
   - `dojo_home_login.sid`
   
   See the section below "Reading Cookies" for more information on how to get the cookies.

2. Run this script and wait for it to finish.

### Troubleshooting

- Make sure you have a correct session cookies set in this script. 
- Make sure you can open the `FEED_URL` listed in this script from within your browser (assuming you can open ClassDojo website)

## How it works:
1. Fetch list of items in the timeline, if there are multiple pages, it will fetch for all pages.
2. Collect list of URLs for the attachment for each item
3. Download the files into local temporary directory, and also save the timeline activity as a json file.

## Reading cookies
You can read cookie values in Chrome and Brave browsers using the following methods:

**Method 1: Using the Chrome DevTools**

1. Open the Chrome browser and navigate to the webpage that sets the cookies.
2. Press F12 or right-click on the page and select "Inspect" to open the Chrome DevTools.
3. In the DevTools, switch to the "Application" tab.
4. Click on the "Cookies" tab.
5. You will see a list of cookies set by the webpage. You can expand each cookie to view its values.

**Method 2: Using the Chrome Console**

1. Open the Chrome browser and navigate to the webpage that sets the cookies.
2. Press F12 or right-click on the page and select "Inspect" to open the Chrome DevTools.
3. In the DevTools, switch to the "Console" tab.
4. Type the following command and press Enter: `document.cookie`
5. This will display the entire cookie string.
6. You can parse the cookie string to extract the values you need.

**Method 3: Using the Brave Browser**

1. Open the Brave browser and navigate to the webpage that sets the cookies.
2. Press F12 or right-click on the page and select "Inspect" to open the Brave DevTools.
3. In the DevTools, switch to the "Elements" tab.
4. Click on the "Elements" tab and then click on the "Cookies" tab.
5. You will see a list of cookies set by the webpage. You can expand each cookie to view its values.

Remember that cookies are specific to the domain that sets them, so you need to access the cookies from the same domain to read their values.
