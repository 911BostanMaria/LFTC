import re

from Symbol import SymbolTable


class Scanner:
    def __init__(self, file_info):
        self._lineCount = 0
        self._file = file_info
        self._SymbolTable= SymbolTable(30)
        self._programInternalForm = []
        self._tokens = []
        try:
            self.readTokens()
            self.scan()
        except ValueError as err:
            print(err)

    def readTokens(self):
        with open("token.in") as token_file:
            for line in token_file:
                self._tokens.append(line.rstrip())

    def writeToFile(self):
        with open('PIF.out', 'w') as PIF_file:
            for element in self._programInternalForm:
                PIF_file.write(str(element) + '\n')

        with open('ST.out', 'w') as ST_file:
            ST_file.write(str(self._SymbolTable.to_string()))


    def scan(self):
        lines = re.split('[\n]', self._file)
        code_lines = []
        for line in lines:
            if line != ' ' and line != '':
                code_lines.append(line)
        for code_line in code_lines:
            line_tokens = self.tokenizeLine(code_line)

            for token in line_tokens:
                if token in self._tokens:
                    self._programInternalForm.append((token, 0))
                else:
                    if self.classifyToken(token) == 0:
                        raise ValueError(
                            "Lexical error: Token {} cannot be classified: line {}".format(token, self._lineCount))
                    if self.classifyToken(token) == 1:
                        self._SymbolTable.add_identifier(token)
                        self._programInternalForm.append(('identifier', (
                            self._SymbolTable.get_position_identifier(token))))
                    if self.classifyToken(token) == 2 or self.classifyToken(token) == 3 or self.classifyToken(
                            token) == 4:
                        self._SymbolTable.add_constant(token)
                        self._programInternalForm.append(('constant', (
                            self._SymbolTable.get_position_constant(token))))

        self.writeToFile()
        print("Lexically corect")

    def tokenizeLine(self, line_string):
        self._lineCount += 1
        # split the line by everything that is not a list of alphanumeric values
        # strings enclosed in double quotes, alphanumeric sequences, and sequences of characters
        line_data = re.findall(r'("[^"]+"|[a-zA-Z0-9]+|[^a-zA-Z0-9"\s]+)', line_string)
        filtered_line_elements = []
        for element in line_data:
            if element is not None and element.strip() != '':
                filtered_line_elements.append(element)
        line_elements = filtered_line_elements
        print(filtered_line_elements)
        final_line_tokens = []
        i = 0
        n = len(line_elements)
        while i < n:
            if i > n:
                break
            if line_elements[i] == '=':
                if line_elements[i + 1] == '=':
                    final_line_tokens.append('==')
                    i = i + 1
                elif line_elements[i + 1] == '>':
                    final_line_tokens.append('=' + line_elements[i + 1])
                    i = i + 1
                else:
                    final_line_tokens.append('=')
            elif line_elements[i] == '<':
                if line_elements[i + 1] == '=':
                    final_line_tokens.append('<' + line_elements[i + 1])
                    i = i + 1
                else:
                    final_line_tokens.append('<')

            elif line_elements[i] in '>':
                final_line_tokens.append('>')

            else:
                final_line_tokens.append(line_elements[i])
            i = i + 1

        return final_line_tokens

    def classifyToken(self, token):
        """
        Classify a token either as an identifier or a constant
        :param token:
        :return:
        """
        # identifier - letter{letter|digit} ->1
        match = re.match('^[a-z]+[a-z0-9]*$', token)
        if match is not None:
            return 1
        # constant
        # string constant - """{character}""" ->2
        # character - 'letter|digit' ->3
        # integer - "0"|["+"|"-"]nzDigit{digit} ->4
        string_match = re.match(r'^"[a-zA-Z0-9\s]+"$', token)
        if string_match is not None:
            return 2
        else:
            char_match = re.match('^\'[a-zA-Z0-9\'$]', token)
            if char_match is not None:
                return 3
            else:
                int_match = re.match('^0$|^(\+|-)?[1-9][0-9]*$', token)
                if int_match is not None:
                    return 4
        return 0




def test_p1():
    file = open('p1.txt', 'r')
    scanner = Scanner(file.read())


def test_p1error():
    file = open('p1_error.txt', 'r')
    scanner = Scanner(file.read())


def test_p2():
    file = open('p2.txt', 'r')
    scanner = Scanner(file.read())


def test_p3():
    file = open('p3.txt', 'r')
    scanner = Scanner(file.read())


test_p1error()