from typing import Optional

from .cruds import T


def convert_object_to_dict(
    record: T | list[T], multi: bool = False
) -> dict | list[dict] | None:
    if not record:
        return list() if multi else None

    __record = record
    if not isinstance(record, list):
        __record = [record]
    dict_records = list()
    for rd in __record:
        dict_record = rd.__dict__
        dict_record.pop("_sa_instance_state")
        dict_records.append(dict_record)
    return dict_records if multi else dict_records[0]
