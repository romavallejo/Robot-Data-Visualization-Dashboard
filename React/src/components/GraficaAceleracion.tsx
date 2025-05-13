import { Line } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, LineElement, PointElement, Title, Tooltip, Legend } from 'chart.js';
import React from 'react';

import { ResponseMediciones } from '../App';

ChartJS.register(
  CategoryScale,
  LinearScale,
  LineElement,
  PointElement,
  Title,
  Tooltip,
  Legend
);

interface GraficaAceleracionProps {
  props?: ResponseMediciones; // Make it optional if `data` might be undefined initially
}

const GraficaAceleracion: React.FC<GraficaAceleracionProps> = ({ props }) => {
  // Datos estáticos para la gráfica
  const data = {
    labels: props?.tiempo,
    datasets: [
      {
        label: 'X',
        data: props?.mediciones[5],
        borderColor: 'rgba(255, 99, 132, 1)',
        backgroundColor: 'rgba(255, 99, 132, 0.2)',
        tension: 0.4,
      },
      {
        label: 'Y',
        data: props?.mediciones[6],
        borderColor: 'rgba(54, 162, 235, 1)',
        backgroundColor: 'rgba(54, 162, 235, 0.2)',
        tension: 0.4,
      },
      {
        label: 'Z',
        data: props?.mediciones[7],
        borderColor: 'rgba(75, 192, 192, 1)',
        backgroundColor: 'rgba(75, 192, 192, 0.2)',
        tension: 0.4,
      },
    ],
  };

  // Opciones de la gráfica
  const options = {
    responsive: true,
    plugins: {
      title: {
        display: true,
        text: 'Histórico de aceleración',
      },
    },
    scales: {
      x: {
        title: {
          display: true,
          text: 'Tiempo',
        },
      },
      y: {
        title: {
          display: true,
          text: 'cm',
        },
        beginAtZero: true,
      },
    },
  };

  return (
    <div className="text-center">
      <h4>Aceleración</h4>
      <div>
        <Line data={data} options={options} />
      </div>
    </div>
  );
};

export default GraficaAceleracion;
