import {Component} from '@angular/core';
import {HttpClient} from "@angular/common/http";

@Component({
  selector: 'app-octgnify',
  templateUrl: './octgnify.component.html',
  styleUrls: ['./octgnify.component.css'],
})
export class OctgnifyComponent {

  fileName = '';
  inputDeck = '';

  constructor(private http: HttpClient) {
  }

  onFileSelected(event: Event): void {

    const element = event.currentTarget as HTMLInputElement;
    let fileList: FileList | null = element.files;

    const file: File | null | undefined = fileList?.item(0);

    if (file) {

      this.fileName = file.name;
      file.text().then(text => this.inputDeck = text);
    }
  }

  convert(): void {
    console.log("convert")
    let payload = {
      'filename': this.fileName,
      'deck': this.inputDeck
    }
    const upload = this.http.post("/api/convert", payload, {responseType: 'blob' as 'text'}).subscribe(
      (response: any) => {
        let dataType = response.type;
        let binaryData = [];
        binaryData.push(response);
        let downloadLink = document.createElement('a');
        downloadLink.href = URL.createObjectURL(new Blob(binaryData, {type: dataType}));
        if (this.fileName)
          downloadLink.setAttribute('download', this.fileName.replace(this.fileName.split('.')[1], 'o8d'));
        document.body.appendChild(downloadLink);
        downloadLink.click();

      }
    );
  }

}
