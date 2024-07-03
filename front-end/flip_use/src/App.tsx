// App.tsx
import './App.css'; // Adjust the path based on the location of your CSS file
import React, { useState, useEffect } from 'react';
import DatePicker from 'react-datepicker';
import 'react-datepicker/dist/react-datepicker.css';
import Type1Card from './Type1Card.tsx';
import Type2Card from './Type2Card.tsx';

const options = { timeZone: 'Asia/Shanghai' }; // 选择您想要的时区

const fetchData = async (selectedDate: Date) => {
    try {
        const formattedDate = selectedDate.toLocaleString('zh-CN',options);
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
                // console.log('msgList:', msgList);
                const type1Data = msgList?.filter((item: any) => item.answerType === '1') || [];
                const type2Data = msgList?.filter((item: any) => item.answerType === '2') || [];

                // Debugging: Log the filtered data
                // console.log('type1Data:', type1Data);
                // console.log('type2Data:', type2Data);
                console.log(type1Data[0].msg_time)
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
                <h4>Type 1 Data ({dataList1.length} items)</h4>
                <div className="card-container">
                    {dataList1.map((data, index) => (
                        <Type1Card
                            key={index}
                            msgTime={data.utc_time}
                            question={data.question}
                            answer={data.answer}
                            usrname = {data.userName}
                            cost = {data.cost}
                        />
                    ))}
                </div>
            </div>

            <div>
                <h4>Type 2 Data ({dataList2.length} items)</h4>
                <div className="card-container">
                    {dataList2.map((data, index) => (
                        <Type2Card key={index} msgTime={data.utc_time}
                                   question={data.question} answer={data.answer}
                                   usrname = {data.userName}
                                   cost = {data.cost}
                        />
                    ))}
                </div>
            </div>
        </div>
    );
};

export default App;
