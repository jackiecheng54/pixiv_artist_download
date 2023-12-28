import requests
import json
import os
from bs4 import BeautifulSoup
import re

def main():

    os.chdir(os.path.dirname(__file__))
    current_directory = os.getcwd()

    create_folder(f'{current_directory}\content')

    with open("pixiv_crawl_input.json","r") as f:
        pivix_crawl_input = json.load(f)
    
    headers = {
        "cookie": f'PHPSESSID={pivix_crawl_input["PHPSESSID"]}',
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.82",
        "referer": "https://accounts.pixiv.net"
        }

    for user_id in pivix_crawl_input["user_id"]:

        create_folder(f'{current_directory}\content\{user_id}')

        user_id_response = requests.request("GET", f"https://www.pixiv.net/ajax/user/{user_id}/profile/all", headers=headers).json()

        if user_id_response["error"] == True:
            print(user_id_response["message"])
            continue

        if pivix_crawl_input["illusts"] == True and len(user_id_response["body"]["illusts"]) != 0:
            artwork_crawl(user_id_response,headers,current_directory, user_id, "illusts")

        if pivix_crawl_input["manga"] == True and len(user_id_response["body"]["manga"]) != 0:
            artwork_crawl(user_id_response,headers,current_directory, user_id, "manga")

        if pivix_crawl_input["novels"] == True and len(user_id_response["body"]["novels"]) != 0:
            novel_crawl(user_id_response,headers,current_directory, user_id)

def artwork_crawl(user_id_response,headers, current_directory, user_id, artwork_type):

    print(f"crawling {user_id}'s {artwork_type}.")       
    for artwork_id in user_id_response["body"][artwork_type].keys():

        create_folder(f'{current_directory}\content\{user_id}\{artwork_type}')

        artwork_id_response = requests.request("GET", f'https://www.pixiv.net/ajax/illust/{artwork_id}/pages', headers=headers).json()
        artwork_urls = [artwork_urls["urls"]["original"] for artwork_urls in artwork_id_response["body"]]
        
        for pximg_urls in artwork_urls:
            create_folder(f'{current_directory}\content\{user_id}\{artwork_type}\{artwork_id}')
            pximg_urls_response = requests.request("GET", pximg_urls, headers=headers).content      
            with open(f'{current_directory}\content\{user_id}\{artwork_type}\{artwork_id}\{pximg_urls.split("/")[-1].split("_")[-1]}', 'wb') as f:
                f.write(pximg_urls_response)

def novel_crawl(user_id_response,headers, current_directory, user_id):

    print(f"crawling {user_id}'s novels.")             
    for novel_id in user_id_response["body"]["novels"].keys():

        create_folder(f'{current_directory}\content\{user_id}\\novels')
        novel_response = requests.request("GET", f"https://www.pixiv.net/novel/show.php?id={novel_id}", headers=headers)
        soup = BeautifulSoup(novel_response.text, 'html.parser')
        preload_data = json.loads(soup.find("meta",{"id":"meta-preload-data"})["content"])

        novel_title = re.sub(r'[^\w]', ' ', preload_data["novel"][novel_id]["title"]).rstrip()
        create_folder(f'{current_directory}\content\{user_id}\\novels\{novel_title}')
        novel_content = preload_data["novel"][novel_id]["content"]
        with open(f'{current_directory}\content\{user_id}\\novels\{novel_title}\{novel_id}.txt', 'w', encoding="utf-8") as f:
            f.write(novel_content)

        novel_coverurl = preload_data["novel"][novel_id]["coverUrl"]
        novel_coverurl_response = requests.request("GET", novel_coverurl, headers=headers).content
        with open(f'{current_directory}\content\{user_id}\\novels\{novel_title}\{novel_coverurl.split("/")[-1].split("_")[0]}.{novel_coverurl.split(".")[-1]}', 'wb') as f:
            f.write(novel_coverurl_response)

        novel_textembeddedimages = preload_data["novel"][novel_id]["textEmbeddedImages"]
        if novel_textembeddedimages != None:
            for textembeddedimages_urls in novel_textembeddedimages.values():
                novel_textembeddedimages_pximg_response = requests.request("GET", textembeddedimages_urls["urls"]["original"], headers=headers).content
                with open(f'{current_directory}\content\{user_id}\\novels\{novel_title}\{textembeddedimages_urls["urls"]["original"].split("/")[-1].split("_")[0]}.{textembeddedimages_urls["urls"]["original"].split(".")[-1]}', 'wb') as f:
                    f.write(novel_textembeddedimages_pximg_response)

def create_folder(path):
    if not os.path.isdir(path):
        os.mkdir(path)

if __name__ == '__main__':
    main()