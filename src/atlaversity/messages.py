from prompt_toolkit import print_formatted_text as print
from prompt_toolkit import  HTML

def blue(msg):
    print(HTML(f'<ansiblue>{msg}</ansiblue>'))

def green(msg, end = '\n'):
    print(HTML(f'<ansigreen>{msg}</ansigreen>'), end=end)

def magenta(msg, end = '\n'):
    print(HTML(f'<ansimagenta>{msg}</ansimagenta>'), end=end)

def cyan(msg, end = '\n'):
    print(HTML(f'<ansicyan>{msg}</ansicyan>'), end=end)

def red(msg, end = '\n'):
    print(HTML(f'<ansired>{msg}</ansired>'), end=end)

def yellow(msg, end = '\n'):
    print(HTML(f'<ansiyellow>{msg}</ansiyellow>'), end=end)

def gray(msg, end = '\n'):
    print(HTML(f'<ansigray>{msg}</ansigray>'), end=end)

def ok(msg):
    green(msg)

def warning(msg):
    yellow(msg)

def error(msg):
    red(msg)
    raise ValueError(msg)

