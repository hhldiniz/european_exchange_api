from json import JSONEncoder


class MyJsonEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__
