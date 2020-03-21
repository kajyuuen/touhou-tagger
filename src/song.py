class Song:
    def __init__(self,
                 name: str,
                 smw_id: int,
                 properties: dict = None) -> None:
        self.name = name
        self.smw_id = smw_id
        self.properties = properties

    @classmethod
    def from_params(cls,
                    string_smw_id: str,
                    params: dict):
        if "name" in params.keys() and len(params["name"]) == 1:
            name = params["name"]
            params.pop("name")
        new_song = cls(name, int(string_smw_id), properties=params)
        return new_song
