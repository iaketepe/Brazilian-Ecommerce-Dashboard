from datetime import date, timedelta

def infer_sql_type(datapoint):
    """
    Infer SQL type based on Python value.
    Returns a PostgreSQL-friendly type as a string.
    """

    if isinstance(datapoint, str):
        return "TEXT"

    if isinstance(datapoint, bool):
        return "BOOLEAN"

    if isinstance(datapoint, int):
        return "INTEGER"

    if isinstance(datapoint, float):
        return "NUMERIC"

    if isinstance(datapoint, date):
        return "DATE"

    if isinstance(datapoint, timedelta):
        return "INTERVAL"

    # Default fallback
    return "TEXT"


def infer_sql_types(datapoints):
    """
    Infer SQL types for a list of values.
    Returns a list of SQL type strings.
    """
    return [infer_sql_type(datapoint) for datapoint in datapoints]


def get_sql_types(data):
    """
    Infer SQL types for a row dict.
    Expects a list of dicts like [{'col1': val1, 'col2': val2}, ...]
    Returns a dict mapping column names to SQL types.
    """
    if not data:
        return {}

    first_row = data[0]
    types = infer_sql_types(list(first_row.values()))
    return dict(zip(first_row.keys(), types))
