# Bing Search Bot
## Brief Introduction
This is a bot I created with Microsoft Bot Framework and Azure Bing Search API. Currently, the bot is able to do search by text after I deployed to App Service and then connected it with Facebook Messenger. Please refer to the [link](http://m.me/106050851050687) to test this bot on Messenger.
## To Reproduce
I will post the code with both ways of search, search by text and search by image. This code is only able to run both locally, with Bot Framework Emulator v4, and testing on App Service. 
### Prerequisites
> An Azure Account 

>Install Anaconda or [Miniconda (Python 3.7)](https://docs.conda.io/en/latest/miniconda.html "Miniconda下載頁面")

> Install [Bot Framework Emulator v4](https://github.com/Microsoft/BotFramework-Emulator/releases/tag/v4.7.0)

> Intsall Azure Command-Line Interface (CLI)
>> For [Windows User](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli-windows?view=azure-cli-latest "Windows的下載教學")
> 
>> For [Mac User](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli-macos?view=azure-cli-latest "Mac的下載教學")

> Install [Visual Studio Code(VS Code)](https://code.visualstudio.com/download "VScode下載頁面")
>> Install **Python extension** of VS Code
>
>> Install **Azure App Service Extension** of VS code
### Setup Azure Bing Search Service
1. Go to [Azure Portal](https://portal.azure.com/#home)
2. Search and create `Bing Search ` with F1 pricing tier
3. Copy `Key1` to the clipboard
    <p align = "center">
    <img src="./images/copy key1.jpg" width="50%">
    </p>
### Test the Bot Locally
4. Open `config.py`
5. Paste the `key1`
    <p align = "center">
    <img src="./images/paste key1.jpg" width="50%">
    </p>
6.  Run the following command in terminal
    ```powershell
    python app.py
    ```
7.  Open Bot Framework Emulator v4
8.  Key in the following url and Click **Connect**
    > `http://localhost:3978/api/messages`
    <p align = "center">
    <img src="./images/key in the URL.jpg" width="40%">
    </p>
### Deploy a bot to Azure
9.  Run the command in Azure CLI
    > Please make sure you are in the right directory and download `template-with-preexisting-rg.json`

    * `az login`
    * ```powershell
        az ad app create --display-name "displayName" --password "AtLeastSixteenCharacters_0" --available-to-other-tenants
        ```
    * ```powershell
        az group deployment create --resource-group "<name-of-resource-group>" --template-file "template-with-preexisting-rg.json" --parameters appId="<app-id-from-previous-step>" appSecret="<password-from-previous-step>" botId="<id or bot-app-service-name>" newWebAppName="<bot-app-service-name>" newAppServicePlanName="<name-of-app-service-plan>" appServicePlanLocation="<region-location-name>"
        ```
10. Open Visual Studio Code
11. Deploy the bot to the App Service you just created
    <p align = "center">
    <img src="./images/deploy the bot.jpg" width="40%">
    </p>
### Test the Bot on App Service
12. After the deployment completed, go to [Azure Portal](https://portal.azure.com/#home) and search the `Bot Services`
13. Click `Test in Web Chat`
    <p align = "center">
    <img src="./images/test in web chat.jpg" width="70%">
    </p>


## Limitation
Since I haven't used Azure Cosmos DB or other database yet, I cannot locate the file path of an user's uploaded-image after I connect the bot with Facebook Messenger or LINE. Azure Bing Search API is only triggered by a real image file not by image URL or something else.
