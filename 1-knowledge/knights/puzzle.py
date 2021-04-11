from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# 1// either a knight or a knave, not both

# 2// sentence spoken by a knight is true, by a knave is false

# 3// For each KB, encode two different types of information: 
#   (1) information about the structure of the problem itself (i.e., information given in the definition of a Knight and Knave puzzle), 
#   (2) information about what the characters actually said

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    Or(AKnight, AKnave),
    Or(Implication(AKnight, Not(AKnave)), Implication(AKnave, Not(AKnight))),
    Biconditional(AKnight, And(AKnight, AKnave))
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    Or(AKnight, AKnave),
    Or(Implication(AKnight, Not(AKnave)), Implication(AKnave, Not(AKnight))),
    Or(BKnight, BKnave),
    Or(Implication(BKnight, Not(BKnave)), Implication(BKnave, Not(BKnight))),
    Biconditional(AKnight, And(AKnave, BKnave)) # if he tells the truth
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    Or(AKnight, AKnave),
    Or(Implication(AKnight, Not(AKnave)), Implication(AKnave, Not(AKnight))),
    Or(BKnight, BKnave),
    Or(Implication(BKnight, Not(BKnave)), Implication(BKnave, Not(BKnight))),
    Biconditional(AKnight, Or(And(AKnight, BKnight), And(AKnave, BKnave))), # if A tells the truth
    Biconditional(BKnight, Or(And(AKnight, BKnave), And(AKnave, BKnight))) # if B tells the truth
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    Or(AKnight, AKnave),
    Or(Implication(AKnight, Not(AKnave)), Implication(AKnave, Not(AKnight))),
    Or(BKnight, BKnave),
    Or(Implication(BKnight, Not(BKnave)), Implication(BKnave, Not(BKnight))),
    Or(CKnight, CKnave),
    Or(Implication(CKnight, Not(CKnave)), Implication(CKnave, Not(CKnight))),

    Biconditional(Or(AKnight, AKnight), Or(AKnight, AKnave)),
    Biconditional(BKnight, AKnave),
    Biconditional(BKnight, CKnave),
    Biconditional(CKnight, AKnight),
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
