import React from 'react';
import { Line } from 'react-chartjs-2';

const ProgressTracker = () => {
  const data = {
    labels: ['Week 1', 'Week 2', 'Week 3', 'Week 4'],
    datasets: [
      {
        label: 'Workout Progress',
        data: [5, 10, 15, 20],
        borderColor: 'rgba(75,192,192,1)',
        borderWidth: 2,
      },
    ],
  };

  return (
    <div>
      <h1>Progress Tracker</h1>
      <Line data={data} />
    </div>
  );
};

export default ProgressTracker;
