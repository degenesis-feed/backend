from web3 import Web3

# Example Ethereum transaction input value
input_value = "0xa9059cbb0000000000000000000000008a074f30a75fcfe2f8ecd01c88356c3ed672699b00000000000000000000000000000000000000000000000000000002540be400"


class Web3wrapper:
    def __init__(self):
        self.web3 = Web3()
        pass

    # ABI for the contract
    def parse_input(self, abi: dict, encoded_input: str):
        contract = self.web3.eth.contract(abi=abi)

        # decode input value
        decoded_data = contract.decode_function_input(input_value)

        # get function name and raw values
        function_name = decoded_data[0].fn_name  # Function name (e.g., 'transfer')
        raw_values = decoded_data[1]  # Raw values (e.g., '_to' and '_value')

        print(f"Function Name: {function_name}")
        print(f"Raw Values: {raw_values}")
        return {"function_name": function_name, "raw_values": raw_values}
