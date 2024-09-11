# Power users of Farcaster

This is a short analysis of the on-chain asset holdings and transaction patterns of the Farcaster social network users who have earned the "powerbadge". 

The set of `fids` pertaining to the powerbadge user set and associated farcaster account details is obtained from the [Neynar](https://neynar.com/) api. Details
about user account balances and transaction patters are pulled from the [ThirdWaveLabs](https://thirdwavelabs.com/) service. 

## API Keys

You'll need an api key from both Neynar and Thirdwave Labs. Export the keys to your environment:

```sh
export NEYNAR_API_KEY='blah'
export THIRDWAVE_API_KEY='twv_blah'
```

## Run the script

```sh
pip install -r requirements.txt
python farcaster_power_user_analysis.py
```

> **Note:** Once the pull from either Neynar or Thirdwave finishes, intermediate results are written to csv files. If you run the script again, it'll skip the call to fetch data from the remote service and read the data locally. 