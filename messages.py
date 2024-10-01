from prompt_toolkit import print_formatted_text as print
from prompt_toolkit import  HTML

def ok(msg):
    print(HTML(f'<ansigreen>{msg}</ansigreen>'))

def warning(msg):
    print(HTML(f'<ansiyellow>{msg}</ansiyellow>'))

def error(msg):
    print(HTML(f'<ansired>{msg}</ansired>'))

def blue(msg):
    print(HTML(f'<ansiblue>{msg}</ansiblue>'))

def green(msg, end = '\n'):
    print(HTML(f'<ansigreen>{msg}</ansigreen>'), end=end)

