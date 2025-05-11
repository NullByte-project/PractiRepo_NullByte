import { Component } from '@angular/core';
import { UserModel } from 'src/app/model/user.model';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.css']
})
export class RegisterComponent {
  user: UserModel = {
    name: '',
    email: '',
    password: ''
  };


}
