import logging

from azure.identity import ManagedIdentityCredential
from azure.mgmt.cognitiveservices import CognitiveServicesManagementClient
from azure.mgmt.resource import ResourceManagementClient
import openai

from ..send_message.cache import Redis
from .prompt import Prompt, PromptIndex

# declare static variables
subscription_id  = '<azure subscription ID>'
resource_group_name = '<resource group name>'
openai_account_name = '<Azure OpenAI account name>'

# instantiate azure clients
credential = ManagedIdentityCredential()
resource_client = ResourceManagementClient(credential = credential, 
                                           subscription_id = subscription_id) 
cognitive_client = CognitiveServicesManagementClient(credential = credential, 
                                                     subscription_id = subscription_id)
cognitive_account = cognitive_client.accounts.get(resource_group_name = resource_group_name,
                                                  account_name = openai_account_name)
key = cognitive_client.accounts.list_keys(resource_group_name = resource_group_name,
                                          account_name = openai_account_name).key1
endpoint = cognitive_account.properties.endpoint

# configure openai client
openai.api_type = "azure"
openai.api_base = endpoint
openai.api_version = "2022-12-01"
openai.api_key = key

# instaciante redis client
redis = Redis()

def get_sql_code(text: str) -> str:
    '''Check if the text contains SQL code 
       if it does retun True and the SQL code
       else return False and the original text

       The SQL code is between ###SQL-CODE-START### and ###SQL-CODE-END###
       parameters:
       text: str - the text to check
       
       returns:
       bool - True if the text contains SQL code, False otherwise
       str - the SQL code if the text contains SQL code, the original text otherwise
       '''
    
    if "```" in text:
        start = text.find("```")
        end = text.find("```", start + 3)
        return text[start + 3: end - 1]
    else:
        return text
       
class Chat():
        '''
        Class to manage the chatbot
        It has methods to send messages to the prompt and get the response
        It automatically updates the prompt with the new messages
        
        parameters:
        prompt: Prompt - the prompt to use for the chatbot
        temperature: int - the temperature to use for the chatbot [optional]'''
        def __init__(self, prompt: Prompt, temperature: int = 0):
            self.model = prompt.model
            self.prompt = prompt
            self.temperature = temperature
            self.max_tokens = prompt.max_tokens
            self.last_response = None
        
        def send_message(self):
            self.last_response = openai.Completion.create(
                                                    engine=self.model,
                                                    prompt=self.prompt.messages,
                                                    temperature=self.temperature,
                                                    max_tokens=self.max_tokens)
            self.prompt.add_message(self.last_response['choices'][0]['text'], 
                                    role = 'assistant',
                                    end_token = False)
    
class FullProcessing():
    '''
    Class to process a question and return the answer
    It uses all other classes to peroform the processing
    (Prompt, Chat, RefTable)
    
    parameters:
    question: str - the question to process
    chat_model: str - the model to use for the chatbot
    reference_table: RefTable - the reference table to use for the chatbot
    max_tokens: int - the max tokens to use for the chatbot [optional]
    
    methods:
    send_message: send a message to the chatbot and return the response'''
    def __init__(self, 
                 question: str, 
                 sender: str,
                 chat_model: str, 
                 reference_table: PromptIndex,
                 max_tokens :int = 2048,
                 loop: bool = False):
        self.question = question
        self.sender = sender
        self.chat_model = chat_model
        self.reference_table = reference_table
        self.max_tokens = max_tokens
        self.loop = loop
        self.cache = None
        logging.info('FullProcess object created')
        self.post_init()
        
    def post_init(self):
        self.cache = redis.read_cache(self.sender)
        if not self.loop:
            self.context = self.reference_table.find_context(self.question)
        else:
            self.context = '<|im_start|>A consulta ao banco de dados foi feita, responda a pergunda do user com as informações retornadas.<|im_end|>'
        self._create_prompt()
        logging.info('FullProcess.prompt created')
        self._create_chat()
        logging.info('FullProcess.chat created')

    def _add_cached_messages(self):
        messages_list = self.cache.split('\n')
        messages_list = [item for item in messages_list if len(item) > 0]
        logging.info(f'messages list is {messages_list}')
        temp_text = ''
        temp_role = 'user'
        index = 0 
        for item in messages_list:
            if item == 'user' or item == 'assistant':
                if index > 0:
                    self.prompt.add_message(message = temp_text, role = temp_role)
                    temp_role = item
                    temp_text = ''
            else:
                temp_text = temp_text + item
            index = index + 1 
        self.prompt.add_message(message = temp_text, role = temp_role)
        logging.info('Cached messages added to prompt')
    
    def _create_prompt(self):
        self.prompt = Prompt(model = self.chat_model, max_tokens= self.max_tokens)
        self.prompt.add_message(message = 'O assistente segue as instruções do usuário.' , role = 'system')
        self.prompt.add_message(message = self.context, role = 'context')
        if self.cache:
            self._add_cached_messages()
        self.prompt.add_message(message = self.question, role = 'user')           
             
    def _create_chat(self):
        self.chat = Chat(self.prompt)
        
    def send_message(self):
        '''
        Send a message to the chatbot and return the response
        '''
        logging.info('FullProcess object sending message')
        self.prompt.add_message(message = '', role = 'assistant', end_token = False)
        self.chat.send_message()
        return self.prompt.get_last_response() 