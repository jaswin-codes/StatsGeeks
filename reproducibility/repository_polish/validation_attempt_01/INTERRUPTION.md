# Preserved interruption
The first validator attempt stopped at nbformat import: UnicodeDecodeError in
jsonschema_specifications._schemas reading a non-UTF-8 resource. No model loaded.
The environment was not modified. Subsequent receipts record the import as BLOCKED
and validate the notebook using the exact installed v4.5 schema via fastjsonschema.
