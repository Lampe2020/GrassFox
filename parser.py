import tatsu
ebnf = """
Program                     = zero_to_infinite_space { expression_separator } [ Expression | Scope ] { expression_separator { expression_separator } [ Expression | Scope ] } zero_to_infinite_space ; (* Note: the script itself has to end in an `end: ` statement with one argument which can be <> <0> <1> or any integer Number. If it doesn't it will run into the next wall and crash that way. *)
Scope                       = "[" Program "]" ; (* enclosing a set of instructions in squared braces sets it into an own Scope *)
Error_catching_scope        = "@" Scope "_" Scope [ "_" Scope ] (* Any variables defined inside the first or second scope will be available in all subsequent scopes inside the Error_catching_scope, except <err>, which is always defined in the second and third scope and contains either the error that occurred in the first scope or <>, overriding the <err> variable if defined in the first or second scope. *) ;
Escape_sequence             = "\\" ( '"' | "'" | "\\" | expression_separator ) ;
unicode_character           = ( "\\x" hex_digit hex_digit ) | ( "\\u" hex_digit hex_digit hex_digit hex_digit ) ;
Expression                  = ( String | Regex | Number | Arithmetic_expression | arraylike_access | Array | Object | Object_property_reference | Inline_if | Inversion | Logic_operation | Assignment | Comparison | Function_definition | Function_call | Variable_reference | Scope | Error_catching_scope | ( "(" zero_to_infinite_space [ Expression ] zero_to_infinite_space ")" ) ) ; (* Can be nested. *)
Assignment                  = [ "(" type_assignment ")" ] ( Variable_reference | Object_property_reference ) equal_sign Expression ;
type_assignment             = zero_to_infinite_space Identifier { ";;" Identifier } [ "{" type_assignment [ ":" type_assignment ] "}" ] { zero_to_infinite_space "," zero_to_infinite_space Identifier [ "{" type_assignment [ ":" type_assignment ] "}" ] } zero_to_infinite_space ;
Function_call               = ( Identifier | Expression ) ":" { zero_to_infinite_space [ Flagless_variable_reference equal_sign ] Expression } ;
Function_definition         = Variable_reference { at_least_one_space ( Flagless_variable_reference [ equal_sign Expression ] ) } at_least_one_space Scope ;
expression_separator        = ( zero_to_infinite_space "←" zero_to_infinite_space ) | ( zero_to_infinite_space "↑" zero_to_infinite_space ) | ( zero_to_infinite_space "↓" zero_to_infinite_space ) | ( zero_to_infinite_space "→" zero_to_infinite_space ) ;
Variable_reference          = [ "g" ] [ "c" | "i" | "d" ] Flagless_variable_reference ;
Object_property_reference   = Expression ";;" ( Flagless_variable_reference | Function_call ) ;
Flagless_variable_reference = "<" [ ( "0" | "1" | Identifier ) ] ">" ;
Identifier                  = ( letter | "_" ) { ( letter | digit | "_" ) } ;
String                      = ( '"' { #'[^"]' } '"' ) | ( "'" { #"[^']" } "'" ) ; (* To print out the character used to create the string, use the escape sequence `\ssqu;` for single quote and `\sdqu;` for a double quote. Arrows (that are also separators) in strings can be produced with `\saru;` (↑), `\sard;` (↓), `\sarl;` (←) and `\sarr;` (→). To literally write such an escape sequence, just prefix it with an even amount of backslashes. Escape sequences such as `\n` for newline (UNIX style) and `\r` for carriage return are also valid. `\s[…];` stands for "special character" and is the only escape sequence that has to be terminated with a semicolon. *)
Regex                       = "/" { #"[^\\]" } "/" { "g" | "i" | "m" | "s" | "u" | "y" } ; (* Flags: global, case insensitive, multiline, dotall, unicode, sticky. To match for a slash, use `\ssl;`. *)
Object                      = "{" { ( String | Variable_reference ) equal_sign Expression "," zero_to_infinite_space } "}" ; (* Maybe fix it up to not require a comma after each property *)
Array                       = [ "c" ] "a" "{" { Expression "," zero_to_infinite_space } "}" ;
arraylike_access            = Expression "{" ( Integer_number | Variable_reference ) [ "_" ( Integer_number | Variable_reference ) [ "_" ( Integer_number | Variable_reference ) ] ] "}" ; (* indices are built like this (see square braces as "make optional"): `{startindex[_endindex[_steplength]]}` *)
Inline_if                   = zero_to_infinite_space ( ( "(" zero_to_infinite_space [ Expression ] zero_to_infinite_space ")" ) | Expression ) zero_to_infinite_space "?" zero_to_infinite_space Expression zero_to_infinite_space "*" zero_to_infinite_space Expression zero_to_infinite_space ;
Number                      = Integer_number | Float_number ;
letter                      = lowercase_letter | uppercase_letter ;
lowercase_letter            = "a" | "b" | "c" | "d" | "e" | "f" | "g"
                              | "h" | "i" | "j" | "k" | "l" | "m" | "n"
                              | "o" | "p" | "q" | "r" | "s" | "t" | "u"
                              | "v" | "w" | "x" | "y" | "z" ;
uppercase_letter            = "A" | "B" | "C" | "D" | "E" | "F" | "G"
                              | "H" | "I" | "J" | "K" | "L" | "M" | "N"
                              | "O" | "P" | "Q" | "R" | "S" | "T" | "U"
                              | "V" | "W" | "X" | "Y" | "Z" ;
Comparison                  = Expression zero_to_infinite_space comparison_operator zero_to_infinite_space Expression
comparison_operator         = ( "L" | "l" | "e" | "g" | "G" | "n" | "E" ) equal_sign ; (* less than, less than or equal, equal, greater than or equal, greater than, not equal, self-identical (two references to the same Object) *)
hex_digit                   = digit | "a" | "b" | "c" | "d" | "e" | "f" ;
digit                       = "0" | nonzero_digit ;
Integer_number              = [ Negation ] ( "0" | ( nonzero_digit { positive_integer } ) ) ;
Hex_integer_number          = "0x" hex_digit { hex_digit } ;
Bin_integer_number          = "0b" ( "1" | "0" ) { "1" | "0" } ;
Float_number                = ( Integer_number "." positive_integer ) | "NaN" ;
nonzero_digit               = "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9" ;
at_least_one_space          = " " zero_to_infinite_space ;
zero_to_infinite_space      = { " " } ;
Negation                    = "-" ;
equal_sign                  = "=" ;
power_operator              = "^" ;
dot_operator                = "•" | ":" | "%" ; (* times, divided by, modulo *)
dash_operator               = "+" | Negation ; (* plus, minus *)
arithmatic_operator         = dot_operator | dash_operator ;
positive_integer            = "0" | ( nonzero_digit { digit } ) ; (* zero or any whole Number not starting with zero *)
Logic_operation             = ( Expression zero_to_infinite_space logic_operator zero_to_infinite_space Expression ) ;
Inversion                   = ( "n" ) "^" zero_to_infinite_space Expression ; (* Technically also a logic operation, I just count it as an own thing. *)
logic_operator              = ( "a" | "o" | "x" | "l" | "r" ) "^" ; (* and, or, xor, lshift, rshift *)
Arithmetic_expression       = powerarithmetic_expression | dotarithmetic_expression | dasharithmetic_expression ;
powerarithmetic_expression  = Expression power_operator Expression ;
dotarithmetic_expression    = Expression dot_operator Expression ;
dasharithmetic_expression   = Expression dash_operator Expression ;
"""
model = tatsu.compile(ebnf, 'arrowey')
print(model.parse("""<do_smth> <arg> [out: a{"Hello World", 3•5:3, /.*/gu, <arg>,}] → end: (do_smth: {<XD>=5,}){1} → "x"?3•3*NaN"""))