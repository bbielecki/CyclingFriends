import { useState, useEffect } from "react";
import axios from 'axios'

export const useData = (url: string) => {
    const [data, setData] = useState([])

    useEffect(() => {
        const fetch = async () => {
            const result = await axios.get(url);
            console.log(result);
            setData(result.data);
        };
        if (url) {
            console.log(url)
            fetch();
        }
    }, [url]);

    return { data }
} 