<template>
  <div id="todo-list-example" class="container">
    <!-- set progressbar -->
    <vue-progress-bar></vue-progress-bar>
    <div class="row">
      <div class="col-xxl-8 col-lg-10 col-md-12 mx-auto">
        <h1 class="text-center">Consumer Sentiment Prediction</h1>
        <form v-on:submit.prevent="addNewTask">
          <label for="tasknameinput">Classifying sentiment into positive, negative or neutral based on Transformer Model</label>
          <input type="file" ref="file" id="file" v-on:change="handleFileUpload()" class="form-control">
          <button type="submit" class="btn btn-success btn-block mt-3">
            Submit
          </button>
        </form>

        <h2 class="mt-5">Results</h2>
        <!-- <table class="table">
          <thead class="thead-dark">
            <tr>
              <th class="text-left" scope="col">#</th>
              <th class="text-left" scope="col">Text</th>
              <th class="text-left" scope="col">Prediction</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(txt, index) in textClassify" v-bind:key="txt.id" v-bind:title="txt.title" v-bind:tag="txt.tag">
              <td class="text-left">{{++index}}</td>
              <td class="text-left">{{txt.title}}</td>
              <td class="text-left">{{txt.tag}}</td>
            </tr>
          </tbody>
        </table> -->
        <dx-data-grid
        :data-source="results"
        key-expr="ID"
        >
          <DxSearchPanel :visible="true" />
          <DxSorting mode="single"/>
          <DxFilterRow :visible="true" />
          <DxHeaderFilter :visible="true" />
          <DxFilterPanel :visible="true" />
          <DxPaging
            :page-size="10"
            :page-index="1" />
        </dx-data-grid>

      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import { DxDataGrid, DxSorting, DxFilterRow, DxHeaderFilter, DxSearchPanel, DxFilterPanel, DxPaging } from 'devextreme-vue/data-grid'

export default {
  components: {
    DxDataGrid,
    DxSorting,
    DxFilterRow,
    DxHeaderFilter,
    DxSearchPanel,
    DxFilterPanel,
    DxPaging
  },
  data () {
    return {
      // textClassify: [],
      results: [],
      id: '',
      file: null,
      isEdit: false
    }
  },
  mounted () {
    this.getTasks()
  },
  methods: {
    start () {
      this.$Progress.start()
    },
    set (num) {
      this.$Progress.set(num)
    },
    increase (num) {
      this.$Progress.increase(num)
    },
    decrease (num) {
      this.$Progress.decrease(num)
    },
    finish () {
      this.$Progress.finish()
    },
    fail () {
      this.$Progress.fail()
    },
    handleFileUpload () {
      this.file = this.$refs.file.files[0]
    },
    getTasks () {
      axios({ method: 'GET', url: '/api/tasks' }).then(
        result => {
          console.log(result.data)
          // this.textClassify = result.data
          this.results = result.data
        },
        error => {
          console.error(error)
        }
      )
    },
    addNewTask () {
      let formData = new FormData()
      formData.append('file', this.file)

      this.$Progress.start()
      axios.post('/api/task',
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        })
        .then(res => {
          this.taskname = ''
          this.getTasks()
          console.log(res)
          this.$Progress.finish()
        },
        res => {
          this.$Progress.fail()
        })
        .catch(err => {
          console.log(err)
        })
    }
  }
}
</script>
