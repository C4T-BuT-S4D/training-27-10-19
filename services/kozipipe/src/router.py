from System.Text.RegularExpressions import Regex, RegexOptions
from views import not_found

class Router:
    def __init__(self, strict_slashes=True):
        self.routes = list()
        self.strict_slashes = strict_slashes

    def add_route(self, url, view, method):
        if self.strict_slashes and (len(url) == 0 or url[-1] != '/'):
            url += '/'

        url = '^%s$' % url

        r = Regex(url, RegexOptions.Compiled)

        self.routes.append((r, view, method))

    def get_view(self, url, method):
        for r in self.routes:
            if r[0].IsMatch(url) and r[2] == method:
                view = r[1]
                params = []
                match = r[0].Match(url)
                groups = match.Groups
                for i in range(1, groups.Count):
                    params.append(groups[i].Value)
                return view, params
        return not_found, []