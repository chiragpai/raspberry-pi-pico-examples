class BLEActions:
    def __init__(self):
        self.allowed_actions = {
            "K": "KEYBOARD",
            "M": "MOUSE"
        }

    def process(self, data):
        data = data.strip()
        if(len(data) == 0):
            print("No data to proces")
            return
        try:
            action = self.allowed_actions[data[:1].upper()]
        except:
            return None, None
        seq = data[1:]
        if(len(seq) == 0):
            print(f"No data sequence for action: {action}")
            return None, None
        return action, seq
    