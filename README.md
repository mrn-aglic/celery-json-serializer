# celery-json-serializer

The repository contains an implementation of a custom json serializer for Celery applications. 
The aim was to have a serializer that would allow us to pass nested dataclasses and functions between tasks. 

# Working with the repo
Building the docker images can be done with:
```shell
make build
```

Running:
```shell
make run
```

Running with multiple (4) workers:
```shell
make run-scale workers=4
```

## The celery_json_serializer package


The Celery json serializer package has the following
structure:
```shell
celery_json/celery_json_serializer
├── __init__.py
├── callable_registration
│   ├── __init__.py
│   └── registration.py
├── config
│   ├── __init__.py
│   └── serialization_config.py
├── handler_registration.py
├── handlers
│   ├── __init__.py
│   ├── collection_handler.py
│   ├── crontab_handler.py
│   ├── dataclass_handler.py
│   ├── function_handler.py
│   └── handler_base.py
└── serializer
    ├── __init__.py
    ├── decoder.py
    └── encoder.py
```

### Representing functions as JSON
The JSON representation of a function contains the 
following keys:
- `name` - to determine from which function the 
representation was created (lambda functions are not
supported);
- `args` - the args that were passed to the function in 
case of a partial function;
- `kwargs` - the keyword arguments that were passed in case
of a partial function;
- `_handler` - the name of the handler that was used to 
encode the function.

Here is an example:
```json
"department_greeting": {
    "name": "celery_json.functions.helpers.example_function",
    "args": [],
    "kwargs": {},
    "_handler": "FunctionHandler",
},
```

When deserializing a function JSON, the `FunctionHandler`
returns an instance of the `functools.partial` function.

### Representing dataclasses as JSON
The JSON representation of a dataclass:
```json
{
    "name": "John",
    "id": 3,
    "skills": ["Python", "Data Analysis"],
    "employee_greeting": null,
    "_type": "celery_json.test_encoder_decoder.classes.Employee",
    "_handler": "DataclassHandler",
}
```

Two keys are added to the instance:
- `_type` - so that we know to which dataclass the 
instance belonged to;
- `_handler` - so that we know which handler was 
responsible for encoding the instance.

### Deserialization

In order to deserialize dataclasses and functions, the
entities need to be registered with the appropriate 
handlers. This is done so that:
1. we do not need to do dynamically search for and load the
dataclasses or functions during deserialization;
2. we can keep a whitelist of functions and dataclasses
that are allowed to be deserialized.

In regard to recreating a dataclass instance, any keys
added by the serializer should be dropped. In the current
implementation that means the `_type` and `_handler` keys.

### Serialization config

The `serialization_config` module creates a single instance 
of the `SerializationConfig` class. The instance is 
accessible through `json_serialization_config`.

### Handler registration
Handlers are registered in the `handler_registration` 
module. Currently, all the handlers from handlers directory 
are manually registered.

All handlers need to inherit the `JsonHandler` class. The
class provides the function `register`.
The register function needs to be implemented for handlers
that need to keep a registry of deserializable entities
(e.g. functions and dataclasses). The `FunctionHandler` and
`DataclassHandler` implement this method.

### callable_registration
This subpackage contains wrapper functions that can be used 
for registering serializable functions and dataclasses.

For example:
```python
from celery_json.celery_json_serializer import serializer_registration

@serializer_registration.register_dataclass
@dataclass
class Employee:
    name: str
    id: int
    skills: List[str]
    employee_greeting: Optional[Callable] = None
```

The function `register_dataclass` registerss the dataclass
that can be deserialized with the `DataclassHandler`.
As previously mentioned, functions and dataclasses need to
be registered with the appropriate handler in order to be
deserializable. 

Example of function registration:
```python
from celery_json.celery_json_serializer import serializer_registration

@serializer_registration.register_function
def example_function():
    print("hello from example function")
```
