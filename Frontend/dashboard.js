let chart;

function animateValue(id, start, end, duration) {
    let obj = document.getElementById(id);
    let range = end - start;
    let startTime = null;

    function step(timestamp) {
        if (!startTime) startTime = timestamp;
        let progress = Math.min((timestamp - startTime) / duration, 1);
        obj.innerText = Math.floor(progress * range + start);
        if (progress < 1) {
            requestAnimationFrame(step);
        }
    }

    requestAnimationFrame(step);
}

async function fetchData() {
    const res = await fetch("http://127.0.0.1:8000/analytics");
    return await res.json();
}
async function loadInsights() {
    const res = await fetch("http://127.0.0.1:8000/insights");
    const data = await res.json();

    const list = document.getElementById("insightsList");
    list.innerHTML = "";

    data.insights.forEach(text => {
        const li = document.createElement("li");
        li.innerText = text;
        list.appendChild(li);
    });
}
async function updateDashboard() {

    const data = await fetchData();

    // Animated stats
    animateValue("likes", 0, data.total_liked, 500);
    animateValue("dislikes", 0, data.total_disliked, 500);

    const engagement = data.total_liked - data.total_disliked;
    animateValue("engagement", 0, engagement, 500);

    // Update lists
    const likedList = document.getElementById("likedList");
    const dislikedList = document.getElementById("dislikedList");

    likedList.innerHTML = "";
    dislikedList.innerHTML = "";

    data.liked.forEach(item => {
        const li = document.createElement("li");
        li.innerText = `${item.technique} (${item.count})`;
        likedList.appendChild(li);
    });

    data.disliked.forEach(item => {
        const li = document.createElement("li");
        li.innerText = `${item.technique} (${item.count})`;
        dislikedList.appendChild(li);
    });

    // Chart live update
    if (!chart) {
        const ctx = document.getElementById("chart");

        chart = new Chart(ctx, {
            type: "doughnut",
            data: {
                labels: ["Liked", "Disliked"],
                datasets: [{
                    data: [data.total_liked, data.total_disliked]
                }]
            },
            options: {
                animation: {
                    duration: 800
                },
                plugins: {
                    legend: {
                        labels: { color: "white" }
                    }
                }
            }
        });

    } else {
        chart.data.datasets[0].data = [
            data.total_liked,
            data.total_disliked
        ];
        chart.update();
    }
}

// AUTO REFRESH EVERY 3 SECONDS
setInterval(() => {
    updateDashboard();
    loadInsights();
}, 3000);

// INITIAL LOAD
updateDashboard();