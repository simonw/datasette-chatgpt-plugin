from datasette.app import Datasette
from datasette_chatgpt_plugin import name_for_model, name_for_human
import pytest


@pytest.fixture
def ds():
    datasette = Datasette(memory=True)
    datasette.add_memory_database("example")
    return datasette


@pytest.mark.asyncio
async def test_ai_plugin(ds):
    response = await ds.client.get("/.well-known/ai-plugin.json")
    assert response.status_code == 200
    assert response.json() == {
        "schema_version": "v1",
        "name_for_model": "datasette_localhost_421aa9",
        "name_for_human": "Query localhost",
        "description_for_model": "Run SQLite queries against a database hosted by Datasette.\nDatasette supports most SQLite syntax but does not support PRAGMA statements.\nUse `select group_concat(sql, ';') from sqlite_master` to see the list of tables and their columns\nUse `select sql from sqlite_master where name = 'table_name'` to see the schema for a table, including its columns.\nInstead of `PRAGMA table_info(table_name)` use `select * from pragma_table_info('table_name')`\nPRAGMA statements are not allowed. `select * from pragma_table_info('table_name') is allowed.",
        "description_for_human": "Run SQL against data in Datasette.",
        "auth": {"type": "none"},
        "api": {
            "type": "openapi",
            "url": "https://localhost/-/chatgpt-openapi-schema.yml",
            "has_user_authentication": False,
        },
        "logo_url": "https://avatars.githubusercontent.com/u/126964132?s=400&u=08b2ed680144a4feb421308f09e5f3cc5876211a&v=4",
        "contact_email": "hello@contact.com",
        "legal_info_url": "hello@legal.com",
    }


@pytest.mark.asyncio
async def test_chatgpt_openai_schema(ds):
    response = await ds.client.get("/-/chatgpt-openapi-schema.yml")
    assert response.status_code == 200
    assert (
        response.text
        == """
openapi: 3.0.1
info:
  title: Datasette API
  description: Execute SQL queries against a Datasette database and return the results as JSON
  version: 'v1'
servers:
  - url: https://localhost
paths:
  /example.json:
    get:
      operationId: query
      summary: Execute a SQLite SQL query against the example database
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
    )


@pytest.mark.parametrize(
    "input,expected",
    (
        ("example.com", "datasette_example_com_5ababd"),
        (
            "congress-legislators.datasettes.com",
            "datasette_congress_legislators_datasettes_c_e7c508",
        ),
        ("127.0.0.1:8001", "datasette_127_0_0_1_8001_c69a4f"),
    ),
)
def test_name_for_model(input, expected):
    output = name_for_model(input)
    assert len(output) <= 50
    assert output == expected


@pytest.mark.parametrize(
    "input,expected",
    (
        ("example.com", "Query example.com"),
        (
            "congress-legislators.datasettes.com",
            "Query congress-legislators.dat",
        ),
        ("127.0.0.1:8001", "Query 127.0.0.1:8001"),
    ),
)
def test_name_for_human(input, expected):
    output = name_for_human(input)
    assert len(output) <= 30
    assert output == expected
