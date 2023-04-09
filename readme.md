# MicroFarmer Journal Bot

This is app to record your daily activities of growing microgreens.
The app has no graphical interface and all interation is via chat.
This is a proof of concept not a production version. A lot of improvements are required.

## Requirements
 - Azure Subscription
 - Azure Resource Group
 - Azure OpenAI (deployment dos modelos gpt-35-turbo e text-embedding-ada-002)
 - Azure Function App (Python runtime on version 3.10)
 - Azure SQL DB
 - Azure Event Hubs (3 hubs: chat-ready, execute, send-mesage)
 - Azure Cache for Redis
 - Whatsapp Business API Token
 - Telegram Bot API Token

## Azure Function App configurations
- CONN_STRING: Event Hubs connection string
- REDIS_HOSTNAME: Hostname to Azure Redis Service
- REDIS_PASSWORD: Password to Azure Redis Service
- SQL_CONNECTION_STRING: Azure SQL Database connection string
- TELEGRAM_TOKEN: Telegram Bot API Token
- WHATSAPP_TOKEN: Whatsapp Business API Token

## Azure Function App Identity
- System assigned managed identity most be enable
- Function app must have contributor role on the subscription/resource group level
 This is a PoC, on production this should be hardened. The only reason to require contributor role is to retrieve Azure OpenAI Account key, it can be workarounded by add key to Function App configurations, but some code need to be refactored. If Azure OpenAI account is on the same resource group the contributor role should be granted on resource group level, otherwise on the subscription level.

 ## High Level Flow
 1. Receiver functions<br>
 1.1. Message arrive in the receivers functions (whatsapp in the receive function and telegram in the telegramreceive function). You need to configure this functions in the Whatsapp/Telegram as webhockers<br>
 1.2. The sender must be in a whitelist otherwise messages are ignored<br>
 1.3. Message is treated (flatten and some information is added) and send to chat-ready queue<br>
 2. Chat_call function<br>
 2.1. Message arrive in chat_call function<br>
 2.2. Prompt is created and populated with most similar prompt from prompts options<br>
 2.3. Cached messages are added to prompt<br>
 2.4. Prompt is send to ChatGPT API (gpt-35-turbo). Reponse is added to message<br>
 2.4. If response is an action (SQL Code) it is send to execute queue, if response is a text it is send to send_message queue and to cache (Redis)<br>
 3. Execute function<br>
 3.1. Message arrives at execute function<br>
 3.2. SQL Code is checked, if blocked keywords are present message is ignored<br>
 3.3. SQL Code run<br>
 3.4. If code was for insert date (no output data) the message is send to cache and response to send_message queue; if code was a query the output data is send to chat-ready queue to be processed again<br>
 4. Send_message function<br>
 4.1. Message arrive at send_message function<br>
 4.2. Message is send to correct channel (Telegram or Whatsapp)<br>

 ## Troubleshoot
- Open Azure Functions real-time logs: there are a lot of logging on the functions and you can easily follow message flow to understand where it is breaking (you may need 4 or 5 tabs to see logs of each step)
