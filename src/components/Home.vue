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

        <!-- Data Grid showing data in table form -->
        <dx-data-grid
        :data-source="results"
        key-expr="ID"
        @exporting="onExporting"
        :show-column-lines="showColumnLines"
        :show-row-lines="showRowLines"
        :show-borders="showBorders"
        class="mb-0"
        >
          <DxSearchPanel :visible="true" />
          <DxSorting mode="single"/>
          <DxFilterRow :visible="true" />
          <DxHeaderFilter :visible="true" />
          <DxFilterPanel :visible="true" />
          <DxExport
            :enabled="true"
            :allow-export-selected-data="true"
          />
          <DxPaging
            :page-size="10"
            :page-index="0" />
          <DxPager
            :show-page-size-selector="true"
            :allowed-page-sizes="pageSizes"
            :show-info="true"
          />
        </dx-data-grid>

        <div class="options mt-0">
          <div class="caption">Options</div>
          <div class="option">
            <DxCheckBox
              :value.sync="showColumnLines"
              text="Show Column Lines"
            />
          </div>
          <div class="option">
            <DxCheckBox
              :value.sync="showRowLines"
              text="Show Row Lines"
            />
          </div>
          <div class="option">
            <DxCheckBox
              :value.sync="showBorders"
              text="Show Borders"
            />
          </div>
        </div>

        <!-- Pie Chart showing class distributions -->
        <center class="mt-5">
          <DxPieChart
          :data-source="predictionsStats"
          id="chart"
          title="Sentiment Predictions Contribution"
          palette="Bright"
          @point-click="pointClickHandler($event)"
          @legend-click="legendClickHandler($event)"
          >
            <DxSeries
              argument-field="label"
              value-field="count"
            >
              <DxLabel :visible="true">
                <DxConnector
                  :visible="true"
                  :width="1"
                />
              </DxLabel>
            </DxSeries>
            <DxSize :width="500"/>
            <DxExport :enabled="true"/>
          </DxPieChart>
        </center>

      </div>
    </div>

    <!-- <div id="app">
      <circle9></circle9>
    </div> -->

  </div>
</template>

<script>
import Vue from 'vue'
import axios from 'axios'
import { DxDataGrid, DxSorting, DxFilterRow, DxHeaderFilter, DxSearchPanel, DxFilterPanel, DxPager, DxPaging, DxExport } from 'devextreme-vue/data-grid'
import DxPieChart, { DxSize, DxSeries, DxLabel, DxConnector } from 'devextreme-vue/pie-chart'
import { exportDataGrid } from 'devextreme/excel_exporter'
import { DxCheckBox } from 'devextreme-vue/check-box'
import ExcelJS from 'exceljs'
import saveAs from 'file-saver'
import Loading from 'vue-loading-overlay'
import 'vue-loading-overlay/dist/vue-loading.css'
Vue.use(Loading)
// import {Circle9} from 'vue-loading-spinner'

export default {
  components: {
    DxDataGrid,
    DxSorting,
    DxFilterRow,
    DxHeaderFilter,
    DxSearchPanel,
    DxFilterPanel,
    DxPager,
    DxPaging,
    DxPieChart,
    DxSize,
    DxSeries,
    DxLabel,
    DxConnector,
    DxExport,
    DxCheckBox
    // Circle9
  },
  data () {
    return {
      // textClassify: [],
      results: [],
      id: '',
      file: null,
      isEdit: false,
      predictionsStats: [],
      showColumnLines: false,
      showRowLines: true,
      showBorders: true,
      pageSizes: [5, 10, 20, 40, 100],
      fullPage: true
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
      // this.file = this.$refs.file.files[0]
      let selectedFile = this.$refs.file.files[0]
      var idxDot = selectedFile.name.lastIndexOf('.') + 1
      var extFile = selectedFile.name.substr(idxDot, selectedFile.name.length).toLowerCase()
      if (extFile === 'txt' || extFile === 'csv') {
        console.log(extFile)
        this.file = this.$refs.file.files[0]
      } else {
        alert('Only txt and csv files are allowed!')
      }
    },
    getTasks (result) {
      this.results = result.data
      let pos = 0
      let neg = 0
      let neut = 0
      for (let index = 0; index < result.data.length; index++) {
        // this.predictions.push({tag: result.data[index].tag})
        if (result.data[index].tag === 'positive') {
          pos++
        } else if (result.data[index].tag === 'negative') {
          neg++
        } else if (result.data[index].tag === 'neutral') {
          neut++
        }
      }
      this.predictionsStats = [{label: 'positive', count: pos}, {label: 'negative', count: neg}, {label: 'neutral', count: neut}]
      this.file = null
    },
    addNewTask () {
      let loader = this.$loading.show({
        // Optional parameters
        container: this.fullPage ? null : this.$refs.formContainer,
        canCancel: false,
        onCancel: this.onCancel,
        isFullPage: true,
        color: '#00AB00',
        backgroundColor: '#fffefe'
      })
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
          this.getTasks(res)
          console.log(res.data)
          this.$Progress.finish()
          loader.hide()
        },
        res => {
          this.$Progress.fail()
        })
        .catch(err => {
          console.log(err)
          loader.hide()
        })
    },
    onCancel () {
      console.log('User cancelled the loader.')
    },
    pointClickHandler (e) {
      this.toggleVisibility(e.target)
    },
    legendClickHandler (e) {
      let arg = e.target
      let item = e.component.getAllSeries()[0].getPointsByArg(arg)[0]

      this.toggleVisibility(item)
    },
    toggleVisibility (item) {
      item.isVisible() ? item.hide() : item.show()
    },
    onExporting (e) {
      const workbook = new ExcelJS.Workbook()
      const worksheet = workbook.addWorksheet('Employees')

      exportDataGrid({
        component: e.component,
        worksheet: worksheet,
        autoFilterEnabled: true
      }).then(function () {
        // https://github.com/exceljs/exceljs#writing-xlsx
        workbook.xlsx.writeBuffer().then(function (buffer) {
          saveAs(new Blob([buffer], { type: 'application/octet-stream' }), 'DataGrid.xlsx')
        })
      })
      e.cancel = true
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
#pie {
    height: 440px;
}

#pie * {
    margin: 0 auto;
}
.center-chart {
  margin-left: auto;
  margin-right: auto;
}
.options {
  padding: 20px;
  background-color: rgba(191, 191, 191, 0.15);
  margin-top: 20px;
}

.caption {
  font-size: 18px;
  font-weight: 500;
}

.option {
  width: 24%;
  display: inline-block;
  margin-top: 10px;
}
</style>
