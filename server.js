// Imports
import http from 'http';
import * as fs from 'fs';

// Charger index.html
const indexHtml = fs.readFileSync('./index.html'); 

// Serveur HTTP
const server = http.createServer((req, res) => {

  // Envoyer index.html
  res.statusCode = 200;
  res.setHeader('Content-Type', 'text/html');
  res.end(indexHtml);

});

// Choisir le port
const port = 8080;

// Lancer le serveur
server.listen(port, () => {
  console.log(`Server running on  localhost:${port}`);
});