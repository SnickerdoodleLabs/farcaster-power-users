from neynar import fetch_farcaster_user_info
from thirdwave import fetch_third_wave_wallet_info

def process_farcaster_users_in_blocks(fids, block_size=100):
    # Loop through col2 in blocks of the specified size
    users = {}
    for i in range(0, len(fids), block_size):
        # Get the current block of 100 (or less, if at the end)
        block = fids[i:i + block_size]
        print("fetching block:", block[0], "to", block[-1])
        
        # Call the fetch_farcaster_user_info function for the current block
        results = fetch_farcaster_user_info(block)
        for result in results:
            users[result["fid"]] = result

    return users

def create_address_to_fids_map(fids, users):
    address_to_fids = {}
    for fid in fids:
        users[fid]["balance"] = 0
        users[fid]["botWarning"] = False
        for address in users[fid]["verified_addresses"]['eth_addresses']:
            if address not in address_to_fids:
                address_to_fids[address] = []
            address_to_fids[address].append(fid)
    return address_to_fids

def process_third_wave_data_in_blocks(fids, users, block_size=100):
    # Loop through col2 in blocks of the specified size
    address_to_fids = create_address_to_fids_map(fids, users)
    for i in range(0, len(fids), block_size):
        # Get the current block of 100 (or less, if at the end)
        fid_block = fids[i:i + block_size]
        print("fetching block:", fid_block[0], "to", fid_block[-1])
        address_block = []
        for fid in fid_block:
            verified_addresses = users[fid]["verified_addresses"]['eth_addresses']
            if verified_addresses:
                for verified_address in verified_addresses:
                    address_block.append(verified_address)
        
        # Call the Third Wave api for the current block
        results = fetch_third_wave_wallet_info(address_block)

        # add the third wave data to the user object
        for idx, result in enumerate(results):
            address = address_block[idx]
            fid = address_to_fids[address][0]
            if result:
                users[fid]["balance"] += float(result["balance"])
                users[fid]["botWarning"] = users[fid]["botWarning"] or bool(result["botWarning"])

                if "wallet_info" not in users[fid]:
                    users[fid]["wallet_info"] = {}

                if address not in users[fid]["wallet_info"]:
                    users[fid]["wallet_info"][address] = {}

                users[fid]["wallet_info"][address]["firstSeenAt"] = result["firstSeenAt"]
                users[fid]["wallet_info"][address]["balance"] = float(result["balance"])
                users[fid]["wallet_info"][address]["botWarning"] = bool(result["botWarning"])
                users[fid]["wallet_info"][address]["engagementScore"] = int(result["engagementScore"])
                users[fid]["wallet_info"][address]["hodlerScore"] = result["hodlerScore"]
                users[fid]["wallet_info"][address]["outboundTransactionCount"] = int(result["outboundTransactionCount"])
                users[fid]["wallet_info"][address]["outboundTransactionValue"] = float(result["outboundTransactionValue"])
                users[fid]["wallet_info"][address]["transactionPatterns"] = result["transactionPatterns"]

    return users

def count_values_in_ranges(fids, users):
    # Define the ranges
    ranges = {
        "0-25": 0,
        "25-50": 0,
        "50-100": 0,
        "100-250": 0,
        "250-500": 0,
        "500-1000": 0,
        "1000-2000": 0,
        "2000-4000": 0,
        "4000-8000": 0,
        "8000-16000": 0,
        "16000-32000": 0,
        "32000-64000": 0,
        "64000-128000": 0,
        ">128000": 0
    }

    range_balances = {
        "0-25": 0,
        "25-50": 0,
        "50-100": 0,
        "100-250": 0,
        "250-500": 0,
        "500-1000": 0,
        "1000-2000": 0,
        "2000-4000": 0,
        "4000-8000": 0,
        "8000-16000": 0,
        "16000-32000": 0,
        "32000-64000": 0,
        "64000-128000": 0,
        ">128000": 0
    }

    # Count the values in the defined ranges
    for fid in fids:
        balance = users[fid]["balance"]
        if 0 <= balance < 25:
            ranges["0-25"] += 1
            range_balances["0-25"] += balance
        elif 25 <= balance < 50:
            ranges["25-50"] += 1
            range_balances["25-50"] += balance
        elif 50 <= balance < 100:
            ranges["50-100"] += 1
            range_balances["50-100"] += balance
        elif 100 <= balance < 250:
            ranges["100-250"] += 1
            range_balances["100-250"] += balance
        elif 250 <= balance < 500:
            ranges["250-500"] += 1
            range_balances["250-500"] += balance
        elif 500 <= balance < 1000:
            ranges["500-1000"] += 1
            range_balances["500-1000"] += balance
        elif 1000 <= balance < 2000:
            ranges["1000-2000"] += 1
            range_balances["1000-2000"] += balance
        elif 2000 <= balance < 4000:
            ranges["2000-4000"] += 1
            range_balances["2000-4000"] += balance
        elif 4000 <= balance < 8000:
            ranges["4000-8000"] += 1
            range_balances["4000-8000"] += balance
        elif 8000 <= balance < 16000:
            ranges["8000-16000"] += 1
            range_balances["8000-16000"] += balance
        elif 16000 <= balance < 32000:
            ranges["16000-32000"] += 1
            range_balances["16000-32000"] += balance
        elif 32000 <= balance < 64000:
            ranges["32000-64000"] += 1
            range_balances["32000-64000"] += balance
        elif 64000 <= balance < 128000:
            ranges["64000-128000"] += 1
            range_balances["64000-128000"] += balance
        elif balance > 32000:
            ranges[">128000"] += 1
            range_balances[">128000"] += balance

    total_locked_value = 0
    print("Balance ranges | Number of users | Average balance")
    for range_label, count in ranges.items():
        if ranges[range_label] > 0:
            total_locked_value += range_balances[range_label]
            print(f"${range_label}: {count}, ${(range_balances[range_label]/ranges[range_label]):.2f}")

    print(f"Total locked value: ${total_locked_value:.2f}")