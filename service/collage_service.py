def main():
    polylines = []
    imgs = []
    for i in range(0, specs["len"]):
        single_polyline = polylines["summary_polyline"].iloc[i]
        single_polyline = pd.DataFrame(single_polyline, columns=["start_lat", "start_lng"])
        if len(single_polyline > 0):
            # do image


if __name__ == "__main__":
    main()