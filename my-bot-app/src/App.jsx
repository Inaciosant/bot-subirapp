import React, { useState } from 'react';
import { Button, Form, Container } from 'react-bootstrap';
import axios from 'axios';

function App() {
  const [projectName, setProjectName] = useState('');
  const [status, setStatus] = useState('');

  const handleStartBot = async () => {
    try {
      setStatus('Iniciando o processo...');
      const response = await axios.post('http://localhost:8000/start-bot', { projectName });
      setStatus('Bot iniciado com sucesso!');
    } catch (error) {
      setStatus('Erro ao iniciar o bot.');
    }
  };

  return (
    <Container
  className="text-center d-flex justify-content-center align-items-center"
  style={{ minHeight: "100vh" }}
>
  <div>
    <h1>Subir App</h1>
    <Form>
      <Form.Group className="mb-3">
        <Form.Label>Nome do Projeto</Form.Label>
        <Form.Control
          type="text"
          placeholder="Digite o nome do projeto"
          value={projectName}
          onChange={(e) => setProjectName(e.target.value)}
        />
      </Form.Group>
      <Button variant="primary" onClick={handleStartBot}>Ativar Bot</Button>
    </Form>
    <p>{status}</p>
  </div>
</Container>
  );
}

export default App;
