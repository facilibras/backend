from pydantic import BaseModel, ConfigDict


def to_camel(string: str) -> str:
    """Converte campo para camel case ao escrever objeto JSON."""

    parts = string.split("_")
    return parts[0] + "".join(word.capitalize() for word in parts[1:])


class BaseSchema(BaseModel):
    """Schema base para os DTOs da aplicação."""

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        ser_json_timedelta="iso8601",
    )
