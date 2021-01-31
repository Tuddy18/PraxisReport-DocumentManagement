
class JsonSerializable:
    def json_dict(self):
        dict = {}
        for key in self.__dict__.keys():
            if key[0] != '_':
                if isinstance(self.__dict__[key], JsonSerializable):
                    dict[key] = self.__dict__[key].json_dict()
                else:
                    dict[key] = self.__dict__[key]
        return dict

    def update_from_dict(self, json_dict):
        for key in json_dict.keys():
            if json_dict[key]:
                if isinstance(self.__dict__[key], JsonSerializable):
                    self.__dict__[key].update_from_dict(json_dict[key])
                else:
                    if key != 'id':
                        self.__setattr__(key, json_dict[key])

    # def json_str(self):
