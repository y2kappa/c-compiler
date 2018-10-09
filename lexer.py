

test1 = """int main() { return 2; }"""
test2 = """int main(){return 2;}"""
test3 = """int main() { return -32; } """

DIGITS = "0123456789"
LETTERS = "abcdefghijklmnopqrstuvxyzwABCDEFGHIJKLMNOPQRSTUVXYZW"

def tokenise_array(to_tokenize_array, token):
    result = []

    for to_tokenize_element in to_tokenize_array:

        elements_between_tokens = to_tokenize_element.split(token)
        
        # we take the element and split it into the noise
        # between the tokens. then we build it back with 
        # the new elements being the noise between tokens
        # and the tokens themselves. 

        for i in range(len(elements_between_tokens)):

            # we add the noise first, noise being the stuff in betwen the tokens
            # it could be a group of tokens or literals or anything

            # if the element between tokens is ""
            # it means the token was first or last
            # and there was nothing before or after that
            # so we're not adding it

            if elements_between_tokens[i] != "":
                result.append(elements_between_tokens[i])

            # we add the token second

            # when we reached the last element after the token
            # we don't add it, because the tokens are ALWAYS
            # in between the elements.

            if i != len(elements_between_tokens)-1:
                result.append(token)

    return result

class Identifier:
    def __init__(self, token):
        self.token = token

    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, self.__class__):
            return self.token == other.token

        return False

    def __ne__(self, other):
        """Overrides the default implementation (unnecessary in Python 3)"""
        return not self.__eq__(other)

    def __repr__(self):
        return self.token
        #return "Identifier(`{}`)".format(self.token)

class Punctuation:
    def __init__(self, token):
        self.token = token

    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, self.__class__):
            return self.token == other.token

        return False

    def __ne__(self, other):
        """Overrides the default implementation (unnecessary in Python 3)"""
        return not self.__eq__(other)

    def __repr__(self):
        return "Punctuation(`{}`)".format(self.token)

class Type:
    def __init__(self, token):
        self.token = token

    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, Type):
            return self.token == other.token

        return False

    def __ne__(self, other):
        """Overrides the default implementation (unnecessary in Python 3)"""
        return not self.__eq__(other)

    def __repr__(self):
        return self.token.upper()
        #return "Type(`{}`)".format(self.token)

class Keyword:
    def __init__(self, token):
        self.token = token

    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, self.__class__):
            return self.token == other.token

        return False

    def __ne__(self, other):
        """Overrides the default implementation (unnecessary in Python 3)"""
        return not self.__eq__(other)

    def __repr__(self):
        return self.token.upper()
        #return "Keyword(`{}`)".format(self.token)

class Operator:
    def __init__(self, token):
        self.token = token

    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, self.__class__):
            return self.token == other.token

        return False

    def __ne__(self, other):
        """Overrides the default implementation (unnecessary in Python 3)"""
        return not self.__eq__(other)
        
    def __repr__(self):
        return "Operator(`{}`)".format(self.token)

class Digit:
    def __init__(self, token):
        self.token = token

    def __repr__(self):
        return "Digit(`{}`)".format(self.token)

class Letter:
    def __init__(self, token):
        self.token = token

    def __repr__(self):
        return "Letter(`{}`)".format(self.token)

class Other:
    def __init__(self, token):
        self.token = token

    def __repr__(self):
        return "Other(`{}`)".format(self.token)

class Number:
    def __init__(self, token):
        self.token = token

    def __repr__(self):
        return "Number(`{}`)".format(self.token)


class Name:
    def __init__(self, token):
        self.token = token

    def __repr__(self):
        return "Name(`{}`)".format(self.token)

def is_number_token(token):
    for char in token:
        if char not in DIGITS:
            return False

    if token[0] == "0":
        return False

    return True

def is_name_token(token):
    
    for char in token:
        if char not in DIGITS and char not in LETTERS:
            return False

    if token[0] in DIGITS:
        return False

    return True

tokens_groups = {
    "identifiers": (["main"], (lambda x: Identifier(x))),
    "punctuation": (["(", ")", ";", "{", "}"], (lambda x: Punctuation(x))),
    "types": (["int"], (lambda x: Type(x))),
    "keywords": (["return"], (lambda x: Keyword(x))),
    "operators": (["=", "-", "+", "*", "/", "~", "!"], (lambda x: Operator(x))),
    "digits": (DIGITS, (lambda x: Number(x))),
    "letters": (LETTERS, (lambda x: Name(x)))
}

tokens_split_groups = {
    "punctuation": (["(", ")", ";", "{", "}"], (lambda x: Punctuation(x))),
    "operators": (["=", "-", "+", "*", "/", "~", "!"], (lambda x: Operator(x))),
}

def tokenize_naked(content):

    tokenized = content.split()
    for _, (tokens, _) in tokens_split_groups.items():
        for token in tokens:
            tokenized = tokenise_array(tokenized, token)

    return tokenized

def tokenize_named(tokenized):
    
    fully_tokenized = []
    for token in tokenized:
        found = False
        for _, (tokens, token_wrapper) in tokens_groups.items():
            if token in tokens:
                found = True
                fully_tokenized.append(token_wrapper(token))

        if not found:
            if is_number_token(token):
                fully_tokenized.append(Number(token))

            elif is_name_token(token):
                fully_tokenized.append(Name(token))

            else: 
                fully_tokenized.append(Other(token) )


    return fully_tokenized

if __name__ == "__main__":

    for test in [test1]:
        print ("Testing: {}".format(test))
        
        tokenized = tokenize_naked(test)
        print ("Tokens: {}".format(tokenized))
 
        tokenized_full = tokenize_named(tokenized)
        print ("Named Tokens: {}\n\n".format(tokenized_full))