INPUT_FILE = 'input.txt'

def get_queries():
    print('\nWelcome! Would you like to perform a single line or bulk search request?')

    validInput = False
    while not validInput:
        print('Please enter the number of the option you would like to select.\n')
        print('(1) Single Line Search\n')
        print('(2) Bulk Search Request  (Must prepare a \'input.txt\' file with each query on a new line.)\n')
        print('(3) Quit the program.\n')

        mode = input('')
        queryList = []

        if mode == '1':
            validInput = True
            query = input("\n\n\nWhat would you like to search: ")
            queryList.append(query)
        elif mode == '2':
            validInput = True
            with open(INPUT_FILE, 'r') as fin:
                for line in fin:
                    queryList.append(line.strip())
        elif mode == '3':
            exit()
        elif not mode.isdigit():
            print('\n\nPlease enter only the number.\n\n')
        else:
            print('\n\nPlease select one of the options.\n\n')
    
    return queryList