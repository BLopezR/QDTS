from qdts_client.qdts_etsi_004_client import Client004, Status


"""
ksid 1, ksid 2  and ksid 4 will  be randomly generated by node while ksid 3
will be chosen by the client.

"""

ksid3 = "abcdabcdabcdabcd".encode()

N = 10
key_size = 8

key_size_bytes = int(key_size / 8)


def run():

    client1 = Client004()
    client2 = Client004()

    client1.connect("192.168.5.10")
    client2.connect("192.168.5.10")

    ttl = 100000
    key_chunk_size = key_size_bytes

    
    print("Sending open connects")

    print("\n\n\nStream 1 (munich - nuremberg)")
    response = client1.open_connect("app1@munich", "app2@nuremberg",key_chunk_size,ttl, ksid = None)
    print("Response: \n" + str(response))
    ksid1 = response["ksid"]

    #print ("Testing peer not connected by asking munich for key in stream 1")
    #response = client1.get_key(ksid1)
    #print(response)
    #if response["status"] != Status.GET_KEY_FAILED_PEER_NOT_CONNECTED:
    #    print("[FAILED] Munich should respond with peer not connected")
    #    exit()
    #print("[OK] PEER_NOT_CONNECTED with get key")

    response = client2.open_connect("app1@munich", "app2@nuremberg",key_chunk_size,ttl, ksid = ksid1)
    print("Response: \n" + str(response))


    # print ("\n\n\nStream 2 (nuremberg - salzburg)")
    # response = client2.open_connect("app2@nuremberg","app3@salzburg",key_chunk_size,ttl, ksid = None)
    # print("Response: \n" + str(response))
    # ksid2 = response["ksid"]

    # response = client3.open_connect("app2@nuremberg", "app3@salzburg",key_chunk_size,ttl, ksid = ksid2)
    # print("Response: \n" + str(response))



    # print("\n\n\nStream 3 (munich - salzburg)")
    # response = client1.open_connect("app1@munich", "app3@salzburg",key_chunk_size,ttl, ksid = ksid3)
    # print("Response: \n" + str(response))

    # response = client3.open_connect("app1@munich", "app3@salzburg",key_chunk_size,ttl, ksid = ksid3)
    # print("Response: \n" + str(response))

    print("\n\n\nStream 4 (munich - nuremberg)")

    response = client1.open_connect("app1@munich", "app2@nuremberg",key_chunk_size,ttl, ksid = None)
    print("Response: \n" + str(response))
    ksid4 = response["ksid"]

    response = client2.open_connect("app1@munich", "app2@nuremberg",key_chunk_size,ttl, ksid = ksid4)
    print("Response: \n" + str(response))


    print("Stream 1 tests")
    for i in range(N):
        key1 = None
        key2 = None
        while key1 is None:
            response = client1.get_key(ksid1)
            if response["status"] == Status.SUCCESSFUL:
                print(response)
                key1 = response["key_buffer"]
        while key2 is None:
            response = client2.get_key(ksid1)
            if response["status"] == Status.SUCCESSFUL:
                print(response)
                key2 = response["key_buffer"]

        if key1 != key2:
            print("[FAILED][Different buffer] Test sample " + str(i))
            exit()


        print("[OK] Test sample " + str(i) + ". Key: " + str(key1))

    print("Stream 2 tests")
    for i in range(N):
        key1 = None
        key2 = None
        while key1 is None:
            response = client2.get_key(ksid2)
            if response["status"] == Status.SUCCESSFUL:
                print(response)
                key1 = response["key_buffer"]
        while key2 is None:
            response = client3.get_key(ksid2)
            if response["status"] == Status.SUCCESSFUL:
                print(response)
                key2 = response["key_buffer"]

        if key1 != key2:
            print("[FAILED][Different buffer] Test sample " + str(i))
            exit()


        print("[OK] Test sample " + str(i) + ". Key: " + str(key1))

    # print("Stream 3 tests")
    # for i in range(N):
    #     key1 = None
    #     key2 = None
    #     while key1 is None:
    #         response = client1.get_key(ksid3)
    #         if response["status"] == Status.SUCCESSFUL:
    #             print(response)
    #             key1 = response["key_buffer"]
    #     while key2 is None:
    #         response = client3.get_key(ksid3)
    #         if response["status"] == Status.SUCCESSFUL:
    #             print(response)
    #             key2 = response["key_buffer"]

    #     if key1 != key2:
    #         print("[FAILED][Different buffer] Test sample " + str(i))
    #         exit()


    #     print("[OK] Test sample " + str(i) + ". Key: " + str(key1))

    print("Stream 4 tests")
    for i in range(N):
        key1 = None
        key2 = None
        while key1 is None:
            response = client1.get_key(ksid4)
            if response["status"] == Status.SUCCESSFUL:
                print(response)
                key1 = response["key_buffer"]
        while key2 is None:
            response = client2.get_key(ksid4)
            if response["status"] == Status.SUCCESSFUL:
                print(response)
                key2 = response["key_buffer"]

        if key1 != key2:
            print("[FAILED][Different buffer] Test sample " + str(i))
            exit()


        print("[OK] Test sample " + str(i) + ". Key: " + str(key1))

    print("Close validation")

    # print("Closing stream 3")
    # response = client1.close(ksid3)
    # print(response)
    # response = client3.close(ksid3)
    # print(response)

    print("Closing stream 4")
    response = client1.close(ksid4)
    print(response)
    response = client2.close(ksid4)
    print(response)

    # print("Requesting keys for stream 3")
    # r1 = client1.get_key(ksid3)
    # print(r1)
    # r2 = client3.get_key(ksid3)
    # print(r2)

    # if r1["status"] != Status.STREAM_NOT_FOUND or r2["status"] != Status.STREAM_NOT_FOUND:
    #     print("[FAILED] Get key does not respond with not found after close ")
    #     exit()

    # print("[OK] Key not found for stream 3")

    print("Requesting keys for stream 4")
    r1 = client1.get_key(ksid4)
    print(r1)
    r2 = client2.get_key(ksid4)
    print(r2)

    if r1["status"] != Status.STREAM_NOT_FOUND or r2["status"] != Status.STREAM_NOT_FOUND:
        print("[FAILED] Get key does not respond with not found after close ")
        exit()

    print("[OK] Key not found for stream 4")

    print ("Checking streams 1 and 2 are still open by getting 2 keys from each")
    print("Stream 1 tests")
    for i in range(2):
        key1 = None
        key2 = None
        while key1 is None:
            response = client1.get_key(ksid1)
            if response["status"] == Status.SUCCESSFUL:
                print(response)
                key1 = response["key_buffer"]
        while key2 is None:
            response = client2.get_key(ksid1)
            if response["status"] == Status.SUCCESSFUL:
                print(response)
                key2 = response["key_buffer"]

        if key1 != key2:
            print("[FAILED][Different buffer] Test sample " + str(i))
            exit()


        print("[OK] Test sample " + str(i) + ". Key: " + str(key1))

    # print("Stream 2 tests")
    # for i in range(2):
    #     key1 = None
    #     key2 = None
    #     while key1 is None:
    #         response = client2.get_key(ksid2)
    #         if response["status"] == Status.SUCCESSFUL:
    #             print(response)
    #             key1 = response["key_buffer"]
    #     while key2 is None:
    #         response = client3.get_key(ksid2)
    #         if response["status"] == Status.SUCCESSFUL:
    #             print(response)
    #             key2 = response["key_buffer"]

    #     if key1 != key2:
    #         print("[FAILED][Different buffer] Test sample " + str(i))
    #         exit()


    #     print("[OK] Test sample " + str(i) + ". Key: " + str(key1))
    
    print ("Opening new streams 3 and 4")
    # print("\n\n\nStream 3 (munich - salzburg)")
    # response = client1.open_connect("app1@munich", "app3@salzburg",key_chunk_size,ttl, ksid = ksid3)
    # print("Response: \n" + str(response))

    # response = client3.open_connect("app1@munich", "app3@salzburg",key_chunk_size,ttl, ksid = ksid3)
    # print("Response: \n" + str(response))

    print("\n\n\nStream 4 (munich - nuremberg)")

    response = client1.open_connect("app1@munich", "app2@nuremberg",key_chunk_size,ttl, ksid = None)
    print("Response: \n" + str(response))
    ksid4 = response["ksid"]

    response = client2.open_connect("app1@munich", "app2@nuremberg",key_chunk_size,ttl, ksid = ksid4)
    print("Response: \n" + str(response))

    # print("Getting 3 keys from each")
    # print("Stream 3 tests")
    # for i in range(3):
    #     key1 = None
    #     key2 = None
    #     while key1 is None:
    #         response = client1.get_key(ksid3)
    #         if response["status"] == Status.SUCCESSFUL:
    #             print(response)
    #             key1 = response["key_buffer"]
    #     while key2 is None:
    #         response = client3.get_key(ksid3)
    #         if response["status"] == Status.SUCCESSFUL:
    #             print(response)
    #             key2 = response["key_buffer"]

    #     if key1 != key2:
    #         print("[FAILED][Different buffer] Test sample " + str(i))
    #         exit()


    #     print("[OK] Test sample " + str(i) + ". Key: " + str(key1))

    print("Stream 4 tests")
    for i in range(3):
        key1 = None
        key2 = None
        while key1 is None:
            response = client1.get_key(ksid4)
            if response["status"] == Status.SUCCESSFUL:
                print(response)
                key1 = response["key_buffer"]
        while key2 is None:
            response = client2.get_key(ksid4)
            if response["status"] == Status.SUCCESSFUL:
                print(response)
                key2 = response["key_buffer"]

        if key1 != key2:
            print("[FAILED][Different buffer] Test sample " + str(i))
            exit()


        print("[OK] Test sample " + str(i) + ". Key: " + str(key1))

    print("Closing all streams")

    print("Closing stream 1")
    response = client1.close(ksid1)
    print(response)
    response = client2.close(ksid1)
    print(response)

    # print("Closing stream 2")
    # response = client2.close(ksid2)
    # print(response)
    # response = client3.close(ksid2)
    # print(response)

    # print("Closing stream 3")
    # response = client1.close(ksid3)
    # print(response)
    # response = client3.close(ksid3)
    # print(response)

    print("Closing stream 4")
    response = client1.close(ksid4)
    print(response)
    response = client2.close(ksid4)
    print(response)

    print ("Reclosing stream 4")
    response = client1.close(ksid4)
    print(response)
    if response != Status.STREAM_NOT_FOUND:
        print("[FAILED] Stream not found status not set")
        exit()

    print("[OK] Stream not found set in closed when already closed")
    
    print("ALL TESTS OKAY!")

if __name__ == '__main__':
    run()
