#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
A LARK-based parser for L2m (Lampe2020 Markup)
"""

import lark

parser:lark.Lark = lark.Lark("""%import common.WS -> _WS
%ignore _WS // Wherever unecessary, just ignore it.
%import common.ESCAPED_STRING -> STRING
elmnt_list:         ( STRING | element | block )*
element:            "#" /[a-z0-9_][a-z0-9\-\_\.\: ]*/i taglist "{" elmnt_list "}"
tag:                [ /[a-z0-9_]+/ [ "=" ( STRING | block | /[^\]]+/s ) ] ]
taglist:            ( "[" tag "]" )+
block:              /<<<(.*?)>>>/s  // Waiting on https://github.com/lark-parser/lark/issues/1425 for forgiving syntax
""", start='elmnt_list')

class L2mTransformer(lark.Transformer_NonRecursive):
    """Transforms the lark parse tree to an AST that's usable for us"""

    ##############################################
    # Define methods for each terminal and token #
    ##############################################

    def dummytoken(self, item):
        """Handle dummytoken"""
        return str(item)    # For example.

    def STRING(self, item):
        """Handle STRING"""
        return eval(item)

    def elmnt_list(self, items):
        """Handle elmnt_list"""
        return items

    def element(self, items):
        """Handle element"""
        return {
            'name': items[0].value if isinstance(items[0], lark.Token) else str(items[0]),
            'tags': {   # Remove tag None and set bool tags to empty string
                tag:(items[1][tag] if items[1][tag]!=None else '') for tag in items[1]
                if tag!=None
            },
            'children': items[2]
        }

    def taglist(self, items):
        """Handle taglist"""
        return dict(items)

    def tag(self, items):
        """Handle tag"""
        return (
            items[0].value if isinstance(items[0], lark.Token) else items[0] if items[0] else None,
            items[1].value if isinstance(items[1], lark.Token) else items[1] if items[1] else None
        )

    def block(self, item):
        """Handle block"""
        return lark.Discard if item[0].value.startswith('<<<!') else item[0].value[3:-3]

def parse_l2m(text:str, max_forgiving_retries:int=0) -> any:
    """Parse the given syntax."""
    if not max_forgiving_retries:
        return L2mTransformer().transform(parser.parse(text))
    else:
        for i in range(max_forgiving_retries):
            try:
                return parse_l2m(text=text, max_forgiving_retries=0)
            except lark.exceptions.LarkError as err:
                print(text[:err.pos_in_stream]) #TODO: This will fail as soon as it hits something invalid. Determine
                                                # that invalid thing here and replace it in the source code with a
                                                # string or block (depending on what's appropriate) and go to next
                                                # iteration to try again until max retries reached
                return [text]