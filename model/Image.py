import numpy as np
import plotly.express as px
from io import BytesIO


class Image:
    def __init__(self, polyline: str, width_height: int, background_color: str, line_color: str, line_thickness: int, invert_colors: bool):
        self._polyline = polyline
        self._single_width_height = width_height
        self._background_color = background_color
        self._line_color = line_color
        self._line_thickness = line_thickness
        self._invert_colors = invert_colors

    def _zoom_center(self, df):
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

    def _line_fig(self, df, map_style_selected, line_color, line_thickness, height=500):
        """
        Return plotly map
        """
        fig = px.line_mapbox(df,
                             lat="start_lat",
                             lon="start_lng",
                             height=height,
                             color_discrete_sequence=px.colors.qualitative.Set1)
        zoom, center = self._zoom_center(df)
        fig.update_layout(mapbox_style=map_style_selected,
                          mapbox_zoom=zoom,
                          mapbox_center=center,
                          margin={"r": 0, "t": 0, "l": 0, "b": 0})
        fig.update_traces(line=dict(color=line_color, width=line_thickness))
        return fig

    def get_img(self):
        """
        Return image of polyline as byte object
        """
        fig = self._line_fig(single,
                             map_style_selected,
                             line_color,
                             line_thickness,
                             700)

        img_bytes = fig.to_image(format="png")
        str_file = BytesIO(img_bytes)
        pimg = Image.open(str_file)
        left = 0
        top = 0
        right = 700
        bottom = 680
        pimg = pimg.crop((left, top, right, bottom))

        return pimg


def main():
    image = Image("uqm`Hk{ex@~@LjCK^d@bBfEp@~@h@lBh@t@`@zAr@xApCfJt@fDvA|EfAjCGVlA?XVXpAZh@dEpF|AjCdBvD`BfGNlAv@tAd@n@v@j@r@nAxClANd@^|Cl@jBPtAJnBh@hE?`DzAxDp@zGp@xD|@xBl@\\t@jBbBdK|@pCl@~@p@zF|AzFr@hBfCrE~@nDjAjGl@~BvCfInChGj@~Bd@r@Bl@Gh@s@hBC~DHpDT|AFrETxB`@pBpDhMzCjJX~B`CzItAvCH`@M`@URe@A[QaB}B_AkBe@UgANe@KeCyBm@Gm@NYHU`@R`@lBx@b@rAT|BAhB}BbUTlDvAvGtAvCJQjBA|@w@DTJ?Ha@x@]hAThAt@tDnAf@Ar@dAnAl@^`@~ApCpBhKTf@`ApAjBId@J\\j@h@rFBlIvAjJJzANNvGuAPYEi@Uu@s@uE[cDZ_HEg@P}AUiEqAgFa@aDD_@IqCJy@?}@O}EC{CNuB?wA[cA}@mAkAiCaAoGoBlBeAh@hAxCj@bENhCEfCiAjDMnAQtD?pBbAbNLdBd@~Ah@pFF~GpArIZnCP\\vGeANe@Ak@w@_Es@cHJ}ATaABwBNgB[sEsAsEYcDDqBHcB_@aKRcGCgAkBsB_AeBsAcEGeBK?w@tAoAbA^hAp@lDt@hCDvC_@|B{@~Ak@`DKjABfDbBzRh@zAR|BTbADdInBxMXX|FoAT_@?a@wAcKI{A^yD@}BL}BKcBBo@Em@kBkGIu@FaBEa@LmCYaCAeE[gDJmEY{@oAiBwAkESgAk@mA{AlBeBt@wEfLgCdCmB`DMh@Af@TjEGNoAE[]{Ak@oAcAg@Gk@A]TQd@MDKYaAt@eAOq@R]k@[qAc@_A[iBKsCQw@DkDjByPLwCKuA]aAG{@_@cAwAu@OOCWbBq@b@JxBjBhABdAh@d@x@rA|Dr@Zd@]Je@Q}@UWaCyHe@qBc@wD{EcQeAiEQqAKiC[_CO{HBeBM{CLy@d@}@Hs@Y}@mEyIc@_By@sAa@sA{@_BqA_G_@{@k@cD}AyE{AkDgBmEi@sCQgBi@}Bi@_Am@}B}AcKm@{AoAwB_@sAwAsKgAkDe@{BgAcN{AmF]e@sBiA}@aBuAeBu@iBKu@_ByFmBiEuG_Ky@cBw@q@aAg@{DcLqBwIMuAw@{A",
                  500,
                  "white-bg",
                  "Black",
                  "20",
                  False)
    print(image.get_img())


if __name__ == "__main__":
    main()
