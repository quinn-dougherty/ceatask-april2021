from typing import Tuple, Callable


class Rope:
    def __init__(self, text):
        self.text = text
        self.size = len(text)
        self.left = None
        self.right = None

    def __eq__(self, other) -> bool:
        return all(
            (
                self.text == other.text,
                self.size == other.size,
                self.left == other.left,
                self.right == other.right,
            )
        )

    # prints contents including showing the hierarchy
    # it's not required for this function to work, it's just there to help with debugging
    #
    # e.g. if the  root node has ABC, the left node has DEF, and the right node has GHI,
    # the output will look like:
    # -DEF
    # ABC
    # -GHI
    def to_string_debug(self, indentLevel=0):
        leftText = self.left.to_string_debug(indentLevel + 1) if self.left else ""
        rightText = self.right.to_string_debug(indentLevel + 1) if self.right else ""
        return leftText + ("-" * indentLevel) + self.text + "\n" + rightText

    # just prints the stored text
    def to_string(self):
        leftText = self.left.to_string() if self.left else ""
        rightText = self.right.to_string() if self.right else ""
        return leftText + self.text + rightText

    # How long the text stored is in all of the children combined
    # This is the same as this.to_string().length
    def total_size(self) -> int:
        leftText = self.left.total_size() if self.left else 0
        rightText = self.right.total_size() if self.right else 0
        return leftText + len(self.text) + rightText

    # how deep the tree is (I.e. the maximum depth of children)
    def depth(self) -> int:
        return 1 + max(self.left_depth(), self.right_depth())

    # Whether the rope is balanced, i.e. whether any subtrees have branches
    # which differ by more than one in depth.
    def is_balanced(self) -> bool:
        leftBalanced = self.left.is_balanced() if self.left else True
        rightBalanced = self.right.is_balanced() if self.right else True

        return (
            leftBalanced
            and rightBalanced
            and abs(self.left_depth() - self.right_depth()) < 2
        )

    def left_depth(self) -> int:
        if not self.left:
            return 0
        return self.left.depth()

    def right_depth(self) -> int:
        if not self.right:
            return 0
        return self.right.depth()

    # Helper method which converts the rope into an associative array
    #
    # Only used for debugging, this has no functional purpose
    def to_dictionary(self):
        mapVersion = {"text": self.text}
        if self.right:
            mapVersion["right"] = self.right.to_dictionary()
        if self.left:
            mapVersion["left"] = self.left.to_dictionary()
        return mapVersion


def create_rope_from_map(map):
    rope = Rope(map["text"])
    if "left" in map and map["left"] is not None:
        if isinstance(map["left"], Rope):
            rope.left = map["left"]
        else:
            rope.left = create_rope_from_map(map["left"])
    if "right" in map and map["right"] is not None:
        if isinstance(map["right"], Rope):
            rope.right = map["right"]
        else:
            rope.right = create_rope_from_map(map["right"])
    return rope


def prepend(rope, text):
    if rope.left:
        prepend(rope.left, text)
    else:
        rope.left = Rope(text)

    return rope


def append(rope, text):
    if rope.right:
        append(rope.right, text)
    else:
        rope.right = Rope(text)

    return rope


def fmap_rope(f: Callable[[str], str], rope: Rope) -> Rope:
    if rope is None:
        return rope

    return create_rope_from_map(
        {
            "text": f(rope.text),
            "left": fmap_rope(f, rope.left) if rope.left else None,
            "right": fmap_rope(f, rope.right) if rope.right else None,
        }
    )


def concat_right(rope: Rope, other: Rope) -> Rope:
    if rope.right is not None:
        concat_right(rope.right, other)
    else:
        rope.right = other
    return rope


def concat2(rope: Rope, other: Rope) -> Rope:
    new_rope = Rope("")
    new_rope.left = rope
    new_rope.right = other
    return new_rope


# This is an internal API. You can implement it however you want.
# (E.g. you can choose to mutate the input rope or not)
def split_at_naive(rope: Rope, position: int) -> Tuple[Rope, Rope]:
    """First iteration: kills structure of rope, always returns a 3-node rope.
    see JOURNAL.md for discussion
    """
    text = rope.to_string()
    length = rope.total_size()
    assert position <= length, "position requested is larger than total length of rope"
    new_left = Rope(text[:position])
    right = Rope(text[position:])
    return (new_left, right)


def delete_range_naive(rope: Rope, start: int, end: int) -> Rope:
    left, _ = split_at_naive(rope, start)
    _, right = split_at_naive(rope, end)
    return concat2(left, right)


def insert_naive(rope: Rope, text: str, location: int) -> Rope:
    left, right = split_at_naive(rope, location)
    new_rope = Rope(text)
    new_rope.left = left
    new_rope.right = right
    return new_rope


def split_at(rope: Rope, position: int) -> Tuple[Rope, Rope]:
    """We need to descend into the tree comparing position to length.

    PASSING TEST BUT THE TEST CASES ARE NOT THOROUGH ENOUGH.
    I DO NOT IN THIS ITERATION HANDLE WHEN neither rope.left nor rope.right are None.
    """

    if rope.left is None:
        if rope.right is None:
            if position > rope.size:
                raise ValueError(f"Rope {rope} is not big enough to split at {position}.")
            return (Rope(rope.text[:position]), Rope(rope.text[position:]))
        if position >= rope.total_size():
            raise ValueError(f"Rope {rope} is not big enough to split at {position}.")
        # rope.right is not None and rope.left is None
        if position > rope.size:
            return split_at(rope.right, position - rope.size)
        return (Rope(rope.text[:position]), concat2(Rope(rope.text[position:]), rope.right))
    # rope.left is not None
    if rope.right is None:
        if position >= rope.total_size():
            raise ValueError(f"Rope {rope} is not big enough to split at {position}.")
        if position >= rope.total_size() - rope.size:
            # then then position is in the middle of rope.text
            position -= rope.total_size() - rope.size
            return (
                concat2(rope.left, Rope(rope.text[:position])),
                Rope(rope.text[position:])
            )
        # position < rope.total_size() - rope.size
        return split_at(rope.left, position)
    # neither rope.left nor rope.right are None
    if position >= rope.total_size():
        raise ValueError(f"Rope {rope} is not big enough to split at {position}.")
    # ...

def delete_range(rope: Rope, start: int, end: int) -> Rope:
    left, _ = split_at(rope, start)
    _, right = split_at(rope, end)
    return concat2(left, right)


def insert(rope: Rope, text: str, location: int) -> Rope:
    left, right = split_at(rope, location)
    new_rope = Rope(text)
    new_rope.left = left
    new_rope.right = right
    return new_rope


def rebalance(rope):
    if not rope:
        return rope
    while not rope.is_balanced():
        right_depth = rope.right_depth()
        left_depth = rope.left_depth()

        if left_depth > right_depth:
            rotate_right(rope)
        elif left_depth < right_depth:
            rotate_left(rope)
        else:
            rebalance(rope.left)
            rebalance(rope.right)
    return rope


"""
 Rotates a tree: used for rebalancing.

 Turns:
    b
  /  \
  a   c

  Into:
     c
    /
   b
  /
a
"""


def rotate_left(rope):
    """This can break if rope.right is None"""
    newParent = rope.right
    newLeft = rope
    newLeft.right = newParent.left
    newParent.left = newLeft
    return newParent


"""
/*
 Rotates a tree: used for rebalancing.

 Turns:
    b
  /  \
  a   c

  Into:
     a
      \
       b
        \
         c 
"""


def rotate_right(rope):
    """This can break if rope.left is None"""
    newParent = rope.left
    newRight = rope
    newRight.left = newParent.right
    newParent.right = newRight
    return newParent
