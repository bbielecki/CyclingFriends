import * as React from 'react'
import { Map as LeafletMap, TileLayer } from 'react-leaflet';
import { Rides } from './Rides';
import { Pois } from './Pois';

export const BASE = 'http://localhost:5000/'

export const App: React.FC<{}> = () => {
    const position = [54.349416, 18.648098];
    const [url, setUrl] = React.useState('rides')

    return (
        <div style={{ display: 'flex', height: '100%' }}>
            <LeafletMap center={position} zoom={11}>
                <TileLayer
                    attribution='&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
                    url='https://{s}.tile.osm.org/{z}/{x}/{y}.png'
                />
                {url === 'rides' ? <Rides /> : <Pois />}

            </LeafletMap>
            <select value={url} onChange={(event) => { setUrl(event.target.value) }} style={{ height: 'min-content' }}>
                <option value='rides'>Rides</option>
                <option value='pois'>Pois</option>

            </select>
        </div>
    )
}