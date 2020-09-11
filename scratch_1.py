import sys

def compare_dataval(dataval):
    global data_keys, db1, db2
    for k, v in dataval.items():
        if isinstance(v, dict):
            data_keys.append(k)
            compare_dataval(v)
            data_keys.pop()
        else:
            data_dict = 'sdb'
            if data_keys:
                for i in data_keys:
                    data_dict = "{}['{}']".format(data_dict, i)
            data_dict = "{}['{}']".format(data_dict, k)
            try:
                if v != eval(data_dict):
                    if k in ["settings", "subscriber_property_types"]:
                        print("[{}] {}:".format(db1, k))
                        for i in v:
                            if i not in eval(data_dict):
                                print(i)
                        print("[{}] {}:".format(db2, k))
                        for i in eval(data_dict):
                            if i not in v:
                                print(i)
                    else:
                        print("[{}] {}: {}".format(db1, k, v))
                        print("[{}] {}: {}".format(db2, k, eval(data_dict)))
                    #print(data_dict[1:])
            except KeyError:
                print("KeyError: \"Unable to find '{}!\"".format(data_dict))

if __name__ == "__main__":
    db1 = sys.argv[1]
    db2 = sys.argv[2]
    data_keys = []

    f_dynamo = open("scratch_1.json", "r")
    dynamo=f_dynamo.read()
    dynamo=dynamo.replace('"[\\', '[').replace('\\"]"', '"]')\
        .replace('"{\\', '{').replace('\\"}"', '"}')\
        .replace('\\', '')\
        .replace('"{','{').replace('}"','}')\
        .replace('null', "None").replace('true','True').replace('false', "False")\
        .replace('"["', '["').replace(']""', ']')
    ddb=eval(dynamo)
    print("{} site-id: {}".format(db1, ddb['dataval']['properties']['site_id']))

    f_scylla = open("scratch_2.json", "r")
    scylla=f_scylla.read()
    scylla=scylla.replace('"[\\', '[').replace('\\"]"', '"]')\
        .replace('"{\\', '{').replace('\\"}"', '"}')\
        .replace('\\', '').replace('}"','}')\
        .replace('null', "None").replace('true','True').replace('false', "False")\
        .replace('"["', '["').replace(']""', ']')
    sdb=eval(scylla)
    print("{} site-id: {}".format(db2, sdb['dataval']['properties']['site_id']))

    if not ddb==sdb:
        compare_dataval(ddb)
        print("All other values are equal.")