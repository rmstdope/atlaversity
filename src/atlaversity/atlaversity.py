from CommandLine import CommandLine
import Config

Config.read_config('atlaversity.toml')
command_line = CommandLine()
command_line.run()
