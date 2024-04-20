class File:
    def __init__(self, name, execution, parent):
        self.name = name
        self.execution = execution
        self.parent = parent

    def execute(self, execution_args):
        self.execution(execution_args)
