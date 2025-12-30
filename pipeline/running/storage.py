from pipeline.running import processor
from pipeline.utils import sqlizer

def store(db, schema_base, act_name):
    schema_name = act_name if schema_base == "" else schema_base + "_" + act_name
    table_names = list(processor.acts[act_name].keys())

    db.create_schema(schema_name)

    for table_name in table_names:
        sqltypes = sqlizer.get_sql_types(processor.acts[act_name][table_name])
        db.create_table(schema_name, table_name, sqltypes)
        if (not(db.data_exists(schema_name,table_name))):
            db.write_to_table(schema_name, table_name, processor.acts[act_name][table_name])