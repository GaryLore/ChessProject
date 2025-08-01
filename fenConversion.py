import numpy as np
class FENParser:
    def __init__(self, rows):
        self.rows = rows.split("/")
        self.extra_info = self.rows[-1]

        info = self.extra_info.split(" ", 1)
        self.rows[-1] = info[0]
        self.extra_info = info[1]

    def print_rows(self):
        for row in self.rows:
            print(row)
        print(self.extra_info)

    def parse(self):
        parsed_rows = []
        for row in self.rows:
            parsed_row = []
            ## Get each character in the row and translate
            for i in range(len(row)):
                character = row[i]
                if character.isdigit():
                    for j in range(int(character)):
                        parsed_row.append(0)
                else:
                    parsed_row.append(self.piece_encoding(character))
            parsed_rows.append(parsed_row)
        self.rows = parsed_rows

        info = self.extra_info.split(" ")
        turn = FENParser.check_turn(info[0])
        castling = FENParser.check_castling(info[1])
        en_passant = FENParser.check_enpassant(info[2])

        self.rows.append([turn])
        self.rows.append(castling)
        self.rows.append(en_passant)

        return [item for sublist in self.rows for item in sublist]
        #print(flat_list)

    @staticmethod
    def check_turn(param):
        if param == 'b':
            #print('BLACK')
            return -1
        #print("WHITE")
        return 1

    @staticmethod
    def check_castling(param):
        if param == '-':
            #print("castling Array")
            #print("-1,-1,-1,-1")
            return [-1,-1,-1,-1]

        castling = [-1,-1,-1,-1]
        for letter in param:
            if letter.isupper():
                if letter == 'K':
                    castling[0] = 1
                else: #should be Q if upper and not K
                    castling[1] = 1
            else:
                if letter == 'k':
                    castling[2] = 1
                else: #should be q if lower and not k
                    castling[3] = 1

        #print("castling Array")
        #print(castling)
        return castling

    @staticmethod
    def check_enpassant(param):
        if param == '-':
            #print('no possible enpassant')
            return [-1,-1]

        coordinate = [FENParser.convert_letter(param[0]),int(param[1])/10]
        #print("En Passant Coordinate: ")
        #print(coordinate)
        return coordinate


    @staticmethod
    def convert_letter(char):
        match char:
            ## White Pieces
            case 'a':
                return .1
            case 'b':
                return .2
            case 'c':
                return .3
            case 'd':
                return .4
            case 'e':
                return .5
            case 'f':
                return .6
            case 'g':
                return .7
            case 'h':
                return .8


    @staticmethod
    def piece_encoding(character):
        match character:
            ## White Pieces
            case 'P':
                return .1
            case 'N':
                return .2
            case 'B':
                return .3
            case 'R':
                return .4
            case 'Q':
                return .5
            case 'K':
                return .6
            ## Black Pieces
            case 'p':
                return -.1
            case 'n':
                return -.2
            case 'b':
                return -.3
            case 'r':
                return -.4
            case 'q':
                return -.5
            case 'k':
                return -.6

#FEN = FENParser("8/5k2/3p4/1p1Pp2p/pP2Pp1P/P4P1K/8/8 w KQ - 99 50")
#list = FEN.parse()
#print(len(list))
#print(list)