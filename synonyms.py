import json


class DisjointSet(object):
    def __init__(self):
        self.parents = {}

    def get_root(self, w):
        words_traversed = []
        while w in self.parents and self.parents[w] != w:
            words_traversed.append(w)
            w = self.parents[w]
        for word in words_traversed:
            self.parents[word] = w
        return w

    def add_synonyms(self, w1, w2):
        if w1 not in self.parents:
            self.parents[w1] = w1
        if w2 not in self.parents:
            self.parents[w2] = w2

        w1_root = self.get_root(w1)
        w2_root = self.get_root(w2)
        if w1_root < w2_root:
            w1_root, w2_root = w2_root, w1_root
        self.parents[w2_root] = w1_root

    def are_synonymous(self, w1, w2):
        r1 = self.get_root(w1)
        r2 = self.get_root(w2)
        print(f"r1 {r1}, r2 {r2}")
        return r1 == r2


def preprocess_synonyms(synonym_words):
    ds = DisjointSet()
    for w1, w2 in synonym_words:
        ds.add_synonyms(w1.lower(), w2.lower())
    return ds


def synonym_queries(synonym_words, queries):
    """
    will ensure that all synonyms and queries are put to lower case so comparisons work
    pre-processing words into a disjoint set will allow fastest look up and can confirm if they are synonyms if they have the same root
    """
    synonyms = preprocess_synonyms(synonym_words)

    output = []
    for q1, q2 in queries:
        q1, q2 = q1.split(), q2.split()
        if len(q1) != len(q2):
            output.append("different")
            continue
        result = "synonyms"
        for i in range(len(q1)):
            w1, w2 = q1[i].lower(), q2[i].lower()
            if w1 == w2:
                continue
            elif synonyms.are_synonymous(w1, w2):
                continue
            result = "different"
            break
        output.append(result)
    return output


if __name__ == "__main__":
    ## TODO change to take input from argvars for file names
    f = open("./inputs/example.in.json")
    expected_output = open("./outputs/example.out")
    data = json.load(f)
    print(json.dumps(data))
    with open("./outputs/example.txt", "w") as w:
        ## Take the input and make the output
        for testCase in data.get("testCases"):
            result = synonym_queries(
                testCase.get("dictionary"), testCase.get("queries")
            )
            w.write("\n".join(result))
            w.write("\n")
            print(result)
        f = open("./inputs/example_big.in.json")
    expected_output = open("./outputs/example_big.out")
    data = json.load(f)
    print(json.dumps(data))
    with open("./outputs/example_big.txt", "w") as w:
        ## Take the input and make the output
        for testCase in data.get("testCases"):
            result = synonym_queries(
                testCase.get("dictionary"), testCase.get("queries")
            )
            w.write("\n".join(result))
            w.write("\n")
            print(result)
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
