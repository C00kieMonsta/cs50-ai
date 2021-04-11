from minesweeper import Minesweeper, MinesweeperAI, Sentence

knowledge = []

knowledge.append(Sentence(['A', 'B', 'C', 'D', 'E'], 2))
knowledge.append(Sentence(['A', 'B', 'C'], 1))

inferred_sentences = []

for set1 in knowledge:
    for set2 in knowledge:
        if set2 != set1 and set2.cells.issubset(set1.cells):
            inferred_sentences.append(
                Sentence(set1.cells - set2.cells, set1.count - set2.count)
            )
knowledge.append(*inferred_sentences)
print(knowledge)
