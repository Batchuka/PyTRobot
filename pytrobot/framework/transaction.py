from pandas import DataFrame


class Transaction:
    number: int = 0
    item: dict = {}
    data: DataFrame = DataFrame()

    @staticmethod
    def set_data(data):
        """
        Starts the transaction variables of static Transaction with the provided list of items. 
        Use this method to make ETL of data to process and set the proper structure for transaction. 
        Note: use 'dispatcher' State do enrich the 'data' if necessery.

        :param data: some untyped dataset representing the items to be processed in the job.
        """
        Transaction.data = data
        Transaction.number= 1
        Transaction.item = {}

    @staticmethod
    def get_item():
        """
        Processes the next item in the transaction.
        Updates the item counter and the currently processed item.
        Logs messages to indicate the processing status.

        :return: The dictionary representing the processed item or None if no item is being processed.
        """
        if not Transaction.data.empty:
            number = len(Transaction.data) - Transaction.number
            Transaction.item = Transaction.data.iloc[number].to_dict()
            print(f"Transaction {Transaction.number} | item {Transaction.item}")
            Transaction.number += 1
            return Transaction.item
        else:
            raise ValueError('No items to process.')
    
    @staticmethod
    def update(item):
        """
        Updates the item in the DataFrame based on the current transaction number.

        :param updated_item: The dictionary representing the updated item.
        """
        if Transaction.number > 0:
            number = len(Transaction.data) - Transaction.number
            Transaction.data.iloc[number] = item
            print(f"Transaction {Transaction.number} | item updated: {item}")
        else:
            raise ValueError('Transaction not started. Call set_data() first.')
