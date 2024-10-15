import fetch from 'node-fetch';

// Function to create a delay
const delay = (ms) => new Promise(resolve => setTimeout(resolve, ms));

async function measureLoadTime(urls, repetitions) {
    const results = {}; // Object to store data for each URL

    // Initialize result structure for each URL
    urls.forEach(url => {
        results[url] = {
            successCount: 0,
            errorCount: 0,
            successTimes: [],
            errorTimes: []
        };
    });

    // Perform the calls
    for (let i = 0; i < repetitions; i++) {
        console.log(`Starting round ${i + 1} of ${repetitions}...`);

        const promises = urls.map(async (url) => {
            const startTime = Date.now(); // Start time
            try {
                const response = await fetch(url);
                const endTime = Date.now(); // End time
                const duration = endTime - startTime; // Calculate duration

                if (response.status === 200) {
                    results[url].successCount++;
                    results[url].successTimes.push(duration);
                } else {
                    results[url].errorCount++;
                    results[url].errorTimes.push(duration);
                }
            } catch (error) {
                const endTime = Date.now(); // End time in case of error
                const duration = endTime - startTime; // Calculate duration for error
                results[url].errorCount++;
                results[url].errorTimes.push(duration);
            }
        });

        // Wait for all URLs to finish in this round
        await Promise.all(promises);

        // Wait 1 second before the next round
        await delay(1000);
    }

    // Calculate metrics and log the table
    console.log('\nMetrics Summary:');
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

        return {
            URL: url,
            '% 200': successRate,
            '% Error': errorRate,
            'Avg Response Time (200)': avgSuccessTime,
            'Avg Response Time (Error)': avgErrorTime
        };
    });

    console.table(table);
}

// Example usage
const urlsToTest = [
    'https://jsonplaceholder.typicode.com/posts',
    'https://jsonplaceholder.typicode.com/comments',
    'https://jsonplaceholder.typicode.com/albums',
];

const repetitions = 50; // Number of repetitions
measureLoadTime(urlsToTest, repetitions);
