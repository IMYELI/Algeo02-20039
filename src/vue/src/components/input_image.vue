<template>
    
    <form @submit.prevent="compress" action="">
        <div :class="{'input-wrapper': isInitial||isFailed,'loading_screen': isConverting,'success_page' : isSuccess}">
            <input v-if="isInitial||isFailed" type="file" accept="image/*" class="box-input" @change="fileSelected($event.target.name,$event.target.files)">
            <div v-if="isUploaded" class="image-wrapper">
                <img :src="imageURL"><span v-if="isUploaded" class="material-icons" @click="reset()">update</span>
                <p>{{ namafile }}</p>
            </div>
            <div v-if="isSuccess" class="image-wrapper">
                <img :src="imageURL">
                <p>{{ namafile }}</p>
            </div>
            <div v-if="isSuccess" class="image-wrapper">
                <img :src="imageURL2" v-if="isSuccess">
                <p>Hasil compress</p>
            </div>
            <p v-if="isInitial||isFailed">Klik disini atau drop file anda langsung kesini</p>
            <div :class="{converting : isConverting}">
                <img v-if = "isConverting" src="../assets/pekora_loading.gif" class = "loading_screen">
                <h2 v-if="isConverting">Converting...</h2>
            </div>
            
        </div>
        <div v-if="!isSuccess">
            <div class="input-percentage">
                <p>Persentase compress (berdasarkan rank awal gambar)</p>
                <input :disabled="!(isUploaded ||isInitial)" type="range" min="0" max="100" step="1" v-model = "percentage">
                <div class='persenan'>
                    <input :disabled="!(isUploaded || isInitial)" type="text" v-model = "percentage">
                    <p>%</p>
                </div>
                
            </div>
            <div>
                <button :disabled="!isUploaded">Compress</button> 
            </div>
        </div> 
        <div class="reset_button" v-if="isSuccess">
            <span @click="reset" class="fake_button">Compress Again</span>
            <span @click="download" class="fake_button">Download image</span>
        </div>       
        <div v-if="isSuccess">
            <p class='Time'>Time taken : {{time}} seconds</p>
        </div>
    </form>
</template>

<script>
import axios from 'axios';
const INITIAL_STATUS = 0, UPLOADED_STATUS = 1, SUCCESS_STATUS = 2, FAILED_STATUS = 3, CONVERTING_STATUS = 4;

export default {
    
    data(){
        return{
            fileUpload:[],
            fileGet: [],
            statusUpload:INITIAL_STATUS,
            percentage: 80,
            namafile: '',
            namafile2: '',
            imageURL: '',
            imageURL2: '../assets/test.jpg',
            pathFlask: 'http://localhost:5000/compress',
            base64: '',
            pathJson: 'http://localhost:3000/image',
            test: {},
            time: 0,
            timer: null,
            ext : ''
        }
    },
    computed:{          //Pengecekan status upload gambar
        isInitial(){            
            return this.statusUpload === INITIAL_STATUS;
        },
        isUploaded(){
            return this.statusUpload === UPLOADED_STATUS;
        },
        isSuccess(){
            return this.statusUpload === SUCCESS_STATUS;
        },
        isFailed(){
            return this.statusUpload === FAILED_STATUS;
        },
        isConverting(){
            return this.statusUpload === CONVERTING_STATUS;
        }
    },
    methods:{
        reset(){                   //Digunakan untuk mereset semua state dan server json
            this.fileUpload=[];
            this.statusUpload = INITIAL_STATUS;
            this.time = 0
            fetch(this.pathJson + '/1',{
                method:'DELETE'
            })

        },
        fileSelected(name, listFile){
            this.fileUpload = listFile[0]
            this.namafile = listFile[0].name
            this.statusUpload = UPLOADED_STATUS
            const fileReader = new FileReader()
            fileReader.readAsDataURL(this.fileUpload)
            console.log(this.percentage)                    
            fileReader.addEventListener('load', ()=>{                   
                this.imageURL = fileReader.result
                this.test = {'base64' : this.imageURL, 'percentage' : this.percentage,'namaFile' : this.fileUpload.name} //Membuat data yang akan di send ke json
                fetch('http://localhost:3000/image',{
                    method:'POST', //Upload file ke server json
                    headers:{'Content-Type':'application/json'},
                    body: JSON.stringify(this.test)
                })
            })
            
            

        },
        compress(){             //Fungsi yang dipanggil ketika tombol compress ditekan
            this.statusUpload = CONVERTING_STATUS
            this.startTimer()
            axios.get(this.pathFlask,{ responseType: 'blob'})       //Melakukan request ke server flask
                .then((res)=>{
                    this.stopTimer()
                    this.time = this.time /1000
                    this.fileGet = res.data
                    console.log(this.fileGet)
                    const fileReader = new FileReader()
                    fileReader.readAsDataURL(this.fileGet)
                     fileReader.addEventListener('load', ()=>{
                         this.imageURL2 = fileReader.result
                         console.log(this.imageURL2)
                     })
                    
                    this.statusUpload = SUCCESS_STATUS
                })
                .catch(err=>{console.log(err.message),this.reset()})

        },
        download(){             //Fungsi yang digunakan ketika tombol download ditekan
            var fileURL = window.URL.createObjectURL(this.fileGet)
            var fileLink = document.createElement('a')
            fileLink.href = fileURL
            this.namafile2 = this.namafile.split('.').slice(0,-1).join('.')    //Mengambil namafile
            this.ext = this.namafile.substring(this.namafile.lastIndexOf('.') + 1) //Mengambil extension file
            this.namafile2 = this.namafile2 + '_Compressed.'+this.ext   //Menambahkan compressed di belakang nama file
            fileLink.setAttribute('download',this.namafile2)
            document.body.appendChild(fileLink)
            fileLink.click()
        },
        startTimer(){
            this.time = 0           //Memulai timer
            this.timer = Date.now()
        },
        stopTimer(){
            this.time = Date.now()-this.timer       //memberhentikan timer
            clearInterval(this.timer)
        }
        
        
    },
    mounted(){
        fetch('http://localhost:3000/image')        //Load data pada server json saat pertama kali website dinyalakan
            .then(res=>res.json())
            .then(data=>this.test = data)
            .catch(err=>console.log(err.message))
        this.reset()
    },
    

}
</script>

<style>
    body {
        background-image: url('../assets/Carrot_BG.png');
    }
    form{
        width: 60%;
        margin: 20px auto; 
        min-height: 400px;
        min-width: 800px;
        background: white;
        text-align: justify;
        padding: 40px;
        border-radius: 20px;
    }
    
    .input-wrapper{
        outline: 10px dashed  yellow;
        min-height: 200px;
        background: #ffd278;
        opacity: 50%;
        color: black;
    }
    .input-wrapper:hover{
        background: lightgoldenrodyellow;
    }
    .box-input{
        opacity: 0;
        width: 59.5%;
        height: 200px;
        position: absolute;
        cursor: pointer;
        background:black;
    }
    .input-wrapper p{
        padding-top: 80px;
        text-align: center;
        font-weight: bold;
        font-size: 2em;
    }
    .input-percentage{
        display: block;
        padding-top: 20px;
    }
    .input-percentage p{
        padding-right: 10px;
    }
    .persenan{
        display: flex;
    }
    .persenan input{
        width: 4%;
        text-align: right;
        margin-right: 5px;
    }
    .input-percentage input {
        padding: 1px;
        border: 1;

        height: 20px;
        display: block;
        margin-top: 10px;
    }
    form button{
        background: #e7e7e7;
        border-radius: 8px;
        border: 0px;
        height: 30px;
        cursor: pointer;
    }
    .fake_button{
        background: #e7e7e7;
        border-radius: 8px;
        border: 0px;
        padding: 10px;
        cursor: pointer;
        margin-top: 10px;
        display: block;
    }
    .image-wrapper{
        max-height: 200px;
        margin: 5px auto;
        text-align: center;
    }
    .image-wrapper img{
        max-height: 200px;
        max-width: 450px;
    }
    .loading_screen {
        background: lightblue;
        margin: 0 auto;
        widows: 50%;
    }
    .success_page{
        display: flex;
    }
    .reset_button{
        margin: 20px auto;
        width: 20%;
        text-align: center;
    }
    .Time{
        color:red;
    }
    .converting{
        display: flex;
        width: 50%;
        margin: auto;
    }
</style>




     