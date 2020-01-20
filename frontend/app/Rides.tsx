import * as React from 'react'
import { CircleMarker, Popup, Polyline } from 'react-leaflet'
import { useData } from './useData'
import { BASE } from './App'

export const Rides: React.FC<{}> = () => {
    const data = useData(BASE + 'rides')
    return data.map((marker, index) => (
        <>
            <CircleMarker key={index + marker.StartLocation_Latitude}
                center={[marker.StartLocation_Latitude, marker.StartLocation_Longitude]}
                radius={2}>
                <Popup>{marker.Id}</Popup>
            </CircleMarker>
            <CircleMarker key={index + marker.EndLocation_Latitude}
                center={[marker.EndLocation_Latitude, marker.EndLocation_Longitude]}
                radius={2}
                color={"red"}>
                <Popup>{marker.Id}</Popup>
            </CircleMarker>
            <Polyline
                key={index + marker.Id}
                positions={[[marker.StartLocation_Latitude, marker.StartLocation_Longitude], [marker.EndLocation_Latitude, marker.EndLocation_Longitude]]}
                color={"blue"}
                weight={1}
            />
        </>
    ))
}