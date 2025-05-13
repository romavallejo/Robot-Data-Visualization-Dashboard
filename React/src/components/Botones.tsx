import Boton from './Boton';
import React, { useEffect, useState } from 'react';
import mqtt from 'mqtt';

const Botones = () => {
    const [client, setClient] = useState<any>(null);

    useEffect(() => {
        const mqttClient = mqtt.connect('wss://broker.hivemq.com:8884/mqtt');
        setClient(mqttClient);
        
        mqttClient.on('connect', () => {
            console.log('Connected to MQTT broker');
        });

        return () => {
            mqttClient.end();
        };
    }, []);

    const sendMessage = (message: any) => {
        if (client && client.connected) {
            client.publish('rover/motor', message);
            console.log(`Message sent: ${message}`);
        } else {
            console.log('MQTT client not connected');
        }
    };

    return (
        <div style={{display: 'grid', gridTemplateRows: 'repeat(3, 50px)', gridTemplateColumns: 'repeat(3, 50px)', gap: '10px', justifyContent: 'center', alignItems: 'center',}}
        >
            <div></div>
            <Boton Children="↑" onClick={() => sendMessage('fw')} />
            <div></div>
            <Boton Children="←" onClick={() => sendMessage('lf')} />
            <Boton Children="🛑" onClick={() => sendMessage('st')} />
            <Boton Children="→" onClick={() => sendMessage('rt')} />
            <div></div>
            <Boton Children="↓" onClick={() => sendMessage('bk')} />
            <div></div>
        </div>
    );
};

export default Botones;
