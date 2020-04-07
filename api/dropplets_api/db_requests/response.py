from datetime import datetime

from asyncpg import Record


class Response:
    """ Object class for handling a generic response along its request lifecycle
    """

    # records and records_modeled can be a single object or an array of objects
    records = None
    records_modeled = None
    data_dict = None
    length = 0

    def __init__(self, records=None, records_modeled=None):
        """
        Initializes response object from records (see set_data method)
        """
        self.records = records
        self.records_modeled = records_modeled

    def get_records(self):
        """
        Returns previously stored records attribute
        """
        return self.records

    def get_records_modeled(self):
        """
        Returns previously stored records_modeled attribute
        """
        return self.records_modeled

    def set_records(self, records):
        self.records = records

    def set_records_modeled(self, records_modeled):
        self.records_modeled = records_modeled

    def update_data_dict(self, records, modeled=False):
        """
        Initializes response object and fills 'data_dict' from records.
        Records can either be:
        - single or list of raw Record instances
        - modeled/instantiated sigle or list of records
        """
        def record_to_dict(record):
            """
            Converts a record into a dict
            """
            record_dict = {}
            if modeled:
                record_dict = record.as_dict()
            elif isinstance(record, Record) or isinstance(record, dict):
                record_dict = {key: value for key, value in record.items()}
                for key, value in record_dict.items():
                    if isinstance(value, datetime):
                        record_dict[key] = str(value)
            return record_dict

        if isinstance(records, list):
            # multiple records. 'data' as an array of dicts in JSON
            self.data_dict = []
            for record in records:
                record_dict = record_to_dict(record)
                self.data_dict.append(record_dict)
            self.length = len(self.data_dict)

        elif records is not None:
            # single record. 'data' as a dict in JSON
            record_dict = record_to_dict(records)
            self.data_dict = record_dict
            self.length = 1

    def as_dict(self):
        """
        Method that returns response object as dict for converting to json and
        returned in http body response
        """
        if self.records_modeled is not None:
            self.update_data_dict(self.records_modeled, modeled=True)
        elif self.records is not None:
            self.update_data_dict(self.records)

        d = {
            'data': self.data_dict,
            'metadata': {
                'length': self.length
            }
        }

        return d
