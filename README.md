Negative cycle detection with edge-weighted digraphs. 

I will clean this up later, but for now modify the code manually to adjust the parameters. 
Default size is n=25 cryptocurrencies. 

This code uses Cryptopia's public market-history API but the same logic can be applied to other cryptoexchange sites as well.

Run as follows (requires internet connection): python Arbitrage.py

Expected output: Creates a .csv in current directory to view the adjacency matrix
                 Loads in an existing .json containing previously viewed data if such file exists.
                 Prints the path cycle and log-gain (the higher the better, anything >0 indicates net positive gain per cycle). 
                 
                 
