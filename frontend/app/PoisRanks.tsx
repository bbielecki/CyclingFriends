import * as React from 'react'
import { CircleMarker, Popup } from 'react-leaflet'
import { useData } from './useData'
import { BASE } from './App'



export const PoisRanks: React.FC<{}> = () => {

    const { data: poisRanks } = useData(BASE + 'pois/ranks')
    const { data: pois } = useData(BASE + 'pois')

    return <>
        {poisRanks[0]?.map((marker) => {
            const v = (poisRanks[2][1] - marker[1]) / poisRanks[3]
            console.log(marker[1] * 100)
            return (
                <CircleMarker color={v <= 1 ? 'red' : v > 1 && v <= 2 ? 'orange' : v > 2 && v <= 3 ? 'yellow' : v > 3 && v <= 4 ? 'green' : '#F2A2A2'} key={marker[0]}
                    center={[pois.find(val => val.ClusterId === marker[0])?.Lat, pois.find(val => val.ClusterId === marker[0])?.Lng]}
                    radius={2}>
                    <Popup>{marker[2].tags} ; {marker[1]}</Popup>
                </CircleMarker>
            )
        })} </>
}