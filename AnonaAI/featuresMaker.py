__author__ = 'Gilad Barak'

ENTER_KEY_CODE = 13
BACKSPACE_KEY_CODE = 8
ALT_KEY_CODE = 18
SHIFT_KEY_CODE = 16
PUNCTUATION_CODES = list(range(33, 48)) + list(range(58, 65)) + list(range(91, 97)) + list(range(123, 154))


class FeatureGen(object):
    def __init__(self):
        pass

    @staticmethod
    def type_rate(od):
        """
        :param od: key data of user ending with enter(key code 13).
        :return: a 2d array in shape [type time, key count]
        :type od: ordered dictionary
        """
        deltas = []

        is_first = True
        start = None
        key_count = 0

        for item in od:
            key_count += 1
            if is_first:
                start = item
                is_first = False
            if od[item] == ENTER_KEY_CODE:
                deltas.append([(item - start).total_seconds() * 1000, key_count])
                is_first = True
                key_count = 0

        return deltas

    @staticmethod
    def backspace_count(od):
        """
        :param od: key data of user ending with enter(key code 13).
        :return:
        :type od: ordered dictionary
        """
        backspace_ratio = []

        key_count = 0
        backspace_count = 0

        for item in od:
            key_count += 1
            if item == ENTER_KEY_CODE:
                backspace_ratio.append((backspace_count, key_count))
                key_count = 0
                backspace_count = 0
            elif item == BACKSPACE_KEY_CODE:
                    backspace_count += 1

        return backspace_ratio

    @staticmethod
    def language_switch(od):
        """
        :param od: key data of user ending with enter(key code 13).
        :return:
        :type od: ordered dictionary
        """
        language_shift_ratio = []

        key_count = 0
        language_shift_count = 0
        suspect_shift = False, 0

        for item in od:
            key_count += 1

            if od[item] == ALT_KEY_CODE or od[item] == SHIFT_KEY_CODE:
                if suspect_shift[0]:
                    if suspect_shift[1] != od[item]:
                        language_shift_count += 1
                        suspect_shift = False, 0
                else:
                    suspect_shift = True, od[item]

            if od[item] == ENTER_KEY_CODE:
                language_shift_ratio.append((language_shift_count, key_count))
                key_count = 0
                language_shift_count = 0

        return language_shift_ratio

    @staticmethod
    def punctuation_marks(od):
        """
        :param od: key data of user ending with enter(key code 13).
        :return:
        :type od: ordered dictionary
        """
        punctuation_ratio = []

        punctuation_count = 0
        key_count = 0

        for item in od:
            key_count += 1

            if item in PUNCTUATION_CODES:
                punctuation_count += 1

            if item == ENTER_KEY_CODE:
                punctuation_ratio.append((punctuation_count, key_count))
                key_count = 0
                punctuation_count = 0

        return punctuation_ratio
