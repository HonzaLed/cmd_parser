import cmd
import sys

def print_f(cmd):
    print(*cmd)

def debug(scope, name, random=0):
    print(scope, name, random)
    if scope == "global":
        print(globals()[name])
    elif scope == "local":
        print(locals()[name])
    elif scope == "module":
        print(getattr(sys.modules[name], random))
    else:
        print(getattr(globals()[scope], name))

commands = [
    {"name": "test", "help": "this is the test command"},
    {"name": "print", "help": "print all arguments", "function": "print_f"},
    {"name": "debug",
        "arguments": [
            {"name":"scope", "type":"str", "required": True},
            {"name": "name", "type":"str", "required": True},
            {"name": "random", "type": "list", "required": False}
        ],
        "help": "prints out the value of a variablee passed in first argument", "function":"debug"
    },
    {"name": "testb", "help": "this is the test commanda"},
]

class Parser(cmd.Parser):
    n=0
    def handle_test(self, cmd):
        print("This is test!")
    def gen_prompt(self):
        self.n +=1
        return str(self.n) + self.prompt_text

a = Parser(commands, prompt="[bold blue]> [/bold blue]")
while True:
    a.prompt()
