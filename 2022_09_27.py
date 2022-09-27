from telethon import TelegramClient, events, sync, Button
from web3 import Web3
import json
import requests
import threading
import asyncio

from datetime import datetime
import time

#### User Settings ####
with open("./userconfig.json") as f:
    keys = json.load(f)
user_wallet_address = keys["wallet_address"]
user_private_key = keys["private_key"]
init_BNB = keys["BNB_Amount"]
init_Gaswei = keys["Gaswei"]
init_Gaslimit = keys["Gaslimit"]
init_Slip = keys["Slip"]
init_NumTx = keys["NumTx"]
init_sell_percent = keys["Sell_percent"]
user_RPC = keys["RPC_Node"]
user_WSS = keys["WSS"]

API_ID = keys["API_ID"]
API_HASH = keys["API_HASH"]
BOT_TOKEN = keys["BOT_TOKEN"]
#############################################################

with open("./track_list.json") as f:
    track_list_dict = json.load(f)


############ Tool  Setting ##################
BNBAmount = init_BNB
Gaswei = init_Gaswei
GasLimit = init_Gaslimit
Slip = init_Slip
numTx = init_NumTx
sell_percent = init_sell_percent
#############################################
latest_ca = ""
list_track = list()

#############################################
PCS_ABI = '[{"inputs":[{"internalType":"address","name":"_factory","type":"address"},{"internalType":"address","name":"_WETH","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[],"name":"WETH","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"},{"internalType":"uint256","name":"amountADesired","type":"uint256"},{"internalType":"uint256","name":"amountBDesired","type":"uint256"},{"internalType":"uint256","name":"amountAMin","type":"uint256"},{"internalType":"uint256","name":"amountBMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"addLiquidity","outputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256","name":"amountB","type":"uint256"},{"internalType":"uint256","name":"liquidity","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"amountTokenDesired","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"addLiquidityETH","outputs":[{"internalType":"uint256","name":"amountToken","type":"uint256"},{"internalType":"uint256","name":"amountETH","type":"uint256"},{"internalType":"uint256","name":"liquidity","type":"uint256"}],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"factory","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"uint256","name":"reserveIn","type":"uint256"},{"internalType":"uint256","name":"reserveOut","type":"uint256"}],"name":"getAmountIn","outputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"reserveIn","type":"uint256"},{"internalType":"uint256","name":"reserveOut","type":"uint256"}],"name":"getAmountOut","outputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"}],"name":"getAmountsIn","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"}],"name":"getAmountsOut","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256","name":"reserveA","type":"uint256"},{"internalType":"uint256","name":"reserveB","type":"uint256"}],"name":"quote","outputs":[{"internalType":"uint256","name":"amountB","type":"uint256"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountAMin","type":"uint256"},{"internalType":"uint256","name":"amountBMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"removeLiquidity","outputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256","name":"amountB","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"removeLiquidityETH","outputs":[{"internalType":"uint256","name":"amountToken","type":"uint256"},{"internalType":"uint256","name":"amountETH","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"removeLiquidityETHSupportingFeeOnTransferTokens","outputs":[{"internalType":"uint256","name":"amountETH","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"bool","name":"approveMax","type":"bool"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"removeLiquidityETHWithPermit","outputs":[{"internalType":"uint256","name":"amountToken","type":"uint256"},{"internalType":"uint256","name":"amountETH","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"bool","name":"approveMax","type":"bool"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"removeLiquidityETHWithPermitSupportingFeeOnTransferTokens","outputs":[{"internalType":"uint256","name":"amountETH","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountAMin","type":"uint256"},{"internalType":"uint256","name":"amountBMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"bool","name":"approveMax","type":"bool"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"removeLiquidityWithPermit","outputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256","name":"amountB","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapETHForExactTokens","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactETHForTokens","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactETHForTokensSupportingFeeOnTransferTokens","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForETH","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForETHSupportingFeeOnTransferTokens","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForTokens","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForTokensSupportingFeeOnTransferTokens","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"uint256","name":"amountInMax","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapTokensForExactETH","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"uint256","name":"amountInMax","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapTokensForExactTokens","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"stateMutability":"payable","type":"receive"}]'
PCS_ROUTER_CA = '0x10ED43C718714eb63d5aA57B78B54704E256024E'

WBNB_add = "0xbb4cdb9cbd36b01bd1cbaebf2de08d9173bc095c"
WBNB_Decimal = 18
BUSD_add = "0xe9e7cea3dedca5984780bafc599bd69add087d56"
BUSD_Abi = '[{"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"spender","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"constant":true,"inputs":[],"name":"_decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"_name","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"_symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"burn","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"subtractedValue","type":"uint256"}],"name":"decreaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"getOwner","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"addedValue","type":"uint256"}],"name":"increaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"mint","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[],"name":"renounceOwnership","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"sender","type":"address"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"}]'
BUSD_Decimal = 18
USDT_add = "0x55d398326f99059ff775485246999027b3197955"
USDT_Abi = '[{"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"spender","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"constant":true,"inputs":[],"name":"_decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"_name","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"_symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"burn","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"subtractedValue","type":"uint256"}],"name":"decreaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"getOwner","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"addedValue","type":"uint256"}],"name":"increaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"mint","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[],"name":"renounceOwnership","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"sender","type":"address"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"}]'
USDT_Decimal = 18

## Token common ABI ##
token_ABI = '[{"inputs":[{"internalType":"string","name":"_NAME","type":"string"},{"internalType":"string","name":"_SYMBOL","type":"string"},{"internalType":"uint256","name":"_DECIMALS","type":"uint256"},{"internalType":"uint256","name":"_supply","type":"uint256"},{"internalType":"uint256","name":"_txFee","type":"uint256"},{"internalType":"uint256","name":"_lpFee","type":"uint256"},{"internalType":"uint256","name":"_MAXAMOUNT","type":"uint256"},{"internalType":"uint256","name":"SELLMAXAMOUNT","type":"uint256"},{"internalType":"address","name":"routerAddress","type":"address"},{"internalType":"address","name":"tokenOwner","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"spender","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"minTokensBeforeSwap","type":"uint256"}],"name":"MinTokensBeforeSwapUpdated","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"tokensSwapped","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"ethReceived","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"tokensIntoLiqudity","type":"uint256"}],"name":"SwapAndLiquify","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"bool","name":"enabled","type":"bool"}],"name":"SwapAndLiquifyEnabledUpdated","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"inputs":[],"name":"_liquidityFee","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"_maxTxAmount","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"_owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"_taxFee","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"claimTokens","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"subtractedValue","type":"uint256"}],"name":"decreaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"tAmount","type":"uint256"}],"name":"deliver","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"excludeFromFee","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"excludeFromReward","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"geUnlockTime","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"includeInFee","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"includeInReward","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"addedValue","type":"uint256"}],"name":"increaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"isExcludedFromFee","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"isExcludedFromReward","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"time","type":"uint256"}],"name":"lock","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"numTokensSellToAddToLiquidity","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"tAmount","type":"uint256"},{"internalType":"bool","name":"deductTransferFee","type":"bool"}],"name":"reflectionFromToken","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"liquidityFee","type":"uint256"}],"name":"setLiquidityFeePercent","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"maxTxPercent","type":"uint256"}],"name":"setMaxTxPercent","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"swapNumber","type":"uint256"}],"name":"setNumTokensSellToAddToLiquidity","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bool","name":"_enabled","type":"bool"}],"name":"setSwapAndLiquifyEnabled","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"taxFee","type":"uint256"}],"name":"setTaxFeePercent","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"swapAndLiquifyEnabled","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"rAmount","type":"uint256"}],"name":"tokenFromReflection","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalFees","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"sender","type":"address"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"uniswapV2Pair","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"uniswapV2Router","outputs":[{"internalType":"contract IUniswapV2Router02","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"unlock","outputs":[],"stateMutability":"nonpayable","type":"function"},{"stateMutability":"payable","type":"receive"}]'
ERC20abi_BSC = '[{"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"spender","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"constant":true,"inputs":[],"name":"_decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"_name","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"_symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"burn","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"subtractedValue","type":"uint256"}],"name":"decreaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"getOwner","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"addedValue","type":"uint256"}],"name":"increaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"mint","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[],"name":"renounceOwnership","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"sender","type":"address"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"}]'

## Checker ##
CHECKER_CA = "0x18be7f977Ec1217B71D0C134FBCFF36Ea4366fCD"
CHECKER_ABI = '[{"inputs":[{"internalType": "address","name": "_factory","type": "address"},{"internalType": "address","name": "_WETH","type": "address"},{"internalType": "address","name": "_UTILS","type": "address"},{"internalType": "address","name": "_TIGS","type": "address"}],"stateMutability": "nonpayable","type": "constructor"},{"inputs": [],"name": "DEV","outputs": [{"internalType": "address","name": "","type": "address"}],"stateMutability": "view","type": "function"},{"inputs": [],"name": "FEE","outputs": [{"internalType": "uint256","name": "","type": "uint256"}],"stateMutability": "view","type": "function"},{"inputs": [],"name": "FEEQuote","outputs": [{"internalType": "uint256","name": "","type": "uint256"}],"stateMutability": "view","type": "function"},{"inputs": [],"name": "LimitSwap","outputs": [{"internalType": "address","name": "","type": "address"}],"stateMutability": "view","type": "function"},{"inputs": [],"name": "STATUS","outputs": [{"internalType": "bool","name": "","type": "bool"}],"stateMutability": "view","type": "function"},{"inputs": [],"name": "TIGS","outputs": [{"internalType": "address","name": "","type": "address"}],"stateMutability": "view","type": "function"},{"inputs": [],"name": "TIGSStaking","outputs": [{"internalType": "address","name": "","type": "address"}],"stateMutability": "view","type": "function"},{"inputs": [],"name": "UTILS","outputs": [{"internalType": "contract TIGSSwapUtils","name": "","type": "address"}],"stateMutability": "view","type": "function"},{"inputs": [],"name": "WETH","outputs": [{"internalType": "address","name": "","type": "address"}],"stateMutability": "view","type": "function"},{"inputs": [{"internalType": "address","name": "_token","type": "address"},{"internalType": "address","name": "_spender","type": "address"}],"name": "approveToken","outputs": [],"stateMutability": "nonpayable","type": "function"},{"inputs": [],"name": "factory","outputs": [{"internalType": "address","name": "","type": "address"}],"stateMutability": "view","type": "function"},{"inputs": [{"internalType": "address","name": "Token","type": "address"}],"name": "fetchBestBaseToken","outputs": [{"internalType": "address","name": "","type": "address"}],"stateMutability": "view","type": "function"},{"inputs": [{"internalType": "address","name": "Token","type": "address"}],"name": "fetchLiquidityETH","outputs": [{"internalType": "uint256","name": "","type": "uint256"}],"stateMutability": "view","type": "function"},{"inputs": [{"internalType": "address","name": "owner","type": "address"},{"internalType": "address","name": "Token","type": "address"},{"internalType": "uint256","name": "Slippage","type": "uint256"}],"name": "fromETHtoToken","outputs": [],"stateMutability": "payable","type": "function"},{"inputs": [{"internalType": "address","name": "owner","type": "address"},{"internalType": "address","name": "Token","type": "address"},{"internalType": "uint256","name": "amount","type": "uint256"},{"internalType": "uint256","name": "Slippage","type": "uint256"}],"name": "fromTokentoETH","outputs": [],"stateMutability": "nonpayable","type": "function"},{"inputs": [{"internalType": "address","name": "owner","type": "address"},{"internalType": "address","name": "TokenA","type": "address"},{"internalType": "address","name": "TokenB","type": "address"},{"internalType": "uint256","name": "amount","type": "uint256"},{"internalType": "uint256","name": "Slippage","type": "uint256"}],"name": "fromTokentoToken","outputs": [],"stateMutability": "nonpayable","type": "function"},{"inputs": [{"internalType": "uint256","name": "amountOut","type": "uint256"},{"internalType": "uint256","name": "reserveIn","type": "uint256"},{"internalType": "uint256","name": "reserveOut","type": "uint256"}],"name": "getAmountIn","outputs": [{"internalType": "uint256","name": "amountIn","type": "uint256"}],"stateMutability": "pure","type": "function"},{"inputs": [{"internalType": "uint256","name": "amountIn","type": "uint256"},{"internalType": "uint256","name": "reserveIn","type": "uint256"},{"internalType": "uint256","name": "reserveOut","type": "uint256"}],"name": "getAmountOut","outputs": [{"internalType": "uint256","name": "amountOut","type": "uint256"}],"stateMutability": "pure","type": "function"},{"inputs": [{"internalType": "uint256","name": "amountOut","type": "uint256"},{"internalType": "address[]","name": "path","type": "address[]"}],"name": "getAmountsIn","outputs": [{"internalType": "uint256[]","name": "amounts","type": "uint256[]"}],"stateMutability": "view","type": "function"},{"inputs": [{"internalType": "uint256","name": "amountIn","type": "uint256"},{"internalType": "address[]","name": "path","type": "address[]"}],"name": "getAmountsOut","outputs": [{"internalType": "uint256[]","name": "amounts","type": "uint256[]"}],"stateMutability": "view","type": "function"},{"inputs": [{"internalType": "address","name": "Token","type": "address"},{"internalType": "uint256","name": "amount","type": "uint256"}],"name": "getOutputfromETHtoToken","outputs": [{"internalType": "uint256","name": "","type": "uint256"},{"internalType": "address[]","name": "","type": "address[]"}],"stateMutability": "view","type": "function"},{"inputs": [{"internalType": "address","name": "Token","type": "address"},{"internalType": "uint256","name": "amount","type": "uint256"}],"name": "getOutputfromTokentoETH","outputs": [{"internalType": "uint256","name": "","type": "uint256"},{"internalType": "address[]","name": "","type": "address[]"}],"stateMutability": "view","type": "function"},{"inputs": [{"internalType": "address","name": "TokenA","type": "address"},{"internalType": "address","name": "TokenB","type": "address"},{"internalType": "uint256","name": "amount","type": "uint256"}],"name": "getOutputfromTokentoToken","outputs": [{"internalType": "uint256","name": "","type": "uint256"},{"internalType": "address[]","name": "","type": "address[]"}],"stateMutability": "view","type": "function"},{"inputs": [{"internalType": "address","name": "Token","type": "address"}],"name": "getTokenInformations","outputs": [{"internalType": "uint256","name": "BuyEstimateOutput","type": "uint256"},{"internalType": "uint256","name": "BuyRealOutput","type": "uint256"},{"internalType": "uint256","name": "SellEstimateOutput","type": "uint256"},{"internalType": "uint256","name": "SellRealOutput","type": "uint256"},{"internalType": "bool","name": "Buy","type": "bool"},{"internalType": "bool","name": "Approve","type": "bool"},{"internalType": "bool","name": "Sell","type": "bool"}],"stateMutability": "nonpayable","type": "function"},{"inputs": [],"name": "makeBuyback","outputs": [],"stateMutability": "nonpayable","type": "function"},{"inputs": [],"name": "minWETH","outputs": [{"internalType": "uint256","name": "","type": "uint256"}],"stateMutability": "view","type": "function"},{"inputs": [{"internalType": "address","name": "input","type": "address"},{"internalType": "address","name": "output","type": "address"}],"name": "pairFor","outputs": [{"internalType": "address","name": "","type": "address"}],"stateMutability": "view","type": "function"},{"inputs": [{"internalType": "address","name": "_factory","type": "address"},{"internalType": "address","name": "path1","type": "address"},{"internalType": "address","name": "path2","type": "address"}],"name": "pairForTest","outputs": [{"internalType": "address","name": "","type": "address"}],"stateMutability": "pure","type": "function"},{"inputs": [{"internalType": "uint256","name": "amountA","type": "uint256"},{"internalType": "uint256","name": "reserveA","type": "uint256"},{"internalType": "uint256","name": "reserveB","type": "uint256"}],"name": "quote","outputs": [{"internalType": "uint256","name": "amountB","type": "uint256"}],"stateMutability": "pure","type": "function"},{"inputs": [{"internalType": "uint256","name": "_FEE","type": "uint256"},{"internalType": "uint256","name": "_FEEQuote","type": "uint256"},{"internalType": "uint256","name": "_minWETH","type": "uint256"}],"name": "setFeeOptions","outputs": [],"stateMutability": "nonpayable","type": "function"},{"inputs": [{"internalType": "address","name": "_LimitSwap","type": "address"}],"name": "setLimitSwapContract","outputs": [],"stateMutability": "nonpayable","type": "function"},{"inputs": [{"internalType": "address","name": "_UTILS","type": "address"}],"name": "setNewUtils","outputs": [],"stateMutability": "nonpayable","type": "function"},{"inputs": [{"internalType": "bool","name": "_new","type": "bool"}],"name": "setStatus","outputs": [],"stateMutability": "nonpayable","type": "function"},{"inputs": [{"internalType": "uint256","name": "amountIn","type": "uint256"},{"internalType": "uint256","name": "amountOutMin","type": "uint256"},{"internalType": "address[]","name": "path","type": "address[]"},{"internalType": "address","name": "to","type": "address"},{"internalType": "uint256","name": "deadline","type": "uint256"}],"name": "swapExactTokensForTokensAdmin","outputs": [],"stateMutability": "nonpayable","type": "function"},{"stateMutability": "payable","type": "receive"}]'


my_channel_entity  = 1637929257
my_group_entity = 1001708791345
client = TelegramClient('anon_bot_QAT__update_WSS', API_ID, API_HASH).start(bot_token = BOT_TOKEN)
#web3 = Web3(Web3.HTTPProvider(user_RPC, request_kwargs={'timeout': 60}))
web3 = Web3(Web3.WebsocketProvider(user_WSS))
#print("Connect Status: ", Web3.isConnected(web3))
print(web3.eth.blockNumber)
sender_wallet = user_wallet_address
sender_pkey = user_private_key
pcs_contract = web3.eth.contract(address=web3.toChecksumAddress(PCS_ROUTER_CA), abi=PCS_ABI)
checker = web3.eth.contract(address=web3.toChecksumAddress(CHECKER_CA), abi=CHECKER_ABI)

async def BNB_to_USDT() :
    amountOut = int(pcs_contract.functions.getAmountsOut(1 * 10 ** WBNB_Decimal, [
        web3.toChecksumAddress(WBNB_add),
        web3.toChecksumAddress(USDT_add)]).call()[-1]) / 10 ** 18
    return amountOut

async def updateTracklist(track_list_dict) :
    tmp = json.dumps(track_list_dict, indent=6)
    f = open('track_list.json', 'w')
    print(tmp, file=f)
    f.close()
    #with open('track_list.json', 'w') as convert_file:
    #    convert_file.write(json.dumps(track_list_dict))

async def TokenBuy_BNB(_tokenCA, _BNB_Amount, _GasWei, _GasLimit,_Slip,_numTx):
    spend = web3.toChecksumAddress("0xbb4cdb9cbd36b01bd1cbaebf2de08d9173bc095c")  # WBNB Address
    tokenToBuy = web3.toChecksumAddress(_tokenCA)
    amountOut = pcs_contract.functions.getAmountsOut(web3.toWei(_BNB_Amount, 'ether'), [spend, tokenToBuy]).call()[-1]
    amountMin = amountOut / (1 + _Slip / 100)

    count = 0
    nonce = web3.eth.get_transaction_count(sender_wallet)
    while count < _numTx:
        pancakeswap2_txn = pcs_contract.functions.swapExactETHForTokensSupportingFeeOnTransferTokens(
            int(amountMin),
            # set to 0 means dont care slippage, or specify minimum amount of token you want to receive - consider Decimal!
            [spend, tokenToBuy],
            sender_wallet,
            (int(time.time()) + 120)
        ).buildTransaction({
            'from': sender_wallet,
            'value': web3.toWei(_BNB_Amount, 'ether'),  ## BNB Amount want to Swap from
            'gas': _GasLimit,
            'gasPrice': web3.toWei(_GasWei, 'gwei'),
            'nonce': nonce,
        })
        signed_txn = web3.eth.account.sign_transaction(pancakeswap2_txn, private_key=sender_pkey)
        tx_token = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        await sendMessage("TX Hash {}: https://bscscan.com/tx/{} \n".format(count + 1, web3.toHex(tx_token)))
        count += 1
        nonce += 1

    #await sendMessage("Latest Ethereum block number: {} \n".format(web3.eth.blockNumber))
    #await sendMessage("Waiting for transaction to be done: {} \n".format(datetime.now().strftime("%H:%M:%S")))
    web3.eth.wait_for_transaction_receipt(Web3.toHex(tx_token))
    #await sendMessage("Transaction Done: {} \n".format(datetime.now().strftime("%H:%M:%S")))

    if web3.eth.get_transaction_receipt(tx_token).status == 1:
        await sendMessage("Transaction status: SUCCESS !!! \n")
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
            await sendMessage("Transaction status: FAILED !!! \n")
            await sendMessage("Fail reason: {} !!! \n".format(e))
            if "INSUFFICIENT_OUTPUT_AMOUNT" in str(e):
                await sendMessage("Maybe slippage is to small, please increase your Slippage setting !!! \n")

async def TokenBuy_BNB_handler(_tokenCA, _BNB_Amount, _GasWei, _GasLimit,_Slip,_numTx):
    spend = web3.toChecksumAddress("0xbb4cdb9cbd36b01bd1cbaebf2de08d9173bc095c")  # WBNB Address
    tokenToBuy = web3.toChecksumAddress(_tokenCA)
    amountOut = pcs_contract.functions.getAmountsOut(web3.toWei(_BNB_Amount, 'ether'), [spend, tokenToBuy]).call()[-1]
    amountMin = amountOut / (1 + _Slip / 100)

    count = 0
    nonce = web3.eth.get_transaction_count(sender_wallet)
    while count < _numTx:
        pancakeswap2_txn = pcs_contract.functions.swapExactETHForTokensSupportingFeeOnTransferTokens(
            int(amountMin),
            # set to 0 means dont care slippage, or specify minimum amount of token you want to receive - consider Decimal!
            [spend, tokenToBuy],
            sender_wallet,
            (int(time.time()) + 120)
        ).buildTransaction({
            'from': sender_wallet,
            'value': web3.toWei(_BNB_Amount, 'ether'),  ## BNB Amount want to Swap from
            'gas': _GasLimit,
            'gasPrice': web3.toWei(_GasWei, 'gwei'),
            'nonce': nonce,
        })
        signed_txn = web3.eth.account.sign_transaction(pancakeswap2_txn, private_key=sender_pkey)
        tx_token = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        await sendMessage("TX Hash {}: https://bscscan.com/tx/{} \n".format(count + 1, web3.toHex(tx_token)))
        count += 1
        nonce += 1

    #await sendMessage("Latest Ethereum block number: {} \n".format(web3.eth.blockNumber))
    #await sendMessage("Waiting for transaction to be done: {} \n".format(datetime.now().strftime("%H:%M:%S")))
    web3.eth.wait_for_transaction_receipt(Web3.toHex(tx_token))
    #await sendMessage("Transaction Done: {} \n".format(datetime.now().strftime("%H:%M:%S")))

    if web3.eth.get_transaction_receipt(tx_token).status == 1:
        await sendMessage("Transaction status: SUCCESS !!! \n")
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
            await sendMessage("Transaction status: FAILED !!! \n")
            await sendMessage("Fail reason: {} !!! \n".format(e))
            if "INSUFFICIENT_OUTPUT_AMOUNT" in str(e):
                await sendMessage("Maybe slippage is to small, please increase your Slippage setting !!! \n")
    return True

async def TokenSell_BNB(_web3, _tokenCA, _Token_Percent, _GasWei, _GasLimit, _Slip):
    contract = pcs_contract
    spend = _web3.toChecksumAddress("0xbb4cdb9cbd36b01bd1cbaebf2de08d9173bc095c")  # WBNB Address

    TokenToSell = _web3.toChecksumAddress(_tokenCA)
    sellTokenContract = web3.eth.contract(TokenToSell, abi=ERC20abi_BSC)
    allowance = sellTokenContract.functions.allowance(user_wallet_address, PCS_ROUTER_CA).call()
    token_symbol = sellTokenContract.functions.symbol().call()
    token_decimal = sellTokenContract.functions.decimals().call()
    balance = sellTokenContract.functions.balanceOf(sender_wallet).call()
    readable = balance / 10 ** token_decimal
    tokenValue = balance * int(_Token_Percent) / 100

    if allowance > tokenValue:
        await sendMessage("Swapping {} {} for BNB\n".format(tokenValue / 10 ** token_decimal, token_symbol))

        amountOut = contract.functions.getAmountsOut(int(tokenValue), [TokenToSell, spend]).call()[-1]
        amountMin = amountOut / (1 + _Slip / 100)

        pancakeswap2_txn = contract.functions.swapExactTokensForETHSupportingFeeOnTransferTokens(
            int(tokenValue),
            int(amountMin),
            [TokenToSell, spend],
            sender_wallet,
            (int(time.time()) + 30)
        ).buildTransaction({
            'from': sender_wallet,
            'gas': _GasLimit,
            'gasPrice': web3.toWei(_GasWei, 'gwei'),
            'nonce': web3.eth.get_transaction_count(sender_wallet),
        })

        signed_txn = _web3.eth.account.sign_transaction(pancakeswap2_txn, private_key=sender_pkey)
        tx_token = _web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        web3.eth.wait_for_transaction_receipt(Web3.toHex(tx_token))
        time.sleep(0.2)
        if web3.eth.get_transaction_receipt(tx_token).status == 1:
            await sendMessage("Transaction status: SUCCESS !!! \nTX Hash: https://bscscan.com/tx/{} \n".format(_web3.toHex(tx_token)))
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
                await sendMessage("Transaction status: FAILED !!! \nTX Hash: https://bscscan.com/tx/{} \nFail reason: {} !!! \n".format(_web3.toHex(tx_token),e))
                if "INSUFFICIENT_OUTPUT_AMOUNT" in str(e):
                    await sendMessage("Maybe slippage is to small, please increase your Slippage setting !!! \n")
    else:
        await sendMessage("Token is not approved, please approve first!")

async def TokenSell_BNB_handler(_web3, _tokenCA, _Token_Percent, _GasWei, _GasLimit, _Slip):
    contract = pcs_contract
    spend = _web3.toChecksumAddress("0xbb4cdb9cbd36b01bd1cbaebf2de08d9173bc095c")  # WBNB Address

    TokenToSell = _web3.toChecksumAddress(_tokenCA)
    sellTokenContract = web3.eth.contract(TokenToSell, abi=ERC20abi_BSC)
    allowance = sellTokenContract.functions.allowance(user_wallet_address, PCS_ROUTER_CA).call()
    token_symbol = sellTokenContract.functions.symbol().call()
    token_decimal = sellTokenContract.functions.decimals().call()
    balance = sellTokenContract.functions.balanceOf(sender_wallet).call()
    readable = balance / 10 ** token_decimal
    tokenValue = balance * int(_Token_Percent) / 100

    if allowance > tokenValue:
        await sendMessage("Swapping {} {} for BNB\n".format(tokenValue / 10 ** token_decimal, token_symbol))

        amountOut = contract.functions.getAmountsOut(int(tokenValue), [TokenToSell, spend]).call()[-1]
        amountMin = amountOut / (1 + _Slip / 100)

        pancakeswap2_txn = contract.functions.swapExactTokensForETHSupportingFeeOnTransferTokens(
            int(tokenValue),
            int(amountMin),
            [TokenToSell, spend],
            sender_wallet,
            (int(time.time()) + 30)
        ).buildTransaction({
            'from': sender_wallet,
            'gas': _GasLimit,
            'gasPrice': web3.toWei(_GasWei, 'gwei'),
            'nonce': web3.eth.get_transaction_count(sender_wallet),
        })

        signed_txn = _web3.eth.account.sign_transaction(pancakeswap2_txn, private_key=sender_pkey)
        tx_token = _web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        web3.eth.wait_for_transaction_receipt(Web3.toHex(tx_token))
        time.sleep(0.2)
        if web3.eth.get_transaction_receipt(tx_token).status == 1:
            await sendMessage("Transaction status: SUCCESS !!! \nTX Hash: https://bscscan.com/tx/{} \n".format(_web3.toHex(tx_token)))
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
                await sendMessage("Transaction status: FAILED !!! \nTX Hash: https://bscscan.com/tx/{} \nFail reason: {} !!! \n".format(_web3.toHex(tx_token),e))
                if "INSUFFICIENT_OUTPUT_AMOUNT" in str(e):
                    await sendMessage("Maybe slippage is to small, please increase your Slippage setting !!! \n")
    else:
        await sendMessage("Token is not approved, please approve first!")

    return True


async def ApproveToken(_web3, _tokenCA, _GasWei, _GasLimit):
    contract = _web3.eth.contract(address=PCS_ROUTER_CA, abi=PCS_ABI)
    TokenCA = _web3.toChecksumAddress(_tokenCA)
    TokenContract = web3.eth.contract(TokenCA, abi=ERC20abi_BSC)
    allowance = TokenContract.functions.allowance(sender_wallet, PCS_ROUTER_CA).call()
    if allowance < 115792089237316195423570985008687907853269984665640564039457584007913129639935:
        approve = TokenContract.functions.approve(PCS_ROUTER_CA,
                                                      115792089237316195423570985008687907853269984665640564039457584007913129639935).buildTransaction(
            {
                'from': sender_wallet,
                'gas': _GasLimit,
                'gasPrice': web3.toWei(_GasWei, 'gwei'),
                'nonce': web3.eth.get_transaction_count(sender_wallet),
            })
        signed_txn = _web3.eth.account.sign_transaction(approve, private_key=sender_pkey)
        tx_token = _web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        _web3.eth.wait_for_transaction_receipt(Web3.toHex(tx_token))
        time.sleep(0.5)
        if web3.eth.get_transaction_receipt(tx_token).status == 1:
            await sendMessage("Transaction status: SUCCESS !!! \nTX Hash: https://bscscan.com/tx/{} \n ".format(web3.toHex(tx_token)))
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
                await sendMessage("Transaction status: FAILED !!! \nTX Hash {}: https://bscscan.com/tx/{} \n ".format(web3.toHex(tx_token)))
                await sendMessage("Fail reason: {} !!! \n".format(e))
                if "INSUFFICIENT_OUTPUT_AMOUNT" in str(e):
                    await sendMessage("Maybe slippage is to small, please increase your Slippage setting !!! \n")
    else:
        await sendMessage("Token already approved!")

async def TokenPrice(tokenAddress):
    apiURL = "https://api.pancakeswap.info/api/v2/tokens/"
    response = requests.get(url = apiURL + tokenAddress)
    jsonRaw_00 = response.json()
    price = jsonRaw_00['data']['price']
    return price

async def walletInfo():
    BNB_price = await BNB_to_USDT()
    balance_converted = web3.fromWei(web3.eth.get_balance(sender_wallet), 'ether')
    BUSD_CA = web3.eth.contract(address=web3.toChecksumAddress(BUSD_add), abi=BUSD_Abi)
    BUSD_balance = BUSD_CA.functions.balanceOf(sender_wallet).call()
    USDT_CA = web3.eth.contract(address=web3.toChecksumAddress(USDT_add), abi=USDT_Abi)
    USDT_balance = USDT_CA.functions.balanceOf(sender_wallet).call()
    await sendMessage("Wallet address:\n- {}\n  --> {:.3f} BNB ({:.3f} USD)\n  --> {} BUSD\n  --> {} USDT\n".format(
                         sender_wallet, float(balance_converted), float(balance_converted) * float(BNB_price),
                         str(round(BUSD_balance / 10 ** BUSD_Decimal, 3)),
                         str(round(USDT_balance / 10 ** USDT_Decimal, 3))))

async def checkToken(_checker_CA, _token_CA):
    tokenInfos = _checker_CA.functions.getTokenInformations(_token_CA).call()
    buy_tax = round((tokenInfos[0] - tokenInfos[1]) / tokenInfos[0] * 100)
    sell_tax = round((tokenInfos[2] - tokenInfos[3]) / tokenInfos[2] * 100)
    if tokenInfos[5] and tokenInfos[6] == True:
        honeypot = False
    else:
        honeypot = True
    return buy_tax, sell_tax, honeypot

async def print_setting():
    await sendMessage("BNB Amount: {}\nGaswei: {} \nGas Limit: {} \nSlippage : {} \nNumber of Tx: {} \nSell Percent: {}%\n".format(BNBAmount,Gaswei,GasLimit,Slip,numTx,sell_percent))

async def sendMessage(message):
    await client.send_message(entity=my_group_entity, message=message, parse_mode = 'html')

async def getTokenInfo(token_ca):
    try:
        TokenContract = web3.eth.contract(address=web3.toChecksumAddress(token_ca),
                                          abi=ERC20abi_BSC)
    except:
        await sendMessage("Not a token contract address")
        return False
    else:
        try:
            token_symbol = TokenContract.functions.symbol().call()
        except:
            await sendMessage("Not a token contract address")
            return False
        else:
            token_decimal = TokenContract.functions.decimals().call()
            total_supply = TokenContract.functions.totalSupply().call()
            balance = TokenContract.functions.balanceOf(sender_wallet).call()
            readable = 0
            readable_in_usd = 0
            readable_in_bnb = 0

            BNB_price = await BNB_to_USDT()
            #Tokenprice = float(await TokenPrice(token_ca))
            Tokenprice_in_BNB = int(pcs_contract.functions.getAmountsOut(1 * 10 ** token_decimal, [
                                                web3.toChecksumAddress(token_ca),
                                                web3.toChecksumAddress(WBNB_add)]).call()[-1]) / 10 ** 18
            Tokenprice = Tokenprice_in_BNB * BNB_price
            if (balance != 0) :
                readable = balance / 10 ** token_decimal
                readable_in_bnb = readable * Tokenprice_in_BNB
                readable_in_usd = readable * Tokenprice
            honeypot_str = ""
            buy_tax_str = ""
            sell_tax_str = 999
            try:
                TokenInfo = await checkToken(checker, web3.toChecksumAddress(token_ca))
            except:
                honeypot_str = "Unknown - Maybe not listed yet!"
            else:
                if TokenInfo[2] == True:
                    honeypot_str = "Rugged!!!"
                else:
                    honeypot_str = "Safe"
                if TokenInfo[1] > 80 or TokenInfo[0] > 80 :
                    honeypot_str = "Safe - But high tax (>80%)"
                sell_tax_str = str(TokenInfo[1])
                buy_tax_str = str(TokenInfo[0])

            if Tokenprice < 0.001:
                poocoin_url = "https://poocoin.app/tokens/{}".format(token_ca)
                message = "CA: {}\nToken: {} \nToken Price: {:.3e} USD \nMarket Cap: {:1f} USD \nHoneyPot: {}\nBuy - Sell tax: {}% - {}% \n ---------------------------- \n<b>Wallet balance:</b> {:.3f} {} ({:.3f} USDT - {:.3f} BNB - {:.3f} BNB with Tax)\n ".format(
                    token_ca,
                    token_symbol,
                    Tokenprice,
                    Tokenprice * total_supply/10**token_decimal,
                    honeypot_str,
                    buy_tax_str,
                    sell_tax_str,
                    readable,
                    token_symbol,
                    readable_in_usd,
                    readable_in_bnb,
                    readable_in_bnb - (readable_in_bnb * float(sell_tax_str) / 100)
                    )

                await client.send_message(entity=my_group_entity, message=message, parse_mode='html',
                                          buttons=[
                                                   [Button.url('Poocoin.app!', poocoin_url)],
                                                   [Button.inline("Buy",b"buy"),Button.inline("Sell",b"sell"),Button.inline("Approve",b"approve")],
                                                   [Button.inline("Add Track",b"add"),Button.inline("Remove Track",b"remove")]
                                                  ])
            else:
                poocoin_url = "https://poocoin.app/tokens/{}".format(token_ca)
                message = "CA: {} \nToken: {} \nToken Price: {:.3f} USD \nMarket Cap: {:1f} USD \nHoneyPot: {}\nBuy - Sell tax: {}% - {}% \n ---------------------------- \n<b>Wallet balance:</b> {:.3f} {} ({:.3f} USDT - {:.3f} BNB - {:.3f} BNB with Tax)\n ".format(
                            token_ca,token_symbol,
                            Tokenprice,
                            Tokenprice * total_supply / 10 ** token_decimal,
                            honeypot_str,
                            buy_tax_str,
                            sell_tax_str,
                            readable,
                            token_symbol,
                            readable_in_usd,
                            readable_in_bnb,
                            readable_in_bnb - (readable_in_bnb * float(sell_tax_str) / 100)
                            )

                await client.send_message(entity=my_group_entity,
                                          message=message,
                                          parse_mode='html',
                                          buttons=[[Button.url('Poocoin.app!', poocoin_url)],
                                                   [Button.inline("Buy",b"buy"),Button.inline("Sell",b"sell"),Button.inline("Approve",b"approve")],
                                                   [Button.inline("Add Track",b"add"),Button.inline("Remove Track",b"remove")]])
            return True

async def checkTokenCA(token_ca):
    try:
        TokenContract = web3.eth.contract(address=web3.toChecksumAddress(token_ca),
                                          abi=ERC20abi_BSC)
    except:
        await sendMessage("Not a token contract address")
        return False,"N/A"
    else:
        try:
            token_symbol = TokenContract.functions.symbol().call()
        except:
            await sendMessage("Not a token contract address")
            return False, "N/A"
        else:
            return True,token_symbol

async def tokenTrackThread(token_ca):
    Initial_Price = 0
    flag = 1
    while flag == 1:
        TokenContract = web3.eth.contract(address=web3.toChecksumAddress(token_ca),
                                          abi=ERC20abi_BSC)
        token_symbol = TokenContract.functions.symbol().call()
        token_decimal = TokenContract.functions.decimals().call()
        BNB_price = await BNB_to_USDT()
        Tokenprice_in_BNB = int(pcs_contract.functions.getAmountsOut(1 * 10 ** token_decimal, [
            web3.toChecksumAddress(token_ca),
            web3.toChecksumAddress(WBNB_add)]).call()[-1]) / 10 ** 18
        Tokenprice = Tokenprice_in_BNB * BNB_price
        if Initial_Price == 0:
            Initial_Price = Tokenprice
            percent = 100
        else :
            percent = Tokenprice*100/Initial_Price
        print("Token: {} \nInitial Price: {} \nPrice: {}".format(token_symbol,Initial_Price,Tokenprice))
        print("Percent = {}".format(percent))
        if percent < 95 or percent > 105 :
            flag = 0
            print("Done")
        time.sleep(0.5)
    return True

def between_callback(args):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    loop.run_until_complete(tokenTrackThread(args))
    loop.close()

### Testing purpose
async def ButtonMessage():
    await client.send_message(entity=my_group_entity,message="Button play test",parse_mode = 'html', buttons=[[Button.inline('Left'), Button.inline('Right')],[Button.url('Check this site!', 'https://example.com')]])

Tracking_threads = []
Tracking_threads_job = dict()
Tracking_threads_count = 0
@client.on(events.NewMessage(chats=[my_group_entity]))
async def my_event_handler(event):
    global BNBAmount,Gaswei,GasLimit,Slip,numTx,sell_percent,latest_ca,list_track
    global track_list_dict

    msg = str(event.raw_text)
    msg_lower = msg.lower()
    list_track_len = len(list_track)
    if (msg.startswith("0x") and len(msg) == 42 ) :
        Info = await getTokenInfo(msg)
        if Info == True and msg != latest_ca:
            latest_ca = msg

    if (msg_lower.split()[0] == "add" and msg.split()[1].startswith("0x")) and len(msg.split()[1]) == 42:
        lenght = len(msg_lower.split())
        for token in msg_lower.split():
            if (token.startswith("0x") and len(token) == 42):
                _checkToken = await checkTokenCA(token)
                if _checkToken[0] == True :
                    if token not in track_list_dict:
                        track_list_dict[token] = dict()
                        track_list_dict[token]["Symbol"] = _checkToken[1]
                        await updateTracklist(track_list_dict)
                    else :
                        await sendMessage("Token {} already in track list!".format(_checkToken[1]))

    if (msg_lower.split()[0] == "remove" and msg.split()[1].startswith("0x")) and len(msg.split()[1]) == 42:
        checkToken = await checkTokenCA(msg_lower.split()[1])
        for token in msg_lower.split():
            if (token.startswith("0x") and len(token) == 42):
                checkToken = await checkTokenCA(token)
                if checkToken[0] == True :
                    if token not in track_list_dict:
                        await sendMessage("Token {} is not in track list!".format(checkToken[1]))
                    else:
                        track_list_dict.pop(token,None)
                        await sendMessage("Removing token {} from track list!".format(checkToken[1]))
                        await updateTracklist(track_list_dict)

    if (msg_lower.split()[0] == "remove" and msg_lower.split()[1] == "all"):
        await sendMessage("Removing all tokens in track list!")
        track_list_dict.clear()

    if (msg_lower.split()[0] == "track" or msg_lower.split()[0] == "t"):
        if len(track_list_dict) == 0 :
            await sendMessage("No token is tracked right now!")
        else:
            out_message = "Tracked tokens: \n"
            for token in track_list_dict:
                token_ca = token
                TokenContract = web3.eth.contract(address=web3.toChecksumAddress(token_ca), abi=ERC20abi_BSC)
                token_decimal = TokenContract.functions.decimals().call()
                balance = TokenContract.functions.balanceOf(sender_wallet).call()
                readable = 0
                readable_in_usd = 0
                readable_in_bnb = 0

                BNB_price = await BNB_to_USDT()
                # Tokenprice = float(await TokenPrice(token_ca))
                Tokenprice_in_BNB = int(pcs_contract.functions.getAmountsOut(1 * 10 ** token_decimal, [
                    web3.toChecksumAddress(token_ca),
                    web3.toChecksumAddress(WBNB_add)]).call()[-1]) / 10 ** 18
                Tokenprice = Tokenprice_in_BNB * BNB_price
                if (balance != 0):
                    readable = balance / 10 ** token_decimal
                    readable_in_bnb = readable * Tokenprice_in_BNB
                    readable_in_usd = readable * Tokenprice

                mess = " - {} : {}\n    + <b>Amount:</b> {:.3f} ({:.1f} USDT - {:.3f} BNB)\n---------------------------\n".format(
                    track_list_dict[token]["Symbol"], token, readable, readable_in_usd, readable_in_bnb)
                out_message += mess

                await sendMessage(out_message)
                print(out_message)


    if ( (msg_lower.split()[0] =="b" or msg_lower.split()[0] == "buy" ) and msg.split()[1].startswith("0x")) and len(msg.split()[1]) == 42 :
        token_flag = await checkTokenCA(msg.split()[1])
        if token_flag[0] == True:
            await sendMessage(
                "Buying Token: {} \n + BNB Amount: {} \n + Gaswei: {} \n + GasLimit: {}\n + Slippage: {} \n + Number of Tx: {}".format(token_flag[1],BNBAmount,Gaswei,GasLimit,Slip,numTx))
            await TokenBuy_BNB(msg.split()[1], BNBAmount, Gaswei, GasLimit,Slip,numTx)

    if ( (msg_lower.split()[0] =="s" or msg_lower.split()[0] == "sell" ) and msg.split()[1].startswith("0x")) and len(msg.split()[1]) == 42 :
        token_flag = await checkTokenCA(msg.split()[1])
        if token_flag[0] == True:
            if (len(msg.split()) > 2):
                if (float(msg.split()[2]) > 0 and float(msg.split()[2]) < 100):
                    sell_percent = float(msg.split()[2])
            await sendMessage(
                "Selling Token: {} \n + Sell Percent: {}% \n + Gaswei: {} \n + GasLimit: {}\n + Slippage: {} \n".format(
                    token_flag[1], sell_percent, Gaswei, GasLimit, Slip))
            await TokenSell_BNB(web3, msg.split()[1], sell_percent, Gaswei, GasLimit, Slip)

    if ( (msg_lower.split()[0] == "a" or msg_lower.split()[0] == "approve" ) and msg.split()[1].startswith("0x")) and len(msg.split()[1]) == 42 :
        token_flag = await checkTokenCA(msg.split()[1])
        if token_flag[0] == True:
            await sendMessage("Approving Token: {} \n".format(token_flag[1]))
            await ApproveToken(web3, msg.split()[1], Gaswei, GasLimit)

    if (msg_lower == ("preset")) : await print_setting()

    if (msg_lower == ("wallet")): await walletInfo()

    if (msg_lower == ("latest") or msg_lower == "/l" or msg_lower == ("ll") ) :
        await sendMessage("Checking latest token ca: {}".format(latest_ca))
        await getTokenInfo(latest_ca)

    if ( msg_lower.split()[0].startswith("set") ):
        if (msg_lower.split()[1] != None and msg_lower.split()[2] != None):
            if (msg_lower.split()[1] == "amount" or msg_lower.split()[1] == "bnbamount" or msg_lower.split()[1] == "bnb" ):
                try :
                    new_amount = float(msg_lower.split()[2])
                except:
                    await sendMessage("BNB Amount should be a float number!")
                else:
                    if new_amount > 0:
                        await sendMessage("Change BNB Amount to swap to: {}".format(new_amount))
                        BNBAmount = new_amount
            if (msg_lower.split()[1] == "gaswei" or msg_lower.split()[1] == "gw" or msg_lower.split()[1] == "wei"):
                try:
                    new_amount = int(msg_lower.split()[2])
                except:
                    await sendMessage("Gaswei Amount should be a integer number!")
                else:
                    if new_amount > 0:
                        await sendMessage("Change Gaswei to: {}".format(new_amount))
                        Gaswei = new_amount
            if (msg_lower.split()[1] == "gaslimit" or msg_lower.split()[1] == "limit" ):
                try:
                    new_amount = int(msg_lower.split()[2])
                except:
                    await sendMessage("Gaslimit Amount should be a integer number!")
                else:
                    if new_amount > 300000:
                        await sendMessage("Change Gaslimit to: {}".format(new_amount))
                        GasLimit = new_amount
                    else:
                        await sendMessage("Gaslimit should atleast bigger than 300000")
            if (msg_lower.split()[1] == "slip" or msg_lower.split()[1] == "slippage" ):
                try:
                    new_amount = float(msg_lower.split()[2])
                except:
                    await sendMessage("Slippage should be a float number!")
                else:
                    if new_amount > 0 and new_amount < 100:
                        await sendMessage("Change Slippage to: {}".format(new_amount))
                        Slip = new_amount
                    else:
                        await sendMessage("Slippage should be between 0% ~ 100%")
            if (msg_lower.split()[1] == "percent" or msg_lower.split()[1] == "sellpercent" ):
                try:
                    new_amount = float(msg_lower.split()[2])
                except:
                    await sendMessage("Sell percent should be a float number (no need to type %)!")
                else:
                    if new_amount > 0 and new_amount < 100:
                        await sendMessage("Sell percent to: {}%".format(new_amount))
                        sell_percent = new_amount
                    else:
                        await sendMessage("Sell percent should be between 0% ~ 100%")

    if (msg_lower.startswith("price bnb")) :
        await BNB_to_USDT()

    if (msg_lower.split()[0] == ("test")):
        keyboard = [
            [
                Button.inline("New Command", "edit_command"),
                Button.inline("Anything", "any"),
            ],
        ]


event_flag = 0
executing = False
@client.on(events.CallbackQuery())
async def call_handler(event):
    global BNBAmount, Gaswei, GasLimit, Slip, numTx, sell_percent, latest_ca, list_track
    global track_list_dict,event_flag, executing
    print(event.id)
    if event_flag == 0:
        if event.data == b"buy":
            event_flag = 1
            get_message = await event.get_message()
            message_text = get_message.text
            loc = message_text.find("0x")
            token_ca = message_text[loc:loc+42]
            token_flag = await checkTokenCA(token_ca)
            await sendMessage(
                "Buying Token: {} \n + BNB Amount: {} \n + Gaswei: {} \n + GasLimit: {}\n + Slippage: {} \n + Number of Tx: {}".format(
                    token_flag[1], BNBAmount, Gaswei, GasLimit, Slip, numTx))
            await TokenBuy_BNB(token_ca, BNBAmount, Gaswei, GasLimit, Slip, numTx)
            time.sleep(0.2)
            event_flag = 0
            return

        if event.data == b"sell":
            event_flag = 1
            get_message = await event.get_message()
            message_text = get_message.text
            loc = message_text.find("0x")
            token_ca = message_text[loc:loc+42]
            token_flag = await checkTokenCA(token_ca)
            await sendMessage(
                "Selling Token: {} \n + Sell Percent: {}% \n + Gaswei: {} \n + GasLimit: {}\n + Slippage: {} \n".format(
                    token_flag[1], sell_percent, Gaswei, GasLimit, Slip))
            await TokenSell_BNB(web3, token_ca, sell_percent, Gaswei, GasLimit, Slip)
            time.sleep(0.2)
            event_flag = 0
            return

        if event.data == b"approve":
            event_flag = 1
            get_message = await event.get_message()
            message_text = get_message.text
            loc = message_text.find("0x")
            token_ca = message_text[loc:loc+42]
            token_flag = await checkTokenCA(token_ca)
            await sendMessage("Approving Token: {} \n".format(token_flag[1]))
            await ApproveToken(web3, token_ca, Gaswei, GasLimit)
            time.sleep(0.2)
            event_flag = 0
            return

        if event.data == b"add":
            event_flag = 1
            get_message = await event.get_message()
            message_text = get_message.text
            loc = message_text.find("0x")
            token_ca = message_text[loc:loc+42]
            token_flag = await checkTokenCA(token_ca)
            if token_flag[0] == True:
                token = token_ca.lower()
                if token not in track_list_dict:
                    track_list_dict[token] = dict()
                    track_list_dict[token]["Symbol"] = token_flag[1]
                    await sendMessage("Added  {} to track list!".format(token_flag[1]))
                    await updateTracklist(track_list_dict)
                else:
                    await sendMessage("Token {} already in track list!".format(token_flag[1]))
                    time.sleep(0.1)
            time.sleep(0.2)
            event_flag = 0
            return

        if event.data == b"remove":
            event_flag = 1
            get_message = await event.get_message()
            message_text = get_message.text
            loc = message_text.find("0x")
            token_ca = message_text[loc:loc+42]
            checkToken = await checkTokenCA(token_ca)
            if checkToken[0] == True:
                if token_ca not in track_list_dict:
                    await sendMessage("Token {} is not in track list!".format(checkToken[1]))
                    time.sleep(0.1)
                else:
                    track_list_dict.pop(token_ca, None)
                    await sendMessage("Removing token {} from track list!".format(checkToken[1]))
                    await updateTracklist(track_list_dict)
            time.sleep(0.2)
            event_flag = 0
            return
        time.sleep(0.2)
    else:
        print(event_flag)
    time.sleep(1)


client.start()
print("Start client!")
ent = client.get_entity(my_group_entity)
print(ent.id)

client.run_until_disconnected()

