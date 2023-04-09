import logging
import os

from openai.embeddings_utils import get_embedding, cosine_similarity 
import pandas
import tiktoken

def get_prompt_sources(path: str) -> dict:
    '''
    Get the list of files in the path and return a dictionary with 
    the file name as key and the file path as value

    parameters:
    path: str - the path to the folder containing the files

    returns:
    dict - a dictionary with the file name as key and the file path as value
    '''
    prompts_sources = {}
    files_list = [x for x in os.listdir(path) if x.endswith('.sql')]
    for file in files_list:
        name = file.split('.')[0]
        prompts_sources[name] = path + file

    return prompts_sources

class Prompt():
    ''' 
    Class to manage the prompts for the chatbot
    It contains the methods to write and read messages to the prompts
    It also auto flush old messages when max token is reached
    
    parameters:
    model: str - name of the GPT model
    max_tokens: int - maximum number of max tokens for the prompt
    '''
    def __init__(self, model = 'gpt-3.5-turbo-0301', max_tokens: int = 800):
        self.model = model
        self.messages = ''
        self.tokens_lenght = 0
        self.max_tokens = max_tokens
        self.start_token = '<|im_start|>'
        self.end_token = '<|im_end|>\n'
        self._pos_init()
        
    def _pos_init(self):
        try:
            self.encoding = tiktoken.encoding_for_model(self.model)
        except KeyError:
            self.encoding = tiktoken.get_encoding('cl100k_base')
       
    def _add_context(self, message: str):       
        self.messages = self.messages + message
    
    def add_message(self, message: str, role: str, end_token: bool = True):
        if role == 'context':
            self._add_context(message)
        else:
            new_message = self.start_token + role + '> ' + message
            if end_token:
                new_message = new_message + self.end_token
            self.messages = self.messages + new_message
        self.count_tokens_lenght()
        
    def count_tokens_lenght(self):
        '''
        Count the number of tokens in the prompt
        '''
        self.tokens_lenght = len(self.encoding.encode(self.messages))
    
    def get_last_response(self):
        '''
        Get the last response from the prompt
        
        returns:
        str - the last response from the prompt
        '''
        start_tag = self.start_token + 'assistant> '
        start = self.messages.rfind(start_tag)
        end = self.messages.find(self.end_token, start)
        return self.messages[start + len(start_tag): end - 9]
        
    def print_last_message(self):
        '''
        Print the last response from the prompt
        '''
        print(self.get_last_response())

class PromptIndex():
    '''
    Class to create a reference table with all prompts for the chatbot
    It reads prompts from files, create the DataFrame, generate embeddings
    It has a method to find the closest prompt to a given context
    
    parameters:
    embeddings_model: str - the name of the embeddings model to use
    prompts_sources: dict - a dictionary with the file name as key and the file path as value
    
    methods:
    find_closest_prompt: find the closest prompt to a given context'''
    def __init__(self, embeddings_model: str, prompts_sources: dict[str:str]):
        self.prompts_sources = prompts_sources
        self.embeddings_model = embeddings_model
        self._post_init()
     
    def _post_init(self):
        self._create_prompts_df()
        self._read_context()
        self._generate_embeddings()
        
    def _create_prompts_df(self):
        self.prompts_df = pandas.DataFrame()
        self.prompts_df['name'] = list(self.prompts_sources.keys())
        
    def _read_context(self):
        context = []
        for name in list(self.prompts_sources.keys()):
            with open(self.prompts_sources[name], 'rb') as file:
                context.append(file.read().decode(encoding='utf-8'))
        self.prompts_df['context'] = context
        
    def _generate_embeddings(self):
        self.prompts_df['embeddings'] = self.prompts_df['context'].apply(get_embedding, 
                                                                         engine = self.embeddings_model)
        logging.info(f'after add embeddings table is: {self.prompts_df}')

    def find_context(self, question):
        '''
        Find the closest prompt to a given question
        
        parameters:
        question: str - the question to find the closest prompt to'''
        embedding_question = get_embedding(question, engine = self.embeddings_model)
        self.prompts_df['similarity'] = self.prompts_df['embeddings'].apply(cosine_similarity, 
                                                                            b=embedding_question)
        self.prompts_df = self.prompts_df.sort_values('similarity', ascending=False)
        logging.info(f'Closest prompt found {self.prompts_df.head(1)["name"].values[0]}')
        self.prompt_name = self.prompts_df.head(1)['name'].values[0]
        return self.prompts_df.head(1)['context'].values[0]