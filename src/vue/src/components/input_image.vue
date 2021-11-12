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
            <img v-if = "isConverting" src="../assets/pekora_loading.gif" class = "loading_screen">
        </div>
        <div v-if="!isSuccess">
            <div class="input-percentage">
                <p>Persentase compress</p>
                <input type="text" v-model = "percentage">
                <p>%</p>
            </div>
            <div>
                <button :disabled="!isUploaded">Compress</button> 
            </div>
        </div> 
        <div class="reset_button" v-if="isSuccess">
            <span @click="reset" class="fake_button">Compress Again</span>
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
            errorUpload: null,
            statusUpload:INITIAL_STATUS,
            percentage: 80,
            namafile: '',
            imageURL: '',
            imageURL2: '../assets/test.jpg',
            pathFlask: 'http://localhost:5000/ping',
            base64: '',
            pathJson: 'http://localhost:3000/image',
            test: {}
        }
    },
    computed:{
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
        reset(){
            this.fileUpload=[];
            this.statusUpload = INITIAL_STATUS;
            this.errorUpload = null;
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
            console.log(this.fileUpload)
            fileReader.addEventListener('load', ()=>{
                this.imageURL = fileReader.result
                this.test = {'base64' : this.imageURL, 'percentage' : this.percentage}
                console.log(this.imageURL)
                fetch('http://localhost:3000/image',{
                    method:'POST',
                    headers:{'Content-Type':'application/json'},
                    body: JSON.stringify(this.test)
                })
            })
            
            
            console.log(this.test.length)

        },
        compress(){
            this.statusUpload = CONVERTING_STATUS
            axios.get(this.pathFlask,{ responseType: 'blob'})
                .then((res)=>{
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
        getImg(){
            axios.get(pathPy)
                .then((res)=>{
                    this.imageURL2 = res.data
                })
                .catch((error)=>console.log(error.message))
        }
        
        
    },
    mounted(){
        fetch('http://localhost:3000/image')
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
        display: flex;
        padding-top: 20px;
        text-align: center;
    }
    .input-percentage p{
        padding-right: 10px;
    }
    .input-percentage input {
        padding: 1px;
        border: 1;
        width: 2.5%;
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
    }
    .image-wrapper{
        max-height: 200px;
        margin: 5px auto;
        text-align: center;
    }
    .image-wrapper img{
        max-height: 200px;
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
        width: 50%;
        text-align: center;
    }
</style>




     