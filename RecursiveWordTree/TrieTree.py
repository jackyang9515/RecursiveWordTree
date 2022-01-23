from TrieNodeAbstract import TrieNodeAbstract
from ChildrenDictionary import ChildrenDictionary
import math
from typing import Dict, List, Union, Any, Tuple

# For help in traversing children
ALPHABET = 'abcdefghijklmnopqrstuvwxyz'


class TrieTree(TrieNodeAbstract):
    def __init__(self, char='', value: str = ''):
        """
        Initializes:
            This node's char, `self._char`, ie. your current character in the key
            This node's set of subtrees, 'children', using a dictionary
            This node's value, `self._value`  only set iff its a valid word in the dictionary
        """
        self._value = value
        self._children: ChildrenDictionary = ChildrenDictionary()
        self._char = char

    def set_value(self, n: str) -> None:
        self._value = n

    def get_value(self) -> str:
        return self._value

    def get_char(self) -> str:
        return self._char

    def get_children(self) -> dict:
        return self._children

    def children_pop(self, n: str) -> None:
        if n in self._children:
            self._children.pop(n)
        return

    # TASK 1
    def insert(self, word: str) -> None:
        """
        Insert your new word, keep in mind, you must insert all child nodes
        >>> trie = TrieTree()
        >>> trie.insert("word")
        >>> trie.insert("water")
        >>> trie.insert("banana")
        >>> trie.insert('bananaa')
        >>> trie.insert('world')
        >>> trie.insert('orbit')
        >>> "word" in str(trie)
        True
        >>> "water" in str(trie)
        True
        >>> "bob" in str(trie)
        False
        >>> "banana" in str(trie)
        True
        >>> "bananaa" in str(trie)
        True
        >>> "world" in str(trie)
        True
        >>> "orbit" in str(trie)
        True
        """
        # TODO
        index = 0
        curr = self
        while index < len(word):
            if word[index] in curr._children:
                curr = curr._children[word[index]]
                index += 1
            else:
                curr._children[word[index]] = TrieTree(word[index])
                curr = curr._children[word[index]]
                index += 1
        curr.set_value(word)
        return

    # TASK 2

    def __contains__(self, key: str) -> bool:
        """
        Returns True iff key is in tree, otherwise False
        >>> trie = TrieTree()
        >>> trie.insert("word")
        >>> trie.insert('a')
        >>> 'a' in trie
        True
        >>> "word" in trie
        True
        >>> 'wor' in trie
        False
        >>> "other" in trie
        False
        >>> trie = TrieTree()
        >>> trie.insert("word")
        >>> trie.insert("water")
        >>> trie.insert("banana")
        >>> trie.insert('bananaa')
        >>> trie.insert('world')
        >>> trie.insert('orbit')
        >>> "word" in trie
        True
        >>> "water" in trie
        True
        >>> "bob" in trie
        False
        >>> "banana" in trie
        True
        >>> "bananaa" in trie
        True
        >>> "world" in trie
        True
        >>> "orbit" in trie
        True
        >>> "orb" in trie
        False
        """
        # TODO
        if len(key) == 1:
            if key in self._children:
                return self._children[key].get_char() == key \
                       and self._children[key].get_value() == key
            return False
        elif key == '':
            return True
        else:
            index = 0
            curr = self
            while index < len(key):
                if key[index] in curr._children:
                    curr = curr._children[key[index]]
                    index += 1
                else:
                    return False

            return curr._value == key and curr._char == key[len(key) - 1]

    # TASK 3
    def __delitem__(self, key: str) -> None:
        """
        Deletes entry in tree and prunes unecessary branches if key exists, otherwise changes nothing
        >>> trie = TrieTree()
        >>> trie.insert("word")
        >>> "word" in trie
        True
        >>> del trie["word"]
        >>> "word" in trie
        False
        >>> str(trie)
        'TrieTree'
        >>> trie.insert('ab')
        >>> trie.insert('abs')
        >>> str(trie)
        'TrieTree\\n   `- a\\n      `- b : ab\\n         `- s : abs'
        >>> del trie['ab']
        >>> str(trie)
        'TrieTree\\n   `- a\\n      `- b\\n         `- s : abs'
        >>> trie.insert('about')
        >>> del trie['about']
        >>> str(trie)
        'TrieTree\\n   `- a\\n      `- b\\n         `- s : abs'
        """

        # TODO
        if key == '':
            return
        elif len(key) == 1:
            if key[0] in self._children:
                node = self.get_children()[key[0]]
                if node.get_children() == {}:
                    self.children_pop(key[0])
                else:
                    node.set_value('')
        else:

            index = 0
            curr = self
            stack = []
            # if key[index] in self._children:
            #     start = self._children[key[index]]
            #     end = self._children[key[index]]
            # else:
            #     return
            while not curr.get_value() == key and index < len(key):
                # print(f'here, {key[index]}')
                # push current tree onto stack
                stack.append(curr)
                # Check if the current letter is in our children
                if key[index] not in curr._children:
                    return
                # increment index, and move the pointer to the next letter
                curr = curr._children[key[index]]
                index += 1
            # print(curr._char, index)
            # Make sure curr.value == key, if not then return
            if curr._value != key:
                return
            # now, start is the last point that has a value, whereas end has
            # the value that we want to get rid of.
            if curr.get_children() != {}:
                # if end has more letters after it
                curr.set_value('')
            else:
                # Start popping from our stack
                # curr = stack.pop()
                while not len(stack) == 0:
                    curr = stack.pop()
                    index -= 1
                    if (curr.get_value() != key and curr.get_value() != '') or len(curr.get_children()) > 1:
                        break
                # print(curr._char, index)
                curr._children.pop(key[index])
            return

    # TASK 4
    def sort(self, decreasing=False) -> list:
        """
        Returns list of words in tree sorted alphabetically
        >>> trie = TrieTree()
        >>> trie.insert('banana')
        >>> trie.insert('cherry')
        >>> trie.insert('apple')
        >>> trie.insert('application')
        >>> trie.insert('bbb')
        >>> trie.insert('app')
        >>> trie.sort()
        ['app', 'apple', 'application', 'banana', 'bbb', 'cherry']
        >>> trie.sort(decreasing=True)
        ['cherry', 'bbb', 'banana', 'application', 'apple', 'app']
        >>> t = TrieTree()
        >>> t.insert('apa')
        >>> t.insert('apb')
        >>> t.insert('apc')
        >>> t.insert('ap')
        >>> t.sort()
        ['ap', 'apa', 'apb', 'apc']
        """
        # TODO
        if self._children == {}:
            return []
        else:
            return self.help_sort(decreasing)

    def help_sort(self, decreasing=False, N: int =float('inf')) -> List[str]:
        """
        Helper function for sort(). This function sorts all the elements in
        self._children, since in order to perform recursion on the trie tree,
        we must skip the first node that contains nothing first.
        """
        if self._children == {}:
            return self._value_emptiness()
        else:
            if decreasing is False:
                value_lst = self._value_emptiness()
                for letter in ALPHABET:
                    if letter in self._children:
                        if len(value_lst) < N:
                            value_lst.extend(self._children[letter].help_sort(False, N))
                        else:  # either it is already == N or after the addition
                            break
                # print(value_lst + subtree)
                return value_lst

            else:
                value_lst = []
                for letter in ALPHABET[::-1]:
                    if letter in self._children:
                        if len(value_lst) < N - 1:
                            value_lst.extend(self._children[letter].help_sort(True, N - 1))
                        else:  # either it is already == N or after the addition
                            break
                if self._value != '':
                    value_lst.append(self._value)
                return value_lst

    def _value_emptiness(self) -> list:
        if self._value == '':
            return []
        else:
            return [self._value]

    # TASK 5
    def autoComplete(self, prefix: str, N: int =10) -> list:
        """
        if given a valid prefix, return a list containing N number of
        suggestions starting with that prefix in alphabetical order
        else return an empty list
        >>> trie = TrieTree()
        >>> trie.insert('apple')
        >>> trie.insert('dad')
        >>> trie.insert('apples')
        >>> trie.insert('application')
        >>> trie.insert('app')
        >>> trie.insert('about')
        >>> trie.autoComplete('a')
        ['about', 'app', 'apple', 'apples', 'application']
        >>> trie.autoComplete('a', N=2)
        ['about', 'app']
        >>> trie.autoComplete('app')
        ['app', 'apple', 'apples', 'application']
        >>> trie.autoComplete('c')
        []
        >>> trie.autoComplete('d')
        ['dad']
        >>> trie.autoComplete('', 2)
        ['about', 'app']
        """
        # TODO
        if self._children == {}:
            return []
        elif prefix == '':
            return self.help_sort(False, N)[:N]
        elif N == 0:
            return []
        else:
            curr = self.autoComplete_helper(prefix)
            if curr is None:
                return []
            return curr.help_sort(False, N)[:N]

    def autoComplete_helper(self, prefix: str) -> TrieNodeAbstract:
        """
        Returns the trie tree node at the end of the prefix.
        """
        index = 0
        if prefix[0] in self._children:
            curr = self._children[prefix[0]]
        else:
            return None
        while index < len(prefix) - 1 and curr.get_char() == prefix[index]:
            index += 1
            if prefix[index] in curr.get_children():
                curr = curr.get_children()[prefix[index]]
            else:
                return None
        return curr

    # TASK 6
    def autoCorrect(self, word: str, errorMax: int = 2) -> list:
        """
        A new method of traversing through the tree without checking each word's
        correctness

        >>> trie = TrieTree()
        >>> trie.insert('dab')
        >>> trie.autoCorrect('dod')
        ['dab']
        >>> trie.autoCorrect('dod', errorMax=1)
        []
        >>> trie.autoCorrect('dad', errorMax=1)
        ['dab']
        >>> trie.insert('apple')
        >>> trie.insert('dad')
        >>> trie.insert('dude')
        >>> trie.insert('apples')
        >>> trie.insert('application')
        >>> trie.insert('app')
        >>> trie.insert('about')
        >>> trie.insert("apples")
        >>> trie.insert("application")
        >>> trie.insert('app')
        >>> trie.insert('apple')
        >>> trie.autoCorrect('apl', errorMax=10)
        ['app', 'apple', 'apples', 'application']
        >>> trie.autoCorrect('apple')
        ['apple']
        >>> trie.autoCorrect('aboot')
        ['about']
        >>> trie.autoCorrect('dea')
        ['dab', 'dad']
        >>> trie.autoCorrect('dod')
        ['dab', 'dad', 'dude']
        >>> trie.autoCorrect('dea', errorMax=3)
        ['dab', 'dad', 'dude']
        >>> 'dab' in trie
        True
        >>> trie.insert('hello')
        >>> trie.autoCorrect('pello', 1)
        ['hello']
        >>> t = TrieTree()
        >>> t.insert('dig')
        >>> t.insert('dog')
        >>> t.insert('dug')
        >>> t.insert('duck')
        >>> t.autoCorrect('dpg', 3)
        ['dig', 'dog', 'duck', 'dug']
        """
        index = 0
        if word[index] in self._children:
            start = self._children[word[index]]
            index += 1
        else:
            start = self
        while index < len(word):
            if word[index] not in start.get_children():
                break
            start = start.get_children()[word[index]]
            index += 1
        return start.new_autoCorrect_recursion(index, word, errorMax)

    def new_autoCorrect_recursion(self, index: int, word: str, errorMax: int) -> list:
        """
        The recursion process of new autoCorrect.
        """
        if errorMax < 0:
            return []
        elif self.get_value() == word:
            return [word]
        elif self.get_children() == {}:
            if self.get_value() != '' and errorMax >= 0:
                return [self.get_value()]
        else:
            final_lst = []
            if self.get_value() != '' and abs(len(self.get_value()) - len(word)) <= errorMax:
                final_lst.append(self.get_value())
            for letter in ALPHABET:
                if letter in self._children:
                    if len(word) > index and letter == word[index]:
                        final_lst.extend(self.get_children()[letter].new_autoCorrect_recursion(index + 1, word, errorMax))
                    else:
                        final_lst.extend(self.get_children()[letter].new_autoCorrect_recursion(index + 1, word, errorMax - 1))
            return final_lst

    # TASK 7
    def merge(self, otherTrie: TrieNodeAbstract) -> None:
        """
        Merges another TrieTree into this one
        >>> trie1 = TrieTree()
        >>> trie2 = TrieTree()
        >>> trie1.insert('amazing')
        >>> trie2.insert('amazon')
        >>> trie1.merge(trie2)
        >>> 'amazon' in trie1
        True
        """
        # TODO
        if otherTrie.get_children() == {}:
            if otherTrie.get_value() != '':
                self.insert(otherTrie.get_value())
        else:
            if otherTrie.get_value() != '':
                self.insert(otherTrie.get_value())
            for child in otherTrie.get_children():
                self.merge(otherTrie.get_children()[child])

    def pPrint(self, _prefix="", _last=True, index=0):
        """
        DONT CHANGE THIS
        """
        ret = ''
        if index:
            ret = _prefix + ("`- " if _last else "|- ") + self._char
            _prefix += "   " if _last else "|  "
            if self._value:
                ret += ' : ' + self._value
            ret += '\n'
        else:
            ret = _prefix + "TrieTree"
            _prefix += "   " if _last else "|  "
            ret += '\n'
        child_count = len(self._children)
        for i, child in enumerate(self._children):
            _last = i == (child_count - 1)
            ret += self._children[child].pPrint(_prefix, _last, index + 1)
        return ret

    def __str__(self):
        return self.pPrint().strip()


if __name__ == '__main__':
    import doctest

    doctest.testmod()
