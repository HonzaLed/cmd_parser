from rich.console import Console
from rich.prompt import Prompt
from copy import copy
import sys
import os

class Parser:
    def __init__(self, commands, prompt="[bold yellow]> [/bold yellow]", rich_console=None):
        self.commands = commands
        self.prompt_text = prompt
        if rich_console==None:
            self.console = Console()

    def prompt(self):
        cmd = self.console.input(self.gen_prompt()) #, choices=[i["name"] for i in self.commands])
        self.handle(cmd)

    def gen_prompt(self):
        return self.prompt_text

    def handle(self, cmd):
        cmd = cmd.strip()
        cmd = cmd.split(" ")

        if cmd[0] == "help":
            self.handle_help(cmd[1:])
            return

        cmd_json = None
        for i in self.commands:
            if i["name"] == cmd[0]:
                cmd_json=copy(i)

        if cmd_json == None:
            self.console.print("[bold red]Unknown command [/bold red][white]" + repr(cmd[0]) + "[/white][bold red]![/bold red]")
            return

        try:
            if cmd_json != None and "function" in cmd_json.keys():
                fn = getattr(sys.modules["__main__"], cmd_json["function"])
            else:
                fn = getattr(self, "handle_"+cmd[0])
        except AttributeError:
            self.console.print("[bold red]Error! The command [/bold red][white]" + repr(cmd[0]) + "[/white][bold red] is propably not implemented![/bold red]")
            return

        args={}
        if "arguments" in cmd_json.keys():
            # number of all possible arguments
            arg_count = len(cmd_json["arguments"])
            # count all required arguments
            req_arg_count = 0
            for i in cmd_json["arguments"]:
                if "required" in i.keys() and i["required"]:
                    req_arg_count += 1
            # get args names
            arg_names = [i["name"] for i in cmd_json["arguments"]]

            # check if passed min. required args and max. possible args
            if req_arg_count > len(cmd[1:]) or len(cmd[1:]) > arg_count:
                self.console.print("[bold red]Error! The command [/bold red][white]" + repr(cmd[0]) + "[/white][bold red] requires " + str(req_arg_count) + " arguments, received " + str(len(cmd[1:])) + "![/bold red]")
                return

            # loop over all entered commands in cmd_json
            for i in cmd_json["arguments"][:len(cmd[1:])]:
                # get value of that passed command
                value = cmd[1+cmd_json["arguments"].index(i)]
                # if the command has specified type, try to parse it
                try:
                    if "type" in i.keys():
                        value = __builtins__[i["type"]](value)
                except Exception as err:
                    self.console.print("[bold red]Error while trying to parse the arguments! The argument [/bold red][white]"+i["name"]+"[/white][bold red] requires the type [/bold red][white]"+repr(i["type"])+"[/white][bold red], but your input [/bold red][white]"+repr(value)+"[/white][bold red] cannot be parsed!")
                    return
                # add the value to the args array, will be used to call the function
                args.update( {i["name"]: value} )

        #except Exception as err:
            #self.console.print("[bold red]Error while parsing command arguments![/bold red]\Error:", err)
            #return
        fn(**args)

    def handle_help(self, cmd):
        string = ""
        if cmd == []:
            self.console.print("The available commands are:\n")
        # get the screen size
        screen_size = os.get_terminal_size()[0]
        # loop through commands
        for i in self.commands:
            if not cmd == []:
                if i["name"] != str(cmd[0]):
                    continue
            # if the command has arguments defined, do sth
            if "arguments" in i.keys():
                args=[]
                for j in i["arguments"]:
                    # check if type is defined
                    if "type" in j.keys() and j["type"] != "str":
                        # check if the arg is required
                        if "required" in j.keys() and j["required"]:
                            # append to args list
                            args.append("{"+str(j["name"])+"(" +str(j["type"]+ ")}"))
                        else:
                            # append to args list
                            args.append("\["+str(j["name"])+"(" +str(j["type"]+ ")]"))
                    else:
                        # check if the arg is required
                        if "required" in j.keys() and j["required"]:
                            # append to args list
                            args.append("{"+str(j["name"])+"}")
                        else:
                            # append to args list
                            args.append("\["+str(j["name"])+"]")
            # create string about this command that will be printer out
            string = i["name"]
            # define l (length of the string) variable, will be usefull later
            l=0
            # if the command has args, add them to the string
            if "arguments" in i.keys():
                string += " " + " ".join(args)
                # also decrease the length of the string by the number of "\[" because we have to escape every single "[" because we are using the rich library that uses "[" for colors and other formating stuff
                l-=sum([i.count("\[") for i in args])

            l+=len(string)
            string += (screen_size//2 - l) * " "
            string += i["help"]
            self.console.print(string)
        if string == "":
            self.console.print("[bold red]Unknown command [/bold red][white]" + repr(cmd[0]) + "[/white][bold red]![/bold red]")
