from functools import wraps
from bs4 import BeautifulSoup
from requests import get
from flask import session, redirect


def strong_password(s):
    specials = [
        "~", "!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "_", "+", "[", "]", "{", "}", "?"
    ]
    special = 0
    number = 0
    alphabet = 0
    for i in s:
        if i in specials:
            special += 1
        if i.isnumeric():
            number += 1
        if i.isalpha():
            alphabet += 1

    if special >= 1 and number >= 1 and alphabet >= 1 and len(s) >= 6:
        return True
    else:
        return False


def login_required(f):
    """ Decorate routes to require login.
    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def news(w):

    # Eliminate keywords
    keys_vn = [

        'f0', 'dịch bệnh', 'covid-19', 'ubnd', 'vn-index', 'nhà đầu tư', 'trường sa', 'hoàng sa', 'cục thuế',
        'cầu thủ', 'thủ môn', 'tiền đạo', 'bóng đá', 'ca nhiễm', 'tiền vệ', 'đeo khẩu trang', 'tay trống', 'ngôi sao truyền hình',
        'christiano ronaldo', 'wayne rooney', 'diễn xuất', 'diễn viên', 'cú đúp', 'bán kết', 'chung kết', 'đội bóng',
        'khán giả', 'người hâm mộ', 'mùa giải', 'hoa hậu', 'luân lưu', 'play-off'

    ]


    """ Get articles from vnexpress page """
    # Get vnexpress page
    page_vnexpress = get("https://vnexpress.net/")
    soup_vnexpress = BeautifulSoup(page_vnexpress.content, 'html.parser')
    vnexpress_articles = soup_vnexpress.find_all('p', class_="description")
    vne_articles = [i.text.split('. ')[0].strip() for i in vnexpress_articles]
    vn_articles = difference(vne_articles, keys_vn)


    """ Get articles from zing page """
    # Get zing page
    page_zing = get("https://zingnews.vn/")
    soup_zing = BeautifulSoup(page_zing.content, 'html.parser')
    zing_articles_tab = soup_zing.find_all('p', class_='article-summary')
    zing_articles_raw = [i.text.split('. ')[0].strip() for i in zing_articles_tab]
    zing_articles = difference(zing_articles_raw, keys_vn)


    """ Get articles from aljajeera page """
    # Get aljajeera
    al_page = get("https://www.aljazeera.com/")

    # Paste page to parser
    soup_al = BeautifulSoup(al_page.content, 'html.parser')

    # Find all articles
    al_news_tab = soup_al.find_all('a', class_='fte-article__title-link u-clickable-card__link')

    # Split articles into parts in a list
    al_news = [i.text.split('. ')[0].strip() for i in al_news_tab]

    """ Get articles from reuster """
    # Get reuster page
    page_reu = get("https://www.reuters.com/")
    soup_reu = BeautifulSoup(page_reu.content, 'html.parser')
    reu_articles_tab = soup_reu.find_all('a', class_='text__text__1FZLe text__dark-grey__3Ml43 text__medium__1kbOh text__heading_5_and_half__3YluN heading__base__2T28j heading_5_half media-story-card__heading__eqhp9')
    reu_articles_raw = [i.text.split('. ')[0].strip() for i in reu_articles_tab]

    keys_reu = ['world', 'gallery', 'energy', 'video', 'europe', 'retail & consumer', 'environment', 'asia pacific',
        'china', 'business', 'technology', 'united states', 'sustainable business',
        'sign up to the sustainable switch newsletter, article with image', 'united kingdom'
    ]

    reu_articles = difference(reu_articles_raw, keys_reu)

    z = get_from_list(vn_articles, w) + get_from_list(zing_articles, w) + get_from_list(al_news, w) + get_from_list(reu_articles, w)

    return z

def difference(s, q):
    # s is a list of articles
    # q is a list of keywords

    # Add an empty list
    r = []

    # for every article in articles list
    for i in s:

        # if article doesn't have any of keyword in keyword list, add to r
        key_count = 0
        for j in q:
            if j.lower() in i.lower():
                key_count += 1

        if key_count == 0:
            r.append(i)
    return r


def get_from_list(s, p):
    # s is a list of articles
    # p is number of articles need to get
    # Define an empty list
    z = []
    count = 0
    for i in s:
        if count < p:
            z.append(i)
            count += 1
    return z