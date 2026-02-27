const bgSecondaryColor = getComputedStyle(document.documentElement).getPropertyValue('--color-background-secondary').trim();

const options = {
  responsive: true,
  aspectRatio: 1,
  legend: {
    labels: {
      fontColor: "white",
      fontSize: 14,
      fontStyle: "bold",
    }
  }
};


function displayAttendanceChart(ctx, { assigned, checkedIn, checkedInExtra, noShows, totalSlots }) {
  const chartData = { assigned, checkedIn, checkedInExtra, noShows, totalSlots };

  const labels = {
    checkedInExtra: { name: "Ekstrahjelp", color: '#6EE7B7' },
    checkedIn: { name: "Sjekket inn", color: '#34D399' },
    noShows: { name: "No-shows", color: '#EF4444' },
    assigned: { name: "Tildelt", color: '#FBBF24' },
    availableSlots: { name: "Ledige plasser", color: '#E5E7EB' },
  }

  const chart = new Chart(ctx, {
    type: 'doughnut',
    data: generateData(chartData),
    options,
  });

  return { chart, chartData, updateData }

  // the main challenge here is to keep the objects consistent to not cause everything to re-render
  function updateData(changes) {
    for (const [key, value] of Object.entries(changes)) {
      chartData[key] = (chartData[key] || 0) + value;
      if (chartData[key] < 0) delete chartData[key];
    }
    const newData = generateData(chartData);
    chart.data.labels = newData.labels;
    chart.data.datasets[0].data = newData.datasets[0].data;
    chart.data.datasets[0].backgroundColor = newData.datasets[0].backgroundColor;
    chart.update();
  }

  function generateData(chartData) {
    const data = {
      checkedInExtra: chartData.checkedInExtra || 0,
      checkedIn: chartData.checkedIn || 0,
      noShows: chartData.noShows || 0,
      assigned: (chartData.assigned || 0) - (chartData.checkedIn || 0) - (chartData.checkedInExtra || 0) - (chartData.noShows || 0),
      availableSlots: Math.max(chartData.totalSlots - (chartData.assigned || 0), 0),
    }

    return {
      labels: Object.entries(labels).filter(([key]) => data[key] > 0).map(([, label]) => label.name),
      datasets: [{
        data: Object.entries(data).filter(([key, value]) => value > 0).map(([, value]) => value),
        backgroundColor: Object.entries(labels).filter(([key]) => data[key] > 0).map(([, label]) => label.color),
        borderColor: bgSecondaryColor,
        borderWidth: 3,
      }],
    }
  }
}


function displayCrewComparisonChart(ctx, crews = []) {
  const crewCounts = crews.reduce((acc, crew) => {
    acc[crew] = (acc[crew] || 0) + 1;
    return acc;
  }, {});

  const colors = ["#ff6900", "#ff4f52", "#ff3981", "#f346ad", "#cc5dce", "#9a71e0", "#5f7ee0", "#0084d1"];

  const chart = new Chart(ctx, {
    type: 'doughnut',
    data: generateData(crewCounts),
    options
  });

  return { chart, crewCounts, updateData }

  function updateData(changes) {
    console.log(changes);
    for (const [key, value] of Object.entries(changes)) {
      crewCounts[key] = (crewCounts[key] || 0) + value;
      if (crewCounts[key] <= 0) delete crewCounts[key];
    }
    const newData = generateData(crewCounts);
    console.log(newData);
    chart.data.labels = newData.labels;
    chart.data.datasets[0].data = newData.datasets[0].data;
    chart.data.datasets[0].backgroundColor = newData.datasets[0].backgroundColor;
    chart.update();
  }

  function generateData(crewCounts) {
    const entries = Object.entries(crewCounts).sort(([keyA, countA], [keyB, countB]) => {
      if (keyA === "Multi-crew") return 1;
      if (keyB === "Multi-crew") return -1;
      return countB - countA;
    })

    const minifiedCrewCounts = {};
    let otherCount = 0;

    entries.forEach(([crew, count], index) => {
      if (index < colors.length || crew === "Multi-crew") minifiedCrewCounts[crew] = count;
      else otherCount += count;
    });

    if (otherCount > 0) minifiedCrewCounts["Andre crew"] = otherCount;

    return {
      labels: Object.keys(minifiedCrewCounts),
      datasets: [{
        data: Object.values(minifiedCrewCounts),
        backgroundColor: Object.keys(minifiedCrewCounts).map((key, index) => {
          if (key === "Multi-crew") return '#ffb700';
          if (key === "Andre crew") return '#aaaaaa';
          return colors[index % colors.length];
        }),
        borderColor: bgSecondaryColor,
        borderWidth: 3,
      }],
    }
  }
}
