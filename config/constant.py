class RelationshipTypeConstant:
    HISTORY = 'HISTORY'
    HAS_ROOT = 'HAS_ROOT'
    TRANSFERS = 'TRANSFERS'
    DEPOSITS = 'DEPOSITS'
    WITHDRAWS = 'WITHDRAWS'
    BORROWS = 'BORROWS'
    REPAYS = 'REPAYS'
    LIQUIDATE = 'LIQUIDATE'


class TransactionConstant:
    gas = "gas"
    gas_price = "gas_price"
    value = "value"
    input = "input"
    hash = "hash"
    transaction_hash = "transaction_hash"
    related_addresses = "related_addresses"
    block_number = "block_number"
    from_address = "from_address"
    to_address = "to_address"
    block_timestamp = "block_timestamp"


class TokenConstant:
    value = "value"
    contract_address = "contract_address"
    type = "type"
    native_token = "0x"
    event_type = "event_type"
    total_supply = "total_supply"
    address = "address"
    symbol = "symbol"
    decimals = 'decimals'
    name = "name"
    block_number = "block_number"
    price = "price"

class Neo4jWalletConstant:
    address = "address"
    lastUpdatedAt = "lastUpdatedAt"
    creditScore = "creditScore"
    tokens = "tokens"
    tokenBalances = "tokenBalances"
    balanceInUSD = "balanceInUSD"
    balanceChangeLogTimestamps = "balanceChangeLogTimestamps"
    balanceChangeLogValues = "balanceChangeLogValues"
    createdAt = "createdAt"
    depositTokens = "depositTokens"
    depositTokenBalances = "depositTokenBalances"
    depositInUSD = "depositInUSD"
    depositChangeLogTimestamps = "depositChangeLogTimestamps"
    depositChangeLogValues = "depositChangeLogValues"
    borrowTokens  = "borrowTokens"
    borrowTokenBalances = "borrowTokenBalances"
    borrowInUSD = "borrowInUSD"
    borrowChangeLogTimestamps = "borrowChangeLogTimestamps"
    borrowChangeLogValues = "borrowChangeLogValues"
    numberOfLiquidation = "numberOfLiquidation"
    totalValueOfLiquidation = "totalValueOfLiquidation"
    dailyTransactionAmounts = "dailyTransactionAmounts"
    dailyTransactionAmountsTimestamp = 'dailyTransactionAmountsTimestamp'
    dailyFrequencyOfTransactions = "dailyFrequencyOfTransactions"
    dailyFrequencyOfTransactionsTimestamp = 'dailyFrequencyOfTransactionsTimestamp'

class Neo4jTokenConstant:
    address = "address"
    totalSupply = "totalSupply"
    symbol = "symbol"
    name = "name"
    decimal ="decimal"
    dailyFrequencyOfTransactions ="dailyFrequencyOfTransactions"
    creditScore = "creditScore"
    price = "price"
    highestPrice = "highestPrice"
    marketCap = "marketCap"
    tradingVolume24 = "tradingVolume24"
    lastUpdatedAt = "lastUpdatedAt"

class Neo4jLendingPoolConstant:
    address = "address"
    tokens = "tokens"
    supply = "supply"
    borrow = "borrow"

class Neo4jTransferConstant:
    transactionID = "transactionID"
    timestamp = "timestamp"
    fromWallet = "fromWallet"
    toWallet = "toWallet"
    token = "token"
    value = "value"


class Neo4jTransfersConstant:
    fromWalletAddress = "fromWalletAddress"
    toWalletAddress = "toWalletAddress"
    transferLogTimestamps = "transferLogTimestamps"
    transferLogValues = "transferLogValues"
    totalNumberOfTransfer = "totalNumberOfTransfer"
    totalAmountOfTransferInUSD = "totalAmountOfTransferInUSD"
    highestValueTransferInUSD = "highestValueTransferInUSD"
    lowestValueTransferInUSD = 'lowestValueTransferInUSD'
    averageValueTransferInUSD = "averageValueTransferInUSD"


class Neo4jDepositsConstant:
    walletAddress = "walletAddress"
    lendingPoolAddress = "lendingPoolAddress"
    depositLogValues = "depositLogValues"
    depositLogTimestamps = "depositLogTimestamps"
    depositTokens = "depositTokens"
    depositTokenBalances = "depositTokenBalances"
    totalNumberOfDeposit = "totalNumberOfDeposit"
    totalAmountOfDepositInUSD = "totalAmountOfDepositInUSD"
    highestDepositInUSD = "highestDepositInUSD"
    lowestDepositInUSD = "lowestDepositInUSD"
    averageDepositInUSD = "averageDepositInUSD"


class Neo4jBorrowsConstant:
    walletAddress = "walletAddress"
    lendingPoolAddress = "lendingPoolAddress"
    borrowLogTimestamps = "borrowLogTimestamps"
    borrowLogValues = "borrowLogValues"
    borrowTokens = "borrowTokens"
    borrowTokenBalances = "borrowTokenBalances"
    totalNumberOfBorrow = "totalNumberOfBorrow"
    totalAmountOfBorrowInUSD = "totalAmountOfBorrowInUSD"
    highestBorrowInUSD = "highestBorrowInUSD"
    lowestBorrowInUSD = "lowestBorrowInUSD"
    averageBorrowInUSD = "averageBorrowInUSD"


class Neo4jWithdrawsConstant:
    walletAddress = "walletAddress"
    lendingPoolAddress = "lendingPoolAddress"
    withdrawLogValues = "withdrawLogValues"
    withdrawLogTimestamps = "withdrawLogTimestamps"
    totalNumberOfWithdraw = "totalNumberOfWithdraw"
    totalAmountOfWithdrawInUSD = "totalAmountOfWithdrawInUSD"
    highestWithdrawInUSD = "highestWithdrawInUSD"
    lowestWithdrawInUSD = "lowestWithdrawInUSD"
    averageWithdrawInUSD = "averageWithdrawInUSD"


class Neo4jRepaysConstant:
    walletAddress = "walletAddress"
    lendingPoolAddress = "lendingPoolAddress"
    repayLogValues = "repayLogValues"
    repayLogTimestamps = "repayLogTimestamps"
    totalNumberOfRepay = "totalNumberOfRepay"
    totalAmountOfRepayInUSD = "totalAmountOfRepayInUSD"
    highestRepayInUSD = "highestRepayInUSD"
    lowestRepayInUSD = "lowestRepayInUSD"
    averageRepayInUSD = "averageRepayInUSD"


class Neo4jLiquidatesConstant:
    fromWalletAddress = "fromWalletAddress"
    toWalletAddress = "toWalletAddress"
    lendingPoolAddress = "lendingPoolAddress"
    toBalance = "toBalance"
    toAmount = "toAmount"
    fromBalance = "fromBalance"
    fromAmount = "fromAmount"
    protocol = "protocol"
    transactionID = "transactionID"
    timestamp = "timestamp"


class Neo4jDepositConstant:
    transactionID = "transactionID"
    timestamp = "timestamp"
    fromWallet = "fromWallet"
    toAddress = "toAddress"
    token = "token"
    value = "value"


class Neo4jBorrowConstant:
    transactionID = "transactionID"
    timestamp = "timestamp"
    fromWallet = "fromWallet"
    toAddress = "toAddress"
    token = "token"
    value = "value"


class Neo4jRepayConstant:
    transactionID = "transactionID"
    timestamp = "timestamp"
    fromWallet = "fromWallet"
    toAddress = "toAddress"
    token = "token"
    value = "value"

class Neo4jWithdrawConstant:
    transactionID = "transactionID"
    timestamp = "timestamp"
    fromWallet = "fromWallet"
    toAddress = "toAddress"
    token = "token"
    value = "value"


class Neo4jLiquidateConstant:
    transactionID = "transactionID"
    timestamp = "timestamp"
    protocol = "protocol"
    fromWallet = "fromWallet"
    toWallet = "toWallet"
    fromBalance = "fromBalance"
    fromAmount = "fromAmount"
    toBalance = "toBalance"
    toAmount = "toAmount"


class ExporterConstant:
    list_out_date = 100
    seconds_in_day = 86400
    seconds_in_15_minutes = 900
