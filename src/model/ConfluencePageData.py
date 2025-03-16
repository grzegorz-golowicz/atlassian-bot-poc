class ConfluencePageData:
    def __init__(self, id, space, title, contents, url, last_updated):
        self.id = id
        self.space = space
        self.title = title
        self.contents = contents
        self.url = url
        self.last_updated = last_updated

    def to_dict(self):
        return {
            'id': self.id,
            'space': self.space,
            'title': self.title,
            'contents': self.contents,
            'url': self.url,
            'last_updated': self.last_updated
        }