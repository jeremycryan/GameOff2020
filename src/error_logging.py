##!/usr/bin/env python3

from traceback import format_exception

def error_logging(path):
    return ErrorLoggingContext(path)

class ErrorLoggingContext:
    def __init__(self, path):
        self.path = path

    def __enter__(self):
        return self

    def __exit__(self,
        exception_type,
        exception_value,
        traceback):
        if not issubclass(exception_type, Exception):
            return
        tb_list = format_exception(exception_type,
                                   exception_value,
                                   traceback,
                                   100)
        tb_string = "".join(tb_list)
        with open(self.path, "a") as f:
            f.write(tb_string)
            f.write(f"{'-'*10}\n")
        print(f"Exception logged to {self.path}.")
