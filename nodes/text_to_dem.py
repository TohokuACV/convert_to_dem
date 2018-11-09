#!/usr/bin/env python

import rospy
from grid_map_msgs.msg import GridMap

from convert_to_dem.csv_to_df import CsvToDf
from convert_to_dem.df_to_dem import DfToDem


def main():
    rospy.init_node('csv_to_dem')
    pub = rospy.Publisher('elevation_map', GridMap, latch=True, queue_size=1)

    x_csv = rospy.get_param('~csv/x')
    y_csv = rospy.get_param('~csv/y')
    z_csv = rospy.get_param('~csv/z')
    resolution = rospy.get_param('~resolution')

    df = CsvToDf.read(x_csv, y_csv, z_csv)
    gm = DfToDem.convert(df, resolution)

    rospy.sleep(1)
    pub.publish(gm)
    print('Published DEM. Exiting')


if __name__ == '__main__':
      main()
