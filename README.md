Cryptocurrency Arbitrage

Theory:
Triangular Arbitrage within a single exchange. By taking advantage of the fluctuations in market prices, we should be able to trade from some coin A -> B -> C -> A and basically get more of the same coin that we started with. 
Assumptions:
	We have an infinite supply of currency. 
The quantity of buy/sell orders for their given prices are infinite. 
We can find all the arbitrage opportunities and complete all the orders for arbitrage immediately (in other words, we can do everything in 0 time).
Considerations:
	There is a transaction fee associated with each transaction (0.5% for our selected exchange). 
	There is a minimum transaction amount. 
Any latency such as computation time might mean that the market prices change. 
If too much time passes, buy/sell orders that existed before may no longer exist. 
The price of a coin may also change and an arbitrage opportunity may disappear immediately. 
Getting stuck in the middle of a cycle may have a costly exit. 

Methodology:
We used Python and tried compiling to C using Cython, but gains in speed were negligible for our purposes (one example, 1.3 seconds to 0.6 seconds).
	Pulled market data from Cryptopia’s public API using GET requests. 
Used depth-first-search to find all cycles in a graph and checked if each one yielded positive returns (a.k.a starting with 1 unit of A and running the cycle will result in having more than 1 unit of A). We limited the size of the maximum number of conversions per cycle to be 4 so we can run our algorithm in about a second. 
We checked for the maximum amount of currency we can put through a cycle which is determined by the minimum quantity of an order at its given price. We cannot settle with anything worse than the best price possible otherwise we will lose money since our margins for the arbitrage opportunity are very small. This is important because we have a minimum transaction amount and we cannot use a cycle if it does not meet the minimum transaction requirement. 


Reality:
There are no true arbitrage cycles. In all potential candidates for arbitrage, we found that none of them met the minimum transaction requirement. Either the market is able to correct itself very quickly or bots are closing out all cycles.
Future considerations:
Introduce risk. Instead of fulfilling orders immediately by selling to the highest price that someone is willing to pay, we will be patient and sell at the lowest price that other sellers are willing to sell for. Same logic for buying. This should give us better margins, but we need to wait for our order to be filled at each stage of the cycle.  
