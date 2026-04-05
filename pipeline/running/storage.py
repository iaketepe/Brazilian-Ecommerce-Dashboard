from pipeline.running import processor
from pipeline.utils import sqlizer

def store(db, schema_base, act_name):
    schema_name = act_name if schema_base == "" else schema_base + "_" + act_name
    acts = processor.setup_acts()
    table_names = list(acts[act_name].keys())

    db.create_schema(schema_name)

    for table_name in table_names:
        sqltypes = sqlizer.get_sql_types(acts[act_name][table_name])
        db.create_table(schema_name, table_name, sqltypes)
        if (not(db.data_exists(schema_name,table_name))):
            db.write_to_table(schema_name, table_name, acts[act_name][table_name])