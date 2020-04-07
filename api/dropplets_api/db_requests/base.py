import time
import traceback
import logging

from dropplets_api.db import DBRecordNotFound, DBConflict, Forbidden

from .response import Response


def instantiate_class_from_records(classinfo, records):

    if isinstance(records, list):
        new_records = []
        if records is not None:
            for record in records:
                if isinstance(record, classinfo):
                    new_records.append(record)
                else:
                    new_records.append(classinfo(record=record))
        return new_records

    else:
        new_record = None
        record = records
        if isinstance(record, classinfo):
            new_records.append(record)
        else:
            new_records.append(classinfo(record=record))


async def run_query(request, query, classinfo=None, single=False):
    """
    Returns a Response instance from the result of running the query, either:
    - (sigle=False) : containing a list of Record
    - (sigle=True)  : containing the first row as Record
    """
    response = Response()

    result = None
    records = None
    try:
        if single:
            async with request.app['db_pool_dropplets'].acquire() as conn:
                records = await conn.fetchrow(query)
        else:
            async with request.app['db_pool_dropplets'].acquire() as conn:
                records = await conn.fetch(query)
    except Exception as e:
        raise DBConflict(e)

    if records is None: # will occur for single records operations
        raise DBRecordNotFound()

    response.set_records(records)

    # additionally set modeled records if class is provided
    if classinfo is not None:
        records_modeled = instantiate_class_from_records(classinfo, records)
        response.set_records_modeled(records_modeled)

    return response
