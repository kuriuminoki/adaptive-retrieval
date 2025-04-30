"""
  Wikipediaの情報をAPIで取得する。
  リクエスト数を1秒あたり200件以下に制限するよう注意
"""

import requests

from logging import getLogger
logger = getLogger(__name__)


def get_page_history_counts(title, type):
    """
    Wikipediaの編集回数を取得する。
    title: page title as Wikipedia
    type:
        anonymous: Edits made by anonymous users. Limit: 10,000
        bot: Edits made by bots. Limit: 10,000
        editors: Users or bots that have edited a page. Limit: 25,000
        edits: Any change to page content. Limit: 30,000
        minor: Edits marked as minor. If the minor edit count exceeds 2,000, the API returns a 500 error. Limit: 1,000
        reverted: Edits that revert an earlier edit. Limit: 30,000
    """

    url = f'https://en.wikipedia.org/w/rest.php/v1/page/{title}/history/counts/{type}'

    headers = {
        'User-Agent': 'MediaWiki REST API docs examples/0.1 (https://www.mediawiki.org/wiki/API_talk:REST_API)'
    }
    params = {
    }

    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    # print(data)

    if not ("count" in data):
        logger.warn(data)
        return -1
    
    if data["limit"] is True:
        logger.warn(f'{title}: the data point exceeds the type\'s limit.')

    return data["count"]


def wikipedia_action_api():
    S = requests.Session()

    URL = "https://en.wikipedia.org/w/api.php"

    PARAMS = {
        "action": "query",
        "meta": "siteinfo",
        "formatversion": "2",
        "format": "json",
        "siprop": "statistics",
        "titles": "George_Rankin"
    }

    R = S.get(url=URL, params=PARAMS)
    DATA = R.json()

    print(DATA)


def main():
    get_page_history_counts("George_Rankin", "edits")


if __name__ == "__main__":
    main()
