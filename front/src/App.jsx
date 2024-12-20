import { useState } from 'react';
import { Container, Form, Button, Spinner } from 'react-bootstrap';
import axios from 'axios';
const App = () => {
  const [projectName, setProjectName] = useState('');
  const [systemUrl, setSystemUrl] = useState('');
  const [appPackageName, setAppPackageName] = useState('');
  const [logo, setLogo] = useState(null);
  const [googleJson, setGoogleJson] = useState(null);
  const [status, setStatus] = useState('');
  const [loading, setLoading] = useState(false);

  const handleStartBot = async () => {
    // Verificação se o nome do projeto tem mais de 30 caracteres
    if (projectName.length > 30) {
      setStatus('Erro: O nome do projeto deve ter no máximo 30 caracteres.');
      return;
    }

    // Verificação para garantir que o logo e o arquivo JSON sejam enviados
    if (!logo || !googleJson) {
      setStatus('Erro: É necessário fazer upload do logo e do arquivo google.json.');
      return;
    }

    try {
      setStatus('O bot está rodando...');
      setLoading(true);
      
      console.log("Enviando dados:", {
        projectName,
        systemUrl,
        appPackageName,
        logo,
        googleJson
      });
      // Criar o FormData para enviar os dados
      const formData = new FormData();
      formData.append('projectName', projectName);
      formData.append('uri', systemUrl);
      formData.append('bundleIdentifier', appPackageName);
      formData.append('image', logo);  // Enviar a imagem (logo)
      formData.append('googleServicesPath', googleJson); // Enviar o arquivo .json do Firebase

      // Enviar a requisição para o back-end
      const response = await axios.post('http://127.0.0.1:8000/start-bot', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      setStatus('Foi criado o app na EXPO');
    } catch (error) {
      setStatus('Erro ao iniciar o bot.');
      console.error(error); // Log para verificar o erro
    } finally {
      setLoading(false); // Esconde o spinner
    }
  };

  return (
    
    <Container
      className="text-center d-flex justify-content-center align-items-center"
      style={{ minHeight: '100vh' }}
    >
      <div>
        <h1>Subir App</h1>
        <Form>
          <Form.Group className="mb-3">
            <Form.Label>Nome do Projeto (até 30 caracteres)</Form.Label>
            <Form.Control
              type="text"
              placeholder="Digite o nome do projeto"
              value={projectName}
              onChange={(e) => setProjectName(e.target.value)}
              maxLength={30} // Limita o tamanho do campo no formulário
            />
          </Form.Group>

          <Form.Group className="mb-3">
            <Form.Label>URL do Sistema</Form.Label>
            <Form.Control
              type="url"
              placeholder="Digite a URL do sistema do cliente"
              value={systemUrl}
              onChange={(e) => setSystemUrl(e.target.value)}
            />
          </Form.Group>

          <Form.Group className="mb-3">
            <Form.Label>Name pro App (Pacote)</Form.Label>
            <Form.Control
              type="text"
              placeholder="Ex: com.ibsystemLote.clienteTeste"
              value={appPackageName}
              onChange={(e) => setAppPackageName(e.target.value)}
            />
          </Form.Group>

          <Form.Group className="mb-3">
            <Form.Label>Logo do App</Form.Label>
            <Form.Control
              type="file"
              accept="image/*"
              onChange={(e) => setLogo(e.target.files[0])}
            />
          </Form.Group>

          <Form.Group className="mb-3">
            <Form.Label>google-services.json (Firebase)</Form.Label>
            <Form.Control
              type="file"
              accept=".json"
              onChange={(e) => {
                const file = e.target.files[0];
                if (file && file.name.endsWith('.json')) {
                  setGoogleJson(file);
                  setStatus('');
                } else {
                  setGoogleJson(null);
                  setStatus('Erro: Apenas arquivos .json são permitidos.');
                }
              }}
            />
          </Form.Group>

          <Button variant="primary" onClick={handleStartBot} disabled={loading}>
            {loading ? (
              <>
                <Spinner animation="border" size="sm" role="status" aria-hidden="true" />
                {' '}Iniciando...
              </>
            ) : (
              'Ativar Bot'
            )}
          </Button>
        </Form>
        <p>{status}</p>
      </div>

      
      
    </Container>
   
  );
};

export default App;
