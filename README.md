Chatbot for RU meals:

this applications uses bs4 lib for web scrapping on: https://prefeitura.unicamp.br/cardapio/ , in order to gather info about todays university's restaurant menu.

How it works:

- First the aplication goes to the previous link and collects, using the bs4 + request lib, the html formated info about weekly meals;

- After processing each information into readable text strings, the program saves the week's lunch and dinner in a .json file that will be stored and rewritten each week;

- Finally, the program converts the content of the JSON file into a dictionary, sends a message on WhatsApp with the current meal features and, based on the feature, it writes a personalized message.
