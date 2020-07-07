import requests

def get_joke():
    joke = requests.get('https://icanhazdadjoke.com/slack').json().get('attachments')[0].get('text')
    return joke

def get_quote():
    data = requests.get('http://api.quotable.io/random').json()
    quote = data.get('content')
    author = data.get('author')

    return f"""> {quote}
    > 
    > - {author}
    """