from gapfinder.themes import stability


def test_stability_scores_overlap():
    themes = [{"a", "b", "c", "d"}, {"x", "y"}]
    other_runs = [
        [{"a", "b", "c", "d"}, {"x"}],          # theme 1 identical, theme 2 half
        [{"a", "b"}, {"c", "d"}, {"x", "y"}],   # theme 1 split, theme 2 identical
    ]
    assert stability(themes, other_runs) == [0.75, 0.75]
    assert stability(themes, []) == [1.0, 1.0]
