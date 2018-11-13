import rospy
from std_msgs.msg import Float32MultiArray, MultiArrayDimension
from geometry_msgs.msg import Pose
from grid_map_msgs.msg import GridMap

import numpy as np
import pandas as pd


class DfToDem(object):
    def __init__(self):
        pass

    @staticmethod
    def convert(df, resolution, **kwargs):
        """
        Converts a DataFrame to GridMap

        Convention of the GridMap is described in:
        https://github.com/ANYbotics/grid_map/raw/master/grid_map_core/doc/grid_map_conventions.pdf

                          ^
                          |
                          |
                          |
                 length_x |
                          |
                          |
           length_y       |
        <-----------------+

        :param df:
        :type df: pd.DataFrame
        :param resolution:
        :return:
        """
        frame_id = kwargs['frame_id'] if 'frame_id' in kwargs else 'world'
        layer = kwargs['layer'] if 'layer' in kwargs else 'elevation'
        origin = kwargs['origin'] if 'origin' in kwargs else None

        grids_x = df['x'].nunique()
        grids_y = df['y'].nunique()
        df = df.sort_values(['y', 'x'], ascending=False)

        gm = GridMap()
        gm.info.header.frame_id = frame_id
        if 'stamp' in kwargs and kwargs['stamp'] != 'now':
            gm.info.header.stamp = kwargs['stamp']
        else:
            gm.info.header.stamp = rospy.Time.now()
        gm.info.resolution = resolution
        gm.info.length_x = grids_x * resolution
        gm.info.length_y = grids_y * resolution
        if origin is None:
            # Put origin at the center
            pose = Pose()
            pose.position.x = 0
            pose.position.y = 0
            pose.orientation.w = 1
        elif type(origin) is list or type(origin) is tuple:
            pose = Pose()
            pose.position.x = origin[0]
            pose.position.y = origin[1]
            pose.orientation.w = 1
        else:
            pose = origin
        gm.info.pose = pose
        gm.layers.append(layer)
        gm.basic_layers.append(layer)

        # The dimensions
        dim_col = MultiArrayDimension()
        dim_col.label = 'column_index'
        dim_col.size = grids_y
        dim_col.stride = grids_x * grids_y
        dim_row = MultiArrayDimension()
        dim_row.label = 'row_index'
        dim_row.size = grids_x
        dim_row.stride = grids_x

        # The actual data
        flma = Float32MultiArray()
        flma.layout.data_offset = 0
        flma.layout.dim = [dim_col, dim_row]
        flma.data = df['z'].values.tolist()
        gm.data.append(flma)
        return gm
