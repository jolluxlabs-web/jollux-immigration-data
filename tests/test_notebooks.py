import json
from pathlib import Path


NOTEBOOKS = {
    "pwd-introduction.ipynb": "ingest_pwd",
    "perm-introduction.ipynb": "ingest_perm",
}


def test_introductory_notebooks_are_valid_self_contained_examples():
    notebook_directory = Path(__file__).parents[1] / "notebooks"

    for filename, public_api in NOTEBOOKS.items():
        notebook = json.loads((notebook_directory / filename).read_text(encoding="utf-8"))
        source = "\n".join(
            "".join(cell["source"])
            for cell in notebook["cells"]
            if cell["cell_type"] == "code"
        )

        assert notebook["nbformat"] == 4
        assert public_api in source
        assert "TemporaryDirectory" in source
        assert all(not cell.get("outputs") for cell in notebook["cells"])
