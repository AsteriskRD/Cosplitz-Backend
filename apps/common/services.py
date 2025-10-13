from typing import TypeVar

from django.db import models
DjangoModelType = TypeVar("DjangoModelType", bound=models.Model)
def model_update(*, instance: DjangoModelType, fields, data, auto_updated_at=True):
    has_updated = False
    m2m_data = {}
    update_fields = []

    model_fields = {fields.name : fields for field in instance._meta.get_fields() }
    # output model_filed = {"first_name": <CharField>,"last_name": <CharField>,}
    for field in fields:
        if field not in data:
            continue

        model_field = model_fields.get(field) # e.g EmailField or CharField

        assert model_field is not None, f"{field} is not part of {instance.__class__.__name__} fields."

    if isinstance(model_field, model.ManyToManyField):
        m2m_data[field] = data[fields]
        continue