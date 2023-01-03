import re

# return a query url from base url + parameter dictionary object
def compile_url(base: str, url_params: dict = None) -> str:
    if not url_params:
        return base
    qs = '?'
    for par, val in url_params.items():
        qs += '{}={}&'.format(par, val)
        
    url = base + qs[:-1]
    return url


# return base url + parameter dictionary object from a query url
def decompile_url(url: str) -> tuple[str, dict]:
    res = re.search('(?:\?)(.*)$', url)

    base_url = url.replace(res.group(0), '')
    url_params = dict()

    params = res.group(1).split('&')
    for par in params:
        kv = par.split('=')
        url_params[kv[0]] = kv[1]

    return base_url, url_params
