from .utils import *


class Connection(happybase.Connection):
    def tables(self):
        tables = super().tables()
        return [convert_get_type(table) for table in tables]

    def table(self, name, use_prefix=True):
        name = ensure_bytes(name)
        if use_prefix:
            name = super()._table_name(name)
        return Table(name, self)


class Table(happybase.table.Table):
    def row(self, row, columns=None, timestamp=None, include_timestamp=False):
        rowdic = super().row(row, columns, timestamp, include_timestamp)
        return convert_get_mapping_dic(rowdic)

    def rows(self, rows, columns=None, timestamp=None, include_timestamp=False):
        rowslist = super().rows(rows, columns, timestamp, include_timestamp)
        return [(key, convert_get_mapping_dic(data),) for key, data in rowslist]
