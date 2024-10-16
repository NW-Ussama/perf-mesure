import axios from 'axios';
import dotenv from 'dotenv';

dotenv.config();

const repetitions = parseInt(process.env.REPETITIONS, 10) || 10;

const urlsToTest = process.env.URLS ? process.env.URLS.split(',') : [];

const authCookie = process.env.COOKIE;

if (urlsToTest.length === 0) {
    console.error("No URLs provided in the .env file.");
    process.exit(1);
}

const delay = (ms) => new Promise(resolve => setTimeout(resolve, ms));

async function measureLoadTime(urls, repetitions) {
    const scriptStartTime = Date.now();

    const results = {};

    urls.forEach(url => {
        results[url] = {
            successCount: 0,
            errorCount: 0,
            successTimes: [],
            errorTimes: []
        };
    });

    for (let i = 0; i < repetitions; i++) {
        console.log(`Starting round ${i + 1} of ${repetitions}...`);

        for (const url of urls) {
            const startTime = Date.now();
            try {
                const response = await axios.get(url, {
                    headers: {
                        'Cookie': authCookie
                    }
                });
                const endTime = Date.now();
                const duration = endTime - startTime;

                if (response.status === 200) {
                    results[url].successCount++;
                    results[url].successTimes.push(duration);
                } else {
                    results[url].errorCount++;
                    results[url].errorTimes.push(duration);
                }
            } catch (error) {
                const endTime = Date.now();
                const duration = endTime - startTime;
                results[url].errorCount++;
                results[url].errorTimes.push(duration);
            }
        }

        await delay(1000);
    }

    console.log('\nMetrics Summary:');
    let totalSuccessTime = 0;
    let totalSuccessCount = 0;
    let totalErrorTime = 0;
    let totalErrorCount = 0;

    const table = Object.entries(results).map(([url, data]) => {
        const totalCalls = data.successCount + data.errorCount;
        const successRate = ((data.successCount / totalCalls) * 100).toFixed(2) + '%';
        const errorRate = ((data.errorCount / totalCalls) * 100).toFixed(2) + '%';
        const avgSuccessTime = data.successTimes.length
            ? (data.successTimes.reduce((sum, time) => sum + time, 0) / data.successTimes.length).toFixed(2) + ' ms'
            : 'N/A';
        const avgErrorTime = data.errorTimes.length
            ? (data.errorTimes.reduce((sum, time) => sum + time, 0) / data.errorTimes.length).toFixed(2) + ' ms'
            : 'N/A';

        totalSuccessTime += data.successTimes.reduce((sum, time) => sum + time, 0);
        totalSuccessCount += data.successTimes.length;
        totalErrorTime += data.errorTimes.reduce((sum, time) => sum + time, 0);
        totalErrorCount += data.errorTimes.length;

        return {
            URL: url,
            '% 200': successRate,
            '% Error': errorRate,
            'Avg Response Time (200)': avgSuccessTime,
            'Avg Response Time (Error)': avgErrorTime
        };
    });

    console.table(table);

    const avgTotalSuccessTime = totalSuccessCount ? (totalSuccessTime / totalSuccessCount).toFixed(2) + ' ms' : 'N/A';
    const avgTotalErrorTime = totalErrorCount ? (totalErrorTime / totalErrorCount).toFixed(2) + ' ms' : 'N/A';

    console.log('\nOverall Averages:');
    console.log(`Avg Response Time (200) for All Pages: ${avgTotalSuccessTime}`);
    console.log(`Avg Response Time (Error) for All Pages: ${avgTotalErrorTime}`);

    const scriptEndTime = Date.now();
    const totalExecutionTime = (scriptEndTime - scriptStartTime) / 1000;
    console.log(`\nTotal Execution Time: ${totalExecutionTime.toFixed(2)} seconds`);
}

measureLoadTime(urlsToTest, repetitions);
