'''
Code for interacting with GPT-3 in Python.
'''
import openai

class GPT():
    ''' initialize GPT with apikey '''
    def __init__(self):
        ''' store the apikey in an instance variable '''
        self.apikey="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"
        # Set up the OpenAI API client
        openai.api_key = "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" 

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

