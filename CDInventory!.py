#------------------------------------------#
# Title: CDInventory.py
# Desc: Working with classes and functions.
# Change Log: (Who, When, What)
    # DBiesinger, 2030-Jan-01, Created File
    # Bita Massoudi, Nov/26/2022, Add Structured error handling and binary data storage
#------------------------------------------#

import pickle

# -- DATA -- #
strChoice = '' # User input
lstTbl = []  # list of lists to hold data
dicRow = {}  # list of data row
strFileName = 'CDInventory.dat'  # data storage dat file
objFile = None  # file object
strID = int()
intID = int()
strTitle= ''
strArtist=''
table=[]
intRowNr=int()
         


# -- PROCESSING -- #
class DataProcessor:
    """Processing the data in the memory"""

    def CD_appendRow(strID, strTitle, strArtist): 
        """function to append input data into dicts.
        Args:
            'ID': intID, 'Title': strTitle, 'Artist': strArtist 
            data to be appended into memory
        Return:
            table:2Dlist of dicts
        """   
        
        intID = int(strID)
        dicRow = {'ID': intID, 'Title': strTitle, 'Artist': strArtist}     
        lstTbl.append(dicRow)
        for row in lstTbl:
            print('{}\t{} (by:{})'.format(*row.values()))
        print('======================================')
        return lstTbl
        #IO.show_inventory(lstTbl)
    def delete_file (table):
        """Function to delete data from user input from dic.
        Args:
              intIDDel-ID number to be deleted
        Returns:
                  None
              """
        # TODone: improve error handling if the user tries deleting a non-numeric ID
        intIDDel = '' # set intIDDel to empty
        while type(intIDDel) != int: # don't let the user go anywhere until they select a numeric ID
            try:
                intIDDel = int(input('Which ID would you like to delete? ').strip())
            except ValueError:
                print('\nSorry, that didn\'t work. Please select an ID from your current inventory.\n')              
                #intIDDel = int(input('Which ID would you like to delete? ').strip())
        intRowNr = -1
        blnCDRemoved = False
        for row in table:
            intRowNr += 1
            if int(row['ID']) == intIDDel:
                del table[intRowNr]
                blnCDRemoved = True
                break
        if blnCDRemoved:
            print('The CD # ',intIDDel,' was removed')

         #Error handling against non integers              
        try:    
            if blnCDRemoved ==True:
                 print ('The CD Number', intIDDel, 'was removed')
            if blnCDRemoved ==False:
                 raise Exception            
        except Exception:
             print('\nPlease select an ID from the inventory.\n')
             
        return table

class FileProcessor:
    """Processing the data to and from text file"""
    

    @staticmethod
    def read_file(file_name, table):
        """Function to read the contents of the binary file and load to memory
        Args:
            file_name (string): name of file used to read the data from
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime

        Returns:
            none
        """
         #TODone modify existing code to work with binary instead of text
        table.clear()  
        #load binary data from .dat file
        with open(file_name,'rb') as file:
           table = pickle.load(file)
        return table
    
    @staticmethod
    def write_file(file_name, table):
        """Function to save the CDs in memory to a binary file 
        Args:
            file_name (string)
            table (list of dict) 
        return:            
            none
        """
        # Display current inventory and ask user for confirmation to save
        # Error Handling if user doesnt enter anything
        while True:
            try:
                strYesNo=input('Save this inventory to file? [y/n] ').strip().lower()
                if not strYesNo:
                    raise Exception
                break
            except Exception:
                print('Please enter yes or no')
            #process choice 'y'
            #save data in binary form
        if strYesNo == 'y':
            with open(file_name,'wb') as file:
                pickle.dump(table, file, protocol=pickle.HIGHEST_PROTOCOL)
        else:
            input('The inventory was NOT saved to file. Press [ENTER] to return to the menu.')
        

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
        choice = ' '
        #Error Handling if user doesnt enter anything in [l, a, i, d, s, x]

        while True:
            try:
                choice = input('Which operation would you like to perform? [l, a, i, d, s or x]: ').lower().strip()
                if (choice == 'a') or (choice == 'l') or(choice == 'i') or(choice == 'd') or(choice == 's') or(choice == 'x'):
                    break
                else: raise Exception
            except Exception:
                print('This is an invalid choice! Please try again!!')
        print()  # Add extra space for layout
        return choice


    @staticmethod
    def show_inventory(table):
        print(lstTbl)
        print() # Add extra space for layout
        """
        Displays current inventory table
        Args:
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime.
        Returns:
            None.
        """
            
        print('======= The Current Inventory: =======')
        print('ID\tCD Title (by: Artist)\n')
        for row in table:
            print('{}\t{} (by:{})'.format(*row.values()))
        print('======================================')


    @staticmethod
    def add_file():
        """user input, and return values for, CD ID, Title, and Artist 
           try - except method to ensure users inputs an integer ID.
        Args:
            None.
        Returns:
            strID (string): user selected ID value
            strTitle (string): user input for CD name
            strArtist (string): user input for Artist
        """ 
        strID=''
        while True:
            strID = input('Enter ID: ').strip()
            #Error Handling if user enter non-numeric value
            try:
                intID = int(strID)
                break
            except ValueError:
                print('Please choose an integer! Try again!')
        strTitle = input('What is the CD\'s title? ').strip()
        stArtist = input('What is the Artist\'s name? ').strip()
        return intID, strTitle, stArtist
# 1. When program starts, read in the currently saved Inventory
# Error Hadling if no CDInventory.dat file found
while True:
    Item=False #use Item to decide when to break the loop
    try:
        FileProcessor.read_file(strFileName, lstTbl)
    except FileNotFoundError:
        print ('File not found!\n')
        break
    # 2. start main loop
    while True:
    # 2.1 Display Menu to user and get choice
        IO.print_menu()
        strChoice = IO.menu_choice()
    # 3. Process menu selection
    # 3.1 process exit first
        if strChoice == 'x':
            Item = True #if Item==True, break the loop
            break
    # 3.2 process load inventory
        if strChoice == 'l':
            print('WARNING: If you continue, all unsaved data will be lost and the Inventory re-loaded from file.')
            strYesNo = input('type \'yes\' to continue and reload from file. otherwise reload will be canceled\n')
            if strYesNo.lower() == 'yes':
                print('reloading...')
                #FileProcessor.read_file(strFileName, lstTbl)
                IO.show_inventory(lstTbl)
            else:
                input('canceling... Inventory data NOT reloaded. Press [ENTER] to continue to the menu.')
                IO.show_inventory(lstTbl)
            continue  # start loop back at top.
    # 3.3 process add a CD
        elif strChoice == 'a':
            A1, A2, A3= IO.add_file()
            DataProcessor.CD_appendRow(A1, A2, A3)
            continue

    # 3.4 process display current inventory 
        elif strChoice == 'i':
            IO.show_inventory(lstTbl)
            continue  # start loop back at top.
    # 3.5 process delete a CD
        elif strChoice == 'd':
            # 3.5.1 get Userinput for which CD to delete
            # 3.5.1.1 display Inventory to user
           IO.show_inventory(lstTbl)
          # intIDDel = int(input('Which ID would you like to delete? ').strip())
           DataProcessor.delete_file(lstTbl)
           continue  # start loop back at top.

    # 3.6 process save inventory to file
        elif strChoice == 's':
            # 3.6.1 Display current inventory and ask user for confirmation to save
            IO.show_inventory(lstTbl)
            strYesNo = input('Save this inventory to file? [y/n] ').strip().lower()
            # 3.6.2 Process choice
            if strYesNo == 'y':
                FileProcessor.write_file(strFileName, lstTbl)
            else:
                input('The inventory was NOT saved to file. Press [ENTER] to return to the menu.')
            continue  # start loop back at top.


        print('General Error')

    if Item == True:
        break

