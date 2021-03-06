import unittest

from human_name_compare import match_name

name_sets = [
    "Robert Schönthal",
    "Robert R. Schönthal",
    "Robert R Schönthal",
    "Robert R Peter Schönthal",
    "R. Schönthal",
    "R Schönthal",
    "Robert Robert Schönthal"
]

no_sets = [
    "Robert Müller",
    "Peter Schönthal",
]


class CompareTestCase(unittest.TestCase):

    def test_names(self):
        self.assertTrue(match_name('Dr. med. Claudius Gall, Bac. phil. MBA', 'Claudius Gall'))
        self.assertFalse(match_name('Martin Auer', 'Martin Bauer'))
        self.assertTrue(match_name('Martin Drewes', 'Martin J Drewes'))
        self.assertTrue(match_name('Dagmar Fuhrer', 'Dagmar Führer-Sakel'))
        self.assertTrue(match_name('Ch Grohé', 'Christian Grohé'))
        self.assertTrue(match_name('Young Jun Kim', 'Youngjun Kim'))
        self.assertTrue(match_name('T Majic', 'Tomislav Maji'))
        self.assertTrue(match_name('Susan Kralisch', 'Susann Kralisch'))
        self.assertTrue(match_name('Sara Kammerer', 'Sarah Kammerer'))
        self.assertFalse(match_name('Bernhard König','Burkhard König'))
        self.assertFalse(match_name('Uwe Töpfer', 'Udo Töpfer'))
        self.assertFalse(match_name('Maria-Christina Jung', 'Carin Jung'))
        self.assertTrue(match_name('Darius Schlemmer', 'Dariusz Schlemmer'))
        self.assertTrue(match_name('Horst von Schlemmer', 'Horst Schlemmer'))
        self.assertTrue(match_name('Horst-Eugen Schlemmer', 'HORST SCHLEMMER'))
        self.assertTrue(match_name('Horst-Eugen Schlemmer', 'Horst Eugen Schlemmer'))
        self.assertTrue(match_name('Horst E. Schlemmer', 'Horst Eugen Schlemmer'))
        self.assertFalse(match_name('Horst E. Schlemmer', 'Horst Klaus Schlemmer'))
        self.assertTrue(match_name('Jörn Müller', 'Joern Mueller'))
        self.assertTrue(match_name('Andrè Müller', 'Andre Mueller'))
        self.assertTrue(match_name('H.-Eberhard Börngen', 'Horst E Börngen'))
        self.assertFalse(match_name('Lutz König', 'Lars König'))
        self.assertFalse(match_name('Kerstin König', 'Kristin König'))

        for n in name_sets:
            for on in name_sets:
                self.assertTrue(match_name(n, on), "{} matches on {}".format(n, on))

    def test_names_no_matches(self):
        for n in name_sets:
            for on in no_sets:
                self.assertFalse(match_name(n, on), "{} must not match {}".format(n, on))

    def test_split_medic_names(self):
        name = "Victor-Felix Hugo Mauthner"
        expected = ['%Mauthner',
                    'Victor% Mauthner',
                    'V% Mauthner',
                    'Victor% Felix% Mauthner',
                    'Victor% F% Mauthner',
                    'V% F% Mauthner',
                    'Victor% Felix% Hugo% Mauthner',
                    'Victor% Felix% H% Mauthner',
                    'Victor% F% Hugo% Mauthner',
                    'Victor% F% H% Mauthner',
                    'V% F% Hugo% Mauthner',
                    'V% F% H% Mauthner'
                    ]

        for n in expected:
            self.assertTrue(match_name(name, n.replace('%', '')), n)


if __name__ == '__main__':
    unittest.main()
