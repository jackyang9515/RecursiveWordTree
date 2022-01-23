"""
The test suite for TrieTree.
"""

from TrieTree import TrieTree
import pytest

# insert, contains and delete test case:


def test_first_1() -> None:
    t = TrieTree()
    t.insert('app')
    t.insert('apple')
    t.insert('application')
    t.insert('applications')

    assert 'app' in t
    assert 'apple' in t
    assert 'application' in t
    # makes sure the __contain__ function checks value as well.
    assert 'ap' not in t

    del t['apple']
    assert 'apple' not in t
    assert 'application' in t
    assert 'app' in t

    del t['app']
    assert 'app' not in t
    assert 'application' in t

    del t['applicatiou']
    assert 'application' in t

    del t['applications']
    assert 'applications' not in t
    assert 'application' in t

    t.insert('applications')
    del t['application']
    assert 'application' not in t and 'applications' in t


def test_first_2() -> None:
    t = TrieTree()
    t.insert('mom')
    t.insert('t-shirt')
    t.insert('')

    assert '' in t
    assert 't-shirt' in t
    assert 'shirt' not in t

    del t['tshirt']
    assert 't-shirt' in t

    del t['mom']
    assert 'mom' not in t

    del t['']
    assert '' in t


def test_first_3() -> None:
    t = TrieTree()
    t.insert('a')
    t.insert('b')
    t.insert('c')
    t.insert('cucumber')
    t.insert('cucumbep')
    t.insert('cm')
    t.insert('cn')

    assert 'c' in t
    assert 'cucumber' in t
    assert 'cucumbep' in t

    del t['cucumber']
    assert 'cucumber' not in t
    assert 'c' in t and 'cucumbep' in t

    del t['b']
    assert 'b' not in t

    del t['cn']
    assert 'cn' not in t and 'cm' in t


# sort, autoComplete, autoCorrect and merge
def test_sort_1() -> None:
    t = TrieTree()
    t.insert('hello')
    t.insert('urmama')
    t.insert('motherfucker')
    t.insert('booty')
    assert t.sort() == ['booty', 'hello', 'motherfucker', 'urmama']
    assert t.sort(True) == ['urmama', 'motherfucker', 'hello', 'booty']

    del t['poop']
    del t['booty']
    assert t.sort() == ['hello', 'motherfucker', 'urmama']


def test_sort_2() -> None:
    t = TrieTree()
    t.insert('debra')
    t.insert('david')
    t.insert('devil')
    t.insert('dev')
    t.insert('deval')
    t.insert('degree')
    assert t.sort() == ['david', 'debra', 'degree', 'dev', 'deval', 'devil']
    reversed = t.sort()
    reversed.reverse()
    assert t.sort(True) == reversed

    del t['dev']
    assert 'dev' not in t
    assert 'deval' in t and 'devil' in t

    assert t.sort() == ['david', 'debra', 'degree', 'deval', 'devil']

    del t['deval']
    assert 'deval' not in t
    assert 'devil' in t

    assert t.sort() == ['david', 'debra', 'degree', 'devil']


def test_autoComplete_1() -> None:
    t = TrieTree()
    t.insert('debra')
    t.insert('david')
    t.insert('devil')
    t.insert('dev')
    t.insert('deval')
    t.insert('degree')
    assert t.autoComplete('', 5) == ['david', 'debra', 'degree', 'dev', 'deval']
    assert t.autoComplete('d') == ['david', 'debra', 'degree', 'dev', 'deval', 'devil']
    assert t.autoComplete('de') == ['debra', 'degree', 'dev', 'deval', 'devil']
    assert t.autoComplete('de', 2) == ['debra', 'degree']
    assert t.autoComplete('di') == []


def test_autoComplete_2() -> None:
    t = TrieTree()
    t.insert('d')
    t.insert('dd')
    t.insert('dda')
    t.insert('ddb')
    t.insert('')
    t.insert('deabrajumbo')
    assert t.autoComplete('') == ['d', 'dd', 'dda', 'ddb', 'deabrajumbo']
    assert t.autoComplete('dd', 1) == ['dd']
    assert t.autoComplete('dd') == ['dd', 'dda', 'ddb']


def test_autoCorrect_1() -> None:
    t = TrieTree()
    t.insert('debra')
    t.insert('david')
    t.insert('devil')
    t.insert('dev')
    t.insert('deval')
    t.insert('degree')
    assert t.autoCorrect('dir', 4) == ['david', 'debra', 'dev', 'deval', 'devil']
    assert t.autoCorrect('avadacadabra') == []
    assert t.autoCorrect('deval') == ['deval']
    assert t.autoCorrect('devop') == ['dev', 'deval', 'devil']
    assert t.autoCorrect('deprp', 3) == ['debra', 'degree', 'dev', 'deval', 'devil']


def test_autoCorrect_2() -> None:
    t = TrieTree()
    t.insert('shithead')
    t.insert('dicksucker')
    assert t.autoCorrect('shitread') == ['shithead']
    assert t.autoCorrect('dpckspckpr') == []


def test_merge() -> None:
    t1 = TrieTree()
    t2 = TrieTree()
    t1.merge(t2)
    assert t1.sort() == []

    t1.insert('moon')
    t2.insert('monster')
    t2.insert('hamburger')
    t1.merge(t2)
    assert t1.sort() == ['hamburger', 'monster', 'moon']
    assert t2.sort() == ['hamburger', 'monster']


def test_total() -> None:
    t1 = TrieTree()
    t2 = TrieTree()
    t1.insert('pig')
    t2.insert('halo')
    t1.insert('pog')
    t1.insert('genius')
    t2.insert('meat')
    t2.insert('stick')
    assert t1.sort() == ['genius', 'pig', 'pog']
    assert t2.sort() == ['halo', 'meat', 'stick']
    assert t1.autoComplete('p') == ['pig', 'pog']
    assert t2.autoComplete('a') == []
    assert t2.autoComplete('') == ['halo', 'meat', 'stick']
    assert t2.autoComplete('m') == ['meat']
    assert t1.autoCorrect('ptg') == ['pig', 'pog']
    assert t1.autoCorrect('p', 1) == []
    t1.merge(t2)
    assert t1.sort() == ['genius', 'halo', 'meat', 'pig', 'pog', 'stick']


if __name__ == '__main__':

    pytest.main(['TrieTreeTest.py'])
