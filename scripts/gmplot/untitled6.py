import gmplot
gmap = gmplot.GoogleMapPlotter(37.766956, -122.438481, 13)

hidden_gem_lat, hidden_gem_lon = 37.770776, -122.461689
gmap.marker(hidden_gem_lat, hidden_gem_lon, 'cornflowerblue')
gmap.draw("my_map2.html")
