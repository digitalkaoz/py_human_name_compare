import re
import unicodedata
from typing import Optional, List

import gender_guesser.detector as gender
from Levenshtein import distance
from nameparser import HumanName
from nameparser.config import Constants

_additional_titles = ["med.", "Dipl.", "Psych.", "Apl.", "Ass.", "rer.", "nat.", "phil.", "univ.", "Priv.", "Doz.",
                      "PD", "Prof. (FH)", "Dott.", "MUDr.", "MU", "habil.", "Dr./Univ.", "Dott./Univ.", "Doctor-medic",
                      "Med.", "sc.", "medic.", "dent.", "AO", "a.o.", "OFA", "oec.", "troph.", "Doctor-medic",
                      "Honorarprof.", "Doctor-medic/Univ.", "Universitätsprof.", "Phys.", "PMU", "Dipl.-Psych.",
                      "chem.", "Biol.", "Ph.D.", "hom.", "disc.", "pol.", "M.B", "M.Sc.", "MSc", "MHBA",
                      "Honorarprofessorin", "PH", "M.A.", "Honorem/RCh", "Dr./TR", "Tip", "M.D./Afghanistan",
                      "M.B.CH.B", "Sanitätsrat", "dr/Universität", "-Ing.", "DrPH", "jur.", "Cirug./EC",
                      "professor/NGMU", "Ing.", "M.D./Ain", "Universität", "M.D./SYR", "EC", "pocetny", "vet.",
                      "DrM/Univ.", "Cirug.", "drs.", "h.c.", "d-r", "M. A.", "M. D./Univ.", "Diplom-Sozialwirt",
                      "B.Ch.", "M.B.", "scient.", "pth.", "Dipl.-Psych.","Bac.",
                      "D.O.", "DAAO", "Ch.B./Univ.", "HMA", "Diplom-Psychologe", "physiol.", "P.H.", "hab.", "M.B.B.S.",
                      "hum.", "M.D.", "/OAK", "vrac", "Diplom-Biologe", "dr/Univ.", "Docteur", "Médecine/Univ.",
                      "B.M.D.", "doktor", "medicine", "/Mediz.", "M.B.", "M.D./Univ.", "M.B.,B.Ch.(ET)", "M.S.P.",
                      "Conf.", "MScIH", "MaHM", "Medica", "MOM", "M.Sc.", "Profesor", "Honorario", "honorary", "Lic.",
                      "Assistant", "agr.", "soc.", "Privatdozent", "ZA.", "ZA", "dr./Uni.", "OA", "Doctor-Medic/IMF",
                      "Privat-Dozent", "MB", "ChB", "Duktur", "fi-t-tibb", "al-bashari", "Priv-Doz.", "I.N.E.S.S.",
                      "Stom.", "MS/Tufts", "ZÄ", "Dr./IMF", "B.D.S./Univ.", "D.D.S.", "/IMF", "Mag.", "LA", "CA", "MBA",
                      "Prim.", "mult.", "MAS", "Univ.-Prof.", "Assoz.-Prof.", "PD", "PhD", "MSc", "DM", "asoc.", "FEBO",
                      "Oradea", "Doc.", "Deptl.", "MB.Ch.B.", "OMR", "OMD", "Fachärztin", "D.A.L.M.", "DEAA", "jun.",
                      "Assistenzärztin", "Klinikdirektor", "Soz.", "M.B.A.", "FEAN", "FNCS", "IFAANS", "M.S.",
                      "Med.-Dir.", "Sportwiss.", "OTA", "a.D.", "medic/R", "B.S.", "M.B.", "Ch.B.", "D.A.L.M.", "MaHM",
                      "B.A.", "UIPA", "universae/Semmelweis", "Doktor-e-reste-ye", "dr.sc.", "VUB", "DoktoFru/Univ.",
                      "Doktor-i", "pezeski/Univ.", "medic/Univ.", "medicinae", "universae", "San.-Rat", "Medizinalrat",
                      "Dott/Univ.", "M.D./Univ.Damaskus", "Ped.", "/I.N.E.S.S.", "LL.M.", "Ltd.", "Doktor-e", "M.sc.",
                      "Lic./Univ.", "pezeski/Univ.", "Odessa/UdSSR", "Medizinaldirektor", "Doktore", "pezeski/",
                      "Diplom-Biologin", "/Univ.", "dr.sc.", "-Phys.", "Universitätsprofessor", "Dozent", "MoHM",
                      "Oberfeldarzt", "reste-ye", "Doktora-ye", "reshte-ye", "pezeshki", "Tg.-Mures", "Akademische",
                      "Direktorin", "Diplom-Sozialpädagogin", "M.P.H.", "postgrad.", "asociat/Univ.", "-medic/IMF",
                      "-medic/IMP", "San.", "-Rat", "-medic", "medic/IM", "-med.", "-medic/ifM", "Frf.", "Honprof.",
                      "Theol.", "MPH-HAM", "D.E.A.A.", "Frhr.", "Drs.", "FEBS"]

_surname_titles = ["Von ", "von ", "van ", "Van ", "dos ", "Dos "]

# some titles are actual names, the result would be None, therefore we remove some
_remove_title = ["mahdi", "graf", "singer", "lama", "pastor", "imam", "jun", "baba", "baron"]

constants = Constants()
for a in _additional_titles:
    constants.titles.add(a)
for a in _remove_title:
    constants.titles.remove(a)

guess_gender = gender.Detector()


def normalize_title(inp: str) -> Optional[str]:
    """
    normalizes medical titles
    """
    if type(inp) is not str:
        return None

    if inp.strip() == "":
        return None
    return inp.replace("dr/Universität", "Dr. Univ.") \
        .replace("Universitätsprofessor", "Prof. Univ.") \
        .replace("Universitätsprof.", "Prof. Univ.") \
        .replace("Univ. Doz.", "PD") \
        .replace("Universität", "Univ.") \
        .replace("Professor", "Prof.") \
        .replace("prof.", "Prof.") \
        .replace("doktor medicine", "Dr. med.") \
        .replace("Doktor", "Dr.") \
        .replace("Doctor", "Dr.") \
        .replace("dr.", "Dr.") \
        .replace("medic.", "med.") \
        .replace("Priv. -Doz.", "PD") \
        .replace("Priv-Doz.", "PD") \
        .replace("Privatdozent", "PD") \
        .replace("Privat - Dozent", "PD") \
        .replace("Priv.-Doz.", "PD") \
        .replace("Priv.Doz.", "PD") \
        .replace("Priv. Doz.", "PD") \
        .replace("PDDr.", "PD Dr.") \
        .replace("PD.", "PD") \
        .replace(" / ", " ") \
        .replace("./", ". ") \
        .replace(". /", ". ") \
        .replace(" - ", " ") \
        .replace(".-", ".") \
        .replace(". -", ". ") \
        .replace('Dr.med.', 'Dr. med.').replace('Dr', 'Dr.').replace('Prof', 'Prof.')\
        .replace('..', '.').replace('.','. ') \
        .replace("  ", " ") \
        .strip()


def person_title(inp: str, normalize=True) -> Optional[str]:
    """
    extract the medic title from "GENDER? TITLE? NAME" strings
    """
    if type(inp) is not str:
        return None

    if inp.strip() == "":
        return None
    inp = _remove_gender(inp)

    # fix titles at the end
    if "," not in inp:
        for t in _additional_titles:
            if inp.endswith(t):
                inp = inp.replace(" {}".format(t), " ,{}".format(t))

    while "," in inp:
        suffix = inp[inp.rindex(","):]
        inp = "{} {}".format(suffix[1:], inp[:inp.rindex(",")])

    inp = _clean_name(inp)

    # for t in additional_titles:
    #    inp = inp.replace(t, "{} ".format(t)).replace("  ", " ").strip()

    n = HumanName(str(inp), constants=constants)
    title = n.title
    t = title
    if t is not None and t != "":
        inp = inp.replace(t, "").strip()
        n = HumanName(inp, constants=constants)
        t = n.title
        if t is not None and t != "":
            title = "{} {}".format(title, t)

        # sometime we have "TITLE some_city TITLE name, but we need to check if its not really an name!
        n = HumanName(" ".join(inp.replace(title, "").strip().split(" ")[1:]).strip(), constants=constants)
        t = n.title
        if t is not None and t != "":
            city = inp.replace(title, "").strip().split(" ")[0]
            if guess_gender.get_gender(city) == 'unknown':
                title = "{} {} {}".format(title, city, t)

    if title is not None and normalize is True:
        title = normalize_title(title)

    return None if title is None or title.strip() == "" else title


def remove_title(inp: str) -> Optional[str]:
    """
    removes the academic title from a string so the real medic name persists
    Args:
        inp: the medic name with title

    Returns: only the medic name
    """
    if type(inp) is not str:
        return None

    if inp.strip() == "":
        return None

    title = person_title(inp, False)
    cleaned_title = person_title(inp)
    if title is not None:
        for t in title.split(" "):
            if len(t) == 1:
                t = " {} ".format(t)
            inp = inp.replace(t, "")
    if inp is None or inp.strip() == "":
        return None

    inp = _clean_name(inp).strip()
    # remove optional Univ. Belgrad (e.g.) prefix
    if cleaned_title is not None and cleaned_title.endswith("Univ."):
        parts = inp.split(" ")
        if "unknown" == guess_gender.get_gender(parts[0]):
            inp = " ".join(parts[1:])

    if inp.endswith(","):
        inp = inp[:-1]
    return inp


def _clean_name(inp: str) -> Optional[str]:
    """
    removes possible nicknames (FH) from the Person name
    """
    if inp is None:
        return None

    if ";" in inp:
        inp = inp[0:inp.index(";")]
    if "|" in inp:
        inp = inp[0:inp.index("|")]

    # remove optional suffixes like "bis 10.2019)
    inp = re.sub(r"\(?(bis|Bis|Ab|ab|Seit|seit) [\d]+.+$", "", inp)

    n = HumanName(str(inp), constants=constants)
    if n.nickname is not None:
        for nn in n.nickname_list:
            inp = inp.replace("({})".format(nn), "").replace("  ", " ")

    return inp.replace("/ ", " ").replace("  ", " ")


def _remove_gender(inp: str) -> Optional[str]:
    """
    removes gender Mann|Frau prefixes from the name
    """
    if inp is None:
        return None

    prefixes = ["Herr ", "Herrn ", "Frau ", "Fr. "]

    for p in prefixes:
        if str(inp).startswith(p):
            return inp.split(p)[1]

    return inp


def parse_name(inp: str) -> Optional[HumanName]:
    """
    converts a name string (with optional gender and title) into the name only

    Args:
        inp: the full name
    Return: the HumanName object for further work
    """
    if inp is None or inp.strip() == "":
        return None

    if type(inp) is not str:
        return None

    if " " not in inp and "." in inp:
        # if there are missing spaces, split them up
        inp = inp.replace(".", ". ")

    inp = inp.title()
    # remove gender and title
    inp = _remove_gender(inp)
    inp = remove_title(inp)

    if inp is None or inp.strip() == "":
        return None

    inp = inp.replace(".-", ".").replace(".", ". ").replace("  ", " ")

    hn = HumanName(inp, constants=constants)

    # if there was only a last name given, the parser is confused
    if hn.last == "":
        hn.last_list = hn.first_list
        hn.first_list = []

    # if the first or middle names contains "-" we split up those names into seperate ones
    if hn.middle != "" and "-" in hn.middle:
        hn.middle_list = hn.middle.split("-")
        hn.middle = " ".join(hn.middle_list)
        hn.middle_list = [n for n in hn.middle_list if n.strip() != ""]

    if hn.first != "" and "-" in hn.first:
        firsts = hn.first.split("-")
        hn.first_list = [firsts[0]]
        hn.first = " ".join(hn.first_list)
        hn.middle_list = [*firsts[1:], *hn.middle_list]
        hn.middle = " ".join(hn.middle_list)
        hn.first_list = [n for n in hn.first_list if n.strip() != ""]
        hn.middle_list = [n for n in hn.middle_list if n.strip() != ""]

    if hn.first.endswith(".") and len(hn.first) > 1:
        hn.first = hn.first[0:-1]

    return hn


def _remove_umlaut(string: str) -> str:
    """
    Removes umlauts from strings and replaces them with the letter+e convention

    Args:
        string: string to remove umlauts from
    Returns: unumlauted string
    """
    u = 'ü'.encode()
    U = 'Ü'.encode()
    a = 'ä'.encode()
    A = 'Ä'.encode()
    o = 'ö'.encode()
    O = 'Ö'.encode()
    ss = 'ß'.encode()

    string = string.encode()
    string = string.replace(u, b'ue')
    string = string.replace(U, b'Ue')
    string = string.replace(a, b'ae')
    string = string.replace(A, b'Ae')
    string = string.replace(o, b'oe')
    string = string.replace(O, b'Oe')
    string = string.replace(ss, b'ss')

    string = string.decode('utf-8')
    return string


def person_name(inp: str) -> Optional[str]:
    """
    extract the person name from "GENDER? TITLE? NAME" strings
    """
    if type(inp) is not str:
        return None

    if inp.strip() == "":
        return None

    n = parse_name(inp)
    if n is None:
        return None

    return "{} {} {}".format(n.first, n.middle, n.last).replace("  ", " ").strip()


def match_name(own: str, other: str) -> bool:
    """
    compares 2 names (respects missing middle names, or abbrev. name parts)

    Args:
        own: the first name
        other: the last name

    Returns: True if both names match
    """
    # the simplest case, both name match completely
    if own is None or other is None:
        return True

    own = unicodedata.normalize('NFKD', _remove_umlaut(own)).encode('ASCII', 'ignore').decode("utf-8").lower()
    other = unicodedata.normalize('NFKD', _remove_umlaut(other)).encode('ASCII', 'ignore').decode("utf-8").lower()

    if own == other:
        return True

    hn_other = parse_name(other)
    hn_own = parse_name(own)

    def _remove_surname_titles(surnames: List[str]) -> List[str]:
        def _remove(s: str) -> str:
            for t in _surname_titles:
                s = s.replace(t, "")
            return s

        return list(map(_remove, surnames))

    if hn_own is None or hn_other is None:
        return False

    # remove surname titles like "von" from surnames
    hn_other.last_list = _remove_surname_titles(hn_other.last_list)
    hn_other.last = " ".join(hn_other.last_list)
    hn_own.last_list = _remove_surname_titles(hn_own.last_list)
    hn_own.last = " ".join(hn_own.last_list)

    # if the last names doesnt match, we skip here
    own_lasts = " ".join([on.lower() for on in hn_own.last_list])
    other_lasts = " ".join([on.lower() for on in hn_other.last_list])

    # compound surnames
    if "-" in own_lasts or "-" in other_lasts:
        own_lasts_splitted = own_lasts.split("-")
        other_lasts_splitted = other_lasts.split("-")
        matches = 0
        for o in own_lasts_splitted:
            for ot in other_lasts_splitted:
                if o == ot or distance(o, ot) <= 1 and (len(o) >= 5 or len(ot) >= 5):
                    matches += 1
        for o in reversed(own_lasts_splitted):
            for ot in other_lasts_splitted:
                if o == ot or distance(o, ot) <= 1 and (len(o) >= 5 or len(ot) >= 5):
                    matches += 1
        if matches < 2:
            return False
    elif own_lasts[0] != other_lasts[0] or (own_lasts != other_lasts and distance(own_lasts, other_lasts) > 1):
        return False

    def _match_name_list(name: str, other: List[str]):
        if name in other:
            # full name match
            return True
        elif name.endswith(".") and name in ["{}.".format(f[0:len(name) - 1]) for f in other]:
            # A. name match
            return True
        elif len(name) == 1 and name in [f[0] for f in other]:
            # A name match
            return True
        return False

    def _compare_names(a: List[str], b: List[str]) -> bool:
        m_a = list(map(lambda n: _match_name_list(n, b), a))
        m_b = list(map(lambda n: _match_name_list(n, a), b))
        return m_a.count(True) >= m_a.count(False) or m_b.count(
            True) >= m_b.count(False)

    # check if the firstnames matches (if one side has no firstname we assume a match
    first_name_matches = True if (hn_own.first == "" or hn_other.first == "") else _compare_names(hn_own.first_list,
                                                                                                  hn_other.first_list)
    own_first_middles = hn_own.first + hn_own.middle
    other_first_middles = hn_other.first + hn_other.middle

    # check if the firstnames+middlename matches (if one side has no firstname we assume a match
    first_name_matches_fuzzy = own_first_middles.lower() == other_first_middles.lower() or (
                own_first_middles.startswith(other_first_middles) or other_first_middles.startswith(own_first_middles))

    if first_name_matches is False or first_name_matches_fuzzy is False:
        # if the initials dont match, dont match
        if (len(hn_own.first) > 0 and len(hn_own.first) > 0) and hn_own.first[0] != hn_other.first[0]:
            return False

        # if the names are longer than 5 and start with the same letter we allow tiny typos
        l_distance = distance(hn_own.first, hn_other.first)
        if l_distance < 2 and (len(hn_other.first) >= 5 or len(hn_own.first) >= 5):
            first_name_matches = True

    # if none has middle name its a match
    if len(hn_own.middle_list) == 0 and len(hn_other.middle_list) == 0:
        return first_name_matches or first_name_matches_fuzzy

    # if only one side has a middle name its a match
    if len(hn_own.middle_list) == 0 and len(hn_other.middle_list) > 0 or len(hn_own.middle_list) > 0 and len(
            hn_other.middle_list) == 0:
        return first_name_matches or first_name_matches_fuzzy

    return _compare_names(hn_own.middle_list, hn_other.middle_list)
