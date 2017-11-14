import urllib.request
import requests, argparse, os, time, shutil
import pandas as pd
from bs4 import BeautifulSoup
#url = 'https://www.ettoday.net/news/20171113/1050978.htm'
def getContent(url):
    print(url)
    page = urllib.request.urlopen(url)
    token = 'your access token'
    try:
        print('https://graph.facebook.com/?id={}'.format(url))
        facebook_id = requests.get('https://graph.facebook.com/?id={}'.format(url)).json()['og_object']['id']
    except:
        print('https://graph.facebook.com/?id={}'.format(url))
        error_message = requests.get('https://graph.facebook.com/?id={}'.format(url)).json()['error']['message']
        print('error: ' + error_message)
        delete_path = os.getcwd()
        print(delete_path)
        os.chdir('..')
        shutil.rmtree(delete_path)
        return
    print(facebook_id)
    print('https://graph.facebook.com/v2.9/{}/comments?order=reverse_chronological&filter=stream&limit=400&access_token={}'.format(facebook_id, token));
    res = requests.get('https://graph.facebook.com/v2.9/{}/comments?order=reverse_chronological&filter=stream&limit=400&access_token={}'.format(facebook_id, token))
    soup = BeautifulSoup(page, 'html.parser')
    try:
        title_box = soup.find('h1', attrs={'class' : 'title'})
        title = title_box.text.strip()
    except:
        title_box = soup.find('h1', attrs={'class': 'title_article'})
        title = title_box.text.strip()
    contents = title
    contents += '\n'
    print(title)
    article_file =  open("Article.txt", "w", encoding='utf-8-sig')
    for content in soup.find('div', {'class' : 'story'}).find_all('p', {'class' : None}):
        if content.find('strong') is None:
            print(content.text.strip() + '\n', file=article_file)
    article_file.close()
    res = requests.get('https://graph.facebook.com/v2.9/{}/comments?order=reverse_chronological&filter=stream&limit=400&access_token={}'.format(facebook_id, token))
    cnt = 0
    for ele in res.json()['data']:
        cnt += 1
        message_file = open("Message" + cnt.__str__() + ".txt", "w", errors='replace')
        print(ele['message'] + '\n', file=message_file)
        print('no. ' + cnt.__str__() + ' message')
        print(ele['message'])
        message_file.close()
    if cnt == 0:
        print('no message in the article')
        delete_path = os.getcwd()
        print(delete_path)
        os.chdir('..')
        shutil.rmtree(delete_path)
    else:
        os.chdir('..')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("target",
                        help="Set the target fans page(at least one) you want to crawling. Ex: 'appledaily.tw' or 'appledaily.tw, ETtoday'")
    parser.add_argument("date", help="Set the date you want to crawl. Format: 'yyyy-mm-dd'")
    args = parser.parse_args()
    date = str(args.date)
    menu_url = 'https://www.ettoday.net/news/news-list-' + date + '-0.htm'
    menu_page = urllib.request.urlopen(menu_url)
    soup = BeautifulSoup(menu_page, 'html.parser')
    main_url = 'https://www.ettoday.net/'
    cnt = 1
    for content in soup.find('div', {'class' : 'part_list_2'}).find_all('a', href = True):
        url = main_url + content['href']
        print("Target page " + url + " is crawling")
        if cnt - 1 > 0 and not os.path.exists('Result' + (cnt-1).__str__() + '/'):
            cnt -= 1
        result_dir = 'Result' + cnt.__str__() + '/'
        if not os.path.exists(result_dir):
            os.makedirs(result_dir)
        os.chdir(result_dir)
        print(os.getcwd())
        #try:
        getContent(url)
        cnt += 1
            #break
        '''except:
            print('error: cannott get correct content')
            delete_path = os.getcwd()
            print(delete_path)
            os.chdir('..')
            shutil.rmtree(delete_path)
            pass'''

        time.sleep(2)

    #url = str(args.target)


