import pytest
from pathlib import Path
from recipes.recipe import Recipe


def test_recipe__valid__doesnt_exist__recipe_module_instantiates(capsys):
    recipe = Recipe.from_recipe_path(Path('./01_testing_chapter/02_testing_example/example.py'))
    recipe.run()
    out, err = capsys.readouterr()

    assert recipe.module == 'example'
    assert recipe.chapter == 1
    assert recipe.number == 2
    assert recipe.name is None
    assert recipe.package is None
    assert 'Couldn\'t find Recipe' in out
    assert err == ''
    with pytest.raises(ModuleNotFoundError, match='This recipe couldn\'t be found:'):
        recipe.get_module()


def test_recipes_running(recipe_path, capsys):
    recipe = Recipe.from_recipe_path(recipe_path)
    recipe.run()

    out, err = capsys.readouterr()
    assert 'TODO' not in recipe.get_docstring()
    assert "if __name__ == '__main__':" in recipe.get_code()
    assert 'Running...' in out
    assert err == ''
