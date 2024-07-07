def iterative_parse(code:str)->any:
    """
    Parse the given line of code and return its return value

    Follow the parse tree:
    Stack: uppermost node has highest list index
    create a stack, when encountering a node push it onto there and call the stack visit function.
    If stack visitor tells us the uppermost node can have children, go into the uppermost node and put its first child onto the stack,
    if the stack visitor returns nothing, pop the uppermost node off the stack and call its visitor method, then push its next sibling onto the stack if it has such.
    Rinse and repeat.

    ↑ Acceptable?

    To visit node: add to to-parse list with its parent node ID as an attribute to tell the visitor what element to tell that its child has been visited.
    If the node that gets updated then has no unvisited TERMINAL nodes left it is added to a runnable list (?) and if it has non-TERMINAL child nodes left it waits until they are marked runnable.

    When we encounter a node we give it an ID and store it in the flat node buffer. We then iterate over that buffer and extract all child nodes and give them IDs as well as a property telling which node is their parent and adding the child's ID to a children property on the parent.
    When all nodes have no nested children and every node except the `start` node (ID 0) has a parent ID associated with it we iterate over the buffer again and resolve all TERMINALs and store them into their parents.
    When all TERMINALs are resolved we iterate over the buffer from the node 0 (`start`) and through its children etc. to implement the behaviour.
    """

    stack:list[lark.any] = []

    #TODO: Implement stack handling!