#!/usr/bin/env python

import rospy
import tf2_ros
from geometry_msgs.msg import TransformStamped
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
    gnss_frame_id = rospy.get_param('~gnss_frame_id', '')
    map_frame_id = rospy.get_param('~map_frame_id', 'world')

    df = CsvToDf.read(x_csv, y_csv, z_csv)
    # Map center is the origin
    gm = DfToDem.convert(df, resolution, frame_id=map_frame_id)

    rospy.sleep(1)
    pub.publish(gm)
    rospy.loginfo('Published GridMap')

    # Publish transform from GNSS origin to map origin
    if gnss_frame_id is not '' and map_frame_id is not '':
        tf_sb = tf2_ros.StaticTransformBroadcaster()
        tform = TransformStamped()
        tform.header.frame_id = gnss_frame_id
        tform.child_frame_id = map_frame_id
        # Take median GNSS coordinate, since map center is the map origin
        tform.transform.translation.x = df['x'].median()
        tform.transform.translation.y = df['y'].median()
        tform.transform.rotation.w = 1
        tf_sb.sendTransform(tform)
        rospy.spin()


if __name__ == '__main__':
      main()
