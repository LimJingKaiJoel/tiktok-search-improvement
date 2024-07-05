// server.js
const express = require('express');
const axios = require('axios');
const dotenv = require('dotenv');

dotenv.config();

const app = express();
const port = 3000;

app.use(express.json());

app.post('/api/openai', async (req, res) => {
  const { query } = req.body;
  const prompt = `In 1 sentence, answer the following concisely: ${query}`;

  try {
    const response = await axios.post(
      'https://api.openai.com/v1/chat/completions',
      {
        model: 'gpt-3.5-turbo-0125',
        messages: [{ role: 'user', content: prompt }],
      },
      {
        headers: {
          'Authorization': `Bearer ${process.env.OPENAI_API_KEY}`,
          'Content-Type': 'application/json',
        },
      }
    );
    res.json({ recommendation: response.data.choices[0].message.content });
  } catch (error) {
    console.error('Error fetching AI recommendation:', error);
    res.status(500).json({ error: 'Error fetching AI recommendation' });
  }
});

app.listen(port, () => {
  console.log(`Server listening at http://localhost:${port}`);
});