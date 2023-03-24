from datasette import hookimpl, Response
import hashlib


PROMPT = """
Run SQLite queries against a database hosted by Datasette.
Datasette supports most SQLite syntax but does not support PRAGMA statements.
Use `select group_concat(sql, ';') from sqlite_master` to see the list of tables and their columns
Use `select sql from sqlite_master where name = 'table_name'` to see the schema for a table, including its columns.
Instead of `PRAGMA table_info(table_name)` use `select * from pragma_table_info('table_name')`
PRAGMA statements are not allowed. `select * from pragma_table_info('table_name') is allowed.
""".strip()


def make_openapi_schema(datasette, request):
    db_route = first_db(datasette).route
    return f"""
openapi: 3.0.1
info:
  title: Datasette API
  description: Execute SQL queries against a Datasette database and return the results as JSON
  version: 'v1'
servers:
  - url: https://{request.host}
paths:
  /{db_route}.json:
    get:
      operationId: query
      summary: Execute a SQLite SQL query against the {db_route} database
      description: Accepts SQLite SQL query, returns JSON. Does not allow PRAGMA statements.
      parameters:
      - name: sql
        in: query
        description: The SQL query to be executed
        required: true
        schema:
          type: string
      - name: _shape
        in: query
        description: The shape of the response data. Must be "array"
        required: true
        schema:
          type: string
          enum:
            - array
      responses:
        '200':
          description: Successful SQL results
          content:
            application/json:
              schema:
                type: array
                items:
                  type: object
        '400':
          description: Bad request
        '500':
          description: Internal server error
""".strip()


def ai_plugin_schema(request):
    return {
        "schema_version": "v1",
        "name_for_model": name_for_model(request.host),
        "name_for_human": name_for_human(request.host),
        "description_for_model": PROMPT,
        "description_for_human": "Run SQL against data in Datasette.",
        "auth": {"type": "none"},
        "api": {
            "type": "openapi",
            "url": f"https://{request.host}/-/chatgpt-openapi-schema.yml",
            "has_user_authentication": False,
        },
        "logo_url": "https://avatars.githubusercontent.com/u/126964132?s=400&u=08b2ed680144a4feb421308f09e5f3cc5876211a&v=4",
        # TODO: These should be in plugin configuration
        "contact_email": "hello@contact.com",
        "legal_info_url": "hello@legal.com",
    }


def first_db(datasette):
    return [
        value for key, value in datasette.databases.items() if not key.startswith("_")
    ][0]


async def ai_plugin(request):
    return Response.json(ai_plugin_schema(request))


async def openapi_schema(datasette, request):
    return Response.text(make_openapi_schema(datasette, request))


@hookimpl
def register_routes():
    return [
        (r"^/\.well-known/ai-plugin\.json$", ai_plugin),
        (r"^/-/chatgpt-openapi-schema.yml$", openapi_schema),
    ]


def name_for_model(hostname):
    name = hostname.replace(".", "_").replace("-", "_").replace(":", "_")
    md5_hash = hashlib.md5(hostname.encode("utf-8")).hexdigest()[:6]
    output = f"datasette_{name}_{md5_hash}"

    if len(output) > 50:
        excess_length = len(output) - 50
        output = f"datasette_{name[:-excess_length]}_{md5_hash}"

    return output


def name_for_human(hostname):
    output = f"Query {hostname}"

    if len(output) > 30:
        excess_length = len(output) - 30
        output = f"Query {hostname[:-excess_length]}"

    return output
