#!/home/christian/arrowey/parser.py
<name>=in:"Enter your name: "↓
↓                            ←
→<hello_var>=f"Hello World,\nhello {<name>}"↓
↓                                           ←
→out:<hello_var>;end:<>
←↓↑→

<var>=in:"Irgendwas: "→if:(<var>=="Ups!")→{out:"Tja..."→end:<>}→{end:<var>}