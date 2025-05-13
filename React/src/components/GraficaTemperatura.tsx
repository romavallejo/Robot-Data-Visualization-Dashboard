import { Line } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, LineElement, PointElement, Title, Tooltip, Legend } from 'chart.js';
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

interface GraficaTemperaturaProps {
  props?: ResponseMediciones; // Make it optional if `data` might be undefined initially
}

const GraficaTemperatura: React.FC<GraficaTemperaturaProps> = ({ props }) => {
  // Datos estáticos para la gráfica
  const data = {
    labels: props?.tiempo,
    datasets: [
      {
        label: 'Temperatura C°',
        data: props?.mediciones[3],
        borderColor: 'rgba(255, 99, 132, 1)',
        backgroundColor: 'rgba(255, 99, 132, 0.2)',
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
        text: 'Histórico Temperatura',
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
          text: 'C°',
        },
        beginAtZero: true,
      },
    },
  };

  return (
    <div className="text-center">
      <h4>Temperatura</h4>
      <div>
        <Line data={data} options={options} />
      </div>
    </div>
  );
};

export default GraficaTemperatura;
