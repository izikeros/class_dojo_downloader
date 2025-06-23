# class_dojo_downloader

Download all ClassDojo notes, photos, and videos from your timeline.

> NOTE: The original author is unknown. The original script mentions kecebongsoft, and the earliest gist is by dedy-purwanto, at https://gist.github.com/dedy-purwanto/6ad1fa7c702981f35f25da780c50914d
> >
> This version has several features not present in the original version:
> - add group name to the downloaded files (useful for multiple children
> - ~create classdojo directory in the current directory if it does not exist~
> - use .env file for storing session cookies and "start" date (NOT_BEFORE) value
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

1. Create the folder/directory "classdojo_output" in the same folder as this script
2. Copy the `.env_template` to `.env` and add your session cookie values. Check your session cookie by opening ClassDojo in the browser and copy the following cookies (See the section below "Reading Cookies" for more information on how to get the cookies.) :
   - `dojo_log_session_id`,
   - `dojo_login.sid`,
   - `dojo_home_login.sid`
3. You will also want to edit NOT_BEFORE to align to the beginning of the school year you want to download.
4. Run this script ( source venv/bin/activate ; python3 main.py ) and wait for it to finish.

### Troubleshooting

- Make sure you have a correct session cookies set in this script. 
- Make sure you can open the `FEED_URL` listed in this script from within your browser (assuming you can open ClassDojo website)

## How it works:
1. Fetch list of items in the timeline, if there are multiple pages, it will fetch for all pages.
2. Collect list of URLs for the attachment for each item
3. Download the files into local temporary directory, and also save the timeline activity as a json file.
4. **NOTE: The script presumes most attachments are photos. You will have to rename any video files (usually larger, won't preview correctly) as .mpg instead of .jpg**

## Reading cookies
You can read cookie values in browsers using the following methods:

**Method 1: Using the Chrome DevTools**

1. Open the Chrome browser and navigate to https://home.classdojo.com, log in if you are not already
2. Press F12 or right-click on the page and select "Inspect" to open the Chrome DevTools.
3. In the DevTools, switch to the "Application" tab.
4. Click on the "Cookies" tab.
5. You will see a list of cookies set by the webpage. You can expand each cookie to view its values.

**Method 2: Using the Chrome Console**

1. Open the Chrome browser and navigate to https://home.classdojo.com, log in if you are not already
2. Press F12 or right-click on the page and select "Inspect" to open the Chrome DevTools.
3. In the DevTools, switch to the "Console" tab.
4. Type the following command and press Enter: `document.cookie`
5. This will display the entire cookie string.
6. You can parse the cookie string to extract the values you need.

**Method 3: Using the Brave Browser**

1. Open the Brave browser and navigate to https://home.classdojo.com, log in if you are not already
2. Press F12 or right-click on the page and select "Inspect" to open the Brave DevTools.
3. In the DevTools, switch to the "Elements" tab.
4. Click on the "Elements" tab and then click on the "Cookies" tab.
5. You will see a list of cookies set by the webpage. You can expand each cookie to view its values.

**Method 4: Using the Firefox Browser**
1. Open Firefox and navigate to https://home.classdojo.com, log in if you are not already
3. Press CTRL-SHIFT-I or user the ☰ menu, select "More Tools", then "Web Developer Tools" to open DevTools.
4. In the DevTools, switch to the "Storage" tab.
6. You will see a list of cookies set by the webpage. You can double click on the value of each cookie to copy it.
