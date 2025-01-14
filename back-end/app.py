from flask import Flask, request, jsonify
import os
import subprocess
import json
import shutil

from flask_cors import CORS

app = Flask(__name__)
CORS(app)

NPM_PATH = r"C:\Users\ibsys\AppData\Roaming\npm\npm.cmd"
NPX_PATH = r"C:\Users\ibsys\AppData\Roaming\npm\npx.cmd"
EAS_PATH = r"C:\Users\ibsys\AppData\Roaming\npm\eas.cmd"


## Nome do projeto até 30 caracteres.
# URL do sistema do cliente para alterar na App.js
# Imagens para pasta assets
# Name pro app (com.ibsystemLote.clienteTeste)
# Google.json para firebase

def criar_projeto_expo(project_name, uri, bundle_identifier, google_services_path):
    try:
        if len(project_name) > 30:
            raise ValueError("O nome do projeto não pode ter mais de 30 caracteres.")
        
        if not uri or not bundle_identifier or not google_services_path or 'image' not in request.files:
            raise ValueError("Todos os campos obrigatórios devem ser preenchidos.")



        desktop_dir = os.path.join(os.path.expanduser('~'), 'Desktop')

        projeto_dir = os.path.join(desktop_dir, project_name)
        os.makedirs(projeto_dir, exist_ok=True)

        print(f"App será criado em: {projeto_dir}")
        
        print(f"Pasta {projeto_dir} criada com sucesso!")
        
        os.chdir(projeto_dir)
        print(f"Diretório atual: {os.getcwd()}")  

        subprocess.run([NPX_PATH, 'create-expo-app', project_name, '--template', 'blank'], check=True)
        print(f"Projeto Expo {project_name} criado com sucesso!")

        projeto_path = os.path.join(projeto_dir, project_name)
        os.chdir(projeto_path)
        print(f"Diretório atual após criação: {os.getcwd()}")
        package_json_path = os.path.join(projeto_path, "package.json")

        # Verifica se o package.json foi criado
        if not os.path.exists(package_json_path):
            raise FileNotFoundError(f"Erro: O arquivo {package_json_path} não foi encontrado!")

        print(f"Arquivo package.json encontrado: {package_json_path}")

        # Atualiza as dependências no package.json
        novas_dependencias = {
            "expo": "~52.0.9",
            "expo-status-bar": "~2.0.0",
            "react": "18.3.1",
            "react-native": "0.76.6",
            "react-native-webview": "13.12.5",
            "expo-notifications": "~0.29.6",
            "expo-device": "7.0.2",
            "expo-constants": "~17.0.3"
        }

        with open(package_json_path, "r") as f:
            package_data = json.load(f)

        package_data["dependencies"] = novas_dependencias

        with open(package_json_path, "w") as f:
            json.dump(package_data, f, indent=2)
        print("Arquivo package.json atualizado com sucesso!")

        # Instala as dependências
        subprocess.run([NPM_PATH, "install"], cwd=projeto_path, check=True)
        print("Dependências instaladas com sucesso!")

    

        # Instalar dependências do projeto (exemplo: webview, notifications, etc.)
        # Substituir código do App.js com o código correto do webview
        # Adicionar imagens corretas na pasta 'assets'
        # Alterar app.json para os dados do cliente
        # Integrar com o Firebase (google-services.json)
        # Rodar o EAS

        assets_dest_path = os.path.join(projeto_dir, "assets")

        if not os.path.exists(assets_dest_path):
            os.makedirs(assets_dest_path)
            print(f"Pasta 'assets' criada com sucesso em: {assets_dest_path}")

        image = request.files['image']


        if image:
            image_temp_path = os.path.join(os.getcwd(), image.filename)

            image.save(image_temp_path)
            print(f"Imagem salva temporariamente em: {image_temp_path}")

            image_dest_path = os.path.join(assets_dest_path, image.filename)

            shutil.move(image_temp_path, image_dest_path)
            print(f"Imagem movida com sucesso para {image_dest_path}")
        else:
            print("Nenhuma imagem foi recebida no formulário.")

##para criar o codigo que cria o arquivo googles.json e jogar ele para a pasta do app e depois pegar arquivo que joguei nos files e jogar o codigo dele nesse
        destino_google_json = os.path.join(projeto_dir, "google-services.json")

        try:
          if os.path.exists(google_services_path):
            shutil.copy(google_services_path, destino_google_json)
            print(f"Arquivo google-services.json copiado para: {destino_google_json}")
          else:
            print(f"Erro: O arquivo {google_services_path} não foi encontrado na pasta do bot!")
        except Exception as e:
          print(f"Erro ao copiar o arquivo google-services.json: {e}")


        app_json_path = os.path.join(projeto_dir, 'app.json')
            

        

        instalar_dependencias(projeto_path)

        app_js_path = os.path.join(projeto_path, "App.js")
        atualizar_app_js(app_js_path, uri)
        

        app_json_path = os.path.join(projeto_path, "app.json")
        atualizar_app_json(app_json_path, bundle_identifier, google_services_path)

        rodar_eas(projeto_path)

           
        return projeto_path
    

    except Exception as e:
        print(f"Erro ao criar ou publicar o projeto: {str(e)}")

        return None
    
    






def atualizar_app_js(app_js_path, uri):
    
    app_js_template = """
import * as Device from "expo-device";
import * as Notifications from "expo-notifications";
import React, { useState, useEffect, useLayoutEffect, useRef } from "react";
import { Platform, SafeAreaView } from "react-native";
import { StatusBar } from "expo-status-bar";
import WebView from "react-native-webview";
import Constants from "expo-constants";

Notifications.setNotificationHandler({
  handleNotification: async () => ({
    shouldShowAlert: true,
    shouldPlaySound: true,
    shouldSetBadge: true,
  }),
});

const App = () => {
  const [expoPushToken, setExpoPushToken] = useState("");
  const [notification, setNotification] = useState(false);
  const notificationListener = useRef();
  const responseListener = useRef();

  useEffect(() => {
    registerForPushNotificationsAsync().then((token) =>
      setExpoPushToken(token)
    );
  }, []);

  useLayoutEffect(() => {
    notificationListener.current =
      Notifications.addNotificationReceivedListener((notification) => {
        setNotification(notification);
      });

    responseListener.current =
      Notifications.addNotificationResponseReceivedListener((response) => {
        console.log(response);
      });

    return () => {
      Notifications.removeNotificationSubscription(
        notificationListener.current
      );
      Notifications.removeNotificationSubscription(responseListener.current);
    };
  }, [expoPushToken]);

  return (
    <>
      <SafeAreaView
        style={{
          flex: 1,
          marginTop: 40,
        }}
      >
        <StatusBar style="dark" translucent />
        <WebView
          source={{
            uri: "{uri}",
          }}
          startInLoadingState={true}
          javaScriptEnabled={true}
          injectedJavaScript={`
            (function(){
              let tk = window.localStorage.getItem('tokenKey');
              if(!tk || (tk && tk !== '${expoPushToken}')){
                window.localStorage.setItem('tokenKey', '${expoPushToken}');
              }
            })();
          `}
        />
      </SafeAreaView>
    </>
  );
};

async function registerForPushNotificationsAsync() {
  let token;

  if (Platform.OS === "android") {
    Notifications.setNotificationChannelAsync("default", {
      name: "default",
      importance: Notifications.AndroidImportance.MAX,
      vibrationPattern: [0, 250, 250, 250],
      lightColor: "#FF231F7C",
    });
  }

  if (Device.isDevice) {
    const { status: existingStatus } =
      await Notifications.getPermissionsAsync();
    let finalStatus = existingStatus;
    if (existingStatus !== "granted") {
      const { status } = await Notifications.requestPermissionsAsync();
      finalStatus = status;
    }
    if (finalStatus !== "granted") {
      console.log("Failed to get push token for push notification!");
      return;
    }
    token = await Notifications.getExpoPushTokenAsync({
      projectId: Constants.expoConfig.extra.eas.projectId,
    });
    console.log(token);
  } else {
    console.log("Must use physical device for Push Notifications");
  }

  return token.data;
}

export default App;
"""

    app_js_content = app_js_template.replace("{uri}", uri)

    with open(app_js_path, "w") as f:
        f.write(app_js_content)
    print(f"App.js atualizado com a URL: {uri}.")

    with open(app_js_path, "w") as f:
        f.write(app_js_content)

def atualizar_app_json(app_json_path, bundle_identifier, google_services_path):
    with open(app_json_path, "r") as f:
        app_json_data = json.load(f)

    app_json_data["expo"]["ios"]["bundleIdentifier"] = bundle_identifier
    app_json_data["expo"]["android"]["package"] = bundle_identifier
    app_json_data["expo"]["ios"]["infoPlist"] = {
        "NSFaceIDUsageDescription": "Permitir a $(PRODUCT_NAME) utilizar o FACE ID para login.",
        "NSCameraUsageDescription": "Este app utiliza a câmera para alterar sua foto de perfil.",
        "NSNotification": "Este app utiliza notificações para te manter atualizado sobre seus dados e novidades."
    }

    # if google_services_path:
    #     app_json_data["expo"]["android"]["googleServicesFile"] = "./google-services.json"
    #     destino_google_json = os.path.join(os.path.dirname(app_json_path), "google-services.json")
    #     try:
    #         shutil.copy(google_services_path, destino_google_json)  
    #         print(f"Arquivo google-services.json copiado para: {destino_google_json}")
    #     except Exception as e:
    #         print(f"Erro ao copiar o arquivo google-services.json: {e}")

    # Adiciona a chave "plugins" no Android
    app_json_data["expo"]["plugins"] = [
        [
            "expo-notifications",
            {
                "icon": "./assets/notification-icon.png",
                "color": "#ffffff"
            }
        ]
    ]
    
    app_json_data["expo"]["extra"] = {
        "eas": {
            "projectId": "82306b80-a69b-45f4-a95a-bca2d52af4c1"
        }
    }

    app_json_data["expo"]["owner"] = "ibsystemlote"

    with open(app_json_path, "w") as f:
        json.dump(app_json_data, f, indent=2)
    
    print(f"app.json atualizado com o identificador: {bundle_identifier}")

def instalar_dependencias(projeto_path):
    subprocess.run([NPX_PATH, "expo", "install", "react-native-webview", "expo-notifications"], cwd=projeto_path, check=True)
    print("Dependências instaladas com sucesso.")

def rodar_eas(projeto_path):
    subprocess.run([NPX_PATH, "expo", "install", "--check"], cwd=projeto_path, check=True)
    print("Deu bom")

@app.route('/start-bot', methods=['POST'])
def start_bot():
    try:
        print(f"request.form: {request.form}")  
        print(f"request.files: {request.files}") 
        if 'image' in request.files and 'projectName' in request.form and 'uri' in request.form and 'bundleIdentifier' in request.form and 'googleServicesPath' in request.files:
            
            image = request.files['image']  
            project_name = request.form['projectName']
            uri = request.form['uri']
            bundle_identifier = request.form['bundleIdentifier']
            google_services_path = request.files['googleServicesPath']  

            image_folder = './images'
            if not os.path.exists(image_folder):
                os.makedirs(image_folder)  
            image_path = os.path.join(image_folder, image.filename)
            image.save(image_path)
            
            # Salvar o arquivo google-services.json
            google_json_path = os.path.join( google_services_path.filename)  # Salve o arquivo JSON na pasta raiz
            google_services_path.save(google_json_path)

            projeto_dir = criar_projeto_expo(project_name, uri, bundle_identifier,   google_json_path)
            
            
            if not projeto_dir:
                return jsonify({"error": "Erro ao criar projeto Expo."}), 500

            # Retornar a resposta de sucesso
            return jsonify({"message": "Bot e projeto inicializados com sucesso!"}), 200
        
        else:
            return jsonify({"error": "Faltando dados ou imagem no formulário."}), 400

    except Exception as e:
        print(f"Erro durante o processo: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)
