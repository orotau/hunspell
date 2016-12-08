# this is in the test directory directly
# which ensures that it gets added to the path 
# see
# http://docs.pytest.org/en/latest/goodpractices.html#test-discovery
import sys

# use the -s flag to see the sys.path when running pytest
# i.e.
# ~/PythonProjects/hunspell/hunspell$ python -m pytest -s

print(sys.path)
