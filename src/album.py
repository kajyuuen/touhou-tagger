class Album:
    def __init__(self,
                 name: str,
                 smw_id: int = None,
                 properties: dict = None):
        self.name = name
        self.smw_id = smw_id
        self.properties = properties

    @classmethod
    def from_params(cls, params: dict):
        if "alname" in params.keys() and len(params["alname"]) == 1:
            name = params["alname"]
            params.pop("alname")
        new_album = cls(name, properties=params)
        return new_album
