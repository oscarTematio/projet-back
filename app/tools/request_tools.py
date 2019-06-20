
class Link:

    """
    Materialization of a link added to a HATOAS resource
    """
    def __init__(self, rel, href):
        self.rel = rel
        self.href = href


class ResourceWithLinks:
    """
    Allows adding links to a resource, in order to make the API HATOAS compliant
    """
    def __init__(self, source_object, namespace):

        self.__dict__ = source_object.__dict__.copy()
        self.links = []
        self.namespace = namespace
        self.base_url = self.namespace.apis[0].base_url
        if self.base_url[-1] == '/':
            self.base_url = self.base_url[0:-1]


    def add_link(self, rel, href=False):
        link = self.base_url+self.namespace.path + "/"
        if href:
               link = link + href
        self.links.append(Link(rel,link))

