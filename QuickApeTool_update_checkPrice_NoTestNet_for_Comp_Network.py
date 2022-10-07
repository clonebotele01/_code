import tkinter.messagebox
from tkinter import *
from tkinter import ttk
from web3 import Web3
import time
from datetime import datetime
from tkinter.ttk import Combobox
import threading
import webbrowser
from eth_abi.packed import encode_abi_packed
from os.path import exists as file_exists
import json
import requests
from eth_account import Account

### Userconfig reading ###
with open("./lp.json") as file:
    LP_abi = json.load(file)
with open("./userconfig.json") as f:
    keys = json.load(f)
with open("./pancake.json") as file1:
    dex = json.load(file1)

user_wallet_address = keys["wallet_address"]
user_private_key = keys["private_key"]
init_BNB = keys["BNB_Amount"]
init_BUSD = keys["BUSD_Amount"]
user_RPC = keys["RPC_Node"]

##### config ##
## PancakeSwap ##
factory_address = dex["FACTORY"]
TESTNET_RPC = "https://data-seed-prebsc-1-s1.binance.org:8545/"
DT_CONV_ABI = '[{"constant":true,"inputs":[{"name":"timestamp","type":"uint256"}],"name":"getHour","outputs":[{"name":"","type":"uint16"}],"type":"function"},{"constant":true,"inputs":[{"name":"timestamp","type":"uint256"}],"name":"getWeekday","outputs":[{"name":"","type":"uint8"}],"type":"function"},{"constant":true,"inputs":[{"name":"year","type":"uint16"},{"name":"month","type":"uint8"},{"name":"day","type":"uint8"},{"name":"hour","type":"uint8"},{"name":"minute","type":"uint8"}],"name":"toTimestamp","outputs":[{"name":"timestamp","type":"uint256"}],"type":"function"},{"constant":true,"inputs":[{"name":"timestamp","type":"uint256"}],"name":"getDay","outputs":[{"name":"","type":"uint16"}],"type":"function"},{"constant":true,"inputs":[{"name":"year","type":"uint16"},{"name":"month","type":"uint8"},{"name":"day","type":"uint8"},{"name":"hour","type":"uint8"}],"name":"toTimestamp","outputs":[{"name":"timestamp","type":"uint256"}],"type":"function"},{"constant":true,"inputs":[{"name":"timestamp","type":"uint256"}],"name":"getSecond","outputs":[{"name":"","type":"uint16"}],"type":"function"},{"constant":true,"inputs":[{"name":"year","type":"uint16"},{"name":"month","type":"uint8"},{"name":"day","type":"uint8"}],"name":"toTimestamp","outputs":[{"name":"timestamp","type":"uint256"}],"type":"function"},{"constant":true,"inputs":[{"name":"year","type":"uint16"},{"name":"month","type":"uint8"},{"name":"day","type":"uint8"},{"name":"hour","type":"uint8"},{"name":"minute","type":"uint8"},{"name":"second","type":"uint8"}],"name":"toTimestamp","outputs":[{"name":"timestamp","type":"uint256"}],"type":"function"},{"constant":true,"inputs":[{"name":"timestamp","type":"uint256"}],"name":"getYear","outputs":[{"name":"","type":"uint16"}],"type":"function"},{"constant":true,"inputs":[{"name":"timestamp","type":"uint256"}],"name":"getMonth","outputs":[{"name":"","type":"uint16"}],"type":"function"},{"constant":true,"inputs":[{"name":"year","type":"uint16"}],"name":"isLeapYear","outputs":[{"name":"","type":"bool"}],"type":"function"},{"constant":false,"inputs":[],"name":"__throw","outputs":[],"type":"function"},{"constant":true,"inputs":[{"name":"timestamp","type":"uint256"}],"name":"getMinute","outputs":[{"name":"","type":"uint16"}],"type":"function"}]'
PCS_ABI = '[{"inputs":[{"internalType":"address","name":"_factory","type":"address"},{"internalType":"address","name":"_WETH","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[],"name":"WETH","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"},{"internalType":"uint256","name":"amountADesired","type":"uint256"},{"internalType":"uint256","name":"amountBDesired","type":"uint256"},{"internalType":"uint256","name":"amountAMin","type":"uint256"},{"internalType":"uint256","name":"amountBMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"addLiquidity","outputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256","name":"amountB","type":"uint256"},{"internalType":"uint256","name":"liquidity","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"amountTokenDesired","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"addLiquidityETH","outputs":[{"internalType":"uint256","name":"amountToken","type":"uint256"},{"internalType":"uint256","name":"amountETH","type":"uint256"},{"internalType":"uint256","name":"liquidity","type":"uint256"}],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"factory","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"uint256","name":"reserveIn","type":"uint256"},{"internalType":"uint256","name":"reserveOut","type":"uint256"}],"name":"getAmountIn","outputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"reserveIn","type":"uint256"},{"internalType":"uint256","name":"reserveOut","type":"uint256"}],"name":"getAmountOut","outputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"}],"name":"getAmountsIn","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"}],"name":"getAmountsOut","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256","name":"reserveA","type":"uint256"},{"internalType":"uint256","name":"reserveB","type":"uint256"}],"name":"quote","outputs":[{"internalType":"uint256","name":"amountB","type":"uint256"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountAMin","type":"uint256"},{"internalType":"uint256","name":"amountBMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"removeLiquidity","outputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256","name":"amountB","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"removeLiquidityETH","outputs":[{"internalType":"uint256","name":"amountToken","type":"uint256"},{"internalType":"uint256","name":"amountETH","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"removeLiquidityETHSupportingFeeOnTransferTokens","outputs":[{"internalType":"uint256","name":"amountETH","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"bool","name":"approveMax","type":"bool"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"removeLiquidityETHWithPermit","outputs":[{"internalType":"uint256","name":"amountToken","type":"uint256"},{"internalType":"uint256","name":"amountETH","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"bool","name":"approveMax","type":"bool"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"removeLiquidityETHWithPermitSupportingFeeOnTransferTokens","outputs":[{"internalType":"uint256","name":"amountETH","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountAMin","type":"uint256"},{"internalType":"uint256","name":"amountBMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"bool","name":"approveMax","type":"bool"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"removeLiquidityWithPermit","outputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256","name":"amountB","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapETHForExactTokens","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactETHForTokens","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactETHForTokensSupportingFeeOnTransferTokens","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForETH","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForETHSupportingFeeOnTransferTokens","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForTokens","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForTokensSupportingFeeOnTransferTokens","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"uint256","name":"amountInMax","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapTokensForExactETH","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"uint256","name":"amountInMax","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapTokensForExactTokens","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"stateMutability":"payable","type":"receive"}]'
PCS_ROUTER_CA = '0x10ED43C718714eb63d5aA57B78B54704E256024E'

## ApeSwap ##
APE_ABI = '[{"inputs":[{"internalType":"address","name":"_factory","type":"address"},{"internalType":"address","name":"_WETH","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[],"name":"WETH","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"},{"internalType":"uint256","name":"amountADesired","type":"uint256"},{"internalType":"uint256","name":"amountBDesired","type":"uint256"},{"internalType":"uint256","name":"amountAMin","type":"uint256"},{"internalType":"uint256","name":"amountBMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"addLiquidity","outputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256","name":"amountB","type":"uint256"},{"internalType":"uint256","name":"liquidity","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"amountTokenDesired","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"addLiquidityETH","outputs":[{"internalType":"uint256","name":"amountToken","type":"uint256"},{"internalType":"uint256","name":"amountETH","type":"uint256"},{"internalType":"uint256","name":"liquidity","type":"uint256"}],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"factory","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"uint256","name":"reserveIn","type":"uint256"},{"internalType":"uint256","name":"reserveOut","type":"uint256"}],"name":"getAmountIn","outputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"reserveIn","type":"uint256"},{"internalType":"uint256","name":"reserveOut","type":"uint256"}],"name":"getAmountOut","outputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"}],"name":"getAmountsIn","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"}],"name":"getAmountsOut","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256","name":"reserveA","type":"uint256"},{"internalType":"uint256","name":"reserveB","type":"uint256"}],"name":"quote","outputs":[{"internalType":"uint256","name":"amountB","type":"uint256"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountAMin","type":"uint256"},{"internalType":"uint256","name":"amountBMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"removeLiquidity","outputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256","name":"amountB","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"removeLiquidityETH","outputs":[{"internalType":"uint256","name":"amountToken","type":"uint256"},{"internalType":"uint256","name":"amountETH","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"removeLiquidityETHSupportingFeeOnTransferTokens","outputs":[{"internalType":"uint256","name":"amountETH","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"bool","name":"approveMax","type":"bool"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"removeLiquidityETHWithPermit","outputs":[{"internalType":"uint256","name":"amountToken","type":"uint256"},{"internalType":"uint256","name":"amountETH","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"bool","name":"approveMax","type":"bool"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"removeLiquidityETHWithPermitSupportingFeeOnTransferTokens","outputs":[{"internalType":"uint256","name":"amountETH","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountAMin","type":"uint256"},{"internalType":"uint256","name":"amountBMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"bool","name":"approveMax","type":"bool"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"removeLiquidityWithPermit","outputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256","name":"amountB","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapETHForExactTokens","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactETHForTokens","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactETHForTokensSupportingFeeOnTransferTokens","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForETH","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForETHSupportingFeeOnTransferTokens","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForTokens","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForTokensSupportingFeeOnTransferTokens","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"uint256","name":"amountInMax","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapTokensForExactETH","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"uint256","name":"amountInMax","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapTokensForExactTokens","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"stateMutability":"payable","type":"receive"}]'
APE_ROUTER_CA = '0xcF0feBd3f17CEf5b47b0cD257aCf6025c5BFf3b7'

## Token common ABI ##
token_ABI = '[{"inputs":[{"internalType":"string","name":"_NAME","type":"string"},{"internalType":"string","name":"_SYMBOL","type":"string"},{"internalType":"uint256","name":"_DECIMALS","type":"uint256"},{"internalType":"uint256","name":"_supply","type":"uint256"},{"internalType":"uint256","name":"_txFee","type":"uint256"},{"internalType":"uint256","name":"_lpFee","type":"uint256"},{"internalType":"uint256","name":"_MAXAMOUNT","type":"uint256"},{"internalType":"uint256","name":"SELLMAXAMOUNT","type":"uint256"},{"internalType":"address","name":"routerAddress","type":"address"},{"internalType":"address","name":"tokenOwner","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"spender","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"minTokensBeforeSwap","type":"uint256"}],"name":"MinTokensBeforeSwapUpdated","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"tokensSwapped","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"ethReceived","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"tokensIntoLiqudity","type":"uint256"}],"name":"SwapAndLiquify","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"bool","name":"enabled","type":"bool"}],"name":"SwapAndLiquifyEnabledUpdated","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"inputs":[],"name":"_liquidityFee","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"_maxTxAmount","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"_owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"_taxFee","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"claimTokens","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"subtractedValue","type":"uint256"}],"name":"decreaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"tAmount","type":"uint256"}],"name":"deliver","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"excludeFromFee","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"excludeFromReward","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"geUnlockTime","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"includeInFee","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"includeInReward","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"addedValue","type":"uint256"}],"name":"increaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"isExcludedFromFee","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"isExcludedFromReward","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"time","type":"uint256"}],"name":"lock","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"numTokensSellToAddToLiquidity","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"tAmount","type":"uint256"},{"internalType":"bool","name":"deductTransferFee","type":"bool"}],"name":"reflectionFromToken","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"liquidityFee","type":"uint256"}],"name":"setLiquidityFeePercent","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"maxTxPercent","type":"uint256"}],"name":"setMaxTxPercent","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"swapNumber","type":"uint256"}],"name":"setNumTokensSellToAddToLiquidity","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bool","name":"_enabled","type":"bool"}],"name":"setSwapAndLiquifyEnabled","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"taxFee","type":"uint256"}],"name":"setTaxFeePercent","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"swapAndLiquifyEnabled","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"rAmount","type":"uint256"}],"name":"tokenFromReflection","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalFees","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"sender","type":"address"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"uniswapV2Pair","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"uniswapV2Router","outputs":[{"internalType":"contract IUniswapV2Router02","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"unlock","outputs":[],"stateMutability":"nonpayable","type":"function"},{"stateMutability":"payable","type":"receive"}]'
ERC20abi_BSC = '[{"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"spender","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"constant":true,"inputs":[],"name":"_decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"_name","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"_symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"burn","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"subtractedValue","type":"uint256"}],"name":"decreaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"getOwner","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"addedValue","type":"uint256"}],"name":"increaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"mint","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[],"name":"renounceOwnership","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"sender","type":"address"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"}]'

## Checker ##
CHECKER_CA = "0x18be7f977Ec1217B71D0C134FBCFF36Ea4366fCD"
CHECKER_ABI = '[{"inputs":[{"internalType": "address","name": "_factory","type": "address"},{"internalType": "address","name": "_WETH","type": "address"},{"internalType": "address","name": "_UTILS","type": "address"},{"internalType": "address","name": "_TIGS","type": "address"}],"stateMutability": "nonpayable","type": "constructor"},{"inputs": [],"name": "DEV","outputs": [{"internalType": "address","name": "","type": "address"}],"stateMutability": "view","type": "function"},{"inputs": [],"name": "FEE","outputs": [{"internalType": "uint256","name": "","type": "uint256"}],"stateMutability": "view","type": "function"},{"inputs": [],"name": "FEEQuote","outputs": [{"internalType": "uint256","name": "","type": "uint256"}],"stateMutability": "view","type": "function"},{"inputs": [],"name": "LimitSwap","outputs": [{"internalType": "address","name": "","type": "address"}],"stateMutability": "view","type": "function"},{"inputs": [],"name": "STATUS","outputs": [{"internalType": "bool","name": "","type": "bool"}],"stateMutability": "view","type": "function"},{"inputs": [],"name": "TIGS","outputs": [{"internalType": "address","name": "","type": "address"}],"stateMutability": "view","type": "function"},{"inputs": [],"name": "TIGSStaking","outputs": [{"internalType": "address","name": "","type": "address"}],"stateMutability": "view","type": "function"},{"inputs": [],"name": "UTILS","outputs": [{"internalType": "contract TIGSSwapUtils","name": "","type": "address"}],"stateMutability": "view","type": "function"},{"inputs": [],"name": "WETH","outputs": [{"internalType": "address","name": "","type": "address"}],"stateMutability": "view","type": "function"},{"inputs": [{"internalType": "address","name": "_token","type": "address"},{"internalType": "address","name": "_spender","type": "address"}],"name": "approveToken","outputs": [],"stateMutability": "nonpayable","type": "function"},{"inputs": [],"name": "factory","outputs": [{"internalType": "address","name": "","type": "address"}],"stateMutability": "view","type": "function"},{"inputs": [{"internalType": "address","name": "Token","type": "address"}],"name": "fetchBestBaseToken","outputs": [{"internalType": "address","name": "","type": "address"}],"stateMutability": "view","type": "function"},{"inputs": [{"internalType": "address","name": "Token","type": "address"}],"name": "fetchLiquidityETH","outputs": [{"internalType": "uint256","name": "","type": "uint256"}],"stateMutability": "view","type": "function"},{"inputs": [{"internalType": "address","name": "owner","type": "address"},{"internalType": "address","name": "Token","type": "address"},{"internalType": "uint256","name": "Slippage","type": "uint256"}],"name": "fromETHtoToken","outputs": [],"stateMutability": "payable","type": "function"},{"inputs": [{"internalType": "address","name": "owner","type": "address"},{"internalType": "address","name": "Token","type": "address"},{"internalType": "uint256","name": "amount","type": "uint256"},{"internalType": "uint256","name": "Slippage","type": "uint256"}],"name": "fromTokentoETH","outputs": [],"stateMutability": "nonpayable","type": "function"},{"inputs": [{"internalType": "address","name": "owner","type": "address"},{"internalType": "address","name": "TokenA","type": "address"},{"internalType": "address","name": "TokenB","type": "address"},{"internalType": "uint256","name": "amount","type": "uint256"},{"internalType": "uint256","name": "Slippage","type": "uint256"}],"name": "fromTokentoToken","outputs": [],"stateMutability": "nonpayable","type": "function"},{"inputs": [{"internalType": "uint256","name": "amountOut","type": "uint256"},{"internalType": "uint256","name": "reserveIn","type": "uint256"},{"internalType": "uint256","name": "reserveOut","type": "uint256"}],"name": "getAmountIn","outputs": [{"internalType": "uint256","name": "amountIn","type": "uint256"}],"stateMutability": "pure","type": "function"},{"inputs": [{"internalType": "uint256","name": "amountIn","type": "uint256"},{"internalType": "uint256","name": "reserveIn","type": "uint256"},{"internalType": "uint256","name": "reserveOut","type": "uint256"}],"name": "getAmountOut","outputs": [{"internalType": "uint256","name": "amountOut","type": "uint256"}],"stateMutability": "pure","type": "function"},{"inputs": [{"internalType": "uint256","name": "amountOut","type": "uint256"},{"internalType": "address[]","name": "path","type": "address[]"}],"name": "getAmountsIn","outputs": [{"internalType": "uint256[]","name": "amounts","type": "uint256[]"}],"stateMutability": "view","type": "function"},{"inputs": [{"internalType": "uint256","name": "amountIn","type": "uint256"},{"internalType": "address[]","name": "path","type": "address[]"}],"name": "getAmountsOut","outputs": [{"internalType": "uint256[]","name": "amounts","type": "uint256[]"}],"stateMutability": "view","type": "function"},{"inputs": [{"internalType": "address","name": "Token","type": "address"},{"internalType": "uint256","name": "amount","type": "uint256"}],"name": "getOutputfromETHtoToken","outputs": [{"internalType": "uint256","name": "","type": "uint256"},{"internalType": "address[]","name": "","type": "address[]"}],"stateMutability": "view","type": "function"},{"inputs": [{"internalType": "address","name": "Token","type": "address"},{"internalType": "uint256","name": "amount","type": "uint256"}],"name": "getOutputfromTokentoETH","outputs": [{"internalType": "uint256","name": "","type": "uint256"},{"internalType": "address[]","name": "","type": "address[]"}],"stateMutability": "view","type": "function"},{"inputs": [{"internalType": "address","name": "TokenA","type": "address"},{"internalType": "address","name": "TokenB","type": "address"},{"internalType": "uint256","name": "amount","type": "uint256"}],"name": "getOutputfromTokentoToken","outputs": [{"internalType": "uint256","name": "","type": "uint256"},{"internalType": "address[]","name": "","type": "address[]"}],"stateMutability": "view","type": "function"},{"inputs": [{"internalType": "address","name": "Token","type": "address"}],"name": "getTokenInformations","outputs": [{"internalType": "uint256","name": "BuyEstimateOutput","type": "uint256"},{"internalType": "uint256","name": "BuyRealOutput","type": "uint256"},{"internalType": "uint256","name": "SellEstimateOutput","type": "uint256"},{"internalType": "uint256","name": "SellRealOutput","type": "uint256"},{"internalType": "bool","name": "Buy","type": "bool"},{"internalType": "bool","name": "Approve","type": "bool"},{"internalType": "bool","name": "Sell","type": "bool"}],"stateMutability": "nonpayable","type": "function"},{"inputs": [],"name": "makeBuyback","outputs": [],"stateMutability": "nonpayable","type": "function"},{"inputs": [],"name": "minWETH","outputs": [{"internalType": "uint256","name": "","type": "uint256"}],"stateMutability": "view","type": "function"},{"inputs": [{"internalType": "address","name": "input","type": "address"},{"internalType": "address","name": "output","type": "address"}],"name": "pairFor","outputs": [{"internalType": "address","name": "","type": "address"}],"stateMutability": "view","type": "function"},{"inputs": [{"internalType": "address","name": "_factory","type": "address"},{"internalType": "address","name": "path1","type": "address"},{"internalType": "address","name": "path2","type": "address"}],"name": "pairForTest","outputs": [{"internalType": "address","name": "","type": "address"}],"stateMutability": "pure","type": "function"},{"inputs": [{"internalType": "uint256","name": "amountA","type": "uint256"},{"internalType": "uint256","name": "reserveA","type": "uint256"},{"internalType": "uint256","name": "reserveB","type": "uint256"}],"name": "quote","outputs": [{"internalType": "uint256","name": "amountB","type": "uint256"}],"stateMutability": "pure","type": "function"},{"inputs": [{"internalType": "uint256","name": "_FEE","type": "uint256"},{"internalType": "uint256","name": "_FEEQuote","type": "uint256"},{"internalType": "uint256","name": "_minWETH","type": "uint256"}],"name": "setFeeOptions","outputs": [],"stateMutability": "nonpayable","type": "function"},{"inputs": [{"internalType": "address","name": "_LimitSwap","type": "address"}],"name": "setLimitSwapContract","outputs": [],"stateMutability": "nonpayable","type": "function"},{"inputs": [{"internalType": "address","name": "_UTILS","type": "address"}],"name": "setNewUtils","outputs": [],"stateMutability": "nonpayable","type": "function"},{"inputs": [{"internalType": "bool","name": "_new","type": "bool"}],"name": "setStatus","outputs": [],"stateMutability": "nonpayable","type": "function"},{"inputs": [{"internalType": "uint256","name": "amountIn","type": "uint256"},{"internalType": "uint256","name": "amountOutMin","type": "uint256"},{"internalType": "address[]","name": "path","type": "address[]"},{"internalType": "address","name": "to","type": "address"},{"internalType": "uint256","name": "deadline","type": "uint256"}],"name": "swapExactTokensForTokensAdmin","outputs": [],"stateMutability": "nonpayable","type": "function"},{"stateMutability": "payable","type": "receive"}]'

## UniCrypt ##
UniABI = '[{"inputs":[{"internalType":"address","name":"_presaleGenerator","type":"address"},{"internalType":"contract IPresaleSettings","name":"_presaleSettings","type":"address"},{"internalType":"address","name":"_tokenVesting","type":"address"},{"internalType":"address","name":"_weth","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"BUYERS","outputs":[{"internalType":"uint256","name":"baseDeposited","type":"uint256"},{"internalType":"uint256","name":"tokensOwed","type":"uint256"},{"internalType":"uint256","name":"unclOwed","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"CONTRACT_VERSION","outputs":[{"internalType":"uint16","name":"","type":"uint16"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"PRESALE_FEE_INFO","outputs":[{"internalType":"uint256","name":"UNICRYPT_BASE_FEE","type":"uint256"},{"internalType":"uint256","name":"UNICRYPT_TOKEN_FEE","type":"uint256"},{"internalType":"uint256","name":"REFERRAL_FEE","type":"uint256"},{"internalType":"address payable","name":"REFERRAL_1","type":"address"},{"internalType":"address payable","name":"REFERRAL_2","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"PRESALE_GENERATOR","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"PRESALE_INFO","outputs":[{"internalType":"contract IERC20","name":"S_TOKEN","type":"address"},{"internalType":"contract IERC20","name":"B_TOKEN","type":"address"},{"internalType":"uint256","name":"TOKEN_PRICE","type":"uint256"},{"internalType":"uint256","name":"MAX_SPEND_PER_BUYER","type":"uint256"},{"internalType":"uint256","name":"AMOUNT","type":"uint256"},{"internalType":"uint256","name":"HARDCAP","type":"uint256"},{"internalType":"uint256","name":"SOFTCAP","type":"uint256"},{"internalType":"uint256","name":"LIQUIDITY_PERCENT","type":"uint256"},{"internalType":"uint256","name":"LISTING_RATE","type":"uint256"},{"internalType":"uint256","name":"START_BLOCK","type":"uint256"},{"internalType":"uint256","name":"END_BLOCK","type":"uint256"},{"internalType":"uint256","name":"LOCK_PERIOD","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"PRESALE_INFO_2","outputs":[{"internalType":"address payable","name":"PRESALE_OWNER","type":"address"},{"internalType":"bool","name":"PRESALE_IN_ETH","type":"bool"},{"internalType":"uint16","name":"COUNTRY_CODE","type":"uint16"},{"internalType":"uint128","name":"UNCL_MAX_PARTICIPANTS","type":"uint128"},{"internalType":"uint128","name":"UNCL_PARTICIPANTS","type":"uint128"},{"internalType":"uint128","name":"WHITELIST_MAX_PARTICIPANTS","type":"uint128"},{"internalType":"uint128","name":"WHITELIST_ASSIGNED","type":"uint128"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"PRESALE_LOCK_FORWARDER","outputs":[{"internalType":"contract IPresaleLockForwarder","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"PRESALE_SETTINGS","outputs":[{"internalType":"contract IPresaleSettings","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"PRESALE_VESTING","outputs":[{"internalType":"bool","name":"REQUEST_VESTING","type":"bool"},{"internalType":"bool","name":"IMPLEMENT_VESTING","type":"bool"},{"internalType":"bool","name":"LINEAR_LOCK","type":"bool"},{"internalType":"uint256","name":"VESTING_START_EMISSION","type":"uint256"},{"internalType":"uint256","name":"VESTING_END_EMISSION","type":"uint256"},{"internalType":"uint256","name":"VESTING_PERCENTAGE","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"STATUS","outputs":[{"internalType":"bool","name":"LP_GENERATION_COMPLETE","type":"bool"},{"internalType":"bool","name":"FORCE_FAILED","type":"bool"},{"internalType":"uint256","name":"TOTAL_BASE_COLLECTED","type":"uint256"},{"internalType":"uint256","name":"TOTAL_TOKENS_SOLD","type":"uint256"},{"internalType":"uint256","name":"TOTAL_TOKENS_WITHDRAWN","type":"uint256"},{"internalType":"uint256","name":"TOTAL_BASE_WITHDRAWN","type":"uint256"},{"internalType":"uint256","name":"ROUND1_LENGTH","type":"uint256"},{"internalType":"uint256","name":"ROUND_0_START","type":"uint256"},{"internalType":"uint256","name":"NUM_BUYERS","type":"uint256"},{"internalType":"uint256","name":"PRESALE_END_DATE","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"TOKEN_VESTING","outputs":[{"internalType":"contract ITokenVesting","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"UNCL_AMOUNT_OVERRIDE","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"UNCL_BURN_ON_FAIL","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"UNI_FACTORY","outputs":[{"internalType":"contract IUniswapV2Factory","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"WETH","outputs":[{"internalType":"contract IWETH","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"addLiquidity","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address[]","name":"_users","type":"address[]"},{"internalType":"bool","name":"_add","type":"bool"}],"name":"editWhitelist","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"forceFailByPresaleOwner","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"forceFailByUnicrypt","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"getElapsedSinceRound0","outputs":[{"internalType":"int256","name":"","type":"int256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getElapsedSinceRound1","outputs":[{"internalType":"int256","name":"","type":"int256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getInfo","outputs":[{"internalType":"uint16","name":"","type":"uint16"},{"components":[{"internalType":"contract IERC20","name":"S_TOKEN","type":"address"},{"internalType":"contract IERC20","name":"B_TOKEN","type":"address"},{"internalType":"uint256","name":"TOKEN_PRICE","type":"uint256"},{"internalType":"uint256","name":"MAX_SPEND_PER_BUYER","type":"uint256"},{"internalType":"uint256","name":"AMOUNT","type":"uint256"},{"internalType":"uint256","name":"HARDCAP","type":"uint256"},{"internalType":"uint256","name":"SOFTCAP","type":"uint256"},{"internalType":"uint256","name":"LIQUIDITY_PERCENT","type":"uint256"},{"internalType":"uint256","name":"LISTING_RATE","type":"uint256"},{"internalType":"uint256","name":"START_BLOCK","type":"uint256"},{"internalType":"uint256","name":"END_BLOCK","type":"uint256"},{"internalType":"uint256","name":"LOCK_PERIOD","type":"uint256"}],"internalType":"struct Presale01.PresaleInfo","name":"","type":"tuple"},{"components":[{"internalType":"address payable","name":"PRESALE_OWNER","type":"address"},{"internalType":"bool","name":"PRESALE_IN_ETH","type":"bool"},{"internalType":"uint16","name":"COUNTRY_CODE","type":"uint16"},{"internalType":"uint128","name":"UNCL_MAX_PARTICIPANTS","type":"uint128"},{"internalType":"uint128","name":"UNCL_PARTICIPANTS","type":"uint128"},{"internalType":"uint128","name":"WHITELIST_MAX_PARTICIPANTS","type":"uint128"},{"internalType":"uint128","name":"WHITELIST_ASSIGNED","type":"uint128"}],"internalType":"struct Presale01.PresaleInfo2","name":"","type":"tuple"},{"components":[{"internalType":"uint256","name":"UNICRYPT_BASE_FEE","type":"uint256"},{"internalType":"uint256","name":"UNICRYPT_TOKEN_FEE","type":"uint256"},{"internalType":"uint256","name":"REFERRAL_FEE","type":"uint256"},{"internalType":"address payable","name":"REFERRAL_1","type":"address"},{"internalType":"address payable","name":"REFERRAL_2","type":"address"}],"internalType":"struct Presale01.PresaleFeeInfo","name":"","type":"tuple"},{"components":[{"internalType":"bool","name":"LP_GENERATION_COMPLETE","type":"bool"},{"internalType":"bool","name":"FORCE_FAILED","type":"bool"},{"internalType":"uint256","name":"TOTAL_BASE_COLLECTED","type":"uint256"},{"internalType":"uint256","name":"TOTAL_TOKENS_SOLD","type":"uint256"},{"internalType":"uint256","name":"TOTAL_TOKENS_WITHDRAWN","type":"uint256"},{"internalType":"uint256","name":"TOTAL_BASE_WITHDRAWN","type":"uint256"},{"internalType":"uint256","name":"ROUND1_LENGTH","type":"uint256"},{"internalType":"uint256","name":"ROUND_0_START","type":"uint256"},{"internalType":"uint256","name":"NUM_BUYERS","type":"uint256"},{"internalType":"uint256","name":"PRESALE_END_DATE","type":"uint256"}],"internalType":"struct Presale01.PresaleStatus","name":"","type":"tuple"},{"components":[{"internalType":"bool","name":"REQUEST_VESTING","type":"bool"},{"internalType":"bool","name":"IMPLEMENT_VESTING","type":"bool"},{"internalType":"bool","name":"LINEAR_LOCK","type":"bool"},{"internalType":"uint256","name":"VESTING_START_EMISSION","type":"uint256"},{"internalType":"uint256","name":"VESTING_END_EMISSION","type":"uint256"},{"internalType":"uint256","name":"VESTING_PERCENTAGE","type":"uint256"}],"internalType":"struct Presale01.PresaleVesting","name":"","type":"tuple"},{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_start","type":"uint256"},{"internalType":"uint256","name":"_count","type":"uint256"}],"name":"getPagedWhitelist","outputs":[{"components":[{"internalType":"address","name":"userAddress","type":"address"},{"internalType":"uint256","name":"baseDeposited","type":"uint256"}],"internalType":"struct Presale01.WhitelistPager[]","name":"","type":"tuple[]"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getUNCLOverride","outputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_user","type":"address"}],"name":"getUserWhitelistStatus","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_index","type":"uint256"}],"name":"getWhitelistedUserAtIndex","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getWhitelistedUsersLength","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint16","name":"_countryCode","type":"uint16"},{"internalType":"uint256","name":"_amount","type":"uint256"},{"internalType":"uint256","name":"_tokenPrice","type":"uint256"},{"internalType":"uint256","name":"_maxEthPerBuyer","type":"uint256"},{"internalType":"uint256","name":"_hardcap","type":"uint256"},{"internalType":"uint256","name":"_softcap","type":"uint256"},{"internalType":"uint256","name":"_liquidityPercent","type":"uint256"},{"internalType":"uint256","name":"_listingRate","type":"uint256"},{"internalType":"uint256","name":"_roundZeroStart","type":"uint256"},{"internalType":"uint256","name":"_startblock","type":"uint256"},{"internalType":"uint256","name":"_endblock","type":"uint256"},{"internalType":"uint256","name":"_lockPeriod","type":"uint256"}],"name":"init1","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address payable","name":"_presaleOwner","type":"address"},{"internalType":"contract IERC20","name":"_baseToken","type":"address"},{"internalType":"contract IERC20","name":"_presaleToken","type":"address"},{"internalType":"uint256","name":"_unicryptBaseFee","type":"uint256"},{"internalType":"uint256","name":"_unicryptTokenFee","type":"uint256"},{"internalType":"uint256","name":"_referralFee","type":"uint256"},{"internalType":"address payable","name":"_referral_1","type":"address"},{"internalType":"address payable","name":"_referral_2","type":"address"},{"internalType":"bool","name":"_requestVesting","type":"bool"}],"name":"init2","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"ownerWithdrawTokens","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"presaleStatus","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"reserveAllocationWithUNCL","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address payable","name":"_referrer","type":"address"}],"name":"setReferrer","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bool","name":"_implementVesting","type":"bool"},{"internalType":"bool","name":"_linearLock","type":"bool"},{"internalType":"uint256","name":"_startIncrement","type":"uint256"},{"internalType":"uint256","name":"_endIncrement","type":"uint256"},{"internalType":"uint256","name":"_percentage","type":"uint256"}],"name":"setTokenVestingParams","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"setUNCLAmount","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_startBlock","type":"uint256"},{"internalType":"uint256","name":"_endBlock","type":"uint256"}],"name":"updateBlocks","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"userDeposit","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"userWithdrawBaseTokens","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"userWithdrawTokens","outputs":[],"stateMutability":"nonpayable","type":"function"}]'
UNCL_proxy_abi = '[{"constant":true,"inputs":[],"name":"mintingFinished","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"name","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"approve","outputs":[{"name":"result","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"_bridgeContract","type":"address"}],"name":"setBridgeContract","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_sender","type":"address"},{"name":"_recipient","type":"address"},{"name":"_amount","type":"uint256"}],"name":"transferFrom","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"PERMIT_TYPEHASH","outputs":[{"name":"","type":"bytes32"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"DOMAIN_SEPARATOR","outputs":[{"name":"","type":"bytes32"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_to","type":"address"},{"name":"_addedValue","type":"uint256"}],"name":"increaseAllowance","outputs":[{"name":"result","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"_to","type":"address"},{"name":"_value","type":"uint256"},{"name":"_data","type":"bytes"}],"name":"transferAndCall","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"_to","type":"address"},{"name":"_amount","type":"uint256"}],"name":"mint","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"_value","type":"uint256"}],"name":"burn","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"version","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_spender","type":"address"},{"name":"_subtractedValue","type":"uint256"}],"name":"decreaseApproval","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"_token","type":"address"},{"name":"_to","type":"address"}],"name":"claimTokens","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"_owner","type":"address"}],"name":"balanceOf","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[],"name":"renounceOwnership","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"_address","type":"address"}],"name":"isBridge","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[],"name":"finishMinting","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"","type":"address"}],"name":"nonces","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"getTokenInterfacesVersion","outputs":[{"name":"major","type":"uint64"},{"name":"minor","type":"uint64"},{"name":"patch","type":"uint64"}],"payable":false,"stateMutability":"pure","type":"function"},{"constant":true,"inputs":[],"name":"owner","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_holder","type":"address"},{"name":"_spender","type":"address"},{"name":"_nonce","type":"uint256"},{"name":"_expiry","type":"uint256"},{"name":"_allowed","type":"bool"},{"name":"_v","type":"uint8"},{"name":"_r","type":"bytes32"},{"name":"_s","type":"bytes32"}],"name":"permit","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"symbol","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"spender","type":"address"},{"name":"subtractedValue","type":"uint256"}],"name":"decreaseAllowance","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transfer","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"_to","type":"address"},{"name":"_amount","type":"uint256"}],"name":"push","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"_from","type":"address"},{"name":"_to","type":"address"},{"name":"_amount","type":"uint256"}],"name":"move","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"bridgeContract","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_spender","type":"address"},{"name":"_addedValue","type":"uint256"}],"name":"increaseApproval","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"_owner","type":"address"},{"name":"_spender","type":"address"}],"name":"allowance","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_from","type":"address"},{"name":"_amount","type":"uint256"}],"name":"pull","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"_newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"","type":"address"},{"name":"","type":"address"}],"name":"expirations","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"inputs":[{"name":"_name","type":"string"},{"name":"_symbol","type":"string"},{"name":"_decimals","type":"uint8"},{"name":"_chainId","type":"uint256"}],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"name":"to","type":"address"},{"indexed":false,"name":"amount","type":"uint256"}],"name":"Mint","type":"event"},{"anonymous":false,"inputs":[],"name":"MintFinished","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"previousOwner","type":"address"}],"name":"OwnershipRenounced","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"previousOwner","type":"address"},{"indexed":true,"name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"burner","type":"address"},{"indexed":false,"name":"value","type":"uint256"}],"name":"Burn","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"from","type":"address"},{"indexed":true,"name":"to","type":"address"},{"indexed":false,"name":"value","type":"uint256"},{"indexed":false,"name":"data","type":"bytes"}],"name":"Transfer","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"owner","type":"address"},{"indexed":true,"name":"spender","type":"address"},{"indexed":false,"name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"from","type":"address"},{"indexed":true,"name":"to","type":"address"},{"indexed":false,"name":"value","type":"uint256"}],"name":"Transfer","type":"event"}]'
UNCL_CA = '0x0e8d5504bf54d9e44260f8d153ecd5412130cabb'

## BNB &BUSD & USDT##
WBNB_add = "0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c"
WBNB_Decimal = 18
BUSD_add = "0xe9e7CEA3DedcA5984780Bafc599bD69ADd087D56"
BUSD_Abi = '[{"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"spender","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"constant":true,"inputs":[],"name":"_decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"_name","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"_symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"burn","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"subtractedValue","type":"uint256"}],"name":"decreaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"getOwner","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"addedValue","type":"uint256"}],"name":"increaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"mint","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[],"name":"renounceOwnership","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"sender","type":"address"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"}]'
BUSD_Decimal = 18
USDT_add = "0x55d398326f99059fF775485246999027B3197955"
USDT_Abi = '[{"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"spender","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"constant":true,"inputs":[],"name":"_decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"_name","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"_symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"burn","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"subtractedValue","type":"uint256"}],"name":"decreaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"getOwner","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"addedValue","type":"uint256"}],"name":"increaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"mint","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[],"name":"renounceOwnership","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"sender","type":"address"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"}]'
USDT_Decimal = 18

## LP check
factory = "0xcA143Ce32Fe78f1f7019d7d551a6402fC5350c73"
hexadem_= '0x00fb7f630766e6a796048ea87d01acd3068e8ff67d078148a3fa3f4a84f69bd5' ## PancakeSwap Hexadem

## License ABI
License_ABI = '[{"inputs": [{"internalType": "string","name": "name","type": "string"},{"internalType": "string","name": "symbol","type": "string"},{"internalType": "uint8","name": "decimals","type": "uint8"}],"payable": false,"stateMutability": "nonpayable","type": "constructor"},{"anonymous": false,"inputs": [{"indexed": true,"internalType": "address","name": "owner","type": "address"},{"indexed": true,"internalType": "address","name": "spender","type": "address"},{"indexed": false,"internalType": "uint256","name": "value","type": "uint256"}],"name": "Approval","type": "event"},{"anonymous": false,"inputs": [{"indexed": true,"internalType": "address","name": "from","type": "address"},{"indexed": true,"internalType": "address","name": "to","type": "address"},{"indexed": false,"internalType": "uint256","name": "value","type": "uint256"}],"name": "Transfer","type": "event"},{"constant": true,"inputs": [{"internalType": "address","name": "account_wallet","type": "address"}],"name": "EndLicenseOf","outputs": [{"internalType": "uint256","name": "","type": "uint256"}],"payable": false,"stateMutability": "view","type": "function"},{"constant": true,"inputs": [{"internalType": "address","name": "account_wallet","type": "address"}],"name": "IsDemo","outputs": [{"internalType": "uint256","name": "","type": "uint256"}],"payable": false,"stateMutability": "view","type": "function"},{"constant": true,"inputs": [{"internalType": "address","name": "account_wallet","type": "address"}],"name": "IsFull","outputs": [{"internalType": "uint256","name": "","type": "uint256"}],"payable": false,"stateMutability": "view","type": "function"},{"constant": true,"inputs": [],"name": "ShowTotalDemoDay","outputs": [{"internalType": "uint256","name": "","type": "uint256"}],"payable": false,"stateMutability": "view","type": "function"},{"constant": true,"inputs": [{"internalType": "address","name": "account_wallet","type": "address"}],"name": "StartLicenseOf","outputs": [{"internalType": "uint256","name": "","type": "uint256"}],"payable": false,"stateMutability": "view","type": "function"},{"constant": true,"inputs": [],"name": "_Tokenowner","outputs": [{"internalType": "string","name": "","type": "string"}],"payable": false,"stateMutability": "view","type": "function"},{"constant": true,"inputs": [{"internalType": "address","name": "owner","type": "address"},{"internalType": "address","name": "spender","type": "address"}],"name": "allowance","outputs": [{"internalType": "uint256","name": "","type": "uint256"}],"payable": false,"stateMutability": "view","type": "function"},{"constant": false,"inputs": [{"internalType": "address","name": "spender","type": "address"},{"internalType": "uint256","name": "value","type": "uint256"}],"name": "approve","outputs": [{"internalType": "bool","name": "","type": "bool"}],"payable": false,"stateMutability": "nonpayable","type": "function"},{"constant": true,"inputs": [{"internalType": "address","name": "who","type": "address"}],"name": "balanceOf","outputs": [{"internalType": "uint256","name": "","type": "uint256"}],"payable": false,"stateMutability": "view","type": "function"},{"constant": true,"inputs": [],"name": "decimals","outputs": [{"internalType": "uint8","name": "","type": "uint8"}],"payable": false,"stateMutability": "view","type": "function"},{"constant": true,"inputs": [],"name": "name","outputs": [{"internalType": "string","name": "","type": "string"}],"payable": false,"stateMutability": "view","type": "function"},{"constant": true,"inputs": [],"name": "symbol","outputs": [{"internalType": "string","name": "","type": "string"}],"payable": false,"stateMutability": "view","type": "function"},{"constant": true,"inputs": [],"name": "totalSupply","outputs": [{"internalType": "uint256","name": "","type": "uint256"}],"payable": false,"stateMutability": "view","type": "function"},{"constant": false,"inputs": [{"internalType": "address","name": "to","type": "address"},{"internalType": "uint256","name": "value","type": "uint256"}],"name": "transferDemoLic","outputs": [{"internalType": "bool","name": "","type": "bool"}],"payable": false,"stateMutability": "nonpayable","type": "function"},{"constant": false,"inputs": [{"internalType": "address","name": "from","type": "address"},{"internalType": "address","name": "to","type": "address"},{"internalType": "uint256","name": "value","type": "uint256"}],"name": "transferFrom","outputs": [{"internalType": "bool","name": "","type": "bool"}],"payable": false,"stateMutability": "nonpayable","type": "function"},{"constant": false,"inputs": [{"internalType": "address","name": "to","type": "address"},{"internalType": "uint256","name": "value","type": "uint256"}],"name": "transferFullLic","outputs": [{"internalType": "bool","name": "","type": "bool"}],"payable": false,"stateMutability": "nonpayable","type": "function"}]'
############

### Definitions ###

def TokenBuy_BNB(_web3, _tokenCA, _Router, _RouterABI, _BNB_Amount, _GasWei, _GasLimit, _sender_address, _sender_pkey,
                 _Output_Box, _Slip, _numTx):
    _Output_Box.delete(1.0, END)
    _Output_Box.insert('insert', "Start Buy with BNB LP: {} \n".format(datetime.now().strftime("%H:%M:%S")))
    _Output_Box.update()
    contract = _web3.eth.contract(address=_Router, abi=_RouterABI)
    spend = _web3.toChecksumAddress("0xbb4cdb9cbd36b01bd1cbaebf2de08d9173bc095c")  # WBNB Address

    tokenToBuy = _web3.toChecksumAddress(_tokenCA)
    amountOut = contract.functions.getAmountsOut(web3.toWei(_BNB_Amount, 'ether'), [spend, tokenToBuy]).call()[-1]
    amountMin = amountOut / (1 + _Slip / 100)

    account_verified = 1
    count = 0
    nonce = _web3.eth.get_transaction_count(_sender_address)
    while count < _numTx:
        pancakeswap2_txn = contract.functions.swapExactETHForTokensSupportingFeeOnTransferTokens(
            int(amountMin),
            # set to 0 means dont care slippage, or specify minimum amount of token you want to receive - consider Decimal!
            [spend, tokenToBuy],
            _sender_address,
            (int(time.time()) + 120)
        ).buildTransaction({
            'from': _sender_address,
            'value': _web3.toWei(_BNB_Amount, 'ether'),  ## BNB Amount want to Swap from
            'gas': _GasLimit,
            'gasPrice': _web3.toWei(_GasWei, 'gwei'),
            'nonce': nonce,
        })
        try:
            signed_txn = _web3.eth.account.sign_transaction(pancakeswap2_txn, private_key=_sender_pkey)
        except Exception as e:
            if "from field must match key" in str(e):
                _Output_Box.insert('end',"Private key is not correct for your wallet, please check again!")
            account_verified = 0
            count += 1
        else:
            tx_token = _web3.eth.send_raw_transaction(signed_txn.rawTransaction)
            _Output_Box.insert('end', "TX Hash {}: https://bscscan.com/tx/{} \n".format(count + 1, _web3.toHex(tx_token)))
            _Output_Box.update()
            count += 1
            nonce += 1

    if account_verified == 1:
        _Output_Box.insert('insert', "Latest Ethereum block number: {} \n".format(_web3.eth.blockNumber))
        _Output_Box.update()
        _Output_Box.insert('insert',
                           "Waiting for transaction to be done: {} \n".format(datetime.now().strftime("%H:%M:%S")))
        _Output_Box.update()
        _web3.eth.wait_for_transaction_receipt(Web3.toHex(tx_token))
        _Output_Box.insert('end', "Transaction Done: {} \n".format(datetime.now().strftime("%H:%M:%S")))
        _Output_Box.update()

        if _web3.eth.get_transaction_receipt(tx_token).status == 1:
            _Output_Box.insert('end', "Transaction status: SUCCESS !!! \n")
        else:
            tx = web3.eth.get_transaction(tx_token)
            replay_tx = {
                'to': tx['to'],
                'from': tx['from'],
                'value': tx['value'],
                'data': tx['input'],
            }
            try:
                web3.eth.call(replay_tx, tx.blockNumber - 1)
            except Exception as e:
                _Output_Box.insert('end', "Transaction status: FAILED !!! \n")
                _Output_Box.insert('end', "Fail reason: {} !!! \n".format(e))
                if "INSUFFICIENT_OUTPUT_AMOUNT" in str(e):
                    _Output_Box.insert('end', "Maybe slippage is to small, please increase your Slippage setting !!! \n")
        _Output_Box.update()

def TokenBuy_BUSD(_web3, _tokenCA, _Router, _RouterABI, _BUSD_Amount, _GasWei, _GasLimit, _sender_address, _sender_pkey,
                  _Output_Box, _Slip, _numTx):
    _Output_Box.delete(1.0, END)
    _Output_Box.insert('insert', "Start Buy with BUSD LP: {} \n".format(datetime.now().strftime("%H:%M:%S")))
    _Output_Box.update()
    contract = _web3.eth.contract(address=_Router, abi=_RouterABI)
    spend = _web3.toChecksumAddress(BUSD_add)  # BUSD Address

    tokenToBuy = _web3.toChecksumAddress(_tokenCA)
    amountOut = contract.functions.getAmountsOut(int(float(_BUSD_Amount) * 10 ** 18), [spend, tokenToBuy]).call()[-1]
    amountMin = amountOut / (1 + _Slip / 100)
    count = 0
    nonce = _web3.eth.get_transaction_count(_sender_address)
    while count < _numTx:
        pancakeswap2_txn = contract.functions.swapExactTokensForTokensSupportingFeeOnTransferTokens(
            web3.toWei(_BUSD_Amount, 'ether'),  # BUSD AMMOUNT You want to spend
            int(amountMin),
            # set to 0 means dont care slippage, or specify minimum amount of token you want to receive - consider Decimal!
            [spend, tokenToBuy],
            _sender_address,
            (int(time.time()) + 120)
        ).buildTransaction({
            'from': _sender_address,
            'gas': _GasLimit,
            'gasPrice': _web3.toWei(_GasWei, 'gwei'),
            'nonce': nonce,
        })
        signed_txn = _web3.eth.account.sign_transaction(pancakeswap2_txn, private_key=_sender_pkey)
        tx_token = _web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        _Output_Box.insert('end', "TX Hash {}: https://bscscan.com/tx/{} \n".format(count + 1, _web3.toHex(tx_token)))
        _Output_Box.update()
        count += 1
        nonce = nonce + 1

    _Output_Box.insert('insert', "Latest Ethereum block number: {} \n".format(_web3.eth.blockNumber))
    _Output_Box.update()
    _Output_Box.insert('insert',
                       "Waiting for transaction to be done: {} \n".format(datetime.now().strftime("%H:%M:%S")))
    _Output_Box.update()
    _web3.eth.wait_for_transaction_receipt(Web3.toHex(tx_token))
    _Output_Box.insert('end', "Transaction Done: {} \n".format(datetime.now().strftime("%H:%M:%S")))
    _Output_Box.update()
    time.sleep(0.2)
    if _web3.eth.get_transaction_receipt(tx_token).status == 1:
        _Output_Box.insert('end', "Transaction status: SUCCESS !!! \n")
    else:
        tx = web3.eth.get_transaction(tx_token)
        replay_tx = {
            'to': tx['to'],
            'from': tx['from'],
            'value': tx['value'],
            'data': tx['input'],
        }
        try:
            web3.eth.call(replay_tx, tx.blockNumber - 1)
        except Exception as e:
            _Output_Box.insert('end', "Transaction status: FAILED !!! \n")
            _Output_Box.insert('end', "Fail reason: {} !!! \n".format(e))
            if "INSUFFICIENT_OUTPUT_AMOUNT" in str(e):
                _Output_Box.insert('end', "Maybe slippage is to small, please increase your Slippage setting !!! \n")
    _Output_Box.update()

def TokenBuy_USDT(_web3, _tokenCA, _Router, _RouterABI, _USDT_Amount, _GasWei, _GasLimit, _sender_address, _sender_pkey,
                  _Output_Box, _Slip, _numTx):
    _Output_Box.delete(1.0, END)
    _Output_Box.insert('insert', "Start Buy with USDT LP: {} \n".format(datetime.now().strftime("%H:%M:%S")))
    _Output_Box.update()
    contract = _web3.eth.contract(address=_Router, abi=_RouterABI)
    spend = _web3.toChecksumAddress(USDT_add)  # BUSD Address

    tokenToBuy = _web3.toChecksumAddress(_tokenCA)
    amountOut = contract.functions.getAmountsOut(int(float(_USDT_Amount) * 10 ** 18), [spend, tokenToBuy]).call()[-1]
    amountMin = amountOut / (1 + _Slip / 100)
    pancakeswap2_txn = contract.functions.swapExactTokensForTokensSupportingFeeOnTransferTokens(
        web3.toWei(_USDT_Amount, 'ether'),  # BUSD AMMOUNT You want to spend
        int(amountMin),
        # set to 0 means dont care slippage, or specify minimum amount of token you want to receive - consider Decimal!
        [spend, tokenToBuy],
        _sender_address,
        (int(time.time()) + 120)
    ).buildTransaction({
        'from': _sender_address,
        'gas': _GasLimit,
        'gasPrice': _web3.toWei(_GasWei, 'gwei'),
        'nonce': _web3.eth.get_transaction_count(_sender_address),
    })
    signed_txn = _web3.eth.account.sign_transaction(pancakeswap2_txn, private_key=_sender_pkey)
    tx_token = _web3.eth.send_raw_transaction(signed_txn.rawTransaction)

    _Output_Box.insert('insert', "Latest Ethereum block number: {} \n".format(_web3.eth.blockNumber))
    _Output_Box.update()
    _Output_Box.insert('insert',
                       "Waiting for transaction to be done: {} \n".format(datetime.now().strftime("%H:%M:%S")))
    _Output_Box.update()
    _web3.eth.wait_for_transaction_receipt(Web3.toHex(tx_token))
    _Output_Box.insert('end', "Transaction Done: {} \n".format(datetime.now().strftime("%H:%M:%S")))
    _Output_Box.update()
    _Output_Box.insert('end', "TX Hash: https://bscscan.com/tx/{} \n".format(_web3.toHex(tx_token)))
    if _web3.eth.get_transaction_receipt(tx_token).status == 1:
        _Output_Box.insert('end', "Transaction status: SUCCESS !!! \n")
    else:
        tx = web3.eth.get_transaction(tx_token)
        replay_tx = {
            'to': tx['to'],
            'from': tx['from'],
            'value': tx['value'],
            'data': tx['input'],
        }
        try:
            web3.eth.call(replay_tx, tx.blockNumber - 1)
        except Exception as e:
            _Output_Box.insert('end', "Transaction status: FAILED !!! \n")
            _Output_Box.insert('end', "Fail reason: {} !!! \n".format(e))
            if "INSUFFICIENT_OUTPUT_AMOUNT" in str(e):
                _Output_Box.insert('end', "Maybe slippage is to small, please increase your Slippage setting !!! \n")
    _Output_Box.update()

def TokenSell_BNB(_web3, _tokenCA, _Router, _RouterABI, _Token_Percent, _GasWei, _GasLimit, _sender_address,
                  _sender_pkey, _Output_Box, _Slip):
    _Output_Box.delete(1.0, END)
    _Output_Box.insert('insert', "Start Sell: {} \n".format(datetime.now().strftime("%H:%M:%S")))
    _Output_Box.update()
    contract = _web3.eth.contract(address=_Router, abi=_RouterABI)
    spend = _web3.toChecksumAddress("0xbb4cdb9cbd36b01bd1cbaebf2de08d9173bc095c")  # WBNB Address

    TokenToSell = _web3.toChecksumAddress(_tokenCA)
    sellTokenContract = web3.eth.contract(TokenToSell, abi=ERC20abi_BSC)
    allowance = sellTokenContract.functions.allowance(user_wallet_address, PCS_ROUTER_CA).call()
    token_symbol = sellTokenContract.functions.symbol().call()
    token_decimal = sellTokenContract.functions.decimals().call()
    balance = sellTokenContract.functions.balanceOf(_sender_address).call()
    readable = balance / 10 ** token_decimal

    _Output_Box.insert('insert', "Token Balance: {} {}\n".format(str(readable), token_symbol))
    _Output_Box.update()
    tokenValue = balance * int(_Token_Percent) / 100

    if allowance > tokenValue:
        _Output_Box.insert('insert', "Swapping {} {} for BNB\n".format(tokenValue / 10 ** token_decimal, token_symbol))
        _Output_Box.update()

        amountOut = contract.functions.getAmountsOut(int(tokenValue), [TokenToSell, spend]).call()[-1]
        amountMin = amountOut / (1 + _Slip / 100)

        pancakeswap2_txn = contract.functions.swapExactTokensForETHSupportingFeeOnTransferTokens(
            int(tokenValue),
            int(amountMin),
            [TokenToSell, spend],
            _sender_address,
            (int(time.time()) + 30)
        ).buildTransaction({
            'from': _sender_address,
            'gas': _GasLimit,
            'gasPrice': web3.toWei(_GasWei, 'gwei'),
            'nonce': web3.eth.get_transaction_count(_sender_address),
        })

        signed_txn = _web3.eth.account.sign_transaction(pancakeswap2_txn, private_key=_sender_pkey)
        tx_token = _web3.eth.send_raw_transaction(signed_txn.rawTransaction)

        _Output_Box.insert('insert', "Latest Ethereum block number: {} \n".format(_web3.eth.blockNumber))
        _Output_Box.update()
        _Output_Box.insert('insert',
                           "Waiting for transaction to be done: {} \n".format(datetime.now().strftime("%H:%M:%S")))
        _Output_Box.update()
        _web3.eth.wait_for_transaction_receipt(Web3.toHex(tx_token))
        _Output_Box.insert('end', "Transaction Done: {} \n".format(datetime.now().strftime("%H:%M:%S")))
        _Output_Box.update()
        _Output_Box.insert('end', "TX Hash: https://bscscan.com/tx/{} \n".format(_web3.toHex(tx_token)))
        _Output_Box.update()
        time.sleep(0.2)
        if _web3.eth.get_transaction_receipt(tx_token).status == 1:
            _Output_Box.insert('end', "Transaction status: SUCCESS !!! \n")
        else:
            tx = web3.eth.get_transaction(tx_token)
            replay_tx = {
                'to': tx['to'],
                'from': tx['from'],
                'value': tx['value'],
                'data': tx['input'],
            }
            try:
                web3.eth.call(replay_tx, tx.blockNumber - 1)
            except Exception as e:
                _Output_Box.insert('end', "Transaction status: FAILED !!! \n")
                _Output_Box.insert('end', "Fail reason: {} !!! \n".format(e))
        _Output_Box.update()
    else:
        _Output_Box.insert('end', "Token is not approved, please approve first!")
        _Output_Box.update()

def TokenSell_BUSD(_web3, _tokenCA, _Router, _RouterABI, _Token_Percent, _GasWei, _GasLimit, _sender_address,
                   _sender_pkey, _Output_Box, _Slip):
    _Output_Box.delete(1.0, END)
    _Output_Box.insert('insert', "Start Sell token for BUSD: {} \n".format(datetime.now().strftime("%H:%M:%S")))
    _Output_Box.update()
    contract = _web3.eth.contract(address=_Router, abi=_RouterABI)
    spend = _web3.toChecksumAddress(BUSD_add)  # BUSD Address

    TokenToSell = _web3.toChecksumAddress(_tokenCA)
    sellTokenContract = web3.eth.contract(TokenToSell, abi=ERC20abi_BSC)
    allowance = sellTokenContract.functions.allowance(user_wallet_address, PCS_ROUTER_CA).call()
    token_symbol = sellTokenContract.functions.symbol().call()
    token_decimal = sellTokenContract.functions.decimals().call()
    balance = sellTokenContract.functions.balanceOf(_sender_address).call()
    readable = balance / 10 ** token_decimal

    _Output_Box.insert('insert', "Token Balance: {} {}\n".format(str(readable), token_symbol))
    _Output_Box.update()
    tokenValue = balance * int(_Token_Percent) / 100

    if allowance > tokenValue:
        amountOut = contract.functions.getAmountsOut(int(tokenValue), [TokenToSell, spend]).call()[-1]
        amountMin = amountOut / (1 + _Slip / 100)
        _Output_Box.insert('insert', "Swapping {} {} for BUSD (~{} BUSD) \n".format(tokenValue / 10 ** token_decimal,
                                                                                    token_symbol,
                                                                                    amountOut / (10 ** 18)))
        _Output_Box.update()

        pancakeswap2_txn = contract.functions.swapExactTokensForTokensSupportingFeeOnTransferTokens(
            int(tokenValue),
            int(amountMin),
            [TokenToSell, spend],
            _sender_address,
            (int(time.time()) + 30)
        ).buildTransaction({
            'from': _sender_address,
            'gas': _GasLimit,
            'gasPrice': web3.toWei(_GasWei, 'gwei'),
            'nonce': web3.eth.get_transaction_count(_sender_address),
        })

        signed_txn = _web3.eth.account.sign_transaction(pancakeswap2_txn, private_key=_sender_pkey)
        tx_token = _web3.eth.send_raw_transaction(signed_txn.rawTransaction)

        _Output_Box.insert('insert', "Latest Ethereum block number: {} \n".format(_web3.eth.blockNumber))
        _Output_Box.update()
        _Output_Box.insert('insert',
                           "Waiting for transaction to be done: {} \n".format(datetime.now().strftime("%H:%M:%S")))
        _Output_Box.update()
        _web3.eth.wait_for_transaction_receipt(Web3.toHex(tx_token))
        _Output_Box.insert('end', "Transaction Done: {} \n".format(datetime.now().strftime("%H:%M:%S")))
        _Output_Box.update()
        _Output_Box.insert('end', "TX Hash: https://bscscan.com/tx/{} \n".format(_web3.toHex(tx_token)))
        _Output_Box.update()
        if _web3.eth.get_transaction_receipt(tx_token).status == 1:
            _Output_Box.insert('end', "Transaction status: SUCCESS !!! \n")
        else:
            tx = web3.eth.get_transaction(tx_token)
            replay_tx = {
                'to': tx['to'],
                'from': tx['from'],
                'value': tx['value'],
                'data': tx['input'],
            }
            try:
                web3.eth.call(replay_tx, tx.blockNumber - 1)
            except Exception as e:
                _Output_Box.insert('end', "Transaction status: FAILED !!! \n")
                _Output_Box.insert('end', "Fail reason: {} !!! \n".format(e))
        _Output_Box.update()
    else:
        _Output_Box.insert('end', "Token is not approved, please approve first!")
        _Output_Box.update()

def TokenSell_USDT(_web3, _tokenCA, _Router, _RouterABI, _Token_Percent, _GasWei, _GasLimit, _sender_address,
                   _sender_pkey, _Output_Box, _Slip):
    _Output_Box.delete(1.0, END)
    _Output_Box.insert('insert', "Start Sell token for USDT: {} \n".format(datetime.now().strftime("%H:%M:%S")))
    _Output_Box.update()
    contract = _web3.eth.contract(address=_Router, abi=_RouterABI)
    spend = _web3.toChecksumAddress(USDT_add)  # USDT Address

    TokenToSell = _web3.toChecksumAddress(_tokenCA)
    sellTokenContract = web3.eth.contract(TokenToSell, abi=ERC20abi_BSC)
    allowance = sellTokenContract.functions.allowance(user_wallet_address, PCS_ROUTER_CA).call()
    token_symbol = sellTokenContract.functions.symbol().call()
    token_decimal = sellTokenContract.functions.decimals().call()
    balance = sellTokenContract.functions.balanceOf(_sender_address).call()
    readable = balance / 10 ** token_decimal

    _Output_Box.insert('insert', "Token Balance: {} {}\n".format(str(readable), token_symbol))
    _Output_Box.update()
    tokenValue = balance * int(_Token_Percent) / 100

    if allowance > tokenValue:
        amountOut = contract.functions.getAmountsOut(int(tokenValue), [TokenToSell, spend]).call()[-1]
        amountMin = amountOut / (1 + _Slip / 100)
        _Output_Box.insert('insert', "Swapping {} {} for USDT (~{} USDT) \n".format(tokenValue / 10 ** token_decimal,
                                                                                    token_symbol,
                                                                                    amountOut / (10 ** 18)))
        _Output_Box.update()

        pancakeswap2_txn = contract.functions.swapExactTokensForTokensSupportingFeeOnTransferTokens(
            int(tokenValue),
            int(amountMin),
            [TokenToSell, spend],
            _sender_address,
            (int(time.time()) + 30)
        ).buildTransaction({
            'from': _sender_address,
            'gas': _GasLimit,
            'gasPrice': web3.toWei(_GasWei, 'gwei'),
            'nonce': web3.eth.get_transaction_count(_sender_address),
        })

        signed_txn = _web3.eth.account.sign_transaction(pancakeswap2_txn, private_key=_sender_pkey)
        tx_token = _web3.eth.send_raw_transaction(signed_txn.rawTransaction)

        _Output_Box.insert('insert', "Latest Ethereum block number: {} \n".format(_web3.eth.blockNumber))
        _Output_Box.update()
        _Output_Box.insert('insert',
                           "Waiting for transaction to be done: {} \n".format(datetime.now().strftime("%H:%M:%S")))
        _Output_Box.update()
        _web3.eth.wait_for_transaction_receipt(Web3.toHex(tx_token))
        _Output_Box.insert('end', "Transaction Done: {} \n".format(datetime.now().strftime("%H:%M:%S")))
        _Output_Box.update()
        _Output_Box.insert('end', "TX Hash: https://bscscan.com/tx/{} \n".format(_web3.toHex(tx_token)))
        _Output_Box.update()
        if _web3.eth.get_transaction_receipt(tx_token).status == 1:
            _Output_Box.insert('end', "Transaction status: SUCCESS !!! \n")
        else:
            tx = web3.eth.get_transaction(tx_token)
            replay_tx = {
                'to': tx['to'],
                'from': tx['from'],
                'value': tx['value'],
                'data': tx['input'],
            }
            try:
                web3.eth.call(replay_tx, tx.blockNumber - 1)
            except Exception as e:
                _Output_Box.insert('end', "Transaction status: FAILED !!! \n")
                _Output_Box.insert('end', "Fail reason: {} !!! \n".format(e))
        _Output_Box.update()
    else:
        _Output_Box.insert('end', "Token is not approved, please approve first!")
        _Output_Box.update()

def TokenApprove(_web3, _tokenCA, _Router, _RouterABI, _GasWei, _GasLimit, _sender_address, _sender_pkey, _Output_Box,
                 _entry_TokenCA):
    _Output_Box.delete(1.0, END)
    _Output_Box.insert('insert', "Start Approving: {} \n".format(datetime.now().strftime("%H:%M:%S")))
    _Output_Box.update()
    contract = _web3.eth.contract(address=_Router, abi=_RouterABI)

    TokenToSell = _web3.toChecksumAddress(_tokenCA)
    sellTokenContract = web3.eth.contract(TokenToSell, abi=ERC20abi_BSC)
    allowance = sellTokenContract.functions.allowance(user_wallet_address, PCS_ROUTER_CA).call()
    if allowance < 115792089237316195423570985008687907853269984665640564039457584007913129639935:
        approve = sellTokenContract.functions.approve(_Router,
                                                      115792089237316195423570985008687907853269984665640564039457584007913129639935).buildTransaction(
            {
                'from': _sender_address,
                'gas': _GasLimit,
                'gasPrice': web3.toWei(_GasWei, 'gwei'),
                'nonce': web3.eth.get_transaction_count(_sender_address),
            })
        signed_txn = _web3.eth.account.sign_transaction(approve, private_key=_sender_pkey)
        tx_token = _web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        _Output_Box.insert('insert',
                           "Waiting for transaction to be done: {} \n".format(datetime.now().strftime("%H:%M:%S")))
        _Output_Box.update()
        _web3.eth.wait_for_transaction_receipt(Web3.toHex(tx_token))
        _Output_Box.insert('end', "Transaction Done: {} \n".format(datetime.now().strftime("%H:%M:%S")))
        _Output_Box.update()
        _Output_Box.insert('end',
                           "Approve done! --> TX Hash: https://bscscan.com/tx/{} \n".format(_web3.toHex(tx_token)))
        _Output_Box.update()
        time.sleep(0.5)
        _entry_TokenCA.delete(0, 'end')
        _entry_TokenCA.insert(END, _tokenCA)
    else:
        _Output_Box.insert('end', "Already approved! \n")
        _Output_Box.update()

def PinkSaleBuy(_web3, _ILO_Address, _BNB_Amount, _GasWei, _GasLimit, _sender_address, _sender_pkey, _Output_Box):
    _Output_Box.insert('insert', "Start Buy Pinksale: {} \n".format(datetime.now().strftime("%H:%M:%S")))
    _Output_Box.update()
    to_wallet = _web3.toChecksumAddress(_ILO_Address)
    txn = {
        'nonce': _web3.eth.get_transaction_count(_sender_address),
        'to': to_wallet,
        'value': _web3.toWei(_BNB_Amount, 'ether'),
        'gas': _GasLimit,
        'gasPrice': _web3.toWei(_GasWei, 'gwei')
    }
    signed_txn = _web3.eth.account.sign_transaction(txn, private_key=_sender_pkey)
    tx_token = _web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    _Output_Box.insert('insert',
                       "Waiting for transaction to be done: {} \n".format(datetime.now().strftime("%H:%M:%S")))
    _Output_Box.update()
    _web3.eth.wait_for_transaction_receipt(Web3.toHex(tx_token))
    _Output_Box.insert('end', "Transaction Done: {} \n".format(datetime.now().strftime("%H:%M:%S")))
    _Output_Box.update()
    _Output_Box.insert('end', "TX Hash: https://bscscan.com/tx/{} \n".format(_web3.toHex(tx_token)))
    _Output_Box.update()

#0xa76dbf7066845abc8750bc52c291078d33f6d985
#0x96475C9B705f23ECDdA127Bac4e2a82b310d0336
def SendToken(_web3, _token_CA,_to_address, _token_amount, _GasWei, _GasLimit, _sender_address, _sender_pkey, _Output_Box):
    to_wallet = _web3.toChecksumAddress(_to_address)
    token_CA = _web3.toChecksumAddress(_token_CA)
    token_contract = web3.eth.contract(token_CA, abi=token_ABI)
    token_decimal = token_contract.functions.decimals().call()
    token_name = token_contract.functions.name().call()
    _Output_Box.delete(1.0, END)
    _Output_Box.insert('insert', "Sending {} token {} to {}: {} \n".format(_token_amount,token_name,_to_address,datetime.now().strftime("%H:%M:%S")))
    _Output_Box.update()
    txn = token_contract.functions.transfer(
        to_wallet,
        int(float(_token_amount) * 10**token_decimal)
    ).buildTransaction(
    {
        'nonce': _web3.eth.get_transaction_count(_sender_address),
        'gas': _GasLimit,
        'gasPrice': _web3.toWei(_GasWei, 'gwei'),
    })
    signed_txn = _web3.eth.account.sign_transaction(txn, private_key=_sender_pkey)
    tx_token = _web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    _Output_Box.insert('insert',
                       "Waiting for transaction to be done: {} \n".format(datetime.now().strftime("%H:%M:%S")))
    _Output_Box.update()
    _web3.eth.wait_for_transaction_receipt(Web3.toHex(tx_token))
    _Output_Box.insert('end', "Transaction Done: {} \n".format(datetime.now().strftime("%H:%M:%S")))
    _Output_Box.update()
    _Output_Box.insert('end', "TX Hash: https://bscscan.com/tx/{} \n".format(_web3.toHex(tx_token)))
    _Output_Box.update()
    if _web3.eth.get_transaction_receipt(tx_token).status == 1:
        _Output_Box.insert('end', "Transaction status: SUCCESS !!! \n")
        balance = token_contract.functions.balanceOf(_sender_address).call()
        lbl_send_Wallet_balance.config(text="Wallet balance: {:.3f}".format(balance / 10 ** token_decimal))
    else:
        tx = web3.eth.get_transaction(tx_token)
        replay_tx = {
            'to': tx['to'],
            'from': tx['from'],
            'value': tx['value'],
            'data': tx['input'],
        }
        try:
            web3.eth.call(replay_tx, tx.blockNumber - 1)
        except Exception as e:
            _Output_Box.insert('end', "Transaction status: FAILED !!! \n")
            _Output_Box.insert('end', "Fail reason: {} !!! \n".format(e))
    _Output_Box.update()

def PinkSaleClaim(_web3, _ILO_Address, _GasWei, _GasLimit, _sender_address, _sender_pkey, _Output_Box):
    _Output_Box.insert('insert', "Start Claim: {} \n".format(datetime.now().strftime("%H:%M:%S")))
    _Output_Box.update()
    to_wallet = _web3.toChecksumAddress(_ILO_Address)
    txn = {
        'nonce': _web3.eth.get_transaction_count(_sender_address),
        'to': to_wallet,
        'gas': _GasLimit,
        'gasPrice': _web3.toWei(_GasWei, 'gwei'),
        'data': '0x4e71d92d'
    }
    signed_txn = _web3.eth.account.sign_transaction(txn, private_key=_sender_pkey)
    tx_token = _web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    _Output_Box.insert('insert',
                       "Waiting for transaction to be done: {} \n".format(datetime.now().strftime("%H:%M:%S")))
    _Output_Box.update()
    _web3.eth.wait_for_transaction_receipt(Web3.toHex(tx_token))
    _Output_Box.insert('end', "Transaction Done: {} \n".format(datetime.now().strftime("%H:%M:%S")))
    _Output_Box.update()
    _Output_Box.insert('end', "TX Hash: https://bscscan.com/tx/{} \n".format(_web3.toHex(tx_token)))
    _Output_Box.update()

def PinkSaleClaimandSell(_web3, _ILO_Address, _BNB_Amount, _GasWei, _GasLimit, _sender_address, _sender_pkey,
                         _Output_Box):
    _Output_Box.insert('insert', "Start Buy Pinksale: {} \n".format(datetime.now().strftime("%H:%M:%S")))
    _Output_Box.update()
    to_wallet = _web3.toChecksumAddress(_ILO_Address)
    txn = {
        'nonce': _web3.eth.get_transaction_count(_sender_address),
        'to': to_wallet,
        'gas': _GasLimit,
        'gasPrice': _web3.toWei(_GasWei, 'gwei'),
        'data': '0x4e71d92d'
    }
    signed_txn = _web3.eth.account.sign_transaction(txn, private_key=_sender_pkey)
    tx_token = _web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    _Output_Box.insert('insert',
                       "Waiting for transaction to be done: {} \n".format(datetime.now().strftime("%H:%M:%S")))
    _Output_Box.update()
    _web3.eth.wait_for_transaction_receipt(Web3.toHex(tx_token))
    _Output_Box.insert('end', "Transaction Done: {} \n".format(datetime.now().strftime("%H:%M:%S")))
    _Output_Box.update()
    _Output_Box.insert('end', "TX Hash: https://bscscan.com/tx/{} \n".format(_web3.toHex(tx_token)))
    _Output_Box.update()

def UniBuy(_web3, _ILO_Address, _BNB_Amount, _GasWei, _GasLimit, _sender_address, _sender_pkey, _Output_Box):
    _Output_Box.insert('insert', "Start Buy Unicrypt: {} \n".format(datetime.now().strftime("%H:%M:%S")))
    _Output_Box.update()
    UniILO_add = _web3.toChecksumAddress(_ILO_Address)
    ILO_CA = _web3.eth.contract(address=UniILO_add, abi=UniABI)
    txn = ILO_CA.functions.userDeposit(
        1
    ).buildTransaction({
        'value': web3.toWei(_BNB_Amount, 'ether'),
        'gas': _GasLimit,
        'gasPrice': web3.toWei(_GasWei, 'gwei'),
        'nonce': _web3.eth.get_transaction_count(_sender_address),
    })
    signed_txn = _web3.eth.account.sign_transaction(txn, private_key=_sender_pkey)
    tx_token = _web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    _Output_Box.insert('insert',
                       "Waiting for transaction to be done: {} \n".format(datetime.now().strftime("%H:%M:%S")))
    _Output_Box.update()
    _web3.eth.wait_for_transaction_receipt(Web3.toHex(tx_token))
    _Output_Box.insert('end', "Transaction Done: {} \n".format(datetime.now().strftime("%H:%M:%S")))
    _Output_Box.update()
    _Output_Box.insert('end', "TX Hash: https://bscscan.com/tx/{} \n".format(_web3.toHex(tx_token)))
    _Output_Box.update()
    if _web3.eth.get_transaction_receipt(tx_token).status == 1:
        _Output_Box.insert('end', "Transaction status: SUCCESS !!! \n")
    else:
        tx = _web3.eth.get_transaction(tx_token)
        replay_tx = {
            'to': tx['to'],
            'from': tx['from'],
            'value': tx['value'],
            'data': tx['input'],
        }
        try:
            _web3.eth.call(replay_tx, tx.blockNumber - 1)
        except Exception as e:
            _Output_Box.insert('end', "Transaction status: FAILED !!! \n")
            _Output_Box.insert('end', "Fail reason: {} !!! \n".format(e))
    _Output_Box.update()

def UniClaim(_web3, _ILO_Address, _GasWei, _GasLimit, _sender_address, _sender_pkey, _Output_Box):
    _Output_Box.insert('insert', "Claim Token from Unicrypt: {} \n".format(datetime.now().strftime("%H:%M:%S")))
    _Output_Box.update()
    UniILO_add = _web3.toChecksumAddress(_ILO_Address)
    ILO_CA = _web3.eth.contract(address=UniILO_add, abi=UniABI)
    txn = ILO_CA.functions.userWithdrawTokens(
    ).buildTransaction({
        'gas': _GasLimit,
        'gasPrice': _web3.toWei(_GasWei, 'gwei'),
        'nonce': _web3.eth.get_transaction_count(_sender_address),
    })
    signed_txn = _web3.eth.account.sign_transaction(txn, private_key=_sender_pkey)
    tx_token = _web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    _Output_Box.insert('insert',
                       "Waiting for transaction to be done: {} \n".format(datetime.now().strftime("%H:%M:%S")))
    _Output_Box.update()
    _web3.eth.wait_for_transaction_receipt(Web3.toHex(tx_token))
    _Output_Box.insert('end', "Transaction Done: {} \n".format(datetime.now().strftime("%H:%M:%S")))
    _Output_Box.update()
    _Output_Box.insert('end', "TX Hash: https://bscscan.com/tx/{} \n".format(_web3.toHex(tx_token)))
    _Output_Box.update()
    if _web3.eth.get_transaction_receipt(tx_token).status == 1:
        _Output_Box.insert('end', "Transaction status: SUCCESS !!! \n")
    else:
        tx = web3.eth.get_transaction(tx_token)
        replay_tx = {
            'to': tx['to'],
            'from': tx['from'],
            'value': tx['value'],
            'data': tx['input'],
        }
        try:
            web3.eth.call(replay_tx, tx.blockNumber - 1)
        except Exception as e:
            _Output_Box.insert('end', "Transaction status: FAILED !!! \n")
            _Output_Box.insert('end', "Fail reason: {} !!! \n".format(e))
    _Output_Box.update()

def UniClaimandSell(_web3, _ILO_Address, _GasWei, _GasLimit, _sender_address, _sender_pkey, _Output_Box):
    _Output_Box.insert('insert', "Claim Token from Unicrypt: {} \n".format(datetime.now().strftime("%H:%M:%S")))
    _Output_Box.update()
    spend = _web3.toChecksumAddress("0xbb4cdb9cbd36b01bd1cbaebf2de08d9173bc095c")  # WBNB Address
    UniILO_add = _web3.toChecksumAddress(_ILO_Address)
    ILO_CA = _web3.eth.contract(address=UniILO_add, abi=UniABI)
    PCS_CA = _web3.eth.contract(address=PCS_ROUTER_CA, abi=PCS_ABI)
    claim_tx = ILO_CA.functions.userWithdrawTokens(
    ).buildTransaction({
        'gas': _GasLimit,
        'gasPrice': _web3.toWei(_GasWei, 'gwei'),
        'nonce': _web3.eth.get_transaction_count(_sender_address),
    })
    signed_txn = _web3.eth.account.sign_transaction(claim_tx, private_key=_sender_pkey)
    tx_token = _web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    _Output_Box.insert('insert',
                       "Waiting for claim transaction to be done: {} \n".format(datetime.now().strftime("%H:%M:%S")))
    _Output_Box.update()
    _web3.eth.wait_for_transaction_receipt(Web3.toHex(tx_token))
    _Output_Box.insert('end', "TX Hash: https://bscscan.com/tx/{} \n".format(_web3.toHex(tx_token)))
    _Output_Box.update()
    _Output_Box.insert('end',
                       "Claim Transaction Done, start Approve: {} \n".format(datetime.now().strftime("%H:%M:%S")))
    _Output_Box.update()
    PRESALE_INFO = ILO_CA.functions.PRESALE_INFO().call()
    Token_CA = PRESALE_INFO[0]
    TokenToSell = Web3.toChecksumAddress(Token_CA)
    sellTokenContract = web3.eth.contract(TokenToSell, abi=ERC20abi_BSC)
    allowance = sellTokenContract.functions.allowance(user_wallet_address, PCS_ROUTER_CA).call()
    balance = sellTokenContract.functions.balanceOf(_sender_address).call()
    tokenValue = balance * 99 / 100
    if allowance < 115792089237316195423570985008687907853269984665640564039457584007913129639935:
        approve = sellTokenContract.functions.approve(PCS_ROUTER_CA,
                                                      115792089237316195423570985008687907853269984665640564039457584007913129639935).buildTransaction(
            {
                'from': _sender_address,
                'gas': _GasLimit,
                'gasPrice': web3.toWei(_GasWei, 'gwei'),
                'nonce': web3.eth.get_transaction_count(_sender_address),
            })
        signed_txn = _web3.eth.account.sign_transaction(approve, private_key=_sender_pkey)
        tx_token = _web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        _Output_Box.insert('insert', "Waiting for approve transaction to be done: {} \n".format(
            datetime.now().strftime("%H:%M:%S")))
        _Output_Box.update()
        _web3.eth.wait_for_transaction_receipt(Web3.toHex(tx_token))
        _Output_Box.insert('end', "Approve Done: {} \n".format(datetime.now().strftime("%H:%M:%S")))
        _Output_Box.update()
        _Output_Box.insert('end', "--> TX Hash: https://bscscan.com/tx/{} \n".format(_web3.toHex(tx_token)))
        _Output_Box.update()
        time.sleep(0.2)
    else:
        _Output_Box.insert('end', "Token already approved!!! \n")
        _Output_Box.update()
    _Output_Box.insert('end', "Start Selling all: {} \n".format(datetime.now().strftime("%H:%M:%S")))
    _Output_Box.update()
    pancakeswap2_txn = PCS_CA.functions.swapExactTokensForETHSupportingFeeOnTransferTokens(
        int(tokenValue),
        0,
        [TokenToSell, spend],
        _sender_address,
        (int(time.time()) + 30)
    ).buildTransaction({
        'from': _sender_address,
        'gas': _GasLimit,
        'gasPrice': _web3.toWei(_GasWei, 'gwei'),
        'nonce': _web3.eth.get_transaction_count(_sender_address),
    })
    signed_txn = _web3.eth.account.sign_transaction(pancakeswap2_txn, private_key=_sender_pkey)
    tx_token = _web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    _Output_Box.insert('insert',
                       "Waiting for Sell transaction to be done: {} \n".format(datetime.now().strftime("%H:%M:%S")))
    _Output_Box.update()
    _web3.eth.wait_for_transaction_receipt(Web3.toHex(tx_token))
    _Output_Box.insert('end', "TX Hash: https://bscscan.com/tx/{} \n".format(_web3.toHex(tx_token)))
    _Output_Box.update()
    _Output_Box.insert('end', "Sell Transaction Done: {} \n".format(datetime.now().strftime("%H:%M:%S")))
    _Output_Box.update()

    if _web3.eth.get_transaction_receipt(tx_token).status == 1:
        _Output_Box.insert('end', "Transaction status: SUCCESS !!! \n")
    else:
        tx = web3.eth.get_transaction(tx_token)
        replay_tx = {
            'to': tx['to'],
            'from': tx['from'],
            'value': tx['value'],
            'data': tx['input'],
        }
        try:
            web3.eth.call(replay_tx, tx.blockNumber - 1)
        except Exception as e:
            _Output_Box.insert('end', "Transaction status: FAILED !!! \n")
            _Output_Box.insert('end', "Fail reason: {} !!! \n".format(e))
    _Output_Box.update()

def UniApproveUNCL(_web3, _ILO_Address, _GasWei, _GasLimit, _sender_address, _sender_pkey, _Output_Box):
    _Output_Box.insert('insert', "Unicrypt - Approving UNCL: {} \n".format(datetime.now().strftime("%H:%M:%S")))
    _Output_Box.update()
    UniILO_add = _web3.toChecksumAddress(_ILO_Address)
    UNCL_add = _web3.toChecksumAddress(UNCL_CA)
    ILO_CA = _web3.eth.contract(address=UniILO_add, abi=UniABI)
    UNCL_contract = web3.eth.contract(address=UNCL_add, abi=UNCL_proxy_abi)
    txn = UNCL_contract.functions.approve(UniILO_add, int(2 * 10 ** 18)).buildTransaction({
        'from': _sender_address,
        'gas': _GasLimit,
        'gasPrice': web3.toWei(_GasWei, 'gwei'),
        'nonce': web3.eth.get_transaction_count(_sender_address),
    })
    signed_txn = _web3.eth.account.sign_transaction(txn, private_key=_sender_pkey)
    tx_token = _web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    _Output_Box.insert('insert',
                       "Waiting for transaction to be done: {} \n".format(datetime.now().strftime("%H:%M:%S")))
    _Output_Box.update()
    _web3.eth.wait_for_transaction_receipt(Web3.toHex(tx_token))
    _Output_Box.insert('end', "Transaction Done: {} \n".format(datetime.now().strftime("%H:%M:%S")))
    _Output_Box.update()
    _Output_Box.insert('end', "TX Hash: https://bscscan.com/tx/{} \n".format(_web3.toHex(tx_token)))
    _Output_Box.update()
    if _web3.eth.get_transaction_receipt(tx_token).status == 1:
        _Output_Box.insert('end', "Transaction status: SUCCESS !!! \n")
    else:
        tx = web3.eth.get_transaction(tx_token)
        replay_tx = {
            'to': tx['to'],
            'from': tx['from'],
            'value': tx['value'],
            'data': tx['input'],
        }
        try:
            web3.eth.call(replay_tx, tx.blockNumber - 1)
        except Exception as e:
            _Output_Box.insert('end', "Transaction status: FAILED !!! \n")
            _Output_Box.insert('end', "Fail reason: {} !!! \n".format(e))
    _Output_Box.update()

def UniR0Reserve(_web3, _ILO_Address, _GasWei, _GasLimit, _sender_address, _sender_pkey, _Output_Box):
    _Output_Box.insert('insert', "Unicrypt - R0 Reserving: {} \n".format(datetime.now().strftime("%H:%M:%S")))
    _Output_Box.update()
    UniILO_add = _web3.toChecksumAddress(_ILO_Address)
    ILO_CA = _web3.eth.contract(address=UniILO_add, abi=UniABI)
    txn = ILO_CA.functions.reserveAllocationWithUNCL().buildTransaction({
        'gas': _GasLimit,
        'gasPrice': web3.toWei(_GasWei, 'gwei'),
        'nonce': web3.eth.get_transaction_count(_sender_address),
    })
    signed_txn = _web3.eth.account.sign_transaction(txn, private_key=_sender_pkey)
    tx_token = _web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    _Output_Box.insert('insert',
                       "Waiting for transaction to be done: {} \n".format(datetime.now().strftime("%H:%M:%S")))
    _Output_Box.update()
    _web3.eth.wait_for_transaction_receipt(Web3.toHex(tx_token))
    _Output_Box.insert('end', "Transaction Done: {} \n".format(datetime.now().strftime("%H:%M:%S")))
    _Output_Box.update()
    _Output_Box.insert('end', "TX Hash: https://bscscan.com/tx/{} \n".format(_web3.toHex(tx_token)))
    _Output_Box.update()
    if _web3.eth.get_transaction_receipt(tx_token).status == 1:
        _Output_Box.insert('end', "Transaction status: SUCCESS !!! \n")
    else:
        tx = web3.eth.get_transaction(tx_token)
        replay_tx = {
            'to': tx['to'],
            'from': tx['from'],
            'value': tx['value'],
            'data': tx['input'],
        }
        try:
            web3.eth.call(replay_tx, tx.blockNumber - 1)
        except Exception as e:
            _Output_Box.insert('end', "Transaction status: FAILED !!! \n")
            _Output_Box.insert('end', "Fail reason: {} !!! \n".format(e))
    _Output_Box.update()

def OpenURL(url):
    webbrowser.open_new(url)

def ButtonBuy():
    LP_Pool = ListB_Pair_list.get()
    entry_TokenCA_input = entry_TokenCA.get()

    if len(entry_TokenCA_input) != 0:
        Token_add = web3.toChecksumAddress(entry_TokenCA_input)
        Token_CA = web3.eth.contract(Token_add, abi=ERC20abi_BSC)
        try:
            Token_CA.functions.symbol().call()
        except:
            tkinter.messagebox.showerror(title="Contract address Error",
                                         message="Invalid Token Contract Address, please check again!")
        else:
            entry_GasWei_input = entry_GasWei.get()
            entry_GasLimit_input = int(entry_GasLimit.get())
            entry_Slippage_input = int(entry_Slippage.get())
            entry_NumTx_input = int(entry_NumTx.get())
            if LP_Pool == "BNB":
                entry_BNBAmount_input = entry_BNBAmount.get()
                TokenBuy_BNB(web3, entry_TokenCA_input, PCS_ROUTER_CA, PCS_ABI, entry_BNBAmount_input,
                             entry_GasWei_input, entry_GasLimit_input, sender_wallet, sender_pkey, OutputBox,
                             entry_Slippage_input, entry_NumTx_input)
            elif LP_Pool == "BUSD":
                entry_BUSDAmount_input = entry_USDAmount.get()
                TokenBuy_BUSD(web3, entry_TokenCA_input, PCS_ROUTER_CA, PCS_ABI, entry_BUSDAmount_input,
                              entry_GasWei_input, entry_GasLimit_input, sender_wallet, sender_pkey, OutputBox,
                              entry_Slippage_input, entry_NumTx_input)
            elif LP_Pool == "USDT":
                entry_USDTAmount_input = entry_USDAmount.get()
                TokenBuy_USDT(web3, entry_TokenCA_input, PCS_ROUTER_CA, PCS_ABI, entry_USDTAmount_input,
                              entry_GasWei_input, entry_GasLimit_input, sender_wallet, sender_pkey, OutputBox,
                              entry_Slippage_input, entry_NumTx_input)
    else:
        tkinter.messagebox.showerror(title="Contract address Error",
                                     message="Please insert Token Contract Address before buy!!!")

def ButtonPastenBuy():
    stringtext = str(top.clipboard_get())
    if "0x" in stringtext:
        entry_TokenCA_input = str(stringtext[stringtext.find("0x"):int(stringtext.find("0x") + 42)])
        if len(entry_TokenCA_input) != 0:
            Token_add = web3.toChecksumAddress(entry_TokenCA_input)
            Token_CA = web3.eth.contract(Token_add, abi=ERC20abi_BSC)
            try:
                Token_CA.functions.symbol().call()
            except:
                tkinter.messagebox.showerror(title="Contract address Error",
                                             message="Invalid Token Contract Address, please check again!")
            else:
                entry_GasWei_input = entry_GasWei.get()
                entry_GasLimit_input = int(entry_GasLimit.get())
                entry_Slippage_input = int(entry_Slippage.get())
                entry_NumTx_input = int(entry_NumTx.get())
                LP_Pool = ListB_Pair_list.get()
                if LP_Pool == "BNB":
                    entry_BNBAmount_input = entry_BNBAmount.get()
                    TokenBuy_BNB(web3, entry_TokenCA_input, PCS_ROUTER_CA, PCS_ABI, entry_BNBAmount_input,
                                 entry_GasWei_input, entry_GasLimit_input, sender_wallet, sender_pkey, OutputBox,
                                 entry_Slippage_input, entry_NumTx_input)
                elif LP_Pool == "BUSD":
                    entry_BUSDAmount_input = entry_USDAmount.get()
                    TokenBuy_BUSD(web3, entry_TokenCA_input, PCS_ROUTER_CA, PCS_ABI,
                                  entry_BUSDAmount_input,
                                  entry_GasWei_input, entry_GasLimit_input, sender_wallet, sender_pkey, OutputBox,
                                  entry_Slippage_input, entry_NumTx_input)
                elif LP_Pool == "USDT":
                    entry_USDTAmount_input = entry_USDAmount.get()
                    TokenBuy_USDT(web3, entry_TokenCA_input, PCS_ROUTER_CA, PCS_ABI,
                                  entry_USDTAmount_input,
                                  entry_GasWei_input, entry_GasLimit_input, sender_wallet, sender_pkey, OutputBox,
                                  entry_Slippage_input, entry_NumTx_input)
                entry_TokenCA.delete(0, END)
                entry_TokenCA.insert(0, entry_TokenCA_input)
    else:
        OutputBox.delete(1.0, END)
        OutputBox.insert('insert', "Not found Contract Address in clipboard, copy again!!! \n")

def ButtonSell():
    entry_TokenCA_input = entry_TokenCA.get()
    if len(entry_TokenCA_input) != 0:
        Token_add = web3.toChecksumAddress(entry_TokenCA_input)
        Token_CA = web3.eth.contract(Token_add, abi=ERC20abi_BSC)
        try:
            Token_CA.functions.symbol().call()
        except:
            tkinter.messagebox.showerror(title="Contract address Error",
                                         message="Invalid Token Contract Address, please check again!")
        else:
            LP_Pool = ListB_Pair_list.get()
            Token_Percent = ListB_sell_per.get()
            entry_GasWei_input = entry_GasWei.get()
            entry_GasLimit_input = int(entry_GasLimit.get())
            entry_Slippage_input = int(entry_Slippage.get())
            if LP_Pool == "BNB":
                TokenSell_BNB(web3, entry_TokenCA_input, PCS_ROUTER_CA, PCS_ABI, Token_Percent,
                              entry_GasWei_input, entry_GasLimit_input, sender_wallet, sender_pkey, OutputBox,
                              entry_Slippage_input)
            elif LP_Pool == "BUSD":
                TokenSell_BUSD(web3, entry_TokenCA_input, PCS_ROUTER_CA, PCS_ABI, Token_Percent,
                               entry_GasWei_input, entry_GasLimit_input, sender_wallet, sender_pkey, OutputBox,
                               entry_Slippage_input)
            elif LP_Pool == "USDT":
                TokenSell_USDT(web3, entry_TokenCA_input, PCS_ROUTER_CA, PCS_ABI, Token_Percent,
                               entry_GasWei_input, entry_GasLimit_input, sender_wallet, sender_pkey, OutputBox,
                               entry_Slippage_input)
    else:
        tkinter.messagebox.showerror(title="Contract address Error",
                                     message="Please insert Token Contract Address before sell!!!")

def ButtonApprove():
    entry_TokenCA_input = entry_TokenCA.get()
    entry_GasWei_input = entry_GasWei.get()
    entry_GasLimit_input = int(entry_GasLimit.get())
    TokenApprove(web3, entry_TokenCA_input, PCS_ROUTER_CA, PCS_ABI, entry_GasWei_input,
                 entry_GasLimit_input, sender_wallet, sender_pkey, OutputBox, entry_TokenCA)

def checkToken(_checker_CA, _token_CA):
    tokenInfos = _checker_CA.functions.getTokenInformations(_token_CA).call()
    buy_tax = round((tokenInfos[0] - tokenInfos[1]) / tokenInfos[0] * 100)
    sell_tax = round((tokenInfos[2] - tokenInfos[3]) / tokenInfos[2] * 100)
    if tokenInfos[5] and tokenInfos[6] == True:
        honeypot = False
    else:
        honeypot = True
    return buy_tax, sell_tax, honeypot

def ButtonPinkSaleBuy():
    entry_PinkILO_input = entry_PinkILO.get()
    entry_Pink_BNBAmount_input = entry_Pink_BNBAmount.get()
    entry_GasWei_input = entry_GasWei.get()
    entry_GasLimit_input = int(entry_GasLimit.get())
    PinkSaleBuy(web3, entry_PinkILO_input, entry_Pink_BNBAmount_input, entry_GasWei_input, entry_GasLimit_input,
                sender_wallet, sender_pkey, OutputBox)

def ButtonPinkSaleClaim():
    entry_PinkILO_input = entry_PinkILO.get()
    entry_GasWei_input = entry_GasWei.get()
    entry_GasLimit_input = int(entry_GasLimit.get())
    PinkSaleClaim(web3, entry_PinkILO_input, entry_GasWei_input, entry_GasLimit_input, sender_wallet, sender_pkey,
                  OutputBox)

def ButtonUniCryptBuy():
    entry_UniILO_input = entry_UniILO.get()
    entry_Uni_BNBAmount_input = entry_Uni_BNBAmount.get()
    entry_GasWei_input = entry_GasWei.get()
    entry_GasLimit_input = int(entry_GasLimit.get())
    UniBuy(web3, entry_UniILO_input, entry_Uni_BNBAmount_input, entry_GasWei_input, entry_GasLimit_input, sender_wallet,
           sender_pkey, OutputBox)

def ButtonUniCryptClaim():
    entry_UniILO_input = entry_UniILO.get()
    entry_GasWei_input = entry_GasWei.get()
    entry_GasLimit_input = int(entry_GasLimit.get())
    UniClaim(web3, entry_UniILO_input, entry_GasWei_input, entry_GasLimit_input, sender_wallet, sender_pkey, OutputBox)

def ButtonUniCryptClaim_Sell():
    entry_UniILO_input = entry_UniILO.get()
    entry_GasWei_input = entry_GasWei.get()
    entry_GasLimit_input = int(entry_GasLimit.get())
    UniClaimandSell(web3, entry_UniILO_input, entry_GasWei_input, entry_GasLimit_input, sender_wallet, sender_pkey,
                    OutputBox)

def ButtonUniCryptApproveUNCL():
    entry_UniILO_input = entry_UniILO.get()
    entry_GasWei_input = entry_GasWei.get()
    entry_GasLimit_input = int(entry_GasLimit.get())
    UniApproveUNCL(web3, entry_UniILO_input, entry_GasWei_input, entry_GasLimit_input, sender_wallet, sender_pkey,
                   OutputBox)

def ButtonUniCryptR0Reserve():
    entry_UniILO_input = entry_UniILO.get()
    entry_GasWei_input = entry_GasWei.get()
    entry_GasLimit_input = int(entry_GasLimit.get())
    UniR0Reserve(web3, entry_UniILO_input, entry_GasWei_input, entry_GasLimit_input, sender_wallet, sender_pkey,
                 OutputBox)

def ButtonPooCoin():
    entry_TokenCA_input = entry_TokenCA.get()
    Poo_link = "https://poocoin.app/tokens/{}".format(entry_TokenCA_input)
    OpenURL(Poo_link)

def ButtonHoneyPot():
    entry_TokenCA_input = entry_TokenCA.get()
    HoneyPot_link = "https://honeypot.is/?address={}".format(entry_TokenCA_input)
    OpenURL(HoneyPot_link)

def ButtonAddtoTrack():
    entry_TokenCA_input = web3.toChecksumAddress(entry_TokenCA.get())
    if file_exists('Tokens_tracking_list.txt'):
        file1 = open("Tokens_tracking_list.txt", "r")
        rl = file1.readlines()
        if entry_TokenCA_input in rl:
            tkinter.messagebox.showinfo("Tracking info", "{} Already added".format(entry_TokenCA_input))
        else:
            if len(rl) < 9:
                tracking_file = open("Tokens_tracking_list.txt", "a")
                tracking_file.write("\n{}".format(entry_TokenCA_input))
                tracking_file.close()
                tkinter.messagebox.showinfo("Tracking info", "Token added!")
            else:
                tkinter.messagebox.showinfo("Tracking info", "Currently can only add 6 tokens, please remove one to add another")
    else:
        tracking_file = open('Tokens_tracking_list.txt', "w+")
        tracking_file.write(entry_TokenCA_input)
        tracking_file.close()

def ButtonRemovefromTrack():
    entry_TokenCA_input = entry_TokenCA.get()
    flag = 0
    if file_exists('Tokens_tracking_list.txt'):
        file1 = open("Tokens_tracking_list.txt", "r")
        rl = file1.readlines()
        re_write_lst = []
        for line1 in rl:
            line1 = line1.replace("\n", "")
            if entry_TokenCA_input.lower() in line1.lower():
                line1 = line1.replace(entry_TokenCA_input, '')
                flag = 1
            else:
                re_write_lst.append(line1)
        file1.close()
        file2 = open("Tokens_tracking_list.txt", "w+")
        for line in re_write_lst:
            file2.write("{}\n".format(line))
        size = file2.tell()
        if(size>2):
            file2.truncate(size-2)
        file2.close()
        if flag == 1:
            tkinter.messagebox.showinfo("Tracking info", "Token removed!")
        else:
            tkinter.messagebox.showinfo("Tracking info", "Token not found in tracking list!")
    else:
        tkinter.messagebox.showinfo("Tracking info", "No tracking data yet!")

def ShowTrackList(_Output_Box):
    if file_exists('Tokens_tracking_list.txt'):
        file1 = open("Tokens_tracking_list.txt", "r")
        Showlist = []
        read_lines = file1.readlines()
        showMessage = "Your tracking {} token(s): \n".format(len(read_lines))
        for token in read_lines:
            token_CA = web3.toChecksumAddress(token.strip())
            token_contract = web3.eth.contract(address=token_CA,
                                           abi=ERC20abi_BSC)
            token_symbol = token_contract.functions.symbol().call()
            token_name = token_contract.functions.name().call()
            Showlist.append([token_name , token_symbol, token_CA])
        file1.close()
        for token in Showlist:
            showMessage = showMessage + "Token name: {} ({}) \n  - Contract adddress: {} \n".format(token[0],token[1],token[2])
        _Output_Box.delete(1.0, END)
        _Output_Box.insert('insert', showMessage)
        _Output_Box.update()

def ButtonShowTrackList():
    ShowTrackList(OutputBox)

def ButtonSendToken():
    entry_send_token_CA_input = entry_send_token_CA.get()
    entry_send_token_Amount = entry_send_Amount.get()
    entry_send_token_to_wallet_input = entry_send_token_to_wallet.get()
    entry_GasWei_input = entry_GasWei.get()
    entry_GasLimit_input = int(entry_GasLimit.get())
    SendToken(web3, entry_send_token_CA_input,entry_send_token_to_wallet_input, entry_send_token_Amount, entry_GasWei_input, entry_GasLimit_input,
                sender_wallet, sender_pkey, OutputBox)
def EnterBuy(event):
    entry_TokenCA_input = entry_TokenCA.get()
    entry_BNBAmount_input = entry_BNBAmount.get()
    entry_GasWei_input = entry_GasWei.get()
    entry_GasLimit_input = int(entry_GasLimit.get())
    TokenBuy_BNB(web3, entry_TokenCA_input, PCS_ROUTER_CA, PCS_ABI, entry_BNBAmount_input,
                 entry_GasWei_input, entry_GasLimit_input, sender_wallet, sender_pkey, OutputBox)

def Auto_Paste():
    flag = AutoPaste_flag.get()
    if flag == 1:
        stringtext = str(top.clipboard_get())
        if "0x" in stringtext:
            CA = str(stringtext[stringtext.find("0x"):int(stringtext.find("0x") + 42)])
            entry_TokenCA.delete(0, END)
            entry_TokenCA.insert(0, CA)

def CtrlD_PastenBuy(event):
    stringtext = str(top.clipboard_get())
    if "0x" in stringtext:
        entry_TokenCA_input = str(stringtext[stringtext.find("0x"):int(stringtext.find("0x") + 42)])
        entry_GasWei_input = entry_GasWei.get()
        entry_GasLimit_input = int(entry_GasLimit.get())
        entry_Slippage_input = int(entry_Slippage.get())
        LP_Pool = ListB_Pair_list.get()
        if LP_Pool == "BNB":
            entry_BNBAmount_input = entry_BNBAmount.get()
            TokenBuy_BNB(web3, entry_TokenCA_input, PCS_ROUTER_CA, PCS_ABI, entry_BNBAmount_input,
                         entry_GasWei_input, entry_GasLimit_input, sender_wallet, sender_pkey, OutputBox,
                         entry_Slippage_input)
        elif LP_Pool == "BUSD":
            entry_BUSDAmount_input = entry_USDAmount.get()
            TokenBuy_BUSD(web3, entry_TokenCA_input, PCS_ROUTER_CA, PCS_ABI, entry_BUSDAmount_input,
                          entry_GasWei_input, entry_GasLimit_input, sender_wallet, sender_pkey, OutputBox,
                          entry_Slippage_input)
        elif LP_Pool == "USDT":
            entry_USDTAmount_input = entry_USDAmount.get()
            TokenBuy_USDT(web3, entry_TokenCA_input, PCS_ROUTER_CA, PCS_ABI, entry_USDTAmount_input,
                          entry_GasWei_input, entry_GasLimit_input, sender_wallet, sender_pkey, OutputBox,
                          entry_Slippage_input)
        entry_TokenCA.delete(0, END)
        entry_TokenCA.insert(0, entry_TokenCA_input)
    else:
        OutputBox.delete(1.0, END)
        OutputBox.insert('insert', "Not found Contract Address in clipboard, copy again!!! \n")

def get_LP_balance(_web3, _token_CA, _token_abi, _LP_add):
    #token_add = _web3.toChecksumAddress(_token_CA)
    #LP_add_checksum = _web3.toChecksumAddress(_LP_add)
    token_contract = _web3.eth.contract(_token_CA, abi=_token_abi)
    token_balance = token_contract.functions.balanceOf(_LP_add).call()
    return token_balance

def get_LP_add(_web3, _token1, _token2):
    token_list_origin = [_token1, _token2]
    sort_list = [token_list_origin[0].lower(), token_list_origin[1].lower()]
    sort_list.sort()
    tokek_list_new = [_web3.toChecksumAddress(sort_list[0]), _web3.toChecksumAddress(sort_list[1])]
    abiEncoded_1 = encode_abi_packed(['address', 'address'], (tokek_list_new[0], tokek_list_new[1]))
    salt_ = Web3.solidityKeccak(['bytes'], ['0x' + abiEncoded_1.hex()])
    abiEncoded_2 = encode_abi_packed(['address', 'bytes32'], (factory, salt_))
    resPair = Web3.solidityKeccak(['bytes', 'bytes'], ['0xff' + abiEncoded_2.hex(), hexadem_])[12:]
    LP_address = _web3.toChecksumAddress(resPair.hex())
    return LP_address

def check_LP(_web3, _token_CA, _token_abi):
    token_add = _web3.toChecksumAddress(_token_CA)
    BNB_add = _web3.toChecksumAddress("0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c")
    BUSD_add = _web3.toChecksumAddress("0xe9e7CEA3DedcA5984780Bafc599bD69ADd087D56")
    USDT_add = _web3.toChecksumAddress("0x55d398326f99059ff775485246999027b3197955")

    BNB_LP_add = get_LP_add(_web3, BNB_add, token_add)
    BUSD_LP_add = get_LP_add(_web3, token_add, BUSD_add)
    USDT_LP_add = get_LP_add(_web3, token_add, USDT_add)
    ## BNB/Token pair ##
    LPBNB_BNB_balance = get_LP_balance(_web3, BNB_add, _token_abi, BNB_LP_add)
    ## BUSD/Token pair ##
    LPBUSD_BUSD_balance = get_LP_balance(_web3, BUSD_add, _token_abi, BUSD_LP_add)
    ## USDT/Token pair ##
    LPUSDT_USDT_balance = get_LP_balance(_web3, USDT_add, _token_abi, USDT_LP_add)
    return LPBNB_BNB_balance, LPBUSD_BUSD_balance, LPUSDT_USDT_balance

def check_LP_v2(_web3,_token_CA,_token_decimal,_BNB_price,_BUSD_price):
    LPBNB_BNB_balance = 0
    LPBUSD_BUSD_balance = 0
    LPUSDT_USDT_balance = 0

    token_address = Web3.toChecksumAddress(_token_CA)
    bnb_pair = factory_contract.functions.getPair(token_address, WBNB_add).call()
    busd_pair = factory_contract.functions.getPair(token_address,BUSD_add).call()
    usdt_pair = factory_contract.functions.getPair(token_address,USDT_add).call()
    default_pair_value = "0x0000000000000000000000000000000000000000"
    if bnb_pair != default_pair_value:
        pair_contract_bnb = _web3.eth.contract(address=bnb_pair, abi=LP_abi)
        is_BNB_reversed = pair_contract_bnb.functions.token0().call() == WBNB_add
        (
            reserve0_bnb,
            reserve1_bnb,
            blockTimestampLast,
        ) = pair_contract_bnb.functions.getReserves().call()
        if is_BNB_reversed:
            peg_reserve = reserve0_bnb
            token_reserve = reserve1_bnb
        else:
            peg_reserve = reserve1_bnb
            token_reserve = reserve0_bnb
        if peg_reserve != 0 and token_reserve != 0:
            LPBNB_BNB_balance = float(peg_reserve) / 10**WBNB_Decimal
            LPBNB_BNB_balance_in_USDT = LPBNB_BNB_balance * _BNB_price
            price_in_BNB = LPBNB_BNB_balance / (float(token_reserve) / 10 ** _token_decimal)
            BNB_price_in_USDT = price_in_BNB * _BNB_price

    if busd_pair != default_pair_value:
        pair_contract_busd = _web3.eth.contract(address=busd_pair, abi=LP_abi)
        is_BUSD_reversed = pair_contract_busd.functions.token0().call() == BUSD_add
        (
            reserve0_busd,
            reserve1_busd,
            blockTimestampLast,
        ) = pair_contract_busd.functions.getReserves().call()
        if is_BUSD_reversed:
            peg_reserve = reserve0_busd
            token_reserve = reserve1_busd
        else:
            peg_reserve = reserve1_busd
            token_reserve = reserve0_busd
        if peg_reserve != 0 and token_reserve != 0:
            LPBUSD_BUSD_balance = float(peg_reserve) / 10**BUSD_Decimal
            price_in_BUSD = LPBUSD_BUSD_balance / (float(token_reserve) / 10 ** _token_decimal)
            LPBUSD_BUSD_balance_in_USDT = LPBUSD_BUSD_balance * _BUSD_price
            BUSD_price_in_USDT = price_in_BUSD * _BUSD_price

    if usdt_pair != default_pair_value:
        pair_contract_usdt = _web3.eth.contract(address=usdt_pair, abi=LP_abi)
        is_USDT_reversed = pair_contract_usdt.functions.token0().call() == USDT_add
        (
            reserve0_usdt,
            reserve1_usdt,
            blockTimestampLast,
        ) = pair_contract_usdt.functions.getReserves().call()
        if is_USDT_reversed:
            peg_reserve = reserve0_usdt
            token_reserve = reserve1_usdt
        else:
            peg_reserve = reserve1_usdt
            token_reserve = reserve0_usdt
        if peg_reserve != 0 and token_reserve != 0:
            LPUSDT_USDT_balance = float(reserve1_usdt) / 10**USDT_Decimal
            USDT_price_in_USDT = LPUSDT_USDT_balance / (float(token_reserve) / 10 ** _token_decimal)

    token_LPs = {"BNB":[BNB_price_in_USDT,LPBNB_BNB_balance_in_USDT] , "BUSD":[BUSD_price_in_USDT,LPBUSD_BUSD_balance_in_USDT] , "USDT":[USDT_price_in_USDT,LPUSDT_USDT_balance]}
    #tokenPrice = min(token_LPs,key=token_LPs.get)
    find_max = max(token_LPs.items(), key=lambda x: x[0][1])
    print(find_max)
    LP_max = find_max[0]
    LP_price = token_LPs[LP_max][0]
    print(LP_max,LP_price)
    #print(tokenPrice.items())
    return float(LPBNB_BNB_balance), float(LPBUSD_BUSD_balance), float(LPUSDT_USDT_balance)

def TokenPrice(tokenAddress):
    apiURL = "https://api.pancakeswap.info/api/v2/tokens/"
    response = requests.get(url = apiURL + tokenAddress)
    jsonRaw_00 = response.json()
    price = jsonRaw_00['data']['price']
    return price

def BNB_to_USDT() :
    amountOut = int(PCScontract.functions.getAmountsOut(1 * 10 ** WBNB_Decimal, [
        web3.toChecksumAddress(WBNB_add),
        web3.toChecksumAddress(USDT_add)]).call()[-1]) / 10 ** 18
    return amountOut

def BUSD_to_USDT() :
    PCScontract = web3.eth.contract(address=web3.toChecksumAddress(PCS_ROUTER_CA), abi=PCS_ABI)
    amountOut = int(PCScontract.functions.getAmountsOut(1 * 10 ** BUSD_Decimal, [
        web3.toChecksumAddress(BUSD_add),
        web3.toChecksumAddress(USDT_add)]).call()[-1]) / 10 ** 18
    return amountOut


################# GUI ##########################

###  Window app Setting ###
top = Tk()
# top.title("All-in-One - V0.0 - By Ikamo | ROD Labs")
top.title("Quick Ape - V0.1 - PancakeSwap - Demo Version")
top.geometry("865x720-800+200")
# top.iconbitmap("Data\RODLabsIcon.ico")
top.iconbitmap("Data\SwapIcon.ico")
top.resizable(False, False)

top.bind('<Control-g>', CtrlD_PastenBuy)

###########################
## Frame ##

frame_setting = LabelFrame(top, text="Settings", width=390, height=100, bd=3)
frame_setting.place(x=8, y=115)
frame_Send_token = LabelFrame(top, text="Send Token", width=470, height=89, bd=3)
frame_Send_token.place(x=378, y=352)
frame_Presale = LabelFrame(top, text="Pre-sales", width=578, height=140, bd=3)
frame_Presale.place(x=8, y=215)
frame_Token_track = LabelFrame(top, text="Tokens tracking", width=257, height=325, bd=3)
frame_Token_track.place(x=590, y=30)

## Lable setting ##
# lbl_BSC_Node = Label(top, text = "BSC Node: " ).place(x=10,y=2)

lbl_TokenCA = Label(top, text="Token Address (CA)").place(x=10, y=30)
lbl_BNBAmount = Label(top, text="BNB Amount").place(x=50, y=131)
lbl_USDAmount = Label(top, text="BUSD/USDT Amount").place(x=11, y=156)
lbl_GasWei = Label(top, text="Gaswei").place(x=180, y=131)
lbl_GasLimit = Label(top, text="Gas Limit").place(x=260, y=131)
lbl_PinkILO = Label(top, text="Pinksale Presale Address").place(x=10, y=235)
lbl_Pink_BNBAmount = Label(top, text="Pinksale BNB Amount").place(x=23, y=260)
lbl_UniILO = Label(top, text="Unicrypt Presale Address").place(x=10, y=295)
lbl_Uni_BNBAmount = Label(top, text="Unicrypt BNB Amount").place(x=21, y=325)
# lbl_Token_Check = Label(top, text = "Crypto Bot | Token Name:").place(x=660,y=31)
lbl_MultiTx = Label(top, text="No. Tx").place(x=180, y=156)
lbl_Sell_Percent = Label(top, text="% Token sell").place(x=260, y=156)
# lbl_DEX = Label(top,text="DEX:").place(x=390,y=3)
lbl_Pair = Label(top, text="Token Pair (or LP)").place(x=45, y=4)
lbl_Slippage = Label(top, text="Slippage (%)").place(x=53, y=180)

lbl_token_name = Label(top, text="Token name: ")
lbl_token_name.place(x=48, y=52)
lbl_token_buytax = Label(top, text="Buy tax: ")
lbl_token_buytax.place(x=210, y=70)
lbl_token_selltax = Label(top, text="Sell tax: ")
lbl_token_selltax.place(x=290, y=70)
lbl_token_honey = Label(top, text="Honey Pot: ")
lbl_token_honey.place(x=415, y=30)

lbl_token_amount = Label(top, text="Token Price:    N/A")
lbl_token_amount.place(x=52, y=70)
lbl_token_balance = Label(top, text="Wallet balance:    N/A")
lbl_token_balance.place(x=36, y=88)

lbl_Clipboard = Label(top, text="Current clipboard ").place(x=10, y=695)
lb_BNB_LP = Label(top, text="-BNB LP:  ")
lb_BNB_LP.place(x=415, y=52)

lb_BUSD_LP = Label(top, text="-BUSD LP:  ")
lb_BUSD_LP.place(x=415, y=70)

lb_USDT_LP = Label(top, text="-USDT LP:  ")
lb_USDT_LP.place(x=415, y=88)

lbl_send_TokenCA = Label(top, text="Token CA").place(x=385, y=370)
lbl_send_Token_amount = Label(top, text="Send Amount").place(x=385, y=392)
lbl_send_to_wallet = Label(top, text="To wallet").place(x=385, y=414)
lbl_send_TokenName = Label(top, text="Token Name: ")
lbl_send_TokenName.place(x=720, y=369)
lbl_send_Wallet_balance = Label(top, text="Wallet balance: ")
lbl_send_Wallet_balance.place(x=535, y=391)

lbl_BNB_Price = Label(top, text="BNB_Price: ")
lbl_BNB_Price.place(x=415, y=4)

## Button setting ##
bt_Buy = Button(top, text="Buy", command=ButtonBuy, width=6, height=1)
bt_Buy.place(x=400, y=122)
bt_Sell = Button(top, text="Sell", command=ButtonSell, width=6, height=1)
bt_Sell.place(x=400, y=187)
bt_approve = Button(top, text="Approve", command=ButtonApprove, width=7, height=1)
bt_approve.place(x=457, y=122)
bt_PasteBuy = Button(top, text="Paste & Buy", command=ButtonPastenBuy, width=15, height=1)
bt_PasteBuy.place(x=400, y=154)

bt_Honey = Button(top, text="HoneyPot", command=ButtonHoneyPot, width=8, height=1)
bt_Honey.place(x=520, y=122)
bt_Poo = Button(top, text="PooCoin", command=ButtonPooCoin, width=8, height=1)
bt_Poo.place(x=520, y=154)
bt_PinkSale = Button(top, text="Pink Buy", command=ButtonPinkSaleBuy, width=10, height=1)
bt_PinkSale.place(x=220, y=258)
bt_PinkClaim = Button(top, text="Pink Claim", command=ButtonPinkSaleClaim, width=10, height=1)
bt_PinkClaim.place(x=305, y=258)
# bt_Pink_Claim_Sell= Button(top, text="Claim & Sell all",width=14,height=1,bg="#33F6FF")
# bt_Pink_Claim_Sell.place(x=390,y=233)

bt_Uni = Button(top, text="Uni Buy", command=ButtonUniCryptBuy, width=10, height=1)
bt_Uni.place(x=220, y=320)
bt_Uni_Claim = Button(top, text="Uni Claim", command=ButtonUniCryptClaim, width=10, height=1)
bt_Uni_Claim.place(x=305, y=320)
bt_Uni_Claim_Sell = Button(top, text="Claim & Sell all", command=ButtonUniCryptClaim_Sell, width=14, height=1)
bt_Uni_Claim_Sell.place(x=390, y=320)
bt_Uni_pre_approve = Button(top, text="Approve UNCL", command=ButtonUniCryptApproveUNCL, width=14, height=1)
bt_Uni_pre_approve.place(x=461, y=290)
bt_Uni_R0_Reserve = Button(top, text="R0 Reserve", command=ButtonUniCryptR0Reserve, width=8, height=1)
bt_Uni_R0_Reserve.place(x=503, y=320)

bt_Add_to_list = Button(top, text="Add track", command=ButtonAddtoTrack, width=9, height=1)
bt_Add_to_list.place(x=590, y=3)
bt_Remove_from_list = Button(top, text="Remove track", command=ButtonRemovefromTrack, width=11, height=1)
bt_Remove_from_list.place(x=667, y=3)
bt_Show_list = Button(top, text="Show track list", command=ButtonShowTrackList, width=11, height=1)
bt_Show_list.place(x=758, y=3)

bt_Send_token = Button(top, text="Send Token", command=ButtonSendToken, width=11, height=1)
bt_Send_token.place(x=725, y=410)

TokenCA_var = StringVar()
entry_TokenCA = Entry(top, width=46, textvariable=TokenCA_var)
entry_TokenCA.place(x=130, y=31)

entry_PinkILO = Entry(top, width=46)
entry_PinkILO.place(x=150, y=235)
entry_Pink_BNBAmount = Entry(top, width=10)
entry_Pink_BNBAmount.place(x=150, y=260)
entry_Pink_BNBAmount.insert(END, init_BNB)

entry_UniILO = Entry(top, width=46)
entry_UniILO.place(x=150, y=295)
entry_Uni_BNBAmount = Entry(top, width=10)
entry_Uni_BNBAmount.place(x=150, y=325)
entry_Uni_BNBAmount.insert(END, init_BNB)

entry_BNBAmount = Entry(top, width=7)
entry_BNBAmount.place(x=130, y=132)
entry_BNBAmount.insert(END, init_BNB)

entry_USDAmount = Entry(top, width=7)
entry_USDAmount.place(x=130, y=157)
entry_USDAmount.insert(END, '50')

entry_GasWei = Entry(top, width=5)
entry_GasWei.place(x=225, y=132)
entry_GasWei.insert(END, '5')

entry_GasLimit = Entry(top, width=10)
entry_GasLimit.place(x=320, y=132)
entry_GasLimit.insert(END, '1500000')

entry_NumTx = Entry(top, width=5)
entry_NumTx.place(x=225, y=157)
entry_NumTx.insert(END, '1')

entry_Slippage = Entry(top, width=7)
entry_Slippage.place(x=130, y=182)
entry_Slippage.insert(END, '100')

send_TokenCA_var = StringVar()
entry_send_token_CA = Entry(top, width=45,textvariable=send_TokenCA_var)
entry_send_token_CA.place(x=445, y=370)

entry_send_Amount = Entry(top, width=10)
entry_send_Amount.place(x=470, y=392)
entry_send_Amount.insert(END, "1")

entry_send_token_to_wallet = Entry(top, width=45)
entry_send_token_to_wallet.place(x=445, y=414)

## Text Box ##
OutputBox = Text(top, height=15, width=104)
OutputBox.place(x=10, y=445)

WalletBox = Text(top, height=5, width=45)
WalletBox.place(x=9, y=355)

ClipboardBox = Text(top, height=1, width=80)
ClipboardBox.place(x=113, y=695)

## Check box ##
AutoLP_flag = IntVar()
AutoLP_CheckBox = Checkbutton(top, text="Auto-LP", variable=AutoLP_flag)
#AutoLP_CheckBox.place(x=213, y=3)

AutoPaste_flag = IntVar()
AutoPaste_CheckBox = Checkbutton(top, text="Auto-Paste", variable=AutoPaste_flag)
AutoPaste_CheckBox.place(x=280, y=3)

## List Box ##
Sell_per_list = ("100", "99", "75", "50", "25", "10")
ListB_sell_per = Combobox(top, value=Sell_per_list, width=4)
ListB_sell_per.insert(END, "99")
ListB_sell_per.place(x=338, y=157)

# DEX_list = ("PCS.v2","ApeSwap")
# ListB_DEX_list = Combobox(top,value=DEX_list,width=6)
# ListB_DEX_list.insert(END,"PCSv2")
# ListB_DEX_list.place(x=420,y=4)

Pair_list = ("BNB", "BUSD", "USDT")
ListB_Pair_list = Combobox(top, value=Pair_list, width=6)
ListB_Pair_list.insert(END, "BNB")
ListB_Pair_list.place(x=150, y=4)

#### LICENSE CHECK #####
Demo_license_CA = "0x2043718096ba51727831DB231556a5889170bd74"  ## QAT License V1R0
# wallet_address_lic  = '0x605D53Fa4892cB2C2B92BE0340461B6C4948540b'
# if userconfig.wallet_address != wallet_address_lic:
#    tkinter.messagebox.showerror(title="Wrong Wallet", message="Please check your wallet setting in userconfig.py. Your registered wallet: {}".format(wallet_address_lic))
#    top.destroy()

### BSC ###
web3 = Web3(Web3.HTTPProvider(user_RPC, request_kwargs={'timeout': 60}))
checker = web3.eth.contract(address=web3.toChecksumAddress(CHECKER_CA), abi=CHECKER_ABI)
factory_contract = web3.eth.contract(address=factory_address, abi=dex["FACTORY_ABI"])
PCScontract = web3.eth.contract(address=web3.toChecksumAddress(PCS_ROUTER_CA), abi=PCS_ABI)

#web3_testnet = Web3(Web3.HTTPProvider(TESTNET_RPC, request_kwargs={'timeout': 60}))
if web3.isConnected() == False:
    tkinter.messagebox.showerror(title="BSC Connection Error",
                                 message="Please check you network then re-open the tool!")
    top.destroy()

### Wallet setting ###
sender_wallet = user_wallet_address
sender_pkey = user_private_key

if not Web3.isAddress(sender_wallet):
    if sender_wallet == "":
        tkinter.messagebox.showerror(title="Wrong wallet address format!", message="No wallet address setting in userconfig.json yet, please set your registerd wallet address and private key before using tool!")
    else:
        tkinter.messagebox.showerror(title="Wrong wallet address format!",
                                     message="Please check your wallet address setting in userconfig.json")

#DateTimeConverter_CA = web3_testnet.eth.contract(address=web3.toChecksumAddress("0xE17C618963f7b0699a7AffEa6592663096eF75ca"), abi=DT_CONV_ABI)

lic_CA = web3.eth.contract(address=web3.toChecksumAddress(Demo_license_CA), abi=License_ABI)
is_Demo = lic_CA.functions.IsDemo(sender_wallet).call()
is_Full = lic_CA.functions.IsFull(sender_wallet).call()
expire_timestamp = lic_CA.functions.EndLicenseOf(sender_wallet).call()

# exp_year = DateTimeConverter_CA.functions.getYear(expire_timestamp).call()
# exp_month = DateTimeConverter_CA.functions.getMonth(expire_timestamp).call()
# exp_day = DateTimeConverter_CA.functions.getDay(expire_timestamp).call()
# exp_hour = DateTimeConverter_CA.functions.getHour(expire_timestamp).call()
# exp_minute = DateTimeConverter_CA.functions.getMinute(expire_timestamp).call()

if is_Full == 0 and is_Demo == 0 :
    tkinter.messagebox.showerror(title="No License detected!", message="Your wallet: {} doesn't have license, please check with us at @QuickApeTool!".format(user_wallet_address))
    top.destroy()

if is_Full == 1 :
    top.title("Quick Ape - V0.1 - PancakeSwap - Full License Version")
#else :
#    top.title("Quick Ape - V0.1 - PancakeSwap - Demo License Version - Expiration date: {}/{}/{} | {}:{} (UTC time)".format(exp_year,exp_month,exp_day,exp_hour,exp_minute))

try:
    acct = Account.from_key(sender_pkey)
except:
    tkinter.messagebox.showwarning(title="Private key format",
                                   message="Maybe your private key is not in good format, please check again!")
else:
    if str(acct.address) != sender_wallet:
        tkinter.messagebox.showwarning(title= "Wrong wallet setting", message="Please check your wallet and private key again, something is wrong!")

def on_closing():
    if tkinter.messagebox.askokcancel("Quit", "Do you want to quit?"):
        top.destroy()

def updateWallet():
    BNB_price = BNB_to_USDT()
    #### Update wallet ####
    balance_converted = web3.fromWei(web3.eth.get_balance(sender_wallet), 'ether')
    BUSD_CA = web3.eth.contract(address=web3.toChecksumAddress(BUSD_add), abi=BUSD_Abi)
    BUSD_balance = BUSD_CA.functions.balanceOf(sender_wallet).call()
    USDT_CA = web3.eth.contract(address=web3.toChecksumAddress(USDT_add), abi=USDT_Abi)
    USDT_balance = USDT_CA.functions.balanceOf(sender_wallet).call()
    WalletBox.delete(1.0, END)
    WalletBox.insert('insert',
                     "Wallet address:\n- {}\n  --> {:.3f} BNB ({:.3f} USD)\n  --> {} BUSD\n  --> {} USDT\n".format(
                         sender_wallet, float(balance_converted), float(balance_converted)*float(BNB_price),
                         str(round(BUSD_balance / 10 ** BUSD_Decimal, 3)),
                         str(round(USDT_balance / 10 ** USDT_Decimal, 3))))
    WalletBox.update()

def updateTokenInfo(var, index, mode):
    entry_TokenCA_input = TokenCA_var.get()
    if entry_TokenCA_input != None:
        try:
            sellTokenContract = web3.eth.contract(address=web3.toChecksumAddress(entry_TokenCA_input),
                                                  abi=ERC20abi_BSC)
        except:
            lbl_token_name.config(text="Token name:    {}".format("Not found!"))
        else:
            try:
                token_symbol = sellTokenContract.functions.symbol().call()
            except:
                lbl_token_name.config(text="Token name:    {}".format("Not found!"))
            else:
                balance = sellTokenContract.functions.balanceOf(sender_wallet).call()
                allowance = sellTokenContract.functions.allowance(user_wallet_address,
                                                                  PCS_ROUTER_CA).call()
                if allowance == 0:
                    lbl_token_name.config(
                        text="Token name:    {}  ---  Please approve token before sell!".format(str(token_symbol)))
                else:
                    if allowance > balance:
                        lbl_token_name.config(text="Token name:    {}  ---  Approved, you can sell if you want!".format(
                            str(token_symbol)))
                    else:
                        sell_percent = (allowance / balance) * 100
                        lbl_token_name.config(
                            text="Token name:    {}  ---  You can only sell {}% of your token!".format(
                                str(token_symbol), str(round(sell_percent, 2))))

def updateSendTokenInfo(var, index, mode):
    send_TokenCA_var_input = send_TokenCA_var.get()
    if send_TokenCA_var_input != None:
        try:
            sellTokenContract = web3.eth.contract(address=web3.toChecksumAddress(send_TokenCA_var_input),
                                                  abi=ERC20abi_BSC)
        except:
            lbl_send_TokenName.config(text="Token name: \n{}".format("Not found!"))
        else:
            try:
                token_symbol = sellTokenContract.functions.symbol().call()
            except:
                lbl_send_TokenName.config(text="Token name: \n{}".format("Not found!"))
                tkinter.messagebox.showerror("Send token error","Provided address is not a BSC Token CA!")
                entry_send_token_CA.insert(END,"")
            else:
                balance = sellTokenContract.functions.balanceOf(sender_wallet).call()
                token_name = sellTokenContract.functions.name().call()
                token_decimal = sellTokenContract.functions.decimals().call()
                lbl_send_TokenName.config(text="Token Name: \n{:<} ({})".format(token_name,token_symbol))
                lbl_send_Wallet_balance.config(text="Wallet balance: {:.3f}".format(balance/10**token_decimal))

def updateStablePrice():
    BNB_price = float(TokenPrice(WBNB_add))
    time.sleep(3)
    BUSD_price = float(TokenPrice(BUSD_add))
    time.sleep(3)
    USDT_price = float(TokenPrice(USDT_add))
    time.sleep(3)
    return BNB_price, BUSD_price, USDT_price

def updateTokenPriceandWalletAmount():
    start = time.perf_counter()
    global checker
    BNB_price_in_USDT = BNB_to_USDT()
    print(f"{time.perf_counter() - start:0.4f} seconds for BNB_to_USDT")
    lbl_BNB_Price.config(text="BNB Price: {:.3f}".format(BNB_price_in_USDT))
    BUSD_price_in_USDT = BUSD_to_USDT()
    entry_TokenCA_input = TokenCA_var.get()
    if len(entry_TokenCA_input) != 0:
        try:
            sellTokenContract = web3.eth.contract(address=web3.toChecksumAddress(entry_TokenCA_input),
                                                  abi=ERC20abi_BSC)
            token_decimal = sellTokenContract.functions.decimals().call()
        except:
            lbl_token_amount.config(text="Token Price: N/A")
            lbl_token_balance.config(text="Wallet balance: N/A")
            lbl_token_buytax.config(
                text="Buy tax: ")
            lbl_token_honey.config(
                text="Honey Pot: ", fg='black')
            lbl_token_selltax.config(
                text="Sell tax: ", fg='black')
        else:
            balance = sellTokenContract.functions.balanceOf(sender_wallet).call()
            readable = balance / 10 ** token_decimal

            ## New token price + LP ##
            #Token_LP = check_LP(web3, entry_TokenCA_input, token_ABI)
            print(f"{time.perf_counter() - start:0.4f} seconds until token check")
            tag1 = time.perf_counter()
            Token_LP = check_LP_v2(web3, entry_TokenCA_input, token_decimal, BNB_price_in_USDT, BUSD_price_in_USDT)
            print(f"{time.perf_counter() - tag1:0.4f} seconds for checkLP_v2")
            ## Find biggest LP ##
            max = float(Token_LP[0]) * float(BNB_price_in_USDT)
            biggest = "BNB"
            if float(Token_LP[1]) > max:
                max = float(Token_LP[1])
                biggest = "BUSD"
            if float(Token_LP[2]) > max:
                max = float(Token_LP[2])
                biggest = "USDT"

            ## Token price calculation ##
            if max != 0:
                try:
                    TokenInfo = checkToken(checker, web3.toChecksumAddress(entry_TokenCA_input))
                except:
                    lbl_token_honey.config(text="Honey Pot: Unknown! ", fg='orange')
                else:
                    if TokenInfo[2] == True:
                        honeypot_str = "Rugged"
                        FG = 'red'
                    else:
                        honeypot_str = "Safe"
                        FG = 'green'
                    if TokenInfo[1] > 80:
                        Sell_FG = 'red'
                        lbl_token_selltax.config(
                            text="Sell tax: {}%".format(str(TokenInfo[1])), fg=Sell_FG)
                    else:
                        lbl_token_selltax.config(
                            text="Sell tax: {}%".format(str(TokenInfo[1])), fg='black')
                    lbl_token_buytax.config(
                        text="Buy tax: {}%".format(str(TokenInfo[0])))
                    lbl_token_honey.config(
                        text="Honey Pot: {}".format(honeypot_str), fg=FG)
                    tag2 = time.perf_counter()
                    TokenPrice = 0.00
                    Wallet_balance_USD = 0.00
                    Wallet_balance_BNB = 0.00
                    if biggest == "BNB":
                        amountOutBNB = int(PCScontract.functions.getAmountsOut(1 * 10 ** token_decimal, [
                            web3.toChecksumAddress(entry_TokenCA_input),
                            web3.toChecksumAddress(WBNB_add)]).call()[-1]) / 10 ** 18
                        TokenPrice = amountOutBNB * BNB_price_in_USDT
                        Wallet_balance_USD = TokenPrice * balance / 10 ** token_decimal
                        Wallet_balance_BNB = Wallet_balance_USD / BNB_price_in_USDT
                        ## Update  LP ##
                        lb_BNB_LP.config(text="-BNB LP: {:.3f} BNB".format( float(Token_LP[0])), fg='green')
                        lb_BUSD_LP.config(
                            text="-BUSD LP: {:.1f} BUSD".format( float(Token_LP[1])), fg='black')
                        lb_USDT_LP.config(
                            text="-USDT LP: {:.1f} USDT".format( float(Token_LP[2])), fg='black')
                    if biggest == "BUSD":
                        amountOutBUSD = int(PCScontract.functions.getAmountsOut(1 * 10 ** token_decimal, [
                            web3.toChecksumAddress(entry_TokenCA_input),
                            web3.toChecksumAddress(BUSD_add)]).call()[-1]) / 10 ** 18
                        TokenPrice = amountOutBUSD * BUSD_price_in_USDT
                        Wallet_balance_USD = TokenPrice * balance / 10 ** token_decimal
                        Wallet_balance_BNB = Wallet_balance_USD / BNB_price_in_USDT
                        ## Update  LP ##
                        lb_BNB_LP.config(text="-BNB LP: {:.3f} BNB".format( float(Token_LP[0])), fg='black')
                        lb_BUSD_LP.config(
                            text="-BUSD LP: {:.1f} BUSD".format( float(Token_LP[1])), fg='green')
                        lb_USDT_LP.config(
                            text="-USDT LP: {:.1f} USDT".format( float(Token_LP[2])), fg='black')
                    if biggest == "USDT":
                        TokenPrice = int(PCScontract.functions.getAmountsOut(1 * 10 ** token_decimal, [
                            web3.toChecksumAddress(entry_TokenCA_input),
                            web3.toChecksumAddress(USDT_add)]).call()[-1]) / 10 ** 18
                        Wallet_balance_USD = TokenPrice * balance / 10 ** token_decimal
                        Wallet_balance_BNB = Wallet_balance_USD / BNB_price_in_USDT

                        lb_BNB_LP.config(text="-BNB LP: {:.3f} BNB".format( float(Token_LP[0]) / 10 ** float(
                            WBNB_Decimal)), fg='black')
                        lb_BUSD_LP.config(
                            text="-BUSD LP: {:.1f} BUSD".format( float(Token_LP[1]) / 10 ** float(
                                WBNB_Decimal)), fg='black')
                        lb_USDT_LP.config(
                            text="-USDT LP: {:.1f} USDT".format( float(Token_LP[2]) / 10 ** float(
                                WBNB_Decimal)), fg='green')
                    ## Print out price and wallet balance info##
                    if TokenPrice < 0.001:
                        lbl_token_amount.config(
                            text="Token Price:  {:.2e} USD".format(TokenPrice))
                    else:
                        lbl_token_amount.config(
                            text="Token Price:  {:.3f} USD".format(TokenPrice))
                    lbl_token_balance.config(
                        text="Wallet balance:  {:.3f} ({:.1f} USD - {:.3f} BNB - {:.3f} BNB(wTax))".format(readable,
                                                                                           Wallet_balance_USD,
                                                                                           Wallet_balance_BNB,
                                                                                           float(Wallet_balance_BNB) - float(Wallet_balance_BNB)*float(TokenInfo[1])/100))
                    print(f"{time.perf_counter() - tag1:0.4f} seconds for token price check and wallet amount")
            else:
                lbl_token_amount.config(text="Token Price: N/A")
                lbl_token_balance.config(text="Wallet balance: N/A")
                lbl_token_buytax.config(
                    text="Buy tax: ")
                lbl_token_honey.config(
                    text="Honey Pot: ", fg='black')
                lbl_token_selltax.config(
                    text="Sell tax: ", fg='black')
                lbl_token_honey.config(
                    text="Honey Pot: Unknown! ", fg='orange')
                lb_BNB_LP.config(text="-BNB LP: N/A BNB", fg='black')
                lb_BUSD_LP.config(
                    text="-BUSD LP: N/A BUSD", fg='black')
                lb_USDT_LP.config(
                    text="-USDT LP: N/A USDT", fg='black')
    else:
        lbl_token_amount.config(text="Token Price: N/A")
        lbl_token_balance.config(text="Wallet balance: N/A")
        lbl_token_buytax.config(
            text="Buy tax: ")
        lbl_token_honey.config(
            text="Honey Pot: ", fg='black')
        lbl_token_selltax.config(
            text="Sell tax: ", fg='black')
        lb_BNB_LP.config(text="-BNB LP: N/A BNB", fg='black')
        lb_BUSD_LP.config(
            text="-BUSD LP: N/A BUSD", fg='black')
        lb_USDT_LP.config(
            text="-USDT LP: N/A USDT", fg='black')
    print(f"Check done in {time.perf_counter() - start:0.4f} seconds")

def updateLP():
    BNB_price = TokenPrice(WBNB_add)
    entry_TokenCA_input = entry_TokenCA.get()
    if len(entry_TokenCA_input) != 0:
        Token_add = web3.toChecksumAddress(entry_TokenCA_input)
        Token_CA = web3.eth.contract(Token_add, abi=ERC20abi_BSC)
        try:
            Token_CA.functions.symbol().call()
        except:
            time.sleep(0.1)
        else:
            #Token_LP = check_LP(web3, entry_TokenCA_input, token_ABI)
            Token_LP = check_LP_v2(web3, entry_TokenCA_input)
            if AutoLP_flag.get() == 1:
                max = float(Token_LP[2] * BNB_price)
                if Token_LP[4] > max:
                    max = Token_LP[4]
                    ListB_Pair_list.set('')
                    ListB_Pair_list.insert(END, "BUSD")
                    # ListB_Pair_list.config(state="readonly")
                if Token_LP[6] > max:
                    max = Token_LP[6]
                    ListB_Pair_list.set('')
                    ListB_Pair_list.insert(END, "USDT")
                    # ListB_Pair_list.config(state="readonly")

            lb_BNB_LP.config(
                text="{}-BNB LP: {:.3f} BNB".format(Token_LP[0], float(Token_LP[2]) / 10 ** float(WBNB_Decimal)))
            lb_BUSD_LP.config(text="{}-BUSD LP: {:.3f} BUSD".format(Token_LP[0], float(Token_LP[4]) / 10 ** float(
                WBNB_Decimal)))
            lb_USDT_LP.config(text="{}-USDT LP: {:.3f} USDT".format(Token_LP[0], float(Token_LP[6]) / 10 ** float(
                WBNB_Decimal)))

created_label = 0
total = 0
current_clipboard = "*Nothing is copied!!*"

def Label_bind(_token_ca):
    entry_TokenCA.delete(0, END)
    entry_TokenCA.insert(0, _token_ca)

def TokensTracking():
    BNB_price_in_USDT = BNB_to_USDT()
    BUSD_price_in_USDT = BUSD_to_USDT()
    global total, created_label, token_symb_n_price_labels, token_amount_labels, token_name_labels, token_USD_BNB_labels

    if file_exists('Tokens_tracking_list.txt'):
        tracking_file = open("Tokens_tracking_list.txt", "r")
        read_lines = tracking_file.readlines()
        if len(read_lines) != 0:
            if created_label == 0:
                y_axis = 45
                token_name_labels = dict()
                token_symb_n_price_labels = dict()
                token_amount_labels = dict()
                token_USD_BNB_labels = dict()
                for lb in range(0, len(read_lines)):
                    token_symb_n_price_labels[lb] = Label(top, text="",fg="blue")
                    token_symb_n_price_labels[lb].place(x=595, y=y_axis)
                    token_name_labels[lb] = Label(top, text="")
                    token_name_labels[lb].place(x=595, y=y_axis + 15)
                    token_amount_labels[lb] = Label(top, text="")
                    token_amount_labels[lb].place(x=720, y=y_axis)
                    token_USD_BNB_labels[lb] = Label(top, text="")
                    token_USD_BNB_labels[lb].place(x=720, y=y_axis + 15)
                    y_axis = y_axis + 33
                total = len(read_lines)
                created_label = 1
            else:
                if len(read_lines) != total:
                    y_axis = 45
                    if len(read_lines) < total:
                        total_tmp = total
                        for lb_cnt in range(0,total):
                            time.sleep(0.2)
                            token_symb_n_price_labels[lb_cnt].destroy()
                            token_name_labels[lb_cnt].destroy()
                            token_amount_labels[lb_cnt].destroy()
                            token_USD_BNB_labels[lb_cnt].destroy()
                        total = len(read_lines)
                    token_name_labels = dict()
                    token_symb_n_price_labels = dict()
                    token_amount_labels = dict()
                    token_USD_BNB_labels = dict()
                    for lb in range(0, len(read_lines)):
                        token_symb_n_price_labels[lb] = Label(top, text="",fg="blue")
                        token_symb_n_price_labels[lb].place(x=595, y=y_axis)
                        token_name_labels[lb] = Label(top, text="")
                        token_name_labels[lb].place(x=595, y=y_axis + 15)
                        token_amount_labels[lb] = Label(top, text="")
                        token_amount_labels[lb].place(x=720, y=y_axis)
                        token_USD_BNB_labels[lb] = Label(top, text="")
                        token_USD_BNB_labels[lb].place(x=720, y=y_axis + 15)
                        y_axis = y_axis + 33
                    total = len(read_lines)
            count = 0
            for token in read_lines:
                if token.strip() != "":
                    token_CA = web3.toChecksumAddress(token.strip())
                    PCScontract = web3.eth.contract(address=Web3.toChecksumAddress(PCS_ROUTER_CA), abi=PCS_ABI)
                    token_contract = web3.eth.contract(address=token_CA,
                                                       abi=ERC20abi_BSC)
                    try :
                        token_decimal = token_contract.functions.decimals().call()
                    except:
                        tracking_file.close()
                        file1 = open("Tokens_tracking_list.txt", "r")
                        rl = file1.readlines()
                        re_write_lst = []
                        for line1 in rl:
                            line1 = line1.replace("\n", "")
                            if token.lower() not in line1.lower():
                                re_write_lst.append(line1)
                        file1.close()
                        file2 = open("Tokens_tracking_list.txt", "w+")
                        for line in re_write_lst:
                            file2.write("{}\n".format(line))
                        size = file2.tell()
                        file2.truncate(size - 2)
                        file2.close()
                    else:
                        balance = token_contract.functions.balanceOf(sender_wallet).call()
                        token_symbol = token_contract.functions.symbol().call()
                        #time.sleep(0.1)
                        token_name = token_contract.functions.name().call()
                        # New token price + LP #
                        #time.sleep(0.1)
                        Token_LP = check_LP(web3, token_CA, token_ABI)

                        # Find biggest LP ##
                        max = float(Token_LP[0]) * float(BNB_price_in_USDT)
                        biggest = "BNB"
                        if float(Token_LP[1]) > max:
                            max = float(Token_LP[1])
                            biggest = "BUSD"
                        if float(Token_LP[2]) > max:
                            biggest = "USDT"
                        # Token price calculation #
                        TokenPrice = 0.00
                        if biggest == "BNB":
                            amountOutBNB = int(PCScontract.functions.getAmountsOut(1 * 10 ** token_decimal, [
                                token_CA,
                                web3.toChecksumAddress(WBNB_add)]).call()[-1]) / 10 ** 18
                            TokenPrice = amountOutBNB * BNB_price_in_USDT
                        if biggest == "BUSD":
                            amountOutBUSD = int(PCScontract.functions.getAmountsOut(1 * 10 ** token_decimal, [
                                token_CA,
                                web3.toChecksumAddress(BUSD_add)]).call()[-1]) / 10 ** 18
                            TokenPrice = amountOutBUSD * BUSD_price_in_USDT
                        if biggest == "USDT":
                            amountOutUSDT = int(PCScontract.functions.getAmountsOut(1 * 10 ** token_decimal, [
                                token_CA,
                                web3.toChecksumAddress(USDT_add)]).call()[-1]) / 10 ** 18
                            TokenPrice = amountOutUSDT

                        # Print out price and wallet balance info##
                        if TokenPrice < 0.001:
                            token_symb_n_price_labels[count].config(text="{} ({:.1e} u)".format(token_symbol, TokenPrice))
                        else:
                            token_symb_n_price_labels[count].config(text="{} ({:.1f} u)".format(token_symbol, TokenPrice))
                        token_name_labels[count].config(text="{}".format(token_name))
                        if balance / 10 ** token_decimal > 100000:
                            token_amount_labels[count].config(text="{:.1e} tokens".format(balance / 10 ** token_decimal))
                        else:
                            token_amount_labels[count].config(text="{:.1f} tokens".format(balance / 10 ** token_decimal))
                        token_USD_BNB_labels[count].config(
                            text="{:.1f} USD ({:.3f} BNB)".format(TokenPrice * balance / 10 ** token_decimal,
                                                                  TokenPrice * balance / 10 ** token_decimal / BNB_price_in_USDT))
                        token_symb_n_price_labels[count].bind("<Button-1>",lambda event, token_CA = token_CA : Label_bind(token_CA))
                        count += 1
                else:
                    tracking_file.close()
                    file1 = open("Tokens_tracking_list.txt", "r")
                    rl = file1.readlines()
                    re_write_lst = []
                    for line1 in rl:
                        line1 = line1.replace("\n", "")
                        if line1 == "" :
                            line1 = line1.replace(token, '')
                        else:
                            re_write_lst.append(line1)
                    file1.close()
                    #print(re_write_lst)
                    file2 = open("Tokens_tracking_list.txt", "w+")
                    for line in re_write_lst:
                        file2.write("{}\n".format(line))
                    size = file2.tell()
                    file2.truncate(size - 2)
                    file2.close()
        else:
            for lb_cnt in range(0, total):
                time.sleep(0.2)
                token_symb_n_price_labels[lb_cnt].destroy()
                token_name_labels[lb_cnt].destroy()
                token_amount_labels[lb_cnt].destroy()
                token_USD_BNB_labels[lb_cnt].destroy()
                total = len(read_lines)
        tracking_file.close()
    else:
        Token_tracking_file = open('Tokens_tracking_list.txt', "w+")
        Token_tracking_file.close()

def thread_TokenPriceandWalletAmount():
    startup_progressbar()
    while 1:
        # print("Start thread: {} \n".format(datetime.now().strftime("%H:%M:%S")))
        try:
            time.sleep(0.1)
            updateTokenPriceandWalletAmount()
        except:
            time.sleep(0.5)
        else:
            time.sleep(0.1)

#Update stabecoin prices
def thread_StablePricesandWalletUpdate():
    global BNBPrice_updated,BUSDPrice_updated,USDTPrice_updated
    while 1:
        try:
            time.sleep(0.1)
            Prices = updateStablePrice()
        except:
            time.sleep(1)
        else:
            BNBPrice_updated = Prices[0]
            lbl_BNB_Price.config(text = "BNB Price: {:.3f}".format(BNBPrice_updated))
            BUSDPrice_updated = Prices[1]
            USDTPrice_updated = Prices[2]
            time.sleep(5)

def thread_clipboard():
    global current_clipboard
    while 1:
        ## Get clipboard
        try:
            time.sleep(0.1)
            updateWallet()
        except:
            time.sleep(0.1)
        else:
            time.sleep(0.1)
        try:
            time.sleep(0.1)
            get_clip = top.clipboard_get()
        except:
            ClipboardBox.delete(1.0, END)
            ClipboardBox.insert('end', "Clippboard Error")
        else:
            if get_clip != current_clipboard:
                ClipboardBox.delete(1.0, END)
                ClipboardBox.insert('end', "{}".format(top.clipboard_get()))
                current_clipboard = get_clip
                if AutoPaste_flag.get() == 1:
                    if "0x" in current_clipboard:
                        CA = str(current_clipboard[current_clipboard.find("0x"):int(current_clipboard.find("0x") + 42)])
                        try:
                            sellTokenContract = web3.eth.contract(address=web3.toChecksumAddress(CA),
                                                                  abi=ERC20abi_BSC)
                        except:
                            time.sleep(0.1)
                        else:
                            try:
                                token_symbol = sellTokenContract.functions.symbol().call()
                            except:
                                time.sleep(0.1)
                            else:
                                entry_TokenCA.delete(0, END)
                                entry_TokenCA.insert(0, CA)

def thread_tokentracking():
    time.sleep(3)
    while 1:
        try:
            time.sleep(0.1)
            TokensTracking()
        except:
            time.sleep(0.5)
        else:
            time.sleep(0.05)

def startup_progressbar():
    popup = tkinter.Toplevel()
    popup.config(width=500,height=500)
    tkinter.Label(popup,text="Loading Quick Ape Tool...").grid(row=0,column=0)
    progress = 0
    progress_var = tkinter.DoubleVar()
    progress_bar = ttk.Progressbar(popup, variable=progress_var, maximum=124)
    progress_bar.grid(row=1, column=0)  # .pack(fill=tk.X, expand=1, side=tk.BOTTOM)
    top_x = top.winfo_x() + 300
    top_y = top.winfo_y() + 100
    popup.pack_slaves()
    popup.geometry(f'+{top_x}+{top_y}')
    count = 7
    for num in range(0,count):
        popup.update()
        time.sleep(1)  # launch task
        progress += 20
        progress_var.set(progress)
    popup.destroy()
    return 0

def checkThread():
    time.sleep(5)
    global t1,t3,t4,web3
    while 1:
        #print(t1.is_alive(), t2.is_alive(), t3.is_alive(), t4.is_alive(), web3.isConnected())
        if t1.is_alive() == False:
            t1.join()
            t1 = None
            t1 = threading.Thread(target=thread_TokenPriceandWalletAmount, daemon=True)
            t1.start()
        #if t2.is_alive() == False:
        #    t2.join()
        #    t2 = None
        #    t2 = threading.Thread(target=thread_StablePricesandWalletUpdate, daemon=True)
        #    t2.start()
        if t3.is_alive() == False:
            t3.join()
            t3 = None
            t3 = threading.Thread(target=thread_clipboard, daemon=True)
            t3.start()
        if t4.is_alive() == False:
            t4.join()
            t4 = None
            t4 = threading.Thread(target=thread_tokentracking, daemon=True)
            t4.start()
        if web3.isConnected() == False:
            web3 = Web3(Web3.HTTPProvider(user_RPC, request_kwargs={'timeout': 60}))
        time.sleep(5)

t1 = threading.Thread(target=thread_TokenPriceandWalletAmount, daemon=True)
t2 = threading.Thread(target=thread_StablePricesandWalletUpdate, daemon=True)
t3 = threading.Thread(target=thread_clipboard, daemon=True)
t4 = threading.Thread(target=thread_tokentracking, daemon=True)
t5 = threading.Thread(target=checkThread, daemon=True)
TokenCA_var.trace_add('write', updateTokenInfo)
send_TokenCA_var.trace_add('write',updateSendTokenInfo)

t1.start()
#t2.start()
t3.start()
t4.start()
t5.start()

top.protocol("WM_DELETE_WINDOW", on_closing)
top.mainloop()
