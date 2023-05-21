from .verify import (
    verify_list, 
    verify_str
)

from .recast import (
    recast_to_list
)

def probe_string_data(data):

    if not verify_list(data):
        data = recast_to_list(data)

    for item in data:
        if not verify_str(item):
            raise ValueError(
                f'Expected all str data, got {type(item)}'
            )
    
    return data