class CommandBase:
    def __init__(self, socket):
        self.socket = socket



class ClientJoined(CommandBase) :
    def __init__(self, socket):
        super().__init__(socket)


class ClientLost(CommandBase) :
    def __init__(self, socket):
        super().__init__(socket)


class ClientMessage(CommandBase) :
    def __init__(self, socket, message):
        super().__init__(socket)
        self.message = message






