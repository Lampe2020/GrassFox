# l2m
*Lampe2020 Markup*

An example:
```l2m
<<<! A page in a similar structure to a typical simple HTML document. >>>
#Page[lang="en"][site="Lampe2020.de"] {
    #Head[] {
        #Meta[name="charset"] {"utf-8"}
        #Title[] {"Some test page"}
        #PageIcon[url="./favicon.ico"] {}
        #StyleSheet[] {
            <<<
                header {
                    color: lightblue;
                }
            >>>
        }
        #Script[] {
            <<<
                <console>;;log: 'Page loaded!'→
                (<dom>;;get_element_by_id: 'test');;<inner_text> = 'Arrowey is working on this page!'
            >>>
        }
    }
    #Body[] {
        #Header[] {"Hello World!"}
        "Lorem ipsum dolor sit amet."
        #Button[onclick="alert:'Consectetur adipiscing elit.'"] {
            "Click me!"
            #Noscript[] {
                " (doesn't work without arrowey)"
            }
        }
        #Text[id="Test] {}
    }
}
```