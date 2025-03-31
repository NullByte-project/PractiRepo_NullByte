import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { EncabezadoComponent } from "./publico/pagina-maestra/encabezado/encabezado.component";
import { InicioComponent } from "./publico/inicio/inicio.component";
import { PiePaginaComponent } from "./publico/pagina-maestra/pie-pagina/pie-pagina.component";

@Component({
  selector: 'app-root',
  imports: [RouterOutlet, EncabezadoComponent, InicioComponent, PiePaginaComponent],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent {
  title = 'Frontend';
}
