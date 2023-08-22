import enum
from typing import Type

import fastjsonschema
from fastapi import HTTPException
from pydantic import BaseModel
from pydantic_core import ErrorDetails


class AuthLevel(enum.Enum):
    """
    - OPERATOR = 0
    - SUPERVISOR = 1
    - ENGINEER = 2
    """

    OPERATOR = 0
    SUPERVISOR = 1
    ENGINEER = 2


async def validate_input(input: dict, model: Type[BaseModel]):
    validator = fastjsonschema.compile(model.model_json_schema())
    try:
        validator(input)
    except fastjsonschema.exceptions.JsonSchemaValueException as err:
        print(err.__dict__)
        detail = ErrorDetails(
            type="value_error",
            loc=err.name.split("."),
            msg=err.message,
            input=err.value,
            ctx=err.definition,
        )
        raise HTTPException(
            status_code=422,
            detail=detail,
        ) from err
