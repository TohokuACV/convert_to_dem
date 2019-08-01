# convert_to_dem

convert_to_dem package.

## Installation

Use of the following packages are recommended to convert a DEM described as
text files into an OccupancyGrid message:

- [`dem_to_occupancy`](https://gitlab.com/tohoku-acv/dem_to_occupancy)

## How to use

An example is shown as follows:

```
$ prefix=~/lab/acv/2018-11-07_UAV_DEM/data/uav_pointclouds/20181016/0.5m
$ rl convert_to_dem convert_to_dem_node.launch \
      x_csv:=${prefix}/x_dem_0.5m_441x555_utm.csv \
      y_csv:=${prefix}/y_dem_0.5m_441x555_utm.csv \
      z_csv:=${prefix}/z_dem_0.5m_441x555_utm.csv \
      resolution:=0.5 \
      gnss_frame_id:=gps_origin \
      map_frame_id:=map
```

This launches the following nodes:

- `text_to_dem.py`: Converts a text file (in this case, CSV file) into
  GridMap, and publishes the TF transform from GNSS origin (`gps_origin`) to
  GridMap origin (`map`)
- `filters_demo`: Filter chain that adds the traversability information to the
  GridMap published by `text_to_dem.py`
- `dem_to_occupancy`: Spawns a service that converts GridMap to OccupancyGrid
- `dem_to_occupancy_client`: Subscribes to the filtered GridMap and uses the
  service spawned by `dem_to_occupancy`to do the actual conversion from
  GridMap to OccupancyGrid
- `rviz`: does the visualization

There is really only one parameter that needs explanation: `threshold` in
`dem_to_occupancy_client.py`. The GridMap published by the filter contains a
`traversability` layer which has values in the range [0, 1]. These values
represent the traversability of that grid. We then convert this to an
OccupancyGrid, in which most cases we need a threshold to determine whether
that grid is occupied or not. The `threshold` value controls how much slope is
needed in order for a grid to be considered occupied, or untraversable.

## License

MIT


## Author

Naoki Mizuno (mizuno.naoki@rm.is.tohoku.ac.jp)
