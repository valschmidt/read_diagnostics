# read_diagnostics
Module to read diagnostics from a ROS1 Bag file to a pandas Dataframe.

Requires:
* `rosbag`
* `pandas`
* `rospy_message_converter`

Examples:
```
import rosbag
from read_diagnostics import read_diagnostics

bag = rosbag('somebagfile.bag')
# Return a dataframe of all the messages
diagdf = read_diagnostics(bag)
# Return only those with "imu" or 'gps' in the name.
diagdf = read_diagnostics(bag, names=['imu','gps'])
# Return only those with a hardware id of 123456.
diagdf = read_diagnostics(bag, hardware_ids=['123456'])
# Return the diagnostic messages as ROS diagnostics message types instead of DataFrame.
diagdf = read_diagnostics(bag, returnraw=True)
# Return only the first 100 diagnostics messages.
diagdf = read_diagnostics(bag, Ntoreturn=10)

```
