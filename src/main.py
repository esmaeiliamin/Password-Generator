from abc import ABC, abstractmethod
import random
import string
import nltk


nltk.download('words')

class PasswordGenerator(ABC):
    """Base class for generating passwords."""
    @abstractmethod
    def generate(self):
        """Subclasses must implement this method to generate passwords.
        """
        pass



class PinGenerator(PasswordGenerator):
    """Class to generate pin code."""
    def __init__(self, lenght):
        self.lenght = lenght

    def generate(self):
        """Generate a numeric pin code """
        return ''.join(random.choice(string.digits) for _ in range(self.lenght))



class RandomPasswordGenerator(PasswordGenerator):
    """Class to generate random passwords."""
    def __init__(self, lenght, include_numbers=False, include_symbols=False):
        self.lenght = lenght
        self.characters = string.ascii_letters
        if include_numbers:
            self.characters += string.digits
        if include_symbols:
            self.characters += string.punctuation

    def generate(self):
        """Generate a password from specified characters."""
        return ''.join(random.choice(self.characters) for _ in range(self.lenght))



class MemorablePasswordGenerator(PasswordGenerator):
    """Class to generate memorable passwords."""
    def __init__(self, num_of_words=5, separator='-', capitalization=False, vocabulary=None):
        if vocabulary is None:
            vocabulary = nltk.corpus.words.words() #edit this to any vocabulary
        self.vocabulary = vocabulary
        self.num_of_words = num_of_words
        self.separator = separator
        self.capitalization = capitalization


    def generate(self):
        """Generate a password from a list of vocabulary words.
        """
        password = [random.choice(self.vocabulary) for _ in range(self.num_of_words)]
        if self.capitalization:
            password = [word.upper() for word in password]

        return self.separator.join(password)


def test_random_password_generator():
    random_gen = RandomPasswordGenerator(lenght=10, include_numbers=True, include_symbols=True)
    password = random_gen.generate()
    print(password)
    assert len(password) == 10
    assert any(char in char.asscii_uppercase for char in password)
    assert any(char in string.digits for char in password)


def test_memorable_password_generator():
    memorable_gen = MemorablePasswordGenerator(num_of_words=5, separator='-', capitalization=True, vocabulary=nltk.corpus.words.words())
    password = memorable_gen.generate()
    print(password)
    assert len(password.split('-')) == 4
    assert all(word[0].isupper() for word in password.split('-'))


def test_pincode_generator():
    pin_gen = PinGenerator(lenght=6)
    pin = pin_gen.generate()
    print(pin)
    assert len(pin) == 6
    assert all(char in string.digits for char in pin)

    def main():
        print('Testing Random Password Generator:')
        test_random_password_generator()
        print('Testing Memorable Password Generator:')
        test_memorable_password_generator()
        print('Testing Pincode Generator:')
        test_pincode_generator()


    if __name__ == '__main__':
        main()
