<template>
  <img src="../assets/Pekompressor_logo_resized2.png" class="Title">
  <input_image />
</template>

<script>
import input_image from "../components/input_image.vue"
export default {
  name: 'App',
  components: {input_image}
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  margin-top: 60px;
}
.Title{
        margin: 10px auto;
        display: block;
        max-width: 50%;
    }
</style>
