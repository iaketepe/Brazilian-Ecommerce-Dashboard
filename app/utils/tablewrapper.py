class TableWrapper:
    def __init__(self, tableData):
        self.tableData = tableData
        self._lookup = {rec['name']: rec['value'] for rec in tableData}

    def __getattr__(self, name):
        return self._lookup.get(name)

    def __getitem__(self, name):
        return self._lookup.get(name)