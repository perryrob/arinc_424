
import simplekml as skml

def get_color( color ):
    switch={        
        'aliceblue': skml.Color.aliceblue,
        'antiquewhite': skml.Color.antiquewhite,
        'aqua': skml.Color.aqua,
        'aquamarine': skml.Color.aquamarine,
        'azure': skml.Color.azure,
        'beige': skml.Color.beige,
        'bisque': skml.Color.bisque,
        'black': skml.Color.black,
        'blanchedalmond': skml.Color.blanchedalmond,
        'blue': skml.Color.blue,
        'blueviolet': skml.Color.blueviolet,
        'brown': skml.Color.brown,
        'red': skml.Color.red,
        'burlywood': skml.Color.burlywood,
        'cadetblue': skml.Color.cadetblue,
        'magenta': skml.Color.magenta,
    }
    return switch.get(color, skml.Color.black)
                      
def geojson_to_kml_primitives( geom, kml ):

    geom_type = geom['type']
    properties = geom.get('properties',{} )

    if geom_type == 'Polygon':
        shp = kml.newpolygon(name=properties.get('name','UNK'),
                             description=properties.get('description','UNK'),
                             altitudemode=skml.AltitudeMode.clamptoground,
                             outerboundaryis=geom['coordinates'][0])
        
        shp.style.linestyle.color = get_color(
            properties.get('line_color','blue')
        )
        
        shp.style.linestyle.width = properties.get('line_width',5)
        shp.style.polystyle.color = skml.Color.changealphaint(
            properties.get('alpha',100), get_color(
                properties.get('fill_color','blue')
            )
        )

    elif geom_type == 'LineString':
        shp = kml.newlinestring(name=properties.get('name','UNK'),
                                description=properties.get('description','UNK'),
                                coords=geom['coordinates'])
        shp.altitudemode=skml.AltitudeMode.clamptoground,
        shp.style.linestyle.color = get_color(
            properties.get('line_color','blue')
        )
        
        shp.style.linestyle.width = properties.get('line_width',5)
        

    elif geom_type == 'Point':
        shp = kml.newpoint(name=properties.get('name','UNK'),
                           description=properties.get('description','UNK'),
                           coords=[geom['coordinates']])
        shp.style.iconstyle.icon.href = properties.get(
            'icon',
            'http://maps.google.com/mapfiles/kml/pushpin/ylw-pushpin.png'
            )

    elif geom_type == 'MultiLineString':
        multi_line = kml.newmultigeometry(
            name=properties.get('name','UNK'),
            description=properties.get('description','UNK')
        )
        for p1,p2 in geom['coordinates']:
            multi_line.newlinestring(
                name=properties.get('name','UNK'),
                description=properties.get('description','UNK'),
                coords=[p1,p2] )
        multi_line.linestyle.color = get_color(
            properties.get('line_color','blue')
        )
        multi_line.linestyle.width = properties.get('line_width',5)
    elif geom_type == 'GeometryCollection':
        for geom in geom['geometries']:
            geojson_to_kml_primitives( geom, kml )
    else:
        print("ERROR: unknown type:", geom_type)
        
def kml_conversion( json_data, kml = None ):

    if kml is None:
        kml = skml.Kml()
    
    for feature in json_data['features']:
        geom = feature['geometry']
        geom_type = geom['type']
        if geom_type in ['Polygon', 'LineString',
                         'Point', 'GeometryCollection']: 
            geojson_to_kml_primitives( geom, kml )
        else:
            print("ERROR: unknown type:", geom_type)

    return kml

def fly_to_camera( center=(0,0,0),roll=0,tilt=0, kml=None):

    if kml is None:
        kml = skml.Kml()
        pnt = kml.newpoint()
        camera = skml.Camera(
            latitude=center[1],
            longitude=center[0],
            altitude=center[2],
            roll=roll,
            tilt=tilt,
            altitudemode=skml.AltitudeMode.relativetoground)

        pnt.camera = camera        

    return kml
    
