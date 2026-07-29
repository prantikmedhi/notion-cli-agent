# Data sources reference

Current docs say:

- use `ntn datasources resolve <database-id>` to map database to data source IDs
- use `ntn api v1/data_sources/<data-source-id>` to retrieve schema
- use `ntn datasources query <data-source-id>` for row listing
- for create/update, drop to `ntn api` with inline body args
- queries support filters, sorts, cursors, JSON output, and `filter_properties`
- query results cap at 10,000 pages
