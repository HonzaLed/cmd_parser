# cmd_parser
As the name suggests, this is a parser for command lines that you can use in you python projects.  

It supports parsing commands and their arguments, checking the type of these arguments, and then calling some function that you specify, passing the command arguments to the function.  
You specify the commands and their arguments in a dictionary that you pass to the `Parser` class, you then call the `Parser.parse` function and give it the command string.  
You can define you own prompt or even a function that generates the prompt, so you can have a different prompt every time (for example you could make a "submenu" system with it).  

For some examples, you can look into the `test.py` file.  
