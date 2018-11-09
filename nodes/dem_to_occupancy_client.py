#!/usr/bin/env python

import rospy
from nav_msgs.msg import OccupancyGrid
from grid_map_msgs.msg import GridMap
from dem_to_occupancy.srv import Conversion, ConversionRequest


class DemToOccupancyClient(object):
    def __init__(self):
        self._dem_sub = rospy.Subscriber('filtered_map',
                                         GridMap,
                                         self.cb_grid_map)
        self._occ_pub = rospy.Publisher('map',
                                        OccupancyGrid,
                                        latch=True,
                                        queue_size=1)

        self._client = rospy.ServiceProxy('dem_to_occupancy', Conversion)
        self._layer_name = rospy.get_param('~layer', 'traversability')
        self._threshold = rospy.get_param('~threshold', 0.8)

    def cb_grid_map(self, msg):
        req = ConversionRequest()
        req.grid_map = msg
        req.layer = self._layer_name
        req.threshold = self._threshold
        res = self._client.call(req)
        self._occ_pub.publish(res.grid)

    def spin(self):
        rospy.spin()


if __name__ == '__main__':
    rospy.init_node('dem_to_occupancy')
    dtoc = DemToOccupancyClient()
    dtoc.spin()
