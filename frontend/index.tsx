import * as React from 'react';
import * as ReactDOM from 'react-dom';

import {Map as LeafletMap, TileLayer, Marker, CircleMarker, Popup, Polyline} from 'react-leaflet';
import axios from 'axios';

const position = [54.349416, 18.648098];

const App: React.FC<{}> = () => {
    const [rides, setRides] = React.useState([]);

    React.useEffect(() => {
        const fetchRides = async () => {
            const result = await axios.get('http://localhost:5000/rides');
            console.log(result);
            setRides(result.data);
        };
        fetchRides();
    }, []);

    return (
        <LeafletMap center={position} zoom={11}>
            <TileLayer
                attribution='&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
                url='https://{s}.tile.osm.org/{z}/{x}/{y}.png'
            />
            {rides.map(((marker, index) => (
                <>
                    <CircleMarker key={index}
                                  center={[marker.StartLocation_Latitude, marker.StartLocation_Longitude]}
                                  radius={2}>
                        <Popup>{marker.Id}</Popup>
                    </CircleMarker>
                    <CircleMarker key={index}
                                  center={[marker.EndLocation_Latitude, marker.EndLocation_Longitude]}
                                  radius={2}
                                  color={"red"}>
                        <Popup>{marker.Id}</Popup>
                    </CircleMarker>
                    <Polyline
                        positions={[[marker.StartLocation_Latitude, marker.StartLocation_Longitude], [marker.EndLocation_Latitude, marker.EndLocation_Longitude]]}
                        color={"blue"}
                        weight={1}
                    />>
                </>
            )))}
        </LeafletMap>
    )
}

ReactDOM.render(<App/>, document.getElementById("app"));

