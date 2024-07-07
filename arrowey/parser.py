#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Implement compiler using https://github.com/numba/llvmlite later on?
import lark, sys, os, nodes
arr_version = '0.1.1-pre-alpha+py3.10-plus'
NaN:float = float('NaN')
Infinity:float = float('Infinity')
with open((os.path.sep if os.path.sep=='/' else '')+os.path.join(*(__file__.split(os.path.sep)[:-1]), 'arrowey.lark'),'r') as larkfile:
    parser = lark.Lark(larkfile.read())

def argument(argument_to_search_for):
    if not argument_to_search_for in sys.argv:
        for arg in sys.argv:
            if arg[0:len(argument_to_search_for)+1] == argument_to_search_for+":":
                return arg.split(":", 1)[1]
        return False
    else:
        return True

def logmsg(mood:int=0,msg:str|tuple[str,...]|list[str]|set[str]='')->None:
    """
    Print one or more log message(s) with associated status.
    """
    if type(msg)==str:
        msg = (msg,)
    elif type(msg) not in (tuple,list,set):
        logmsg(-1, (f'logmsg(): message list has wrong type: {repr(type(msg).__name__)}',))
        msg = (repr(msg),)
    match mood:
        # msym: Mood SYMbol
        case -3:
            msym:str = '!' # fatal error
        case -2:
            msym:str = '-' # error
        case -1:
            msym:str = 'w' # warning
        case 0:
            msym:str = 'i' # info
        case 1:
            msym:str = '+' # success
        case _:
            msym:str = '?' # unknown
    for message in msg:
        print(f'[{msym}] {message}')

def codegrid(code:str) -> tuple[str, ...]:
    """
    Returns the given code as a list of strings of equal length, one string=one line
    """
    rawcodegrid:tuple[str, ...] = code.split('\n')
    if rawcodegrid[0].startswith('#!'):
        rawcodegrid = rawcodegrid[1:] # Remove shebang line
    if rawcodegrid[0].startswith('# -*- ') and rawcodegrid[0].endswith('-*-'):
        rawcodegrid = rawcodegrid[1:] # Remove encoding line
    # Measure for the longest line
    longest:int = 0
    for line in rawcodegrid:
        if len(line) > longest:
            longest = len(line)
    return tuple(line.ljust(longest) for line in rawcodegrid) # Return the code grid for access like `grid[row][col]`

def linearize(code:tuple[str, ...]) -> str:
    """
    Kind-of a preparser,
    converts a code grid into parseable code
    """
    playhead_pos:tuple[int,int] = (0,0)
    codeline:str = ''
    lastdir:str = '→'
    ellipsis:type = type(...)
    def move(pos:tuple[int,int], direction:str|ellipsis=...):
        directions = {'←':(0,-1), '↓':(1,0), '↑':(-1,0), '→':(0,1)} # Relative positions
        if direction in directions.keys():
            return (
                pos[0] + directions[direction][0],
                pos[1] + directions[direction][1]
            )
        else:
            logmsg(-1, f'arrowey.linearize.<move>(): called at position {repr(pos)} with invalid direction {repr(direction)}!')
            return pos
    while True: # Gets stopped by `return` statement
        try:
            codeline += code[playhead_pos[0]][playhead_pos[1]]
            move(playhead_pos, (
                codeline[-1] if (code[playhead_pos[0]][playhead_pos[1]] in ('←', '↓', '↑', '→'))
                else lastdir
            ))
        except IndexError:
            return codeline # We his a border, meaning we must have hit the end.

class ArroweyTransformer(lark.Transformer_NonRecursive):    # TODO: Maybe replace this with https://lark-parser.readthedocs.io/en/latest/visitors.html#interpreter?
    """
    Our Arrowey parsetree→AST transformer
    """
    def __init__(self):
        """
        Initialize the AST generator
        """
        super().__init__()
    ##############################################
    # Define the methods used to visit each node #
    ##############################################

    def start(self, item:lark.Token) -> nodes.Scope:
        """
        Visit the start node
        """
        #TODO: Implement this!
        return nodes.Scope(item.line, item.column, item.value) #TODO: Find out if item.value is the way to go here!

    #TODO: Implement visiting method for each non-questionmarked node name from arrowey.lark!
    # https://medium.com/@mbednarski/creating-a-parser-for-a-programming-language-xdlang-part-3-94997860087e#d67b

    def scope(self, items:list[any]) -> nodes.Node:
        """
        Visit the instruction node
        """
        return nodes.ExprNode(item.line, item.column, )

def compile(code:str)->any:
    """
    Parse the code with the selected parsing function, defaulting to recursive.
    """
    parsetree = parser.parse(code)
    #TODO: Implement parser

if __name__ == '__main__':
    def run_from_parsetree(parsetree:lark.Tree[lark.Token])->any:
        """
        Run the given code by compiling it and running the result.
        """
        #TODO: Implement this!

    # Do the interactive shells with the help of `readline` module? https://docs.python.org/3.10/library/readline.html#module-readline
    if argument('--help') or argument('-h'):
        logmsg(0, f'''arrowey v{arr_version}
            
            Usage:
            <no args>            
            --help|-h           Display this help and exit.
            --parseshell|-p     Open an interactive shell to show code parse trees. 
                                Exit with "end:0" or by pressing [Ctrl]+[D]
            --script|-s         Linearize the code like a script (line by line) instead of following the arrows.
            '''.replace('           ', '')) # Remove unecessary padding.
        sys.exit(0)
    elif ((not (argument('--parseshell') or argument('-p'))) and len(sys.argv)==2) or len(sys.argv)==1:
        file_is_script:bool = bool(argument('--script') or argument('-s'))
        code:str = '' #TODO: get the code either from STDIN or from specified file
        if not file_is_script:
            compile(linearize(codegrid(code)))
    else:
        logmsg(0, (
            f'arrowey v{arr_version}',
            'Type "end:0" (without the double quotes) or press [Ctrl]+[D] to exit.'
        ))
        codebuf:str = ''
        nl:str='\n'
        ending_parse_trees:tuple[lark.Tree[lark.Token], ...] = tuple(parser.parse(endcode) for endcode in (
            'end: 0',
            '~ret',
            '~end'
        ))
        while True:
            try:
                inp:str = input(f'arrowey {"..." if codebuf else ">>>"} ')
            except (EOFError, KeyboardInterrupt):
                inp:str = 'end:0'
            except Exception as err:
                from traceback import format_exception
                logmsg(-3, f'Error while reading stdin!\n{nl.join(format_exception(err))}')
                inp:str = 'end:0'
            if inp or codebuf:
                try:
                    parsetree:lark.Tree[lark.Token] = parser.parse(codebuf or inp)
                    if parsetree in ending_parse_trees:
                        logmsg(0, 'arrowey stopped')
                        sys.exit(0)
                except lark.UnexpectedEOF as err:
                    codebuf = '\n'.join((codebuf, inp))
                    continue
                except Exception as err:
                    AST = None
                    codebuf = ''
                    logmsg(-2, f'Parser error!\n→ {type(err).__name__}: {err}')
                    continue
                if any((argument(arg) for arg in ('-p','--parseshell'))):
                    logmsg(1, f'Parse tree successfully generated:\n{parsetree.pretty()}')
                else:
                    logmsg(1, f'Result:\n{run_from_parsetree(parsetree)}')
                codebuf = ''

