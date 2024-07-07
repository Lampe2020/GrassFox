import abc

##############
# Base nodes #
##############

class Node(abc.ABC):
    """
    Base node for all nodes in the AST.
    All methods of this class should be overridden in child classes, as the base node doesn't do anything.   .
    """
    def __init__(self, line:int, column:int)->None:
        """
        Initialize the node.
        """
        self.line:int = int(line)
        self.column:int = int(column)

class ExprNode(Node):
    """
    Base node for all expressions in the AST.
    """
    def __int__(self, line:int, column:int, items:list[any])->None:
        """
        Initialize the expression node.
        """
        super().__init__(line, column)
        this.items = list(items)

class LiteralNode(ExprNode):
    """
    Base node for all literal nodes in the AST.
    """
    def __int__(self, line:int, column:int, value:any)->None:
        """
        Initialize the literal node.
        """
        super().__init__(line, column)
        self.value:any = value

class NumberLiteral(LiteralNode):
    """
    Base node for all number nodes in the AST
    """
    def __int__(self, line:int, column:int, value:int|float)->None:
        """
        Initialize the literal node.
        """
        super().__init__(line, column, (
            value if type(value)==int else float(value) # This allows even strings like 'nan' to be recognized.
        ))

##################
# The real nodes #
##################

#TODO: Implement all names from arrowey.lark as visitor classes here

class IntLiteral(NumberLiteral):
    """
    Whole number
    """
    def __int__(self, line:int, column:int, value:int)->None:
        """
        Initialize the literal node.
        """
        super().__init__(line, column, int(value))

class FloatLiteral(NumberLiteral):
    """
    Non-whole number
    """
    def __int__(self, line:int, column:int, value:float)->None:
        """
        Initialize the literal node.
        """
        super().__init__(line, column, float(value))

class StringLiteral(LiteralNode):
    """
    String
    """
    def __init__(self, line:int, column:int, value:str)->None:
        """
        Initialize the string node.
        """
        super().__init__(line, column, str(value))

class FormatStringLiteral(StringLiteral):
    """
    Format strings ("template strings" in JavaScript, "f-strings" in Python)
    """
    def __init__(self, line:int, column:int, value:any)->None: #TODO: Find out what type this node gets to match it with the type annotation for `value`!
        """
        Initialize the format string.
        """
        super().__init__(line, column, value)

class Scope(ExprNode):
    """
    Group expressions together.
    """
    def __init__(self, line:int, column:int, exprs:list[ExprNode])->None:
        """
        Initialize the scope.
        """
        super().__init__(line, column)
        self.exprs:list[ExprNode] = exprs

class FuncDef(ExprNode):
    """
    Define a function.
    """
    def __init__(self,
                 line:int,
                 column:int,
                 rettype:str, #TODO: Keep an eye on this, this may be replaced with an actual type!
                 name:str,
                 body:Scope
             )->None:
        """
        Initialize the function definition node.
        """
        super().__init__(line, column)