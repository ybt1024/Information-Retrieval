'''
Code for interacting with GPT-3 in Python.
'''
import openai

'''Initialize your API key registered from https://platform.openai.com/account/api-keys'''
key = "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"

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
            temperature=0.8,
        )    
        response = completion.choices[0].text
        return response

if __name__=='__main__':
    g = GPT()
    print(g.getResponse("what does openai GPT stand for?"))

