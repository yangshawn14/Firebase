import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import json


# Fetch service account key JSON file contents
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()


blank_board =  [

            [ 0, 0, 0, 0, 0, 0, 0, 0, 0 ],
            [ 0, 0, 0, 0, 0, 0, 0, 0, 0 ],
            [ 0, 0, 0, 0, 0, 0, 0, 0, 0 ],
            [ 0, 0, 0, 0, 0, 0, 0, 0, 0 ],
            [ 0, 0, 0, 0, 0, 0, 0, 0, 0 ],
            [ 0, 0, 0, 0, 0, 0, 0, 0, 0 ],
            [ 0, 0, 0, 0, 0, 0, 0, 0, 0 ],
            [ 0, 0, 0, 0, 0, 0, 0, 0, 0 ],
            [ 0, 0, 0, 0, 0, 0, 0, 0, 0 ]
   
]

def main():
    board = read_board(input("Where is your board located? "))
    # board = read_board("medium.json")
    display_board(board)
    
    print("Specify a coordinate to edit or 'Q' to save and quit")
    while play_one_round(board):
        display_board(board) 
    
    write_board(board, input("What file would you like to write to? "))
    # write_board(board, "medium.json")
    
    
    # Add written board to firestore
    # db.collection("boards").add(board)
    # db.collection("coordinates").add(coordinate_list)

def get_coordinate_list(coordinate):
    coordinate_list = []
    coordinate_list.append(coordinate)
    
    db.collection("coordinates").add(coordinate_list)
    
    return coordinate_list

def read_board(filename):
    
    try:
        
        with open(filename, "r") as board_file:
            board_json = json.load(board_file)
            
        
        return board_json["board"]

    except:
        return blank_board

def write_board(board, filename):
    with open(filename, "w") as file:
        board_json = {}
        board_text = json.dumps(board_json)
        file.write(board_text)

def display_board(board):
    print("   A B C D E F G H I")

    for row in range(9):
        if row == 3 or row == 6:
            print("   -----+-----+-----")
        print(row + 1, " ", end="")
        
        for col in range(len(board[0])):
            # pos = board[row][col]
            # if pos == 0:
            #     pos = " "
            # print(f" {pos}", sep="", end="\n" if col == 8 else "")
            # if col == 2 or col == 5:
            #     print(f"|", sep="", end="\n" if col == 8 else "")
            # if col < 2:
            #     print("", sep="", end="\n" if col == 8 else "")
            separator = [" ", " ", "|", " ", " ", "|", " ", " ", "\n"]
            print(board[row][col] if board[row][col] != 0 else " ", end=separator[col])
            

def play_one_round(board):
    # Prompt for input
    # coordinate_list = []
    # num_list = []

    coordinate = input("> ")

    if coordinate.upper() == "Q":
            return False
    
    
        
    # # Quit if user says quit
    # if coordinate == "Q":
    #     return False

    # # Determine if coordinate is valid
    # (row, col, valid) = parse_input(coordinate)
    # if not valid:
    #     print(f"ERROR: Square {coordinate} is invalid")
    #     return True

    # # See if the square is already filled
    # str_coordinate = string_from_coordinate(row, col)

    # if board[row][col] != 0:
    #     print(f"ERROR: Square {str_coordinate} is filled")
    #     return True

    # # Prompt for the number
    # num = int(input(f"What number goes in {str_coordinate}? "))
    # if 0 >= num or 9 < num:
    #     print(f"ERROR: The value {num} is invalid")
    #     return True

    # # Determine if the input is legal
    # message = is_input_legal(board, row, col, num)
    # if message == "OK":
    #     board[row][col] = num
    # else:
    #     print(message)
    # return True

    # ------------------------------------------------------- #

    # check if coordinate is in reverse order
    if coordinate[0].isdigit() and coordinate[1].isalpha():
        coordinate = coordinate[::-1]
    
    # Let user enter coordinate until they write "Q"
    # while coordinate.upper() != "Q":
      # Check if coordinate is valid
    if coordinate[0].upper() in ["A", "B", "C", "D", "E", "F", "G", "H", "I"]\
    and coordinate[1].isdigit() and len(coordinate) == 2:

        (row, col, valid) = parse_input(coordinate)
        str_coordinate = string_from_coordinate(row, col)

        # check coordinate value for debug
        # print(str_coordinate)

        # Check if square is filled in
        if not valid:
            print(f"ERROR: Square {str_coordinate} is filled\n")

        if board[row][col] == 0:
            num = int(input(f"What number goes in {str_coordinate}? "))
            
            
            # while board[row][col] == 0:
            if 1 <= num <= 9:
                print()
                # Check if number is legal
                if is_input_legal(board, row, col, num) == "OK":
                    board[row][col] = num
                    return True
                else:
                    print(is_input_legal(board, row, col, num))
                    return True
            else:
                print(f"Error: the value {num} is invalid. Value must be 1 - 9.")
                num = int(input(f"What number goes in {str_coordinate}? "))
                return True
        else:
            print(f"ERROR: Square {str_coordinate} is filled\n")
            return True
    
    else:
        print(f"ERROR: Sqaure '{coordinate}' is invalid")
        print()
        # coordinate = input("> ")
        # if coordinate == "Q":
        return True

    
    
    

def parse_input(coordinate):
    # for letter in coordinate:
    #   if A <= letter <= Z:
    #       column = ORD(letter) - ORD(A)
    #   if 1 <= letter <= 9
    #       row = letter - 1
    row = col = -1
    for letter in coordinate.upper():
        # Letters are assumed to be columns
        if "A" <= letter <= "I":
            col = ord(letter) - ord("A")
        # Rows are assumed to be rows
        if "1" <= letter <= "9":
            row = int(letter) - 1
    # Code for Lab05
    # col = ord(coordinate[0].upper()) - ord("A") 

    # row = int(coordinate[1]) - 1
    
    return (row, col, True if row != -1 and col != -1 else False)

def string_from_coordinate(row, col):
    return chr(col + ord("A")) + chr(row + ord("1"))

    

def is_input_legal(board, row, col, num):
    # assert(0 <= row < 9)
    # assert(0 <= col < 9)
    # assert(1 <= num <= 9)
    # assert(board[row][col] == 0)

    # Check that the column is unique
    for r in range(9):
        if board[r][col] == num:
            return "ERROR: " + str(num) + " is already present on that column"

    # Check that the row is unique
    for c in range(9):
        if board[row][c] == num:
            return "ERROR: " + str(num) + " is already present on that row"

    # Check the inside square
    for r in range(3):
        for c in range(3):
            if board[row // 3 + r][col // 3 + c] ==  num:
                return "ERROR: " + str(num) + " is already inside that square"

    return "OK"



main()