<template>
  <div id="todo-list-example" class="container">
    <!-- set progressbar -->
    <vue-progress-bar></vue-progress-bar>
    <div class="row">
      <div class="col-xxl-8 col-lg-10 col-md-12 mx-auto">
        <h1 class="text-center">Consumer Sentiment Prediction</h1>
        <form v-on:submit.prevent="addNewTask" class="vld-parent" ref="formContainer">
          <label for="tasknameinput">Classifying sentiment into positive, negative or neutral based on Transformer Model</label>
          <input type="file" ref="file" id="file" v-on:change="handleFileUpload()" class="form-control" accept=".txt, .csv">
          <button type="submit" class="btn btn-success btn-block mt-3" v-bind:disabled="disableBtn">
            Submit
          </button>
        </form>
        <!-- <input type="file" ref="file" id="file" v-on:change="handleFileUpload()" class="form-control" accept=".txt, .csv"> -->

      </div>
    </div>
  </div>
</template>

<script>
export default {
  data () {
    return {
      file: null,
      isEdit: false
    }
  },
  methods: {
    handleFileUpload () {
      this.file = this.$refs.file.files[0]
      let selectedFile = this.$refs.file.files[0]
      var idxDot = selectedFile.name.lastIndexOf('.') + 1
      var extFile = selectedFile.name.substr(idxDot, selectedFile.name.length).toLowerCase()
      if (extFile === 'txt' || extFile === 'csv') {
        console.log(extFile)
        this.file = this.$refs.file.files[0]
      } else {
        this.$refs.file.files[0] = null
        alert('Only txt and csv files are allowed!')
      }
      this.$store.commit('updateFile', this.file)
    },
    addNewTask () {
      this.$router.push('/result')
    }
  },
  computed: {
    disableBtn () {
      return this.file === null
    }
  }
}
</script>
<style scoped>
</style>
