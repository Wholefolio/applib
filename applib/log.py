import logging


class FilterHealthChecks(logging.Filter):
    def filter(self, record):
        if "/healthz/" in record.args[0]:
            return False
        return True
