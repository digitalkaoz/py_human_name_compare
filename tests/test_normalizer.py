import unittest

from human_name_compare import person_name, person_title

NAMES = {
    "Alexander Schwarzenböck ab 01.04.2018": ["male", False, False, None, "Alexander Schwarzenböck"],
    "Alexander Schwarzenböck seit 01.04.2018": ["male", False, False, None, "Alexander Schwarzenböck"],
    "Dr. Peter Greulich bis 07.2019; ab 01.08.2019 Fr. Dr. med. Lioba Essen": ["male", False, True, "Dr.",
                                                                               "Peter Greulich"],
    "Dr. med. Thomas Rösel M.A.": ["male", False, True, "M.A. Dr. med.", "Thomas Rösel"],
    "Dr. med. Juergen Graf": ["male", False, True, "Dr. med.", "Juergen Graf"],
    "Dipl. - Med. Heide-Marie Vieweg": ["female", False, False, "Dipl. Med.", "Heide Marie Vieweg"],
    "Ford Cheikh Baker": ["unknown", False, False, None, "Ford Cheikh Baker"],
    "Herr dr. med. / Universität Zagreb Erwin Pape": ["male", False, True, "Dr. med. Univ.", "Erwin Pape"],
    "Frau dr/Universität Belgrad Dejana Matejic": ["female", False, True, "Dr. Univ.", "Dejana Matejic"],
    "Dr. med. Mootaz Shousha, Ph.D. (Univ. Alexandria)": ["unknown", False, True, "Ph.D. Dr. med.", "Mootaz Shousha"],
    "Univ.-Prof. Dr. med. Nikolaus Gaßler, M.A.": ["male", True, True, "M.A. Univ.Prof. Dr. med.", "Nikolaus Gaßler"],
    "Dr. med. Alexander Unger, M.Sc.": ["male", False, True, "M.Sc. Dr. med.", "Alexander Unger"],
    "Dr. med. Heiko Graf": ["male", False, True, "Dr. med.", "Heiko Graf"],
    "Herr Dr. med. Peter Velling": ["male", False, True, "Dr. med.", "Peter Velling"],
    "Apl. Prof. Dr. med. Dr. med. dent. Peter Velling": ["male", True, True, "Apl. Prof. Dr. med. Dr. med. dent.",
                                                         "Peter Velling"],
    "Dr. med. Peter Velling": ["male", False, True, "Dr. med.", "Peter Velling"],
    "Peter Velling": ["male", False, False, None, "Peter Velling"],
    "Prof. (FH) Dr. med. Peter Velling": ["male", True, True, "Prof. Dr. med.", "Peter Velling"],
    "Dr./Univ.Zagreb Peter Velling": ["male", False, True, "Dr. Univ.Zagreb", "Peter Velling"],
    "Dr. med. (Yu) Dr. (Yu) Peter Velling": ["male", False, True, "Dr. med. Dr.", "Peter Velling"],
    "Peter Velling (bis 30.11.2017)": ["male", False, False, None, "Peter Velling"],
    "Peter Velling, MBA": ["male", False, False, "MBA", "Peter Velling"],
    "Prof. med. Peter Velling": ["male", True, True, "Prof. med.", "Peter Velling"],
    "PMU Dr. med. Dipl.-Psych. Univ. Peter Velling": ["male", False, True, "PMU Dr. med. Dipl.Psych. Univ.",
                                                      "Peter Velling"],
    "a.o. Universitätsprof. /Wien Dr. med. Peter Velling": ["male", True, True, "a.o. Prof. Univ. Wien Dr. med.",
                                                            "Peter Velling"],
    "Prof. Dr. med. Dr. rer. nat. Peter Velling": ["male", True, True, "Prof. Dr. med. Dr. rer. nat.", "Peter Velling"],
    "OFA Priv.-Doz. Dr. med. Dr. med. dent. Peter Velling": ["male", True, True, "OFA PD Dr. med. Dr. med. dent.",
                                                             "Peter Velling"],
    "Prof. apl. Dr. med. Dr. med. dent. Peter Velling": ["male", True, True, "Prof. apl. Dr. med. Dr. med. dent.",
                                                         "Peter Velling"],
    "Dr.med. Dr.med. Peter Velling": ["male", False, True, "Dr.med. Dr.med.", "Peter Velling"],
    "Professor Dr.med. Peter Velling": ["male", True, True, "Prof. Dr.med.", "Peter Velling"],
    "Doctor medic. Peter Velling": ["male", False, True, "Dr. med.", "Peter Velling"],
    "Univ.Prof.Dr.med.Dr.med.dent. Peter Velling": ["male", True, True, "Univ.Prof.Dr.med.Dr.med.dent.",
                                                    "Peter Velling"],
    "Univ. -Prof. Dr. med. Dr. med. dent. Peter Velling": ["male", True, True, "Univ. Prof. Dr. med. Dr. med. dent.",
                                                           "Peter Velling"],
    "AO Univ. Prof. Innsbruck Dr. med.univ. Peter Velling": ["male", True, True,
                                                             "AO Univ. Prof. Innsbruck Dr. med.univ.",
                                                             "Peter Velling"],
    "Priv. -Doz. Dr. med. Peter Velling": ["male", True, True, "PD Dr. med.", "Peter Velling"],
    "Frau Dr. med. Anna Röcken": ["female", False, True, "Dr. med.", "Anna Röcken"],
    "Dr. med. Anna Röcken": ["female", False, True, "Dr. med.", "Anna Röcken"],
    "Anna Röcken": ["female", False, False, None, "Anna Röcken"],
    "Dipl. - Med. Anna Röcken": ["female", False, False, "Dipl. Med.", "Anna Röcken"],
    "Dr. rer. nat. Anna Röcken": ["female", False, True, "Dr. rer. nat.", "Anna Röcken"],
    "Apl.-Prof. Dr. med. Anna Röcken": ["female", True, True, "Apl.Prof. Dr. med.", "Anna Röcken"],
    "Dr. med. Dipl. oec. troph. Univ. Anna Röcken": ["female", False, True, "Dr. med. Dipl. oec. troph. Univ.",
                                                     "Anna Röcken"],
    "Dr. med. Anna Amalia Elisabeth Röcken": ["female", False, True, "Dr. med.",
                                              "Anna Amalia Elisabeth Röcken"],
    "Dr. med. Anna A. B. Röcken": ["female", False, True, "Dr. med.",
                                   "Anna A. B. Röcken"],
    "": ["unknown", False, False, None, None],
}


class NormalizerTestCase(unittest.TestCase):

    def test_title(self):
        self.assertEqual("M.D. Ph.D. Prof.", person_title("Prof. Michael Andrew Borger, M.D. (Alberta), Ph.D."))
        for k, values in NAMES.items():
            self.assertEqual(values[3], person_title(k), k)

    def test_name(self):
        self.assertEqual("Günter Lauer", person_name("Prof.Dr.med. Dr. med. dent. Günter Lauer"))
        for k, values in NAMES.items():
            self.assertEqual(values[4], person_name(k), k)


if __name__ == '__main__':
    unittest.main()
