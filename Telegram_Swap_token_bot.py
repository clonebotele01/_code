from telethon import TelegramClient, events, sync, Button
from web3 import Web3
import json
import requests
import threading
import asyncio

from datetime import datetime
import time
import api_settings

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

API_ID = keys["API_ID"]
API_HASH = keys["API_HASH"]
BOT_TOKEN = keys["BOT_TOKEN"]
#############################################################

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
PCS_ABI = api_settings.PCS_ABI
PCS_ROUTER_CA = api_settings.PCS_ROUTER_CA

WBNB_add = api_settings.WBNB_add
WBNB_Decimal = 18
BUSD_add = api_settings.BUSD_add
BUSD_Abi = api_settings.BUSD_Abi
BUSD_Decimal = 18
USDT_add = api_settings.USDT_add
USDT_Abi = api_settings.USDT_Abi
USDT_Decimal = 18

## Token common ABI ##
token_ABI = api_settings.token_ABI
ERC20abi_BSC = api_settings.ERC20abi_BSC

## Checker ##
CHECKER_CA = api_settings.CHECKER_CA
CHECKER_ABI = api_settings.CHECKER_ABI

my_channel_entity  = 1637929257
my_group_entity = 1001708791345
client = TelegramClient('anon_bot_QAT', API_ID, API_HASH).start(bot_token = BOT_TOKEN)
web3 = Web3(Web3.HTTPProvider(user_RPC, request_kwargs={'timeout': 60}))
sender_wallet = user_wallet_address
sender_pkey = user_private_key
pcs_contract = web3.eth.contract(address=web3.toChecksumAddress(PCS_ROUTER_CA), abi=PCS_ABI)
checker = web3.eth.contract(address=web3.toChecksumAddress(CHECKER_CA), abi=CHECKER_ABI)

async def BNB_to_USDT() :
    amountOut = int(pcs_contract.functions.getAmountsOut(1 * 10 ** WBNB_Decimal, [
        web3.toChecksumAddress(WBNB_add),
        web3.toChecksumAddress(USDT_add)]).call()[-1]) / 10 ** 18
    return amountOut

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
                message = "CA: {}\nToken: {} \nToken Price: {:.3e} USD \nHoneyPot: {}\nBuy - Sell tax: {}% - {}% \n ---------------------------- \n<b>Wallet balance:</b> {:.3f} {} ({:.3f} USDT - {:.3f} BNB - {:.3f} BNB with Tax)\n ".format(
                    token_ca,
                    token_symbol,
                    Tokenprice,
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
                message = "CA: {} \nToken: {} \nToken Price: {:.3f} USD \nHoneyPot: {}\nBuy - Sell tax: {}% - {}% \n ---------------------------- \n<b>Wallet balance:</b> {:.3f} {} ({:.3f} USDT - {:.3f} BNB - {:.3f} BNB with Tax)\n ".format(token_ca,token_symbol,
                                                                                                                                                                                          Tokenprice,
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
@client.on(events.NewMessage(chats=[1001708791345]))
async def my_event_handler(event):
    global BNBAmount,Gaswei,GasLimit,Slip,numTx,sell_percent,latest_ca,list_track
    global Tracking_threads, Tracking_threads_job, Tracking_threads_count

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
                    if token not in list_track:
                        await sendMessage("Adding token {} to track list".format(_checkToken[1]))
                        list_track.append(token)

    if (msg_lower.split()[0] == "remove" and msg.split()[1].startswith("0x")) and len(msg.split()[1]) == 42:
        checkToken = await checkTokenCA(msg_lower.split()[1])
        for token in msg_lower.split():
            if (token.startswith("0x") and len(token) == 42):
                checkToken = await checkTokenCA(token)
                if checkToken[0] == True :
                    if token in list_track:
                        await sendMessage("Removing token {} to track list".format(checkToken[1]))
                        list_track.remove(token)
                    else:
                        await sendMessage("Token {} is not in track list".format(checkToken[1]))

    if (msg_lower.split()[0] == "remove" and msg_lower.split()[1] == "all"):
        await sendMessage("Removing all tokens in track list!")
        list_track.clear()

    if (msg_lower.split()[0] == "track" or msg_lower.split()[0] == "t"):
        if list_track_len != 0:
            out_message = "Tracked tokens: \n"
            for token in list_track:
                checkToken = await checkTokenCA(token)
                if checkToken[0] == True:
                    token_ca = token
                    TokenContract = web3.eth.contract(address=web3.toChecksumAddress(token_ca),abi=ERC20abi_BSC)
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

                    mess = " - {} : {}\n    + <b>Amount:</b> {:.3f} ({:.1f} USDT - {:.3f} BNB)\n---------------------------\n".format(checkToken[1], token, readable, readable_in_usd, readable_in_bnb)
                    out_message += mess
                else :
                    list_track.remove(token)

            await sendMessage(out_message)
            print(out_message)
        else:
            await sendMessage("No token is tracked right now!")

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



@client.on(events.CallbackQuery())
async def call_handler(event):
    global BNBAmount, Gaswei, GasLimit, Slip, numTx, sell_percent, latest_ca, list_track
    global Tracking_threads, Tracking_threads_job, Tracking_threads_count
    if event.data == b"buy":
        get_message = await event.get_message()
        message_text = get_message.text
        loc = message_text.find("0x")
        token_ca = message_text[loc:loc+42]
        token_flag = await checkTokenCA(token_ca)
        await sendMessage(
            "Buying Token: {} \n + BNB Amount: {} \n + Gaswei: {} \n + GasLimit: {}\n + Slippage: {} \n + Number of Tx: {}".format(
                token_flag[1], BNBAmount, Gaswei, GasLimit, Slip, numTx))
        await TokenBuy_BNB(token_ca, BNBAmount, Gaswei, GasLimit, Slip, numTx)

    if event.data == b"sell":
        get_message = await event.get_message()
        message_text = get_message.text
        loc = message_text.find("0x")
        token_ca = message_text[loc:loc+42]
        token_flag = await checkTokenCA(token_ca)
        await sendMessage(
            "Selling Token: {} \n + Sell Percent: {}% \n + Gaswei: {} \n + GasLimit: {}\n + Slippage: {} \n".format(
                token_flag[1], sell_percent, Gaswei, GasLimit, Slip))
        await TokenSell_BNB(web3, token_ca, sell_percent, Gaswei, GasLimit, Slip)

    if event.data == b"approve":
        get_message = await event.get_message()
        message_text = get_message.text
        loc = message_text.find("0x")
        token_ca = message_text[loc:loc+42]
        token_flag = await checkTokenCA(token_ca)
        await sendMessage("Approving Token: {} \n".format(token_flag[1]))
        await ApproveToken(web3, token_ca, Gaswei, GasLimit)

    if event.data == b"add":
        get_message = await event.get_message()
        message_text = get_message.text
        loc = message_text.find("0x")
        token_ca = message_text[loc:loc+42]
        token_flag = await checkTokenCA(token_ca)
        if token_flag[0] == True:
            if token_ca.lower() not in list_track:
                await sendMessage("Adding token {} to track list".format(token_flag[1]))
                list_track.append(token_ca.lower())

    if event.data == b"remove":
        get_message = await event.get_message()
        message_text = get_message.text
        loc = message_text.find("0x")
        token_ca = message_text[loc:loc+42]
        token_flag = await checkTokenCA(token_ca)
        if token_ca.lower() in list_track:
            await sendMessage("Removing token {} to track list".format(token_flag[1]))
            list_track.remove(token_ca.lower())
        else:
            await sendMessage("Token {} is not in track list".format(token_flag[1]))

client.start()
print("Start client!")
#ent = client.get_entity(1708791345)
#print(ent.id)
def checkThread():
    while 1:
        for thr in Tracking_threads:
            if thr.is_alive() == False:
                thr.join()
            time.sleep(1)

#t5 = threading.Thread(target=checkThread)
#t5.start()


client.run_until_disconnected()

