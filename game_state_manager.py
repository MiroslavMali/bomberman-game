class GameStateManager:
    def __init__(self, initial_state='main_menu'):
        self.state = initial_state
        self.reset_requested = False

    def get_state(self):
        return self.state

    def set_state(self, new_state):
        self.state = new_state

    def is_reset_requested(self):
        return self.reset_requested

    def request_reset(self):
        self.reset_requested = True

    def clear_reset_request(self):
        self.reset_requested = False 