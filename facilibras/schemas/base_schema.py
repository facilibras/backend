from pydantic import BaseModel

def to_camel(string: str) -> str:
    parts = string.split('_')
    return parts[0] + ''.join(word.capitalize() for word in parts[1:])

class BaseSchema(BaseModel):
    class Config:
        alias_generator = to_camel
        populate_by_name = True

    def model_dump(self, **kwargs):
        return super().model_dump(by_alias=True, **kwargs)
    
    def model_dump_json(self, **kwargs):
        return super().model_dump_json(by_alias=True, **kwargs)
