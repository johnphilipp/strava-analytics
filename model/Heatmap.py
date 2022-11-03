class Heatmap():
    def __init__(self, boom):
        self._boom = boom
    

    def _zoom_center(df):
        """
        Return zoom and center for mapbox
        """
        lats = df["start_lat"]
        lons = df["start_lng"]

        maxlon, minlon = max(lons), min(lons)
        maxlat, minlat = max(lats), min(lats)
        center = {
            'lon': round((maxlon + minlon) / 2, 6),
            'lat': round((maxlat + minlat) / 2, 6)
        }

        # longitudinal range by zoom level (20 to 1)
        # in degrees, if centered at equator
        lon_zoom_range = np.array([
            0.0007, 0.0014, 0.003, 0.006, 0.012, 0.024, 0.048, 0.096,
            0.192, 0.3712, 0.768, 1.536, 3.072, 6.144, 11.8784, 23.7568,
            47.5136, 98.304, 190.0544, 360.0
        ])

        margin = 2
        height = (maxlat - minlat) * margin * 2.0
        width = (maxlon - minlon) * margin
        lon_zoom = np.interp(width, lon_zoom_range, range(20, 0, -1))
        lat_zoom = np.interp(height, lon_zoom_range, range(20, 0, -1))
        zoom = round(min(lon_zoom, lat_zoom), 2)

        return zoom, center
        

    def heatmap_fig(df, map_style_selected):
        """
        Return plotly heatmap
        """
        fig = px.density_mapbox(df,
                                lat='start_lat',
                                lon='start_lng',
                                radius=10,
                                height=500,
                                center=dict(lat=30, lon=0),
                                zoom=1)
        zoom, center = _zoom_center(df)
        fig.update_layout(mapbox_style=map_style_selected,
                        mapbox_zoom=zoom,
                        mapbox_center=center,
                        margin={"r": 0, "t": 0, "l": 0, "b": 0})
        return fig