import * as React from 'react'
import * as ReactDOM from 'react-dom'

import { Map as LeafletMap, TileLayer, Marker, CircleMarker, Popup } from 'react-leaflet'
import axios from 'axios'

const position = [54.349416, 18.648098]

const App: React.FC<{}> = () => {
    const [rides, setRides] = React.useState([])

    React.useEffect(() => {
        const fetchRides = async () => {
            const result = await axios.get('http://localhost:5000/rides')
            console.log(result)
            setRides(result.data)
        }
        fetchRides()
    }, [])

    return (
        <LeafletMap center={position} zoom={11}>
            <TileLayer
                attribution='&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
                url='https://{s}.tile.osm.org/{z}/{x}/{y}.png'
            />
            {rides.map(((marker, index) => (
                <CircleMarker key={index} center={[marker[1], marker[2]]} radius={2}>
                    <Popup>{marker[0]}</Popup>
                </CircleMarker>
            )))}
        </LeafletMap>
    )
}

ReactDOM.render(<App />, document.getElementById("app"));

