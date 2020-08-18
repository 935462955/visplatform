from visplatform import app

@app.template_filter()
def transformText(s):
    s = s.replace('`','\`')
    s = s.replace('/', '\\/')
    s = s.replace('$', '\$')
    return s
@app.template_filter()
def transformJson(s):

    s = s.replace('\\', '\\\\')
    s = s.replace('`', '\`')
    s = s.replace('$', '\$')
    return s

@app.template_filter()
def str2arr(s,symbol):
    return s.split(symbol)