def old_autoCorrect(self, word: str, errorMax: int =2) -> list:
    """
    Given a word, if misspelt return a list of possible valid words from the last valid prefix, with up to errorMax errors
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
    # TODO
    node = self.last_valid_letter(word)
    return node.autoCorrect_recursion(word, errorMax)

def autoCorrect_recursion(self, word: str, errorMax: int) -> List[str]:
    """
    The recursion process of autoCorrect.
    """
    if errorMax < 0:
        return []
    elif self.get_children() == {}:
        if self.get_value() != '' and mistake_counter(self.get_value(),
                                                      word) <= errorMax:
            return [self.get_value()]
        return []
    else:
        final_lst = []
        if self.get_value() != '' and mistake_counter(self.get_value(), word) == 0:
            return [self.get_value()]
        elif self.get_value() != '' and mistake_counter(self.get_value(),
                                                        word) <= errorMax:
            final_lst.append(self.get_value())
        for letter in ALPHABET:
            if letter in self._children:
                final_lst.extend(
                    self.get_children()[letter].autoCorrect_recursion(word, errorMax))
        return final_lst

def last_valid_letter(self, word: str) -> TrieNodeAbstract:
    """
    Traverse the word until the we arrive at the last letter in word that
    exists in the TrieTree.
    """
    index = 0
    if word[index] in self._children:
        start = self._children[word[index]]
        index += 1
    else:
        return self
    while index < len(word):
        if word[index] not in start.get_children():
            return start
        start = start.get_children()[word[index]]
        index += 1
    return start

def mistake_counter(word1: str, word2: str) -> int:
    """
    Returns the number of letters off from word1 to word2.

    Precondition: word1 and word2 must not be empty.

    >>> mistake_counter('hello', 'bello')
    1
    >>> mistake_counter('immunization', 'cao')
    12
    >>> mistake_counter('dab', 'dea')
    2
    """
    index = 0
    error_count = 0
    while index < min(len(word1), len(word2)):
        if word1[index] != word2[index]:
            error_count += 1
        index += 1
    return error_count + abs(len(word1) - len(word2))


def delete(self, key: str) -> None:
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
        start_index = 0
        if key[index] in self._children:
            start = self._children[key[index]]
            end = self._children[key[index]]
        else:
            return
        while not end.get_value() == key:
            if not len(end.get_children()) == 1 or (end.get_value() != '' and end.get_value() != key):
                start = end
                start_index = index
            index += 1
            if key[index] in end.get_children():
                end = end.get_children()[key[index]]
            else:
                return
        # now, start is the last point that has a value, whereas end has
        # the value that we want to get rid of.
        if end.get_children() != {}:  # if end has more letters after it
            end.set_value('')
        else:
            if start == self._children[key[0]] and start.get_value() == '' and len(start.get_children()) == 1:  # if this is true, that means start hasn't moved at all
                self._children.pop(key[0])
            else:
                start.children_pop(key[start_index + 1])
        # print(start._char, end._char, index, start_index)
        return
