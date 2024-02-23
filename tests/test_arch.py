from pathlib import Path

import pytest
from pytestarch import Rule, get_evaluable_architecture


@pytest.fixture
def evaluable():
    root_dir = Path(__file__).parent.parent
    todo_app_module = str(root_dir / "todo_app")
    return get_evaluable_architecture(todo_app_module, todo_app_module)


def test_models_dont_import_anything(evaluable):
    rule = (
        Rule()
        .modules_that()
        .are_named("todo_app.models")
        .should_not()
        .import_modules_that()
        .are_sub_modules_of("todo_app")
    )
    rule.assert_applies(evaluable)


def test_tables_are_only_imported_by_service(evaluable):
    rule = (
        Rule()
        .modules_that()
        .are_named("todo_app.tables")
        .should_only()
        .be_imported_by_modules_that()
        .are_sub_modules_of("todo_app.services")
    )
    rule.assert_applies(evaluable)
