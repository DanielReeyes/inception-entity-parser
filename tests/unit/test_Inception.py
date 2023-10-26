from unittest import TestCase
from src.Parser.Inception import Inception

class TestInception(TestCase):
    def setUp(self) -> None:
        self.cInception = Inception(filename="Portalegre_Urra.normalisadaRevista")

class TestInception2(TestCase):
    def setUp(self) -> None:
        self.cInception = Inception(filename="InvalidFile")

class TestLoadNotations(TestInception):

    def test_load_notations(self):
        self.assertEqual(len(self.cInception.load_notations()), 870)

class TestLoadNotationsNoFile(TestInception2):

    def test_load_notations_no_file(self):
        self.assertEqual(self.cInception.load_notations(), None)

class TestOrderEntityWordsByIndex(TestInception):
    def test_order_entity_words_by_index(self):
        df = self.cInception.load_notations()
        df = df[df['category_entity'] != '_']

        self.assertEqual(
            len(self.cInception.order_entity_words_by_index(df)),
            98
        )

class TestConcatenateWordEntity(TestInception):
    def test_concatenate_word_entity(self):
        df = self.cInception.load_notations()
        df = df[df['category_entity'] != '_']
        df = self.cInception.order_entity_words_by_index(df)

        self.assertEqual(
            len(self.cInception.concatenate_word_entity(df)),
            30
        )