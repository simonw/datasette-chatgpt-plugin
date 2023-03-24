from datasette.app import Datasette
from datasette_chatgpt_plugin import name_for_model
import pytest


@pytest.mark.asyncio
async def test_plugin_is_installed():
    datasette = Datasette(memory=True)
    response = await datasette.client.get("/-/plugins.json")
    assert response.status_code == 200
    installed_plugins = {p["name"] for p in response.json()}
    assert "datasette-chatgpt-plugin" in installed_plugins


@pytest.mark.parametrize(
    "input,expected",
    (
        ("https://example.com", "datasette_example_com_c984d0"),
        (
            "https://congress-legislators.datasettes.com/",
            "datasette_congress_legislators_datasettes_c_91d42f",
        ),
    ),
)
def test_name_for_model(input, expected):
    output = name_for_model(input)
    assert len(output) <= 50
    assert output == expected
