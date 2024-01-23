from pandas import DataFrame


class TransactionData:
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
        TransactionData.data = data
        TransactionData.number= 1
        TransactionData.item = {}

    @staticmethod
    def get_item():
        """
        Processes the next item in the transaction.
        Updates the item counter and the currently processed item.
        Logs messages to indicate the processing status.

        :return: The dictionary representing the processed item or None if no item is being processed.
        """
        if not TransactionData.data.empty:
            number = len(TransactionData.data) - TransactionData.number
            TransactionData.item = TransactionData.data.iloc[number].to_dict()
            print(f"Transaction {TransactionData.number} | item {TransactionData.item}")
            TransactionData.number += 1
            return TransactionData.item
        else:
            raise ValueError('No items to process.')
    
    @staticmethod
    def update(item):
        """
        Updates the item in the DataFrame based on the current transaction number.

        :param updated_item: The dictionary representing the updated item.
        """
        if TransactionData.number > 0:
            number = len(TransactionData.data) - TransactionData.number
            TransactionData.data.iloc[number] = item
            print(f"Transaction {TransactionData.number} | item updated: {item}")
        else:
            raise ValueError('Transaction not started. Call set_data() first.')
