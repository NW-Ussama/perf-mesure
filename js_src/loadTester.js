import axios from 'axios'; // Import axios
import dotenv from 'dotenv';

// Load environment variables from .env file
dotenv.config();

// Read number of repetitions from environment variables or default to 50
const repetitions = parseInt(process.env.REPETITIONS, 10) || 50;

// Read URLs from environment variables and split by comma
const urlsToTest = process.env.URLS ? process.env.URLS.split(',') : [];

// Read the cookie from the environment variables
const authCookie = process.env.COOKIE;

if (urlsToTest.length === 0) {
    console.error("No URLs provided in the .env file.");
    process.exit(1);
}

// Function to create a delay
const delay = (ms) => new Promise(resolve => setTimeout(resolve, ms));

async function measureLoadTime(urls, repetitions) {
    // Start total execution time measurement
    const scriptStartTime = Date.now();

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

        for (const url of urls) {
            const startTime = Date.now(); // Start time
            try {
                const response = await axios.get(url, {
                    headers: {
                        'Cookie': authCookie // Attach the cookie for authentication
                    }
                });
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
        }

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

    // Log total execution time
    const scriptEndTime = Date.now();
    const totalExecutionTime = (scriptEndTime - scriptStartTime) / 1000;
    console.log(`\nTotal Execution Time: ${totalExecutionTime.toFixed(2)} seconds`);
}

// Call the function
measureLoadTime(urlsToTest, repetitions);
