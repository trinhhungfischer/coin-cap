class Logger:
    def __init__(self, file_path: str, to_console: bool) -> None:
        self.file_path = file_path
        self.to_console = to_console
        self.cache_logs = []
        self.num_cache = 10

    def log(self, *args):
        if self.to_console:
            print(*args)

        log = ""
        size = len(args)
        for idx, arg in enumerate(args):
            log += str(arg) + (" " if idx < size - 1 else "")
        self.cache_logs.append(log)

        if len(self.cache_logs) > self.num_cache:
            self.cache_logs.pop(0)

        if self.file_path is not None:
            with open(self.file_path, "a") as file:
                file.write(log + "\n")

    def cache_logs_to_str(self):
        result = ""
        for log in self.cache_logs:
            result += log + "\n"
        
        return result
    
    def clear(self):
        if self.file_path is not None:
            with open(self.file_path, "w") as f:
                pass
