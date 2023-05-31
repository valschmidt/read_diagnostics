import rosbag
import pandas as pd
from rospy_message_converter.message_converter import convert_ros_message_to_dictionary


def read_diagnostics(bag, names=[], hardware_ids=[],returnraw=False, Ntoreturn = 'all'):
    '''Read diagnostics messages from a bag file and returns a pandas DataFrame
    
    bag:           rosbag.Bag('filename') object
    names:         Python list of diagnostic hardware names to filter by.
    hardware_ids:  Python list of diagnostics hardware ids to filter by.
    returnraw:     boolean, when True, list of diagnostic message types are returned.
    Ntoreturn:     Number of messages to return. Default: 'all'
    output:   DataFrame of diagnostics messages

    Val Schmidt
    Center for Coastal and Ocean Mapping
    University of New Hampshire
    Copyright 2023

    '''
    diagnostics = []
    msgs = []
    for idx, (topic, msg, t) in enumerate(bag.read_messages(topics=['/diagnostics'])):
        tmp = convert_ros_message_to_dictionary(msg)
        # Flattens diagnostics message header, status and key/value pairs into 
        # a single dictionary, which can then be converted to a DataFrame.
        # NB. This may break if the value in a key-value pairs is another data structure.
        for s in tmp['status']:
            if (s['name'] in names or s['hardware_id'] in hardware_ids or
            (len(names) == 0 and len(hardware_ids) == 0)):
            
                # Return only the raw messages if requested.
                if returnraw:
                    msgs.append(msg)
                else:
                    diagnostics.append({'header_seq': tmp['header']['seq'],
                                        'header_stamp_secs': tmp['header']['stamp']['secs'],
                                        'header_stamp_nsecs': tmp['header']['stamp']['nsecs'],
                                        'header_frame_id': tmp['header']['frame_id'],
                                        'level': s['level'],
                                        'name': s['name'],
                                        'message': s['message'],
                                        'hardware_id': s['hardware_id']
                                    } | 
                                    dict([(pair['key'],pair['value']) for pair in s['values']])
                               )
                

            
        # Return only the first N messages.
        if Ntoreturn != 'all':
            if idx == Ntoreturn - 1:
                break

    # Return only the raw messages if requested.
    if returnraw:
        return msgs
    
    diagdf = pd.DataFrame(diagnostics)
    # Convert to numeric and boolean types.
    diagdf = diagdf.apply(pd.to_numeric,errors='ignore')
    diagdf = diagdf.applymap(lambda x: 1 if x == 'true' or x == 'True' else x).applymap(lambda x: 0 if x == 'false' or x == 'False' else x)
    # Convert to datetime and set index.
    diagdf['datetime'] = pd.to_datetime(diagdf['header_stamp_secs'] + 
                                        diagdf['header_stamp_nsecs']/1.0e9,
                                        unit='s')
    diagdf.set_index('datetime',inplace=True)
    
    return diagdf
