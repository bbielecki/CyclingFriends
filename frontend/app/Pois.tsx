import * as React from 'react'
import { CircleMarker, Popup } from 'react-leaflet'
import { useData } from './useData'
import { BASE } from './App'



export const Pois: React.FC<{}> = () => {
    const data = useData(BASE + 'pois')
    return data.map((marker, index) => (
        <>
            <CircleMarker key={index}
                center={[marker.Lat, marker.Lng]}
                radius={2}>
                <Popup>{marker.Tags}</Popup>
            </CircleMarker>
        </>
    ))
}