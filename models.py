import urllib
import folium
from config import MB_TOKEN, OS_TOKEN
from folium.plugins import Draw, MarkerCluster


def basemap_lyrs():

    esri_imagery = "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"
    esri_attr = "<a href='https://www.esri.com'>&copy; ESRI</a>"

    cartodb_imagery = "http://a.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}.png"
    cartodb_attr = "<a href='https://www.carto.com'>&copy; Carto</a>"

    osm_imagery = "https://tile.openstreetmap.org/{z}/{x}/{y}.png"
    osm_attr = "<a href='https://www.openstreetmap.org'>&copy; OSM</a>"

    gh_imagery = "https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}"
    g_attr = "<a href='https://www.google.com'>&copy; Google</a>"

    gr_imagery = "https://mt1.google.com/vt/lyrs=m&x={x}&y={y}&z={z}"

    gs_imagery = "https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}"

    mbs_imagery = "https://api.mapbox.com/v4/mapbox.satellite/{z}/{x}/{y}@2x.png?access_token=" + str(
        MB_TOKEN)
    mb_attr = "<a href='https://www.mapbox.com'>&copy; Mapbox</a>"

    os_imagery = "https://api.os.uk/maps/raster/v1/zxy/Outdoor_3857/{z}/{x}/{y}.png?key=" + str(OS_TOKEN)
    os_attr = "© Crown copyright and database rights"

    return esri_imagery, esri_attr, cartodb_imagery, cartodb_attr, osm_imagery, osm_attr, gh_imagery, gr_imagery, gs_imagery, g_attr, mbs_imagery, mb_attr, os_imagery, os_attr


def init_map(data):

    esri_imagery, esri_attr, cartodb_imagery, cartodb_attr, osm_imagery, osm_attr, gh_imagery, gr_imagery, gs_imagery, g_attr, mbs_imagery, mb_attr, os_imagery, os_attr = basemap_lyrs()

    lat_mean = data["decimalLatitude"].mean()
    lon_mean = data["decimalLongitude"].mean()

    start_coords = (lat_mean, lon_mean)
    m = folium.Map(location=start_coords,
                   zoom_start=12,
                   tiles=None,
                   control_scale=True)

    folium.TileLayer(tiles=cartodb_imagery,
                     attr=cartodb_attr,
                     name="CartoDB Dark Imagery",
                     control=True,
                     show=True).add_to(m)

    folium.TileLayer(tiles=esri_imagery,
                     attr=esri_attr,
                     name="ESRI World Imagery",
                     control=True,
                     show=True).add_to(m)

    folium.TileLayer(tiles=osm_imagery,
                     attr=osm_attr,
                     name="Open Street Map",
                     control=True,
                     show=True).add_to(m)

    folium.TileLayer(tiles=mbs_imagery,
                     attr=mb_attr,
                     name="Mapbox Satellite",
                     control=True,
                     show=True).add_to(m)

    folium.TileLayer(tiles=gh_imagery,
                     attr=g_attr,
                     name="Google Hybrid",
                     control=True,
                     show=True).add_to(m)

    folium.TileLayer(tiles=gr_imagery,
                     attr=g_attr,
                     name="Google Road",
                     control=True,
                     show=True).add_to(m)

    folium.TileLayer(tiles=gs_imagery,
                     attr=g_attr,
                     name="Google Satellite",
                     control=True,
                     show=True).add_to(m)

    folium.TileLayer(tiles=os_imagery,
                     attr=os_attr,
                     name="OS Outdoor",
                     control=True,
                     show=True).add_to(m)

    marker_cluster = MarkerCluster(name="Sightings").add_to(m)

    for index, row in data.iterrows():
        popup=f"""
            <p><b>Scientific Name</b>: {row.scientificName}<br></p>
            <p><b>Common Name</b>: {row.vernacularName}<br></p>
            <p><b>Taxon Rank</b>: {row.taxonRank}</p>
            <p><b>County</b>: {row.stateProvince}</p>
            <p><b>Country</b>: {row.country}</p>
            <p><b>UKSI TVK</b>: {row.speciesGuid}</p>
            """

        folium.Marker(
            location=[row["decimalLatitude"], row["decimalLongitude"]],
            icon=folium.Icon(color="red", icon="info-sign"),
            popup=folium.Popup(popup, max_width="250"),
            show=True,
            control=True
        ).add_to(marker_cluster)

    Draw(export=True,
         filename="drawn_overlay.geojson",
         position="topleft",
         draw_options={
             "polyline": True,
             "polygon": True,
             "rectangle": True,
             "circle": True,
             "marker": True,
             "circlemarker": True}).add_to(m)

    folium.LayerControl().add_to(m)

    main_map = m._repr_html_()
    #main_map = main_map[:4] + main_map[24:29] + main_map[192:]
    data_html = main_map[193:-12]

    data_uri = urllib.parse.quote(data_html)
    chunk_1 = "<iframe id='iframeMap' src='about:blank' data-html="
    chunk_2 = """ onload="this.contentDocument.open();this.contentDocument.write(    decodeURIComponent(this.getAttribute('data-html')));this.contentDocument.close();" allowfullscreen webkitallowfullscreen mozallowfullscreen></iframe>"""
    map_html = chunk_1+data_uri+chunk_2

    return map_html
