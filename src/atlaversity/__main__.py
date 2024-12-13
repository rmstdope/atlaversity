import sys
from atlaversity.editor.CommandLine import CommandLine
from atlaversity.utils.Config import Config

def main():
    cfg = Config('atlaversity.toml')
    command_line = CommandLine(cfg)
    command_line.run()
    sys.exit(0)

if __name__ == '__main__':
    main()
