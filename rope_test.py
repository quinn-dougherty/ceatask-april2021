from rope import (
    Rope,
    prepend,
    append,
    delete_range,
    insert,
    create_rope_from_map,
    rotate_left,
    rotate_right,
    rebalance,
    split_at_naive,
    fmap_rope,
    insert_naive,
    delete_range_naive,
)
import unittest

# These tests are here as a starting point, they are not comprehensive
class Testing(unittest.TestCase):
    def test_rope_basics(self):
        self.assertEqual(Rope("test").to_string(), "test")
        self.assertEqual(prepend(Rope("test"), "abc").to_string(), "abctest")
        self.assertEqual(append(Rope("test"), "abc").to_string(), "testabc")

    def test_deletion_naive(self):
        self.assertEqual(delete_range_naive(Rope("test"), 1, 2).to_string(), "tst")
        self.assertEqual(delete_range_naive(Rope("test"), 2, 4).to_string(), "te")
        self.assertEqual(delete_range_naive(Rope("test"), 0, 2).to_string(), "st")

    def test_insertion_naive(self):
        self.assertEqual(insert_naive(Rope("test"), "123", 2).to_string(), "te123st")
        self.assertEqual(insert_naive(Rope("test"), "123", 4).to_string(), "test123")
        self.assertEqual(insert_naive(Rope("test"), "123", 0).to_string(), "123test")

    def test_deletion(self):
        self.assertEqual(delete_range(Rope("test"), 1, 2).to_string(), "tst")
        self.assertEqual(delete_range(Rope("test"), 2, 4).to_string(), "te")
        self.assertEqual(delete_range(Rope("test"), 0, 2).to_string(), "st")

    def test_insertion(self):
        self.assertEqual(insert(Rope("test"), "123", 2).to_string(), "te123st")
        self.assertEqual(insert(Rope("test"), "123", 4).to_string(), "test123")
        self.assertEqual(insert(Rope("test"), "123", 0).to_string(), "123test")

    def test_split_at_naive(self):
        test = Rope("test")
        self.assertEqual(split_at_naive(test, 2), (Rope("te"), Rope("st")))

    def test_fmap_rope(self):
        test = create_rope_from_map(
            {
                "text": "3",
                "left": {"text": "a"},
                "right": {
                    "text": "5",
                    "left": {"text": "b"},
                    "right": {
                        "text": "7",
                        "left": {"text": "c"},
                        "right": {"text": "d"},
                    },
                },
            }
        )
        test_upper = create_rope_from_map(
            {
                "text": "3",
                "left": {"text": "A"},
                "right": {
                    "text": "5",
                    "left": {"text": "B"},
                    "right": {
                        "text": "7",
                        "left": {"text": "C"},
                        "right": {"text": "D"},
                    },
                },
            }
        )
        self.assertEqual(fmap_rope(lambda s: s.upper(), test), test_upper)

    def test_extra_credit_rebalancing(self):
        self.assertEqual(
            rotate_left(
                create_rope_from_map(
                    {
                        "text": "3",
                        "left": {"text": "a"},
                        "right": {
                            "text": "5",
                            "left": {"text": "b"},
                            "right": {
                                "text": "7",
                                "left": {"text": "c"},
                                "right": {"text": "d"},
                            },
                        },
                    }
                )
            ).to_dictionary(),
            {
                "text": "5",
                "left": {"text": "3", "left": {"text": "a"}, "right": {"text": "b"}},
                "right": {"text": "7", "left": {"text": "c"}, "right": {"text": "d"}},
            },
        )
        self.assertEqual(
            rotate_right(
                create_rope_from_map(
                    {
                        "text": "5",
                        "left": {
                            "text": "3",
                            "right": {"text": "b"},
                            "left": {
                                "text": "2",
                                "left": {"text": "d"},
                                "right": {"text": "c"},
                            },
                        },
                        "right": {"text": "a"},
                    }
                )
            ).to_dictionary(),
            {
                "text": "3",
                "left": {"text": "2", "left": {"text": "d"}, "right": {"text": "c"}},
                "right": {"text": "5", "left": {"text": "b"}, "right": {"text": "a"}},
            },
        )

        balancedTree = {"text": "b", "left": {"text": "a"}, "right": {"text": "c"}}

        self.assertEqual(
            rebalance(
                create_rope_from_map(
                    {"text": "c", "left": {"text": "a", "right": {"text": "b"}},}
                )
            ).to_dictionary(),
            balancedTree,
        )
        self.assertEqual(
            rebalance(
                create_rope_from_map(
                    {"text": "c", "left": {"text": "b", "left": {"text": "a"}},}
                )
            ).to_dictionary(),
            balancedTree,
        )
        self.assertEqual(
            rebalance(
                create_rope_from_map(
                    {"text": "a", "right": {"text": "b", "right": {"text": "c"}},}
                )
            ).to_dictionary(),
            balancedTree,
        )
        self.assertEqual(
            rebalance(
                create_rope_from_map(
                    {"text": "a", "right": {"text": "c", "left": {"text": "b"}},}
                )
            ).to_dictionary(),
            balancedTree,
        )


if __name__ == "__main__":
    unittest.main()
