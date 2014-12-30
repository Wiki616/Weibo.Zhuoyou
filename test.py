import HTMLParser

def decodeHtml(input):
    h = HTMLParser.HTMLParser()
    s = h.unescape(input)
    return s

print decodeHtml('&lt;a href=&#39;/homepage?uid=Wiki_ki&#39;&gt;@Wiki_ki&lt;/a&gt;')
