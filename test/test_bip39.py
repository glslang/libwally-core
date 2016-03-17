import unittest
from binascii import unhexlify
import json
import util
from ctypes import create_string_buffer



class BIP39Tests(unittest.TestCase):

    cases = None

    def setUp(self):
        if self.cases is None:
            with open('data/wordlists/vectors.json', 'r') as f:
                self.cases = json.load(f)["english"]

            util.bind_all(self, util.bip39_funcs + util.wordlist_funcs)
            langs = ['en', 'es', 'fr', 'it', 'jp']
            gwl = lambda lang: self.bip39_get_wordlist(lang)
            self.wordlists = {lang: gwl(lang) for lang in langs}


    def test_bip39_wordlists(self):

        for lang, wl in self.wordlists.iteritems():
            self.assertIsNotNone(wl)

        self.assertEqual(self.bip39_default_wordlist(),
                         self.wordlists['en'])


    def test_accented_lookups(self):

        wl = self.wordlists['fr']
        words_list, _ = util.load_words('french')

        for i in range(2048):
            word = self.wordlist_lookup_index(wl, i)
            self.assertEqual(word, words_list[i])
            idx = self.wordlist_lookup_word(wl, word)
            self.assertEqual(i, idx - 1)


    def test_bip39(self):

        wl = self.bip39_default_wordlist()

        for case in self.cases:
            hex_input, mnemonic = case[0], case[1]
            hex_len = len(hex_input) / 2

            buf = create_string_buffer(unhexlify(hex_input), hex_len)
            result = self.bip39_mnemonic_from_bytes(wl, buf, hex_len)
            self.assertEqual(result, mnemonic)


if __name__ == '__main__':
    unittest.main()