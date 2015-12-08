# File Downloader

Small script to download a web page and replace words and phrases.    
URL should be wrapped in double quotes if special characters are used.    
Search and replace string can be single words, or phrases in double quotes.    

Developed and tested with Python 2.7.10. Any version >= 2.6 < 3 should work.    

### Install

- Clone with git

        git clone https://github.com/kurohai/file-downloader.git
        cd ./file-downloader/

- Install requests

        pip install requests
        pip install -r requirements.txt

### Usage
    python file_downloader.py <url> <search string> <replace string>

### Examples
    python file_downloader.py lipsum.com "Lorem Ipsum" "stuff and things"
    python file_downloader.py "http://lipsum.com/" "Lorem Ipsum" "stuff and things"
