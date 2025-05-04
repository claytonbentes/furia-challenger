const messagesContainer = document.getElementById('messages');
const userInput = document.getElementById('userInput');
const sendButton = document.getElementById('sendButton');

// Função para adicionar mensagens ao chat
function addMessage(text, isUser = false) {
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message');
    messageDiv.classList.add(isUser ? 'user-message' : 'bot-message');
    messageDiv.textContent = text;
    messagesContainer.appendChild(messageDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

// Função para adicionar dados formatados ao chat
function addData(data) {
    if (!data || !Array.isArray(data)) return;

    data.forEach((item, index) => {
        const dataDiv = document.createElement('div');
        dataDiv.classList.add('message', 'bot-message');

        let formattedMessage = `${index + 1}. `;

        // Partidas passadas
        if ("adversario" in item && "resultado" in item) {
            let dataFormatada = formatarData(item.data);
            formattedMessage += `vs ${item.adversario} - ${dataFormatada} - ${item.resultado} (${item.campeonato || ''})`;
        }
        // Próximas partidas
        else if ("adversario" in item) {
            let dataFormatada = formatarData(item.data);
            formattedMessage += `vs ${item.adversario} - ${dataFormatada} (${item.campeonato || ''})`;
        }
        // Notícias
        else if ("titulo" in item) {
            let dataFormatada = formatarData(item.data);
            formattedMessage += `${item.titulo} (${dataFormatada})`;
            if ("descricao" in item) {
                let descricao = item.descricao;
                if (descricao.length > 200) {
                    descricao = descricao.substring(0, 197) + "...";
                }
                formattedMessage += `\n${descricao}`;
            }
        }
        // Campeonatos
        else if ("nome" in item && "status" in item) {
            formattedMessage += `${item.nome} - Status: ${item.status}`;
            if ("data_inicio" in item && "data_fim" in item) {
                let dataInicioFormatada = formatarData(item.data_inicio);
                let dataFimFormatada = formatarData(item.data_fim);
                formattedMessage += `\nDe ${dataInicioFormatada} até ${dataFimFormatada}`;
            }
        }
        // Jogadores
        else if ("nome" in item || "nickname" in item) {
            let playerInfo = [];
        
            // Adicionar nome
            if (item.nome) playerInfo.push(item.nome);
        
            // Adicionar nickname entre aspas simples
            if (item.nickname) playerInfo.push(`'${item.nickname}'`);
        
            // Adicionar sobrenome, se existir
            if (item.sobrenome) playerInfo.push(item.sobrenome);
        
            // Adicionar função
            if (item.funcao) playerInfo.push(`- ${item.funcao}`);
        
            // Formatar mensagem final
            formattedMessage += playerInfo.join(' ');
        
            // Informações adicionais (se houver)
            for (const [key, value] of Object.entries(item)) {
                if (!["nome", "nickname", "funcao", "id", "sobrenome"].includes(key) && value) {
                    const formattedKey = key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
                    formattedMessage += `\n${formattedKey}: ${value}`;
                }
            }
        }
        // Formato genérico
        else {
            formattedMessage += JSON.stringify(item, null, 2);
        }

        dataDiv.textContent = formattedMessage;
        messagesContainer.appendChild(dataDiv);
    });

    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

// Função para formatar datas
function formatarData(dataOriginal) {
    if (!dataOriginal) return '';
    try {
        const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
        if (dataOriginal.includes(',') && months.some(month => dataOriginal.includes(month))) {
            const parsedDate = new Date(dataOriginal);
            return parsedDate.toLocaleDateString('pt-BR');
        } else if (dataOriginal.includes('T')) {
            const dataObj = new Date(dataOriginal);
            return dataObj.toLocaleDateString('pt-BR');
        } else if (dataOriginal.includes('-') && dataOriginal.length >= 10) {
            const dataObj = new Date(dataOriginal);
            return dataObj.toLocaleDateString('pt-BR');
        }
    } catch (error) {
        console.error('Erro ao formatar data:', error);
    }
    return dataOriginal;
}

// Função para enviar a consulta para o backend
async function sendQuery() {
    const query = userInput.value.trim();
    if (!query) return;

    // Adicionar mensagem do usuário
    addMessage(query, true);
    userInput.value = '';

    // Enviar consulta para o backend
    try {
        const response = await fetch('https://furia-9hdbrtqug-claytons-projects-15b8f849.vercel.app/query', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ query })
        });

        if (response.ok) {
            const data = await response.json();
            addMessage(data.message || 'Resposta não encontrada.');
            if (data.data) {
                addData(data.data);
            }
        } else {
            addMessage('Erro ao processar a consulta.');
        }
    } catch (error) {
        console.error('Erro:', error);
        addMessage('Erro ao conectar ao servidor.');
    }
}

sendButton.addEventListener('click', sendQuery);

userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        sendQuery();
    }
});