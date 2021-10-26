import pytest
import os
from hr.tree import Tree


class TestApp:
    @pytest.mark.datafiles("./tests/files/basic_tree.json")
    def test_basic_load(self, datafiles):
        hr_tree = Tree()
        filename = os.path.join(str(datafiles), "basic_tree.json")
        assert os.path.isfile(filename)
        hr_tree.load_file(filename)
        assert hr_tree.headcount() == 3

    @pytest.mark.datafiles("./tests/files/wrong_link.json")
    def test_wrong_links(self, datafiles):
        hr_tree = Tree()
        filename = os.path.join(str(datafiles), "wrong_link.json")
        with pytest.raises(Exception) as e_info:
            hr_tree.load_file(filename)
