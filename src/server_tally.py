import tenseal as ts
import sqlite3
import os

candidatesDict = {1: "Peter Griffin", 2: "Travis Scott", 3: "Lebron James"}
DB_TABLE_NAME = "testElection"


def count_all_votes():

    # connection = sqlite3.connect("/Users/aadarshs/Documents/QueensU/WINTER23/Cryptography/Project/eVote/db/voteDB.db")
    connection = sqlite3.connect("./../db/voteDB.db")
    cursor = connection.cursor()

    cursor.execute(f"SELECT ID, secretVote FROM {DB_TABLE_NAME}")
    rows = cursor.fetchall()

    # for r in rows:
    #     print(r[0])

    #read the public KEY in
    with open('./../keys/publicKey_bfv.hex', 'r') as f:
        publicContext = ts.context_from(bytes.fromhex(f.read()))

    # print(decrypt_result(rows[1][1]))
    #now go line by line and print secretVote
    sum = [0,0,0,0]
    for r in rows:
        encVector = ts.bfv_vector_from(publicContext, bytes.fromhex(r[1]))
        sum = sum + encVector


    counted_result = decrypt_result(sum.serialize().hex())[1:]
    max_index = counted_result.index(max(counted_result))+1
    print("[*] The Vote Tally: ",counted_result)
    print("")

    for i, count in enumerate(counted_result, start=1):
        print(f"[{i}] {candidatesDict[i]}: {count}")


    # print(f"[*] The Winner is: {candidatesDict[max_index]}")

    #need to implement tie logic

    if counted_result.count(max(counted_result)) == 1:
        print(f"\n[*] The Winner is: {candidatesDict[max_index]}")

    else:
        print("[*] There is a tie!")
        tie_candidates = [candidatesDict[i] for i, count in enumerate(counted_result, start=1) if count == max(counted_result)]
        print("[*] The Candidates who have tied: ", tie_candidates)

        
    connection.close()

def decrypt_result(result_hex):
    #read the secret KEY in
    with open('./../keys/privateKey_bfv.hex', 'r') as f:
        privateContext = ts.context_from(bytes.fromhex(f.read()))

    #decrypt the result
    result = ts.bfv_vector_from(privateContext, bytes.fromhex(result_hex))
    return result.decrypt(privateContext.secret_key())

if __name__ == "__main__":
    os.system('clear')
    print("\n+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+\n")
    print("[*] Welcome to Homomorphic Vote Counting!\n")
    count_all_votes()
    print("\n+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+\n\n")
    # print(os.path.abspath('.'))
