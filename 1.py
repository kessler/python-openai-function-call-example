import json
from openai import OpenAI

client = OpenAI(
    # Defaults to os.environ.get("OPENAI_API_KEY")
)

api = {
  'getPageText': lambda url: print('getting url:', url)
}

functions = [{
  'name': 'getPageText',
  'description': 'download a webpage\'s content and remove all the html, returning only the page text',
  'parameters': {
    'type': 'object',
    'properties': {
      'url': {
        'type': 'string',
        'description': 'the url to download the page from, e.g. https://www.openai.com or google.com'
      }
    }
  },
  'required': ['url']
}]

chat_completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "summarize https://unity.com"}],
    functions=functions
)

fn_call = chat_completion.choices[0].message.function_call

name = fn_call.name
args = json.loads(fn_call.arguments)

api[name](**args)
