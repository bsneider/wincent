import json


class DisjointSet(object):
    def __init__(self):
        self.parents = {}

    def get_root(self, word):
        words_traversed = []
        while word in self.parents and self.parents[word] != word:
            words_traversed.append(word)
            word = self.parents[word]
        for word in words_traversed:
            self.parents[word] = word
        return word

    def add_synonyms(self, word1, word2):
        if word1 not in self.parents:
            self.parents[word1] = word1
        if word2 not in self.parents:
            self.parents[word2] = word2

        word1_root = self.get_root(word1)
        word2_root = self.get_root(word2)
        if word1_root < word2_root:
            word1_root, word2_root = word2_root, word1_root
        self.parents[word2_root] = word1_root

    def are_synonymous(self, word1, word2):
        root1 = self.get_root(word1)
        root2 = self.get_root(word2)
        return root1 == root2


def preprocess_synonyms(synonym_words):
    disjoint_set = DisjointSet()
    for word1, word2 in synonym_words:
        disjoint_set.add_synonyms(word1.lower(), word2.lower())
    return disjoint_set


def synonym_queries(synonym_words, queries):
    """
    will ensure that all synonyms and queries are put to lower case so comparisons work
    pre-processing words into a disjoint set will allow fastest look up and can confirm if they are synonyms if they have the same root
    """
    synonyms = preprocess_synonyms(synonym_words)

    output = []
    for query1, query2 in queries:
        query1, query2 = query1.split(), query2.split()
        if len(query1) != len(query2):
            output.append("different")
            continue
        result = "synonyms"
        for i in range(len(query1)):
            word1, word2 = query1[i].lower(), query2[i].lower()
            if word1 == word2:
                continue
            elif synonyms.are_synonymous(word1, word2):
                continue
            result = "different"
            break
        output.append(result)
    return output


if __name__ == "__main__":
    ## TODO change to take input from argvars for file names
    f = open("./inputs/test.in.json")
    data = json.load(f)
    # print(json.dumps(data)) # for debugging only
    with open("./outputs/test.out.txt", "w") as w:
        ## Take the input and make the output
        for testCase in data.get("testCases"):
            result = synonym_queries(
                testCase.get("dictionary"), testCase.get("queries")
            )
            w.write("\n".join(result))
            w.write("\n")
            # print(result) # for debugging only
