from marshmallow import fields, Schema, ValidationError, validate

from masters import exceptions


TRANSLATION_TO_MARSHMALLOW = {
    "string": fields.String,
    "integer": fields.Integer,
    "float": fields.Float,
    "number": fields.Number,
}


def schema_factory(configuration_dict):
    """Creates Marshmallow's Schema Object from dict"""
    validation_dict = {}

    for feature in configuration_dict["features"]:
        val_fun = TRANSLATION_TO_MARSHMALLOW[feature["field"]]

        kwargs = feature.get("extra_config", {})

        validation_key = feature.get("validation", None)
        if validation_key is not None:
            validation = get_validation_fun(validation_key)
        else:
            validation = None

        validation_dict[feature["name"]] = val_fun(validate=validation, **kwargs)

    return Schema.from_dict(validation_dict)


def get_validation_fun(validation):
    """Gets Marshmallow's validation function"""
    key = validation.pop("name")
    try:
        validate_fun = getattr(validate, key)
    except KeyError:
        raise exceptions.ValidationFunctionNotFound(f"{key} was not found!")
    return validate_fun(**validation.get("arguments", {}))


def validate_inputs(*, input_data, validation_schema):
    """Validates input data using validation schema"""
    if not isinstance(input_data, list):
        input_data = [input_data]

    errors = []
    for ix, data in enumerate(input_data):
        try:
            validation_schema().load(data)
        except ValidationError as err:
            fields = list(err.messages.keys())
            # NOTE: field nsvo must exist and be present on the config.yml file
            # I can change this later
            errors.append([data["record_id"], data["nsvo"], ",".join(fields)])

    return errors
