#------------------------------------------#
# Title: CDInventory.py
# Desc: Working with files and handling exceptions.
# Change Log: (Who, When, What)
# DBiesinger, 2030-Jan-01, Created File
# Wdang, 2020-Feb-28, Modified file for assignment06
# Wdang, 2020-Mar-08, Midified file for assignment07
#------------------------------------------#

""" This program is a menu operated CD inventory system """

import pickle # To save and read binary format file

# -- DATA -- #
strChoice = '' # User input
lstTbl = []  # list of lists to hold data
dicRow = {}  # list of data row
strFileName = 'CDInventory.dat'  # data storage file in binary format
objFile = None  # file object


# -- PROCESSING -- #
class DataProcessor:
    """Processing data in memory"""
    
    @staticmethod
    def add_inventory(table):
        """Add user inputs of new CD to inventory table in memory

        Args:
            table: the list of dictionaries containing the CD entries
            
        Returns:    
            the modified list of dictionaries with new entries of CDs
        """
        try:
            strID = input('Enter ID: ').strip()
            strTitle = input('What is the CD\'s title? ').strip()
            strArtist = input('What is the Artist\'s name? ').strip()

            # flexibility of user inputs, e.g. 001 is saved as 1
            intID = int(strID)
            
            # make sure user input doesn't result in duplicate ID number
            intRowNr = -1
            blnCDExist = False
            for row in table:
                intRowNr += 1
                if row['ID'] == intID:
                    blnCDExist = True
                    break
            if blnCDExist:
                print("""CD ID '{}' or '{}' already exsits\n
                      new CD is not added, use a different ID\n""".format(strID, intID))
            else:
                dicRow = {'ID': intID, 'Title': strTitle, 'Artist': strArtist}
                table.append(dicRow)
                return table
            
        # try-except to catch user input ID not in number or digital format
        except ValueError:
            print("ID '{}' was not valid and must be digits such as '1' or '01'\n".format(strID))

    @staticmethod
    def delete_inventory(table):
        """Delete CD from inventory table in memory based on 
        user input CD ID and confirm the deletion with user


        Args:
            table: the list of dictionaries containing the CD entries.
            ID: the ID of the CD to be deleted

        Returns:
            the modified list of dictionaries with removal of entries matching CD ID entered

        """
        IDDel = input('Which ID would you like to delete? ').strip()
        
        try:
            intIDDel = int(IDDel)
        
            intRowNr = -1
            blnCDRemoved = False
            for row in table:
                intRowNr += 1
                if row['ID'] == intIDDel:
                    del table[intRowNr]
                    blnCDRemoved = True
                    break
            if blnCDRemoved:
                print('The CD was removed\n')
            else:
                print('Could not find this CD!\n')
            return table

        # try-except to catch user input ID not in number or digital format
        except ValueError:
            print("ID '{}' was not valid and must be digits such as '1' or '01'\n".format(IDDel))


class FileProcessor:
    """Processing the data to and from text file"""

    @staticmethod
    def read_file(file_name):
        """Function to manage data ingestion from a binary file to a list

        Reads the data from binary file identified by file_name into a list.

        Args:
            file_name (string): name of file used to read the data from

        Returns:
            a list contains file content.
        """
        
        try:
            with open(file_name, 'rb') as objFile: # no file.close() needed using with open
                table = pickle.load(objFile)
            return table
        # try-except to prevent program crash if specified file can't be found due to such as
        # filename error, file not created, file removed
        except FileNotFoundError:
            print("\n\nFile {} was not found and was not able to be loaded\n".format(file_name))
            # below is necessary otherwise table = None when except is invoked
            # this function won't crash but the future code will crash
            table = [] 
            return table


# alternative code for not reading in binary format, maybe useful for future
        # for line in data:
        #     id = line.strip().split(',')
        #     dicRow = {'ID': int(id[0]), 'Title': id[1], 'Artist': id[2]}
        #     table.append(dicRow)


    @staticmethod
    def write_file(table, file_name):

        """Function to manage data ingestion from a list to a binary file

        Args:
            table: data in memory
            file_name: name of file used to save the data to

        Returns:
            None.
        """        
        
        with open(file_name, 'wb') as objFile:
            pickle.dump(table, objFile)


# alternative code for not saving in binary format
    # Overwrite the data from file identified by file_name with the follow:
    # Extract the values only of the each row of the list of dicts as a new list, one row a time
    # Convert the first value to string format
    # Write each of the values comma separated, and start a new line at the end


        # objFile = open(file_name, 'w')
        # for row in table:
        #     lstValues = list(row.values())
        #     lstValues[0] = str(lstValues[0])
        #     objFile.write(','.join(lstValues) + '\n')
        # objFile.close()


# -- PRESENTATION (Input/Output) -- #

class IO:
    """Handling Input / Output"""

    @staticmethod
    def print_menu():
        """Displays a menu of choices to the user

        Args:
            None.

        Returns:
            None.
        """

        print('Menu\n\n[l] load Inventory from file\n[a] Add CD\n[i] Display Current Inventory')
        print('[d] delete CD from Inventory\n[s] Save Inventory to file\n[x] exit\n')

    @staticmethod
    def menu_choice():
        """Gets user input for menu selection

        Args:
            None.

        Returns:
            choice (string): a lower case sting of the users input out of the choices l, a, i, d, s or x

        """
        choice = input('Which operation would you like to perform? [l, a, i, d, s or x]: ').lower().strip()
        while choice not in ['l', 'a', 'i', 'd', 's', 'x']:
            print("'{} is not a valid operation".format(choice))
            choice = input('Which operation would you like to perform? [l, a, i, d, s or x]: ').lower().strip()
        print()  # Add extra line for layout
        return choice

    @staticmethod
    def show_inventory(table):
        """Displays data in memory, only shows the values of the dictionaries  
        

        Args:
            table: data in memory.

        Returns:
            None.

        """
        print('======= The Current Inventory: =======')
        print('ID\tCD Title (by: Artist)\n')

        for row in table:
            print('{}\t{}\t (by:{})'.format(*row.values()))
        print('======================================')



# start main program

# 1. When program starts, read in the currently saved Inventory
lstTbl = FileProcessor.read_file(strFileName)

# 2. start main loop
while True:
    # 2.1 Display Menu to user and get choice
    IO.print_menu()
    strChoice = IO.menu_choice()

    # 3. Process menu selection
    # 3.1 process exit first
    if strChoice == 'x':
        break
    # 3.2 process load inventory
    if strChoice == 'l':
        print('WARNING: If you continue, all unsaved data will be lost and the Inventory re-loaded from file.')
        strYesNo = input('type \'yes\' to continue and reload from file. otherwise reload will be canceled')
        if strYesNo.lower() == 'yes':
            print('reloading...')
            lstTbl = FileProcessor.read_file(strFileName)
            IO.show_inventory(lstTbl)
        else:
            input('canceling... Inventory data NOT reloaded. Press [ENTER] to continue to the menu.')
            IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.3 process add a CD
    elif strChoice == 'a':
        # 3.3.1 Ask user for new ID, CD Title and Artist and add to CD inventory table
        DataProcessor.add_inventory(lstTbl)
        # 3.3.2 Display the updated inventory list
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.4 process display current inventory
    elif strChoice == 'i':
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.5 process delete a CD
    elif strChoice == 'd':
        # 3.5.1 display Inventory to user
        IO.show_inventory(lstTbl)
        # 3.5.2.1 get user input for which CD to delete
        # 3.5.2 2 search thru table and delete CD if found
        DataProcessor.delete_inventory(lstTbl)
        # 3.5.3 display updated Inventory to user
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.6 process save inventory to file
    elif strChoice == 's':
        # 3.6.1 Display current inventory and ask user for confirmation to save
        IO.show_inventory(lstTbl)
        strYesNo = input('Save this inventory to file? [y/n] ').strip().lower()
        # 3.6.2 Process choice
        if strYesNo == 'y':
            # 3.6.2.1 save data
            FileProcessor.write_file(lstTbl, strFileName)
        else:
            input('The inventory was NOT saved to file. Press [ENTER] to return to the menu.')
        continue  # start loop back at top.
    # 3.7 catch-all should not be possible, as user choice gets vetted in IO, but to be safe:
    else:
        print('General Error')




