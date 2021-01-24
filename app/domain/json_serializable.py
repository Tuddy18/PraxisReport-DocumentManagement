
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

    # def json_str(self):
