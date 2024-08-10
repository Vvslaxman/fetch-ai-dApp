from fetchai.ledger.contract import Contract

class MockContract:
    def __init__(self):
        self.state = {"status": "Order Placed"}

    def action(self, api, action, params):
        if action == 'update_status':
            self.state['status'] = params[0]

    def query(self, api, query, params):
        if query == 'get_status':
            return self.state['status']

def deploy_contract():
    return MockContract()
