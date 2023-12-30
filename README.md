# pixiv_artist_download
a simple python code to download pixiv artist illusts, manga and novels.

# how to use?

## step1: edit pixiv_crawl_input.json
you need to edit the pixiv_crawl_input.json file first.

### PHPSESSID
defult NaN, input PHPSESSID to download login required contents.
### user_id
input one or multiple artist id that you wanted to download.
### illusts
defult true, input true if you want to download illusts, else enter false
### manga
defult true, input true if you want to download manga, else enter false
### novels
defult true, input true if you want to download novels, else enter false

### Example: if i wanted to download novels from 2 artists with login required contents, the json file will look like:
{
	"PHPSESSID":12345678_3rzvLrqtQ69jH3bpu0gwPMyds4mOti6k,
	"user_id":["12345678","22345678"],
	"illusts":false,
	"manga":false,
	"novels":true
}

## step2: run the code
run the main.py, and the download result should be located in the content file 

