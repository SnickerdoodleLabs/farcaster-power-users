import os
from neynar import fetch_farcaster_power_users
from csv_utils import write_farcaster_users_to_csv, write_farcaster_users_with_third_wave_to_csv, read_neynar_user_data, read_third_wave_user_data
from processing_utils import process_farcaster_users_in_blocks, process_third_wave_data_in_blocks, count_values_in_ranges

def main(): 
    # first fetch the power users and import their account details, including verified wallet addresses
    farcaster_data_file = "neynar.csv"
    if not os.path.exists(farcaster_data_file):
        print("fetching power users")
        fids = fetch_farcaster_power_users()
        users = process_farcaster_users_in_blocks(fids, 100)
        write_farcaster_users_to_csv(farcaster_data_file, fids, users)
    else:
        print("File with power users already exists, reading from file")
        fids, users = read_neynar_user_data(farcaster_data_file)
    
    print("Number of power users: ", len(fids))

    # now use Third Wave Labs API to fetch wallet info for the verified addresses
    third_wave_data_file = "third-wave.csv"
    if not os.path.exists(third_wave_data_file):
        users_with_third_wave_data = process_third_wave_data_in_blocks(fids, users, 40)
        write_farcaster_users_with_third_wave_to_csv(third_wave_data_file, fids, users_with_third_wave_data)
    else:
        print("File with power users and Third Wave data already exists, reading from file")
        fids, users_with_third_wave_data = read_third_wave_user_data(third_wave_data_file)
    print("Number of power users with Third Wave data: ", len(fids))
    count_values_in_ranges(fids, users_with_third_wave_data)

if __name__ == "__main__":
    main()