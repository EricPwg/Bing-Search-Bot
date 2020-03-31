from botbuilder.core import ActivityHandler, TurnContext, MessageFactory
from botbuilder.schema import ChannelAccount, Attachment

from config import DefaultConfig

import json
import requests
import urllib.request
import os

class BingSearchBot(ActivityHandler):
    # 首次加入的問候的訊息
    async def on_members_added_activity(self, members_added: [ChannelAccount], turn_context: TurnContext):
        for member in members_added:
            if member.id != turn_context.activity.recipient.id:
                await turn_context.send_activity(
                    f"歡迎來到Bing API的機器人，傳圖片以圖搜尋，傳文字以文字搜尋 !")

    # 每一次對話都是由這裏來處理
    async def on_message_activity(self, turn_context: TurnContext):
        image_url_list = []
        host_page_url_list = []
        host_page_name_list = []

        if turn_context.activity.attachments:
            for attachment in turn_context.activity.attachments:
                attachment_info = await self._download_attachment_and_write(attachment)
            
            image_url_list, host_page_url_list, host_page_name_list = self.bing_vision_api(attachment_info['filename'])
            
            for i in range(len(host_page_url_list)):
                await turn_context.send_activity(MessageFactory.content_url(url= image_url_list[i], content_type='image/jpg', text=host_page_name_list[i]))
                await turn_context.send_activity(MessageFactory.text(text= host_page_url_list[i]))


        elif turn_context.activity.text : 
            image_url_list, host_page_url_list, host_page_name_list = self.bing_image_api(turn_context.activity.text)
            for i in range(len(host_page_url_list)):
                await turn_context.send_activity(MessageFactory.content_url(url= image_url_list[i], content_type='image/jpg', text=host_page_name_list[i]))
                await turn_context.send_activity(MessageFactory.text(text= host_page_url_list[i]))
    
    async def _download_attachment_and_write(self, attachment: Attachment) -> dict:
        """
        Retrieve the attachment via the attachment's contentUrl.
        :param attachment:
        :return: Dict: keys "filename", "local_path"
        """
        try:
            response = urllib.request.urlopen(attachment.content_url)
            headers = response.info()

            # If user uploads JSON file, this prevents it from being written as
            # "{"type":"Buffer","data":[123,13,10,32,32,34,108..."
            if headers["content-type"] == "application/json":
                data = bytes(json.load(response)["data"])
            else:
                data = response.read()

            local_filename = os.path.join(os.getcwd(), attachment.name)
            with open(local_filename, "wb") as out_file:
                out_file.write(data)

            return {"filename": attachment.name, "local_path": local_filename}
        except Exception as exception:
            print(exception)
            return {}
    
    def bing_vision_api(self, image) : 
        image_url = []
        host_page_url = []
        host_page_name = []

        headers = {'Ocp-Apim-Subscription-Key': DefaultConfig.BING_SEARCH_API_KEY}
        file = {'image' : ('MY-IMAGE', open(image, 'rb'))} # MY-IMAGE is the name of the image file
        
        try:
            response = requests.post(DefaultConfig.BING_VISION_SEARCH_API_ENDPOINT, headers=headers, files=file)
            response.raise_for_status()

            for i in range(3):
                image_url.append(response.json()['tags'][0]['actions'][2]['data']['value'][i]['contentUrl'])       # 若要更改回傳內容，可修改後面的索引
                host_page_url.append(response.json()['tags'][0]['actions'][2]['data']['value'][i]['hostPageUrl'])
                host_page_name.append(response.json()['tags'][0]['actions'][2]['data']['value'][i]['name'])
        except Exception as ex:
            raise ex
        
        return image_url, host_page_url, host_page_name
    
    def bing_image_api(self, query) : 
        image_url = []
        host_page_url = []
        host_page_name = []

        # Construct a request
        mkt = 'zh-tw'
        params = {'q': query, 'mkt': mkt}
        headers = {'Ocp-Apim-Subscription-Key': DefaultConfig.BING_SEARCH_API_KEY}
        
        try:
            response = requests.get(DefaultConfig.BING_IMAGE_SEARCH_API_ENDPOINT, headers=headers, params=params)
            response.raise_for_status()

            for i in range(3):
                image_url.append(response.json()['value'][i]['contentUrl'])       # 若要更改回傳內容，可修改後面的索引
                host_page_url.append(response.json()['value'][i]['hostPageUrl'])
                host_page_name.append(response.json()['value'][i]['name'])
        except Exception as ex:
            raise ex
        
        return image_url, host_page_url, host_page_name