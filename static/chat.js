document.addEventListener('DOMContentLoaded', () => {
    const form = document.querySelector('form');
    const chat = document.getElementById('chat');

    form.addEventListener('submit', async (event) => {
      event.preventDefault();
      
      const questionInput = document.getElementById('user_question');
      const userQuestion = questionInput.value.trim();

      if (!userQuestion) {
        return;
      }

      addMessageToChat('user', userQuestion);

      // Send the user's question to the server
      const response = await fetch('/ask', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ user_question: userQuestion }),
      });

      const data = await response.json();
      const chatbotResponse = data.response;

      addMessageToChat('chatbot', chatbotResponse);

      // Clear the input field and scroll to the bottom of the chat
      questionInput.value = '';
      chat.scrollTop = chat.scrollHeight;
    });

    function addMessageToChat(sender, text) {
      const messageWrapper = document.createElement('div');
      messageWrapper.classList.add('mb-2');

      const messageFlex = document.createElement('div');
      messageFlex.classList.add('flex');
      messageFlex.classList.add(sender === 'user' ? 'justify-end' : 'justify-start');
      
      const messageBox = document.createElement('div');
      messageBox.classList.add(sender === 'user' ? 'bg-purple-600' : 'bg-gray-300');
      messageBox.classList.add(sender === 'user' ? 'text-white' : 'text-gray-700');
      messageBox.classList.add('max-w-xs', 'mx-2', 'my-1', 'p-3', 'rounded-lg');
      
      const messageText = document.createElement('p');
      messageText.textContent = text;

      messageBox.appendChild(messageText);
      messageFlex.appendChild(messageBox);
      messageWrapper.appendChild(messageFlex);
      chat.appendChild(messageWrapper);
    }
});