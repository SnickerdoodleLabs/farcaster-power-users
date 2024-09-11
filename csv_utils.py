import csv
import ast

def write_farcaster_users_to_csv(csv_file_path, fids, users):
    # Define the header
    header = ["fids", "username", "follower_count", "following_count", "power_badge", "verified_addresses"]

    # Write the list to the CSV file
    with open(csv_file_path, 'w', newline='') as outfile:
        writer = csv.writer(outfile)
        # Write the header
        writer.writerow(header)
        # Write the data
        for fid in fids:
            writer.writerow([fid, users[fid]["username"], 
                             users[fid]["follower_count"], 
                             users[fid]["following_count"], 
                             users[fid]["power_badge"], 
                             users[fid]["verified_addresses"]['eth_addresses']])

def write_farcaster_users_with_third_wave_to_csv(csv_file_path, fids, users):
    # Define the header
    header = ["fids", 
              "username", 
              "follower_count", 
              "following_count", 
              "power_badge", 
              "verified_addresses", 
              "outboundTransactionCount", 
              "outboundTransactionValue",
              "balance", 
              "botWarning"]

    # Write the list to the CSV file
    with open(csv_file_path, 'w', newline='') as outfile:
        writer = csv.writer(outfile)
        # Write the header
        writer.writerow(header)
        # Write the data
        for fid in fids:
            addresses = users[fid]["verified_addresses"]['eth_addresses']
            isbot = False
            totalbalance = 0
            txcount = 0
            txvalue = 0
            for address in addresses:
                try:
                    isbot = isbot or users[fid]["wallet_info"][address]["botWarning"]
                    totalbalance += users[fid]["wallet_info"][address]["balance"]
                    txcount += users[fid]["wallet_info"][address]["outboundTransactionCount"]
                    txvalue += users[fid]["wallet_info"][address]["outboundTransactionValue"]
                except KeyError: # not all addresses have wallet info from third wave
                    continue

            writer.writerow([fid, 
                             users[fid]["username"], 
                             users[fid]["follower_count"], 
                             users[fid]["following_count"], 
                             users[fid]["power_badge"], 
                             users[fid]["verified_addresses"]['eth_addresses'],
                             txcount, 
                             txvalue, 
                             totalbalance, 
                             isbot])

def read_neynar_user_data(farcaster_data_file):           
    with open(farcaster_data_file, 'r') as f:
        reader = csv.reader(f)
        next(reader)
        fids = []
        users = {}
        for row in reader:
            fids.append(int(row[0]))
            users[int(row[0])] = {
                "username": row[1],
                "follower_count": int(row[2]),
                "following_count": int(row[3]),
                "power_badge": row[4],
                "verified_addresses": {
                    "eth_addresses": ast.literal_eval(row[5])
                }
            }
    return fids, users

def read_third_wave_user_data(third_wave_data_file):
    with open(third_wave_data_file, 'r') as f:
        reader = csv.reader(f)
        next(reader)
        fids = []
        users = {}
        for row in reader:
            fids.append(int(row[0]))
            users[int(row[0])] = {
                "username": row[1],
                "follower_count": int(row[2]),
                "following_count": int(row[3]),
                "power_badge": row[4],
                "verified_addresses": {
                    "eth_addresses": ast.literal_eval(row[5])
                },
                "wallet_info": {},
                "balance": float(row[8]),
                "botWarning": bool(row[9]),
                "outboundTransactionCount": int(row[6]),
                "outboundTransactionValue": float(row[7])
            }
            for address in ast.literal_eval(row[5]):
                users[int(row[0])]["wallet_info"][address] = {
                    "outboundTransactionCount": int(row[6]),
                    "outboundTransactionValue": float(row[7]),
                    "balance": float(row[8]),
                    "botWarning": bool(row[9])
                }
    return fids, users
            