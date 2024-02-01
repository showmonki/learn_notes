// App.tsx
import './App.css'; // Adjust the path based on the location of your CSS file
import React, { useState, useEffect } from 'react';
import DatePicker from 'react-datepicker';
import 'react-datepicker/dist/react-datepicker.css';
import ReactAudioPlayer from 'react-audio-player';
import prependUrlPrefix from './private_prefix.ts';

const fetchData = async (selectedDate: Date) => {
    try {
        const formattedDate = selectedDate.toISOString().split('T')[0];
        const response = await fetch(`http://127.0.0.1:2151/msg_extract`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ time: formattedDate }),
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const data = await response.json();
        console.log(data)
        return data || []; // Ensure msg_list is defined or provide a default empty array
    } catch (error) {
        console.error('Error fetching data:', error);
        return [];
    }
};

const App: React.FC = () => {
    const [selectedDate, setSelectedDate] = useState<Date | null>(null); // Initialize with null
    const [dataList1, setDataList1] = useState<any[]>([]);
    const [dataList2, setDataList2] = useState<any[]>([]);

    useEffect(() => {
        const fetchDataList = async () => {
            if (selectedDate) {
                const msgList = await fetchData(selectedDate);

                // Debugging: Log the msgList
                console.log('msgList:', msgList);

                const type1Data = msgList?.filter((item: any) => item.answerType === '1') || [];
                const type2Data = msgList?.filter((item: any) => item.answerType === '2') || [];

                // Debugging: Log the filtered data
                console.log('type1Data:', type1Data);
                console.log('type2Data:', type2Data);

                setDataList1(type1Data);
                setDataList2(type2Data);
            }
        };

        // Only call fetchDataList if a date is selected
        if (selectedDate) {
            fetchDataList();
        }
    }, [selectedDate]);

    return (
        <div>
            <label>
                日期筛选:
                <DatePicker
                    selected={selectedDate}
                    onChange={(date: Date | null) => setSelectedDate(date)}
                    dateFormat="yyyy-MM-dd"
                    isClearable
                />
            </label>

            <div>
                <h2>Type 1 Data</h2>
                <div className="card-container">
                    {dataList1.map((data, index) => (
                        <div key={index} className="card type1-card">
                            <div className="time-label">Time:</div>
                            <div>{new Date(data.msg_time).toLocaleString()}</div>
                            <div><strong>Question:</strong> {data.question}</div>
                            <div><strong>Answer:</strong> {data.answer}</div>
                        </div>
                    ))}
                </div>
            </div>

            <div>
                <h2>Type 2 Data</h2>
                <div className="card-container">
                    {dataList2.map((data, index) => {
                        const jsonData = JSON.parse(data.answer); // Parse the data string
                        const prefixedUrl = prependUrlPrefix(jsonData.url); // Concatenate prefix
                        return (
                            <div key={index} className="card type2-card">
                                <div className="time-label">Time:</div>
                                <div>{new Date(data.msg_time).toLocaleString()}</div>
                                <div><strong>Question:</strong> {data.question}</div>
                                <div><strong>Answer:</strong> {prefixedUrl}</div>
                                {prefixedUrl && <ReactAudioPlayer src={prefixedUrl} controls />}
                            </div>
                        );
                    })}
                </div>
            </div>
        </div>
    );
};

export default App;
