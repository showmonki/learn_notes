import React, { useState, useEffect } from 'react';
import moment from 'moment-timezone';

const TimestampConverter = ({ timestamp }) => {
    const [convertedDate, setConvertedDate] = useState(null);

    useEffect(() => {
        // Convert the timestamp to the correct timezone (UTC+8)
        const convertedDate = moment(timestamp).tz('UTC+8').format('YYYY-MM-DD HH:mm:ss');
        setConvertedDate(convertedDate);
    }, [timestamp]);

    return (
        <div>
            {convertedDate && <p>Converted Date: {convertedDate}</p>}
        </div>
    );
};

export default TimestampConverter;
