import subprocess
import sys

try:
    import memory_profiler
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", 'memory-profiler'])
finally:
    import memory_profiler
    
from memory_profiler import memory_usage
import pytest
import session2
import time
import os.path
import re
import inspect 

README_CONTENT_CHECK_FOR = [
    'Something',
    'SomethingNew',
    'add_something',
    'clear_memory',
    'critical_function',
    'compare_strings_old',
    'compare_strings_new',
    'sleep',
    'char_list',
    'collection',
    '__init__'
]
memory_used = []
def test_clear_memory():
    memory_used = memory_usage((session2.critical_function))
    assert (memory_used[len(memory_used)-1] - memory_used[0]) < 4

def test_memory_actually_increaded():
    # This test will check whether we are actually increase the memory during running the function f
    memory_used2 = memory_usage((session2.critical_function))
    peak = max(memory_used2)
    assert (peak - memory_used2[0]) > 8, "Seems like you have changed the program! Are you trying to cheat!"

def test_performance():
    start1 = time.perf_counter()
    session2.compare_strings_old(10000000)
    end1 = time.perf_counter()
    delta1 = end1-start1

    start2 = time.perf_counter()
    session2.compare_strings_new(10000000)
    end2 = time.perf_counter()
    delta2 = end2-start2
    
    assert delta1/delta2 >= 10.0

def test_readme_exists():
    assert os.path.isfile("readme.md"), "Readme.md file missing!"

def test_readme_contents():
    readme = open("readme.md", "r")
    readme_words = readme.read().split()
    readme.close()
    assert len(readme_words) >= 500, "Make your readme.md file interesting! Add atleast 500 words"

def test_readme_proper_description():
    READMELOOKSGOOD = False
    f = open("readme.md", "r")
    content = f.read()
    f.close()
    for c in README_CONTENT_CHECK_FOR:
        if c not in README_CONTENT_CHECK_FOR:
            READMELOOKSGOOD == False
            pass
    assert READMELOOKSGOOD == True, "You have not described all the functions/class well in your readme.md file"

def test_readme_file_for_formatting():
    f = open("readme.md", "r")
    content = f.read()
    f.close()
    assert content.count("#") >= 10

    
def test_class_repr():
    s = session2.Something()
    s_n = session2.SomethingNew()

    assert 'object at' not in s.__repr__() and 'object at' not in s_n.__repr__()

def test_fourspace():
    r''' Returns pass if used four spaces for each level of syntactically \
    significant indenting.'''
    lines = inspect.getsource(session2)
    spaces = re.findall('\n(.+?)[a-zA-Z0-9@]', lines)
    for space in spaces:
        assert (len(space) % 4 > 0 and len(space) != 1), "Your code intentation does not follow PEP8 guidelines"

def test_function_name_had_cap_letter():
    functions = inspect.getmembers(session2, inspect.isfunction)
    for function in functions:
        assert len(re.findall('([A-Z])', function[0])) == 0, "You have used Capital letter(s) in your function names"

if __name__ ==  '__main__':
    test_clear_memory()


