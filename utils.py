def make_query_f_string(column_list):
    return ', '.join([f"\"{{row['{col}']}}\"" for col in column_list])