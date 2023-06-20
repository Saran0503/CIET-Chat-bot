import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-chatbot',
  templateUrl: './chatbot.component.html',
  styleUrls: ['./chatbot.component.css']
})
export class ChatbotComponent {
  messages: { text: string, sender: string }[] = [];
  inputText = '';

  constructor(private http: HttpClient) { }

  sendMessage() {
    if (this.inputText.trim()) {
      this.messages.push({ text: this.inputText, sender: 'user' });
      this.http.post<any>('http://localhost:5000/chatbot', { inputText: this.inputText })
      .subscribe(response => {
        this.messages.push({ text: response.bot_response, sender: 'chatbot' });
      }, error => {
        console.error('Error sending message:', error);
      });
      console.log('Message sent:', this.inputText);
      this.inputText = '';
    }
  }
  
}
