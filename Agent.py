class Agent:
    def act(self, query: str, context: list) -> dict:
        raise NotImplementedError("Subclasses should implement this method")
