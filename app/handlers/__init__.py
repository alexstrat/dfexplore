import hello
import dataframe
import events
import static

def get_all():
    return hello.default_handlers + \
        dataframe.default_handlers + \
        events.default_handlers +\
        static.default_handlers
