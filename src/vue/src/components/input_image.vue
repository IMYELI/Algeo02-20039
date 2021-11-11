<template>
    
    <form @submit.prevent="compress">
        <div :class="{'input-wrapper': isInitial}">
            <input v-if="isInitial" type="file" accept="image/*" class="box-input" @change="fileSelected($event.target.name,$event.target.files)">
            <div v-if="isUploaded" class="image-wrapper">
                <img :src="imageURL"><span v-if="isUploaded" class="material-icons" @click="reset()">update</span>
                <p>{{ namafile }}</p>
                <img :src="imageURL2">
            </div>
            <p v-if="isInitial">Klik disini atau drop file anda langsung kesini</p>
        </div>
        <div class="input-percentage">
            <p>Persentase compress</p>
            <input type="text" v-model = "percentage">
            <p>%</p>
        </div>
        <div>
            <button>Compress</button> 
        </div>
        
        
    </form>
</template>

<script>
import axios from 'axios';
const INITIAL_STATUS = 0, UPLOADED_STATUS = 1, SUCCESS_STATUS = 2, FAILED_STATUS = 3, CONVERTING_STATUS = 4;
function getBase64(img){
    var canvas = document.createElement("canvas");
    canvas.width = img.width;
    canvas.height = img.height;
    var ctx = canvas.getContext("2d");
    ctx.drawImage(img, 0, 0);
    var dataURL = canvas.toDataURL("image/png");
    return dataURL.replace(/^data:image\/(png|jpg);base64,/, "");
}
export default {
    
    data(){
        return{
            fileUpload:[],
            errorUpload: null,
            statusUpload:INITIAL_STATUS,
            percentage: 80,
            namafile: '',
            imageURL: '',
            imageURL2: '',
            pathJson: 'http://localhost:5000/ping',
            base64: ''
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
        },
        fileSelected(name, listFile){
            this.fileUpload = listFile[0]
            this.namafile = listFile[0].name
            this.statusUpload = UPLOADED_STATUS
            const fileReader = new FileReader()
            fileReader.addEventListener('load', ()=>{
                this.imageURL = fileReader.result
            })
            fileReader.readAsDataURL(this.fileUpload)
            console.log(listFile[0])
            console.log(this.base64)

        },
        compress(){
            this.statusUpload = CONVERTING_STATUS
            //const img = new Blob(this.fileUpload,{type : 'image'})
            axios.post(this.pathJson,this.fileUpload,this.percentage)
                .then(()=>{this.getImg()})
                .catch(err=>{console.log(err.message),this.reset()})
        },
        getImg(){
            axios.get(pathPy)
                .then((res)=>{
                    this.imageURL2 = res
                })
                .catch((error)=>console.log(error.message))
        }
        
        
    },
    mounted(){
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
    .image-wrapper{
        max-height: 200px;
        margin: 5px auto;
        text-align: center;
    }
    .image-wrapper img{
        max-height: 200px;
    }
</style>




     