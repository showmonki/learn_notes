async function fetchBids(id, pageNum) {
    console.log('fetchBids:',id,pageNum)
    const response = await fetch('/bids', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams({
            'id': id,
            'numPerPage': 1000,
            'pageNum': pageNum,
            'r': 0.37446488796774813//Math.random()
        })
    });

    if (!response.ok) {
        const errorData = await response.json();
        console.error('Error:', errorData);
        throw new Error('Network response was not ok');
    }

    return response.json();
}

async function displayBids() {
    console.log("displayBids function called");
    const id = document.getElementById('bidId').value;
    let pageNum = 1;
    let successfulBids = [];

    try {
        while (true) {
            const bids = await fetchBids(id, pageNum);
            console.log(pageNum)
            if (bids.error) {
                console.error(bids.error);
                break; // 停止请求
            }
            if (bids.list.length === 0) break;

            successfulBids = successfulBids.concat(bids.list);
            console.log('fetch done, check next page')
            pageNum++;
        }

        const bidRecordsDiv = document.getElementById('bidRecords');
        bidRecordsDiv.innerHTML = ''; // 清空之前的记录

        // 创建表格的 HTML 字符串
        let tableHTML = `
            <table style="width: 100%; border-collapse: collapse;">
                <thead>
                    <tr>
                        <th style="border: 1px solid #ddd; padding: 8px; text-align: left;">序号</th>
                        <th style="border: 1px solid #ddd; padding: 8px; text-align: left;">用户ID</th>
                        <th style="border: 1px solid #ddd; padding: 8px; text-align: left;">出价</th>
                        <th style="border: 1px solid #ddd; padding: 8px; text-align: left;">出价时间</th>
                    </tr>
                </thead>
                <tbody>
        `;

        // 初始化序号计数器
        let serialNumber = 1;

        // 遍历出价记录并构建表体
        successfulBids.forEach(bid => {
            if (bid.auction_status === 1) { // 过滤出 auction_status 为 1 的出价记录
                const timestamp = parseInt(bid.bid_time.replace(/\/Date\((\d+)\)\//, '$1'));
                const date = new Date(timestamp);
                const formattedDate = date.toLocaleString();

                tableHTML += `
                    <tr>
                        <td style="border: 1px solid #ddd; padding: 8px;">${serialNumber}</td>
                        <td style="border: 1px solid #ddd; padding: 8px;">${bid.user_name}</td>
                        <td style="border: 1px solid #ddd; padding: 8px;">${bid.bid_amt}</td>
                        <td style="border: 1px solid #ddd; padding: 8px;">${formattedDate}</td>
                    </tr>
                `;
                
                // 增加序号计数器
                serialNumber++;
            }
        });

        // 结束表格的 HTML 字符串
        tableHTML += `
                </tbody>
            </table>
        `;

        // 将表格的 HTML 插入到页面
        bidRecordsDiv.innerHTML = tableHTML;
    } catch (error) {
        console.error('Error fetching bids:', error);
        // 这里可以显示一个用户友好的错误消息
        const bidRecordsDiv = document.getElementById('bidRecords');
        bidRecordsDiv.innerHTML = '<div>获取出价记录时发生错误，请稍后再试。</div>';
    }
}

document.getElementById('fetchBidsButton').addEventListener('click', displayBids);
const bidRecordsDiv = document.getElementById('bidRecords');
const bidIdInput = document.getElementById('bidId'); // 假设你有一个输入框用于输入场次ID
let intervalId; // 用于存储 setInterval 的 ID


async function fetchBids(id, pageNum) {
    console.log('fetchBids:',id,pageNum)
    const response = await fetch('/bids', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams({
            'id': id,
            'numPerPage': 2000,
            'pageNum': pageNum,
            'r': 0.37446488796774813//Math.random()
        })
    });

    if (!response.ok) {
        const errorData = await response.json();
        console.error('Error:', errorData);
        throw new Error('Network response was not ok');
    }

    return response.json();
}


async function displayBids() {
    console.log("displayBids function called");
    const id = bidIdInput.value; // 从输入框获取场次ID
    
    let pageNum = 1;
    let successfulBids = [];

    try {
        const bids = await fetchBids(id, pageNum);
        console.log(pageNum)
        if (bids.error) {
            console.error(bids.error);
            ; // 停止请求
        }
        if (bids.list.length === 0) ;

        successfulBids = successfulBids.concat(bids.list);
        console.log('fetch done')


        bidRecordsDiv.innerHTML = ''; // 清空之前的记录

        // 创建表格的 HTML 字符串
        let tableHTML = `
            <table style="width: 100%; border-collapse: collapse;">
                <thead>
                    <tr>
                        <th style="border: 1px solid #ddd; padding: 8px; text-align: left;">序号</th>
                        <th style="border: 1px solid #ddd; padding: 8px; text-align: left;">用户ID</th>
                        <th style="border: 1px solid #ddd; padding: 8px; text-align: left;">出价</th>
                        <th style="border: 1px solid #ddd; padding: 8px; text-align: left;">出价时间</th>
                    </tr>
                </thead>
                <tbody>
        `;

        // 初始化序号计数器
        let serialNumber = 1;

        // 遍历出价记录并构建表体
        successfulBids.forEach(bid => {
            if (bid.auction_status === 1) { // 过滤出 auction_status 为 1 的出价记录
                const timestamp = parseInt(bid.bid_time.replace(/\/Date\((\d+)\)\//, '$1'));
                const date = new Date(timestamp);
                const formattedDate = date.toLocaleString();

                tableHTML += `
                    <tr>
                        <td style="border: 1px solid #ddd; padding: 8px;">${serialNumber}</td>
                        <td style="border: 1px solid #ddd; padding: 8px;">${bid.user_name}</td>
                        <td style="border: 1px solid #ddd; padding: 8px;">${bid.bid_amt}</td>
                        <td style="border: 1px solid #ddd; padding: 8px;">${formattedDate}</td>
                    </tr>
                `;
                
                // 增加序号计数器
                serialNumber++;
            }
        });

        // 结束表格的 HTML 字符串
        tableHTML += `
                </tbody>
            </table>
        `;

        // 将表格的 HTML 插入到页面
        bidRecordsDiv.innerHTML = tableHTML;
    } catch (error) {
        console.error('Error fetching bids:', error);
        // 这里可以显示一个用户友好的错误消息
        const bidRecordsDiv = document.getElementById('bidRecords');
        bidRecordsDiv.innerHTML = '<div>获取出价记录时发生错误，请稍后再试。</div>';
    }
}

async function displayBidsscroll() {
    console.log("displayBids function called");
    const id = bidIdInput.value; // 从输入框获取场次ID
    
    let pageNum = 1;
    let successfulBids = [];

    try {
        while (true) {
            const bids = await fetchBids(id, pageNum);
            console.log(pageNum)
            if (bids.error) {
                console.error(bids.error);
                break; // 停止请求
            }
            if (bids.list.length === 0) break;

            successfulBids = successfulBids.concat(bids.list);
            console.log('fetch done, check next page')
            pageNum++;
        }


        bidRecordsDiv.innerHTML = ''; // 清空之前的记录

        // 创建表格的 HTML 字符串
        let tableHTML = `
            <table style="width: 100%; border-collapse: collapse;">
                <thead>
                    <tr>
                        <th style="border: 1px solid #ddd; padding: 8px; text-align: left;">序号</th>
                        <th style="border: 1px solid #ddd; padding: 8px; text-align: left;">用户ID</th>
                        <th style="border: 1px solid #ddd; padding: 8px; text-align: left;">出价</th>
                        <th style="border: 1px solid #ddd; padding: 8px; text-align: left;">出价时间</th>
                    </tr>
                </thead>
                <tbody>
        `;

        // 初始化序号计数器
        let serialNumber = 1;

        // 遍历出价记录并构建表体
        successfulBids.forEach(bid => {
            if (bid.auction_status === 1) { // 过滤出 auction_status 为 1 的出价记录
                const timestamp = parseInt(bid.bid_time.replace(/\/Date\((\d+)\)\//, '$1'));
                const date = new Date(timestamp);
                const formattedDate = date.toLocaleString();

                tableHTML += `
                    <tr>
                        <td style="border: 1px solid #ddd; padding: 8px;">${serialNumber}</td>
                        <td style="border: 1px solid #ddd; padding: 8px;">${bid.user_name}</td>
                        <td style="border: 1px solid #ddd; padding: 8px;">${bid.bid_amt}</td>
                        <td style="border: 1px solid #ddd; padding: 8px;">${formattedDate}</td>
                    </tr>
                `;
                
                // 增加序号计数器
                serialNumber++;
            }
        });

        // 结束表格的 HTML 字符串
        tableHTML += `
                </tbody>
            </table>
        `;

        // 将表格的 HTML 插入到页面
        bidRecordsDiv.innerHTML = tableHTML;
    } catch (error) {
        console.error('Error fetching bids:', error);
        // 这里可以显示一个用户友好的错误消息
        const bidRecordsDiv = document.getElementById('bidRecords');
        bidRecordsDiv.innerHTML = '<div>获取出价记录时发生错误，请稍后再试。</div>';
    }
}

document.addEventListener('DOMContentLoaded', () => {
    
    const bidRecordsDiv = document.getElementById('bidRecords');
    const bidIdInput = document.getElementById('bidId');
    let intervalId; // 用于存储 setInterval 的 ID

    const fetchBidsButton = document.getElementById('fetchBidsButton');
    const fetchBidsOnceButton = document.getElementById('fetchBidsOnceButton');
    console.log('Button element:', fetchBidsButton);

    if (fetchBidsButton) {
        fetchBidsButton.addEventListener('click', () => {
            console.log('Button clicked');
        
            // 首先调用一次以获取数据
            displayBids();
    
            // 如果已经有定时器在运行，先清除它
            if (intervalId) {
                clearInterval(intervalId);
            }
    
            // 每秒自动刷新获取出价记录
            intervalId = setInterval(displayBids, 1000); // 每1000毫秒（1秒）调用一次 displayBids
            console.log('New interval set:', intervalId); // 添加日志
        });
    } else {
        console.error('fetchBidsButton not found!');
    }

    if (fetchBidsOnceButton) {
        fetchBidsOnceButton.addEventListener('click', () => {
            console.log('Fetch once button clicked');
            // 如果已经有定时器在运行，先清除它
            if (intervalId) {
                clearInterval(intervalId);
            }
            // 只调用一次获取数据
            displayBids();
        });
    } else {
        console.error('fetchBidsOnceButton not found!');
    }
});

//         // 每秒自动刷新获取出价记录
//         // intervalId = setInterval(displayBids, 500); // 每500毫秒（0.5秒）调用一次 displayBids
//         // intervalId = setInterval(displayBids, 30000); // 每30000毫秒（30秒）调用一次 displayBids
//         intervalId = setInterval(displayBids, 1000); // 每1000毫秒（1秒）调用一次 displayBids
//         console.log('New interval set:', intervalId); // 添加日志
//     });
// } else {
//     console.error('fetchBidsButton not found!');
// }