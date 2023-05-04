'''
Code for interacting with GPT-3 in Python.
'''
import openai
import os

'''Initialize your API key registered from https://platform.openai.com/account/api-keys
Then, store your APIKEY locally (Only need to do once), and GPT will fetch the key from local environment
On Mac
% pip3 install openai
% export APIKEY="......."  # in bash
% python3 gpt.py

On Windows:
% pip install openai
% $env:APIKEY="....." # in powershell
% python gpt.py
'''
key = os.environ.get('APIKEY')

class GPT():
    ''' initialize GPT with apikey '''
    def __init__(self):
        ''' store the apikey in an instance variable '''
        self.apikey = key
        # Set up the OpenAI API client
        openai.api_key = key

        # Set up the model and prompt
        self.model_engine = "text-davinci-003"

    def getResponse(self,prompt):
        ''' Generate a GPT response '''
        completion = openai.Completion.create(
            engine=self.model_engine,
            prompt=prompt,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.2,
        )    
        response = completion.choices[0].text.strip()
        return response

if __name__=='__main__':
    g = GPT()
    print(g.getResponse("what does openai GPT stand for?"))
    

