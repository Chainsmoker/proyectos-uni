import { ChatGPTAPI } from 'chatgpt'

import whatsappweb from 'whatsapp-web.js';
const { Client, LocalAuth } = whatsappweb;
import qrcode from 'qrcode-terminal';

const chatgpt = new ChatGPTAPI({
    apiKey: ''
})

const client = new Client({
    authStrategy: new LocalAuth(),
});

client.on('qr', qr => {
    qrcode.generate(qr, {small: true});
});

client.on('ready', () => {
    console.log('Listo para usar');
});

client.on('message', async message => {
	if(message.body.length < 4) {
        client.sendMessage(message.from, "Por favor, Ingresa una entrada valida");
	} else {
        console.log("Nueva consulta: ", message.body)
        const res = await chatgpt.sendMessage(message.body)
		client.sendMessage(message.from, res.text);
    }
});
 
client.initialize();
