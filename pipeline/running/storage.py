from pipeline.running import processor

def store(db, schema_base, act_name):
    try:
        schema_name = act_name if schema_base == "" else schema_base + "_" + act_name
        table_names = list(processor.acts[act_name].keys())

        db.create_schema(schema_name)

        for table_name in table_names:
            db.create_table(schema_name, table_name)
            db.write_to_table(schema_name, table_name, processor.acts[act_name][table_name])

    except Exception as e:
        print(e)