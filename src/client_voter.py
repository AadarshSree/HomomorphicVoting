import tenseal as ts
import sqlite3
import os
import random

username = ""
vote_list = [random.randint(1000,9999),0,0,0]

candidatesDict = {1: "Peter Griffin", 2: "Travis Scott", 3: "Lebron James"}

DB_TABLE_NAME = "testElection"

def insert_vote_into_db():

    connection = sqlite3.connect("./../db/voteDB.db")
    cursor = connection.cursor()

    try:
        with open('./../keys/publicKey_bfv.hex', 'r') as f:
            public_context = ts.context_from(bytes.fromhex(f.read()))
        encryptedVoteList = ts.bfv_vector(public_context, vote_list)

        vote_hex = encryptedVoteList.serialize().hex() 
        # print(username)
        cursor.execute(f"INSERT into {DB_TABLE_NAME} (username,secretVote) values (?,?)", (username, vote_hex))
        connection.commit()
    except Exception as e:
        print(e)
        connection.rollback()

    connection.close()
    return

def print_vote_selection_menu():
    os.system('clear')
    print("+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+")
    print(f"Hi {username}, Please select a candidate to vote for:")
    print("1. "+candidatesDict[1])
    print("2. "+candidatesDict[2])
    print("3. "+candidatesDict[3])
    print("4. Exit")
    print("+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+")
    selection = input("Enter your selection: ")

    if selection not in ['1','2','3','4']:
        print("[*] Invalid selection, please try again...")
        os.system('sleep 1')
        return print_vote_selection_menu()
    return selection

def print_voter_login_menu():
    os.system('clear')
    print("\n+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+")
    print("\nWelcome to Homomorphic e-Voting !")
    t_username = input("[*] Username: ")
    print("\n+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+")
    print("\nHello " + t_username + ", Welcome!")
    os.system('sleep 1')
    
    return t_username

def vote_handler():
    global username, vote_list
    username = str(print_voter_login_menu())
    vote_id = print_vote_selection_menu()

    if vote_id == '4':
        print("[*] Exiting...")
        exit(0)
    
    print("[*] You have selected candidate#" + vote_id + " - " + candidatesDict[int(vote_id)])
    vote_list[int(vote_id)] = 1
    print(vote_list)

    try:
        insert_vote_into_db()
    except Exception as e:
        print("[*] Error inserting vote into db: " + str(e))
        exit(1)

    print("[*] Your Vote has been recorded!")
    print("+---------------------------------------------------------------+")    

if __name__ == "__main__":
    print("[*] Hello World!")


    vote_handler()