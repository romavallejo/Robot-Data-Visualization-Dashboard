import 'bootstrap/dist/css/bootstrap.css';
import HeaderPagina from "./components/HeaderPagina"
import Botones from "./components/Botones"
import GraficaTemperatura from "./components/GraficaTemperatura"
import GraficaAceleracion from "./components/GraficaAceleracion"
import Imagen from './components/Imagen';
import 'bootstrap/dist/css/bootstrap.min.css';

import React, { useEffect, useState } from 'react';
import axios from 'axios';
/* import { getMeasurementsBySensor, getLastMeasurementBySensor } from '.'; */

const API_BASE_URL = 'http://127.0.0.1:8000'; 

// Axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export interface ResponseMediciones {
  mediciones: number[][];
  tiempo: string[]
}

function App() {
  const [data, setData] = useState<ResponseMediciones>();
  
  useEffect(() => {
    const getMeasurementsBySensor = async () => {
      try {
        const response = await api.get(`/sensors/mediciones/`);
        
        console.log(response);

        if (response.status === 200) {
          setData(response.data);
          console.log(data);
        }

      } catch (error) {
        console.error('Error fetching measurements:', error);
        throw error;
      }
    };

    const fetchData = setInterval(() => {
      getMeasurementsBySensor();
    }, 10000);

    return () => clearInterval(fetchData);
  }, []);


  return (
    <>
      <header>
        <HeaderPagina></HeaderPagina>
      </header>
      <body>
        <div className="container" style={{ marginTop: '32px'}}>
          <div className="row">
          <div className="col-md-2 col-sm-12">
              <div className="text-center">
                <h2>Avatar del Equipo</h2>
              </div>
              <Imagen/>
            </div>
            <div className="col-md-5 col-sm-12">
              <div className="text-center">
                <h2>Controles</h2>
              </div>
            <Botones/>
            </div>
            <div className="col-md-5 col-sm-12">
              <div className="text-center">
                <h2>Información</h2>
                <p className="text-muted">Detector de distancia: {data?.mediciones[0][data.mediciones[0].length - 1]} cm</p>
                <p className="text-muted">Fotorecistencia: {data?.mediciones[1][data.mediciones[1].length - 1]} ohms</p>
                <p className="text-muted">Altura: {data?.mediciones[4][data.mediciones[4].length - 1]} m</p>
                <p className="text-muted">Presión: {data?.mediciones[2][data.mediciones[2].length - 1]} hPa</p>
              </div>
            </div>
          </div>
        </div>
        <div className="container" style={{ marginTop: '32px'}}>
          <div className="text-center">
            <h2>Gráficas</h2>
          </div>
          <div className="row">
            <div className="col-md-6 col-sm-12">
              <GraficaTemperatura props={data}/>
            </div>
            <div className="col-md-6 col-sm-12">
              <GraficaAceleracion props={data}/>
            </div>
          </div>
        </div>
      </body>
    </>
  )
}

export default App
