import os

class DefaultConfig:
    """ Bot Configuration """
    PORT = 3978
    APP_ID = os.environ.get("MicrosoftAppId", "")
    APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "")
    
    '''Bing Search API 的基本設定'''
    # (必需修改) 此KEY為Azure Portal上Bing Image API的KEY
    BING_SEARCH_API_KEY = ''
    # (可修改) 使用Bing Vision API所打的endpoint，可修改後面query的內容
    BING_VISION_SEARCH_API_ENDPOINT = 'https://api.cognitive.microsoft.com/bing/v7.0/images/visualsearch?mkt=zh-tw&setLang=zh-tw'
    # (可修改) 使用Bing Image API所打的endpoint，可修改後面query的內容
    BING_IMAGE_SEARCH_API_ENDPOINT = "https://api.cognitive.microsoft.com/bing/v7.0/images/search"