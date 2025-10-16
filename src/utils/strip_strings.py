from pydantic import BaseModel


async def strip_strings(data_model: BaseModel) -> BaseModel:
    data = data_model.model_dump()

    for key, value in data.items():
        if isinstance(value, str):
            data[key] = value.strip()

    return data_model.model_validate(data)
