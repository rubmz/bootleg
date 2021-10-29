"""Test class utils."""
import tempfile
import unittest

from bootleg.end2end.annotator_utils import DownloadProgressBar
from bootleg.utils.classes.vocab_trie import VocabularyTrie
from bootleg.utils.classes.vocabularypairedlist_trie import VocabularyPairedListTrie


class UtilClasses(unittest.TestCase):
    """Class util test."""

    def test_vocab_trie(self):
        """Test vocab trie."""
        input_dict = {"a": 2, "b": 3, "c": -1}
        tri = VocabularyTrie(input_dict=input_dict)

        self.assertDictEqual(tri.to_dict(), input_dict)
        self.assertEqual(tri["b"], 3)
        self.assertEqual(tri["c"], -1)
        self.assertEqual(tri.get_key(-1), "c")
        self.assertEqual(tri.get_key(2), "a")
        self.assertTrue(tri.is_key_in_trie("b"))
        self.assertFalse(tri.is_key_in_trie("f"))
        self.assertTrue("b" in tri)
        self.assertTrue("f" not in tri)
        self.assertTrue(tri.is_value_in_trie(-1))
        self.assertFalse(tri.is_value_in_trie(6))
        self.assertEqual(tri.get_max_id(), 3)
        self.assertEqual(len(tri), 3)

        save_path = tempfile.TemporaryDirectory()
        tri.dump(save_path.name)
        tri2 = VocabularyTrie(load_dir=save_path.name)
        self.assertDictEqual(tri.to_dict(), input_dict)
        self.assertEqual(tri2["b"], 3)
        self.assertEqual(tri2["c"], -1)
        self.assertEqual(tri2.get_key(-1), "c")
        self.assertEqual(tri2.get_key(2), "a")
        self.assertTrue(tri2.is_key_in_trie("b"))
        self.assertFalse(tri2.is_key_in_trie("f"))
        self.assertTrue("b" in tri2)
        self.assertTrue("f" not in tri2)
        self.assertTrue(tri2.is_value_in_trie(-1))
        self.assertFalse(tri2.is_value_in_trie(6))
        self.assertEqual(tri2.get_max_id(), 3)
        self.assertEqual(len(tri2), 3)

        save_path.cleanup()

    def test_paired_vocab_trie(self):
        """Test paired vocab trie."""
        for with_scores in [True, False]:
            raw_input_dict = {"a": ["1", "4", "5"], "b": ["5", "2"], "c": []}
            vocabulary = {"1": 1, "2": 2, "4": 3, "5": 4}
            input_dict = {}
            score = 1.0 if with_scores else 0.0
            for k, lst in list(raw_input_dict.items()):
                input_dict[k] = [[it, score] for it in lst]

            if with_scores:
                tri = VocabularyPairedListTrie(
                    input_dict=input_dict, vocabulary=vocabulary, max_value=3
                )
            else:
                tri = VocabularyPairedListTrie(
                    input_dict=raw_input_dict, vocabulary=vocabulary, max_value=3
                )

            self.assertDictEqual(tri.to_dict(keep_score=True), input_dict)
            self.assertDictEqual(tri.to_dict(keep_score=False), raw_input_dict)
            self.assertEqual(tri.get_value("b"), [["5", score], ["2", score]])
            self.assertTrue(tri.is_key_in_trie("b"))
            self.assertFalse(tri.is_key_in_trie("f"))
            self.assertSetEqual(set(input_dict.keys()), set(tri.keys()))
            self.assertSetEqual(set(vocabulary.keys()), set(tri.vocab_keys()))

            save_path = tempfile.TemporaryDirectory()
            tri.dump(save_path.name)
            tri2 = VocabularyPairedListTrie(load_dir=save_path.name)

            self.assertDictEqual(tri2.to_dict(keep_score=True), input_dict)
            self.assertDictEqual(tri2.to_dict(keep_score=False), raw_input_dict)
            self.assertEqual(tri2.get_value("b"), [["5", score], ["2", score]])
            self.assertTrue(tri2.is_key_in_trie("b"))
            self.assertFalse(tri2.is_key_in_trie("f"))
            self.assertSetEqual(set(input_dict.keys()), set(tri2.keys()))
            self.assertSetEqual(set(vocabulary.keys()), set(tri2.vocab_keys()))

            save_path.cleanup()

    def test_download_progress_bar(self):
        """Test download progress bar."""
        pbar = DownloadProgressBar()
        pbar(1, 5, 10)
        assert pbar.pbar is not None
