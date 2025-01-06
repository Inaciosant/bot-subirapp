import { useState } from 'react';
import { Container, Form, Button, Spinner } from 'react-bootstrap';
import axios from 'axios';
import { ToastContainer, toast } from "react-toastify";
import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap/dist/js/bootstrap.bundle.min.js";
import { SiFreelancer } from "react-icons/si";
import { SiFirebase } from "react-icons/si";
import { MdImageSearch, MdDriveFileRenameOutline } from "react-icons/md";
import { BiCodeCurly,BiSolidPackage  } from "react-icons/bi";
const App = () => {
  const [projectName, setProjectName] = useState('');
  const [systemUrl, setSystemUrl] = useState('');
  const [appPackageName, setAppPackageName] = useState('');
  const [logo, setLogo] = useState(null);
  const [googleJson, setGoogleJson] = useState(null);
  const [status, setStatus] = useState('');
  const [loading, setLoading] = useState(false);
  const [showToast, setShowToast] = useState(false);
  // Define o tipo do Toast
  const handleStartBot = async () => {
    // Verificação se o nome do projeto tem mais de 30 caracteres
    if (projectName.length > 30) {
      toast.error("Erro: O nome do projeto deve ter no máximo 30 caracteres.");
      return;
    }

    // Verificação para garantir que o logo e o arquivo JSON sejam enviados
    if (!logo || !googleJson) {
      toast.error("Erro: É necessário fazer upload do logo e do arquivo google.json.");    
      return;
    }

    try {
      toast.info("O bot está rodando...", {
        icon: (
          <div className="spinner-border spinner-border-sm text-primary" role="status" />
        ),
      });
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

      toast.success("Bot rodou com sucesso!");
     
    } catch (error) {
      toast.error("Erro ao rodar o bot.");
      setStatus('Erro ao iniciar o bot.');
      console.error(error); // Log para verificar o erro
    } finally {
      setLoading(false); // Esconde o spinner
    }
  };

  return (
    <div className=' bg-dark text-white'>
    <Container
      className="text-center d-flex justify-content-center align-items-center  " 
      style={{ minHeight: '100vh' }}
    >
    
      <div>
      <ToastContainer
        position="top-right"
        hideProgressBar={true}
        newestOnTop={false}
        closeOnClick
        rtl={false}
        pauseOnFocusLoss
        draggable
        pauseOnHover
        theme="colored" // Altere para "light" ou "dark" se necessário
      />
       
        <Form className='card' style={{padding:"20px"}}>
        <div  style={{ display: 'flex', alignItems: 'center', gap: '10px', marginLeft:"120px" }}>
  <h1 className="mb-4 text-center" style={{color:"#cf4647"}}>AppLancer</h1>
  <SiFreelancer size={50} style={{color:"#cf4647"}} />
</div>
        
          <Form.Group className="mb-3 mt-4" style={{minWidth:"500px"}}>
            <Form.Label>Nome do Projeto (até 30 caracteres) <MdDriveFileRenameOutline size={30} style={{color:"#cf4647"}} /></Form.Label>
            <Form.Control
              type="text"
              placeholder="Digite o nome do projeto"
              value={projectName}
              onChange={(e) => setProjectName(e.target.value)}
              maxLength={30} // Limita o tamanho do campo no formulário
            />
          </Form.Group>

          <Form.Group className="mb-3">
            <Form.Label>URL do Sistema <BiCodeCurly  size={30} style={{color:"#cf4647"}}/></Form.Label>
            <Form.Control
              type="url"
              placeholder="Digite a URL do sistema do cliente"
              value={systemUrl}
              onChange={(e) => setSystemUrl(e.target.value)}
            />
          </Form.Group>

          <Form.Group className="mb-3">
            <Form.Label>Name pro App (Pacote)<BiSolidPackage size={30} style={{color:"#cf4647"}} /></Form.Label>
            <Form.Control
              type="text"
              placeholder="Ex: com.ibsystemLote.clienteTeste"
              value={appPackageName}
              onChange={(e) => setAppPackageName(e.target.value)}
            />
          </Form.Group>

          <Form.Group className="mb-3">
            <Form.Label>Logo do App <MdImageSearch size={30} style={{color:"#cf4647"}} /></Form.Label>
            <Form.Control
              type="file"
              accept="image/*"
              onChange={(e) => setLogo(e.target.files[0])}
            />
          </Form.Group>

          <Form.Group className="mb-3">
            <Form.Label>google-services.json (Firebase) <SiFirebase size={30} style={{color:"#cf4647"}} /></Form.Label>
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

          <Button variant="danger" onClick={handleStartBot} disabled={loading}>
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
   </div>
  );
};

export default App;
