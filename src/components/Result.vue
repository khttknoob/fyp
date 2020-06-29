<template>
  <div id="sentiman" class="container">
    <!-- set progressbar -->
    <vue-progress-bar></vue-progress-bar>
    <b-button squared variant="primary" class="fixed pl-2 pr-2" @click="$router.push('/')">
      <b-icon icon="arrow-left-circle-fill" aria-hidden="true"></b-icon> Home
    </b-button>
    <div class="row">
      <div class="col-xxl-8 col-lg-10 col-md-12 mx-auto">
        <h1 class="text-center">Consumer Sentiment Prediction</h1>
        <form v-on:submit.prevent="addNewTask" class="vld-parent" ref="formContainer">
          <label for="tasknameinput">Classifying sentiment into positive, negative or neutral based on Transformer Model</label>
          <input type="file" ref="file" id="file" v-on:change="storeFile()" class="form-control" accept=".txt, .csv">
          <button type="submit" class="btn btn-success btn-block mt-3" v-bind:disabled="disableBtn">
            Submit
          </button>
        </form>
      </div>
    </div>

    <!-- If Data, sHow these -->
    <div v-if="results.length > 0">
      <div class="row">
        <div class="col-xxl-8 col-lg-10 col-md-12 mx-auto">
          <h2 class="mt-5">Results</h2>
          <!-- Data Grid showing data in table form -->
          <div v-if="results.length > 0">
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
          </div>

          <div v-else>
            <b-card bg-variant="secondary" text-variant="white" title="No Data">
              <b-card-text>
                We didn't find any data to display <b-icon icon="emoji-frown" aria-hidden="true"></b-icon>
              </b-card-text>
            </b-card>
          </div>
        </div>
      </div>

          <!-- Pie Chart showing class distributions -->
      <div class="row">
        <div class="col-xxl-8 col-lg-10 col-md-12 mx-auto">
          <center class="mt-5">
            <div v-if="predictionsStats.length > 0">
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
            </div>

            <div v-else class="mt-0">
              <h2>Sentiment Predictions Contribution</h2>
              <b-card bg-variant="secondary" text-variant="white" title="No Data">
                <b-card-text>
                  We didn't find any data to display <b-icon icon="emoji-frown" aria-hidden="true"></b-icon>
                </b-card-text>
              </b-card>
            </div>
          </center>

        </div>
      </div>

      <!-- Positive Frequencies -->
      <div class="row">
        <div class="col-xxl-8 col-lg-8 col-md-6 col-md-12 mx-auto">
          <center>
            <h2 class="mt-5 mb-0">Positive Tweets Words Cloud</h2>
            <div v-if="positiveFrequencies.length > 0">
              <vue-word-cloud
                style="
                height: 480px;
                width: 640px;
                "
                :words="positiveFrequencies"
                :color="([, weight]) => weight > 10 ? 'DeepPink' : weight > 5 ? 'RoyalBlue' : 'Indigo'"
                font-family="Roboto"
              />
            </div>
            <div v-else class="mt-0">
              <b-card bg-variant="secondary" text-variant="white" title="No Data">
                <b-card-text>
                  We didn't find any data to display <b-icon icon="emoji-frown" aria-hidden="true"></b-icon>
                </b-card-text>
              </b-card>
            </div>
          </center>
        </div>

        <div class="col-xxl-4 col-lg-4 col-md-6 col-md-12 mx-auto">
          <!-- <center> -->
            <h3 class="mt-5 mb-0">Positive Tweets Frequencies</h3>
            <div v-if="posFreqDictList.length > 0">
              <b-table
                id="my-table"
                :items="posFreqDictList"
                :per-page="perPage"
                :current-page="posCurrentPage"
                :fields="fields"
                head-variant="dark"
                small
              ></b-table>
              <b-pagination
                v-model="posCurrentPage"
                :total-rows="posRows"
                :per-page="perPage"
                first-text="First"
                prev-text="Prev"
                next-text="Next"
                last-text="Last"
              ></b-pagination>
            </div>
            <div v-else class="mt-0">
              <b-card bg-variant="secondary" text-variant="white" title="No Data">
                <b-card-text>
                  We didn't find any data to display <b-icon icon="emoji-frown" aria-hidden="true"></b-icon>
                </b-card-text>
              </b-card>
            </div>
          <!-- </center> -->
        </div>
      </div>

      <!-- Negative Frequencies -->
      <div class="row">
        <div class="col-xxl-8 col-lg-8 col-md-6 col-md-12 mx-auto">
          <center>
            <h2 class="mt-5 mb-0">Negative Tweets Words Cloud</h2>
            <div v-if="negativeFrequencies.length > 0">
              <vue-word-cloud
                style="
                height: 480px;
                width: 640px;
                "
                :words="negativeFrequencies"
                :color="([, weight]) => weight > 10 ? 'DeepPink' : weight > 5 ? 'RoyalBlue' : 'Indigo'"
                font-family="Roboto"
              />
            </div>
            <div v-else class="mt-0">
              <b-card bg-variant="secondary" text-variant="white" title="No Data">
                <b-card-text>
                  We didn't find any data to display <b-icon icon="emoji-frown" aria-hidden="true"></b-icon>
                </b-card-text>
              </b-card>
            </div>
          </center>
        </div>

        <div class="col-xxl-4 col-lg-4 col-md-6 col-md-12 mx-auto">
          <!-- <center> -->
            <h3 class="mt-5 mb-0">Negative Tweets Frequencies</h3>
            <div v-if="negFreqDictList.length > 0">
              <b-table
                id="my-table"
                :items="negFreqDictList"
                :per-page="perPage"
                :current-page="negCurrentPage"
                :fields="fields"
                head-variant="dark"
                small
              ></b-table>
              <b-pagination
                v-model="negCurrentPage"
                :total-rows="negRows"
                :per-page="perPage"
                first-text="First"
                prev-text="Prev"
                next-text="Next"
                last-text="Last"
              ></b-pagination>
            </div>
            <div v-else class="mt-0">
              <b-card bg-variant="secondary" text-variant="white" title="No Data">
                <b-card-text>
                  We didn't find any data to display <b-icon icon="emoji-frown" aria-hidden="true"></b-icon>
                </b-card-text>
              </b-card>
            </div>
          <!-- </center> -->
        </div>
      </div>

      <!-- Neutral Frequencies -->
      <div class="row">
        <div class="col-xxl-8 col-lg-8 col-md-6 col-md-12 mx-auto">
          <center>
            <h2 class="mt-5 mb-0">Neutral Tweets Words Cloud</h2>
            <div v-if="neutralFrequencies.length > 0">
              <vue-word-cloud
                style="
                height: 480px;
                width: 640px;
                "
                :words="neutralFrequencies"
                :color="([, weight]) => weight > 10 ? 'DeepPink' : weight > 5 ? 'RoyalBlue' : 'Indigo'"
                font-family="Roboto"
              />
            </div>
            <div v-else class="mt-0 mb-5">
              <b-card bg-variant="secondary" text-variant="white" title="No Data">
                <b-card-text>
                  We didn't find any data to display <b-icon icon="emoji-frown" aria-hidden="true"></b-icon>
                </b-card-text>
              </b-card>
            </div>
          </center>
        </div>

        <div class="col-xxl-4 col-lg-4 col-md-6 col-md-12 mx-auto">
          <!-- <center> -->
            <h3 class="mt-5 mb-0">Neutral Tweets Frequencies</h3>
            <div v-if="neutFreqDictList.length > 0">
              <b-table
                id="my-table"
                :items="neutFreqDictList"
                :per-page="perPage"
                :current-page="neutCurrentPage"
                :fields="fields"
                head-variant="dark"
                small
              ></b-table>
              <b-pagination
                v-model="neutCurrentPage"
                :total-rows="neutRows"
                :per-page="perPage"
                first-text="First"
                prev-text="Prev"
                next-text="Next"
                last-text="Last"
              ></b-pagination>
            </div>
            <div v-else class="mt-2 mb-5">
              <b-card bg-variant="secondary" text-variant="white" title="No Data">
                <b-card-text>
                  We didn't find any data to display <b-icon icon="emoji-frown" aria-hidden="true"></b-icon>
                </b-card-text>
              </b-card>
            </div>
          <!-- </center> -->
        </div>
      </div>
    </div>

    <!-- if no data, show 'no data' Message -->
    <div v-else class="mt-5">
      <b-card bg-variant="secondary" text-variant="white" title="No Data">
        <b-card-text>
          We didn't find any data to display <b-icon icon="emoji-frown" aria-hidden="true"></b-icon>
        </b-card-text>
      </b-card>
    </div>
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
import VueWordCloud from 'vuewordcloud'
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
    DxCheckBox,
    [VueWordCloud.name]: VueWordCloud
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
      fullPage: true,
      positiveFrequencies: [],
      negativeFrequencies: [],
      neutralFrequencies: [],
      posFreqDictList: [],
      negFreqDictList: [],
      neutFreqDictList: [],
      perPage: 10,
      posCurrentPage: 1,
      negCurrentPage: 1,
      neutCurrentPage: 1
    }
  },
  mounted () {
    // this.getTasks()
    // this.file = this.$store.getters.file
    this.handleFileUpload(true)
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
    storeFile () {
      this.$store.commit('updateFile', this.$refs.file.files[0])
      this.handleFileUpload(false)
    },
    handleFileUpload (passedFromHomePage) {
      this.file = this.$store.getters.file
      // this.file = this.$refs.file.files[0]
      // let selectedFile = null
      // if (typeof this.$refs.file.files[0] === 'undefined' || this.$refs.file.files[0] === null || this.$refs.file.files[0] === '') {
      //   console.log('called')
      //   selectedFile = this.$store.getters.file
      // } else {
      //   console.log(this.$refs.file.files[0])
      //   selectedFile = this.$refs.file.files[0]
      // }
      // selectedFile = this.$store.getters.file
      let selectedFile = this.file
      console.log(selectedFile === null)

      var idxDot = selectedFile.name.lastIndexOf('.') + 1
      var extFile = selectedFile.name.substr(idxDot, selectedFile.name.length).toLowerCase()
      if (extFile === 'txt' || extFile === 'csv') {
        console.log(extFile)
        this.file = selectedFile
      } else {
        this.file = null
        this.$store.commit('removeFile', true)
        alert('Only txt and csv files are allowed!')
      }
      if (selectedFile !== null && passedFromHomePage === true) {
        console.log(passedFromHomePage)
        console.log(selectedFile)
        this.addNewTask()
      }
    },
    getTasks (result) {
      this.results = result.data[0].result
      let pos = 0
      let neg = 0
      let neut = 0
      for (let index = 0; index < result.data[0].result.length; index++) {
        // this.predictions.push({tag: result.data[index].tag})
        if (result.data[0].result[index].tag === 'positive') {
          pos++
        } else if (result.data[0].result[index].tag === 'negative') {
          neg++
        } else if (result.data[0].result[index].tag === 'neutral') {
          neut++
        }
      }
      this.predictionsStats = [{label: 'positive', count: pos}, {label: 'negative', count: neg}, {label: 'neutral', count: neut}]

      // SET FREQUECIES LISTS
      this.positiveFrequencies = result.data[0].positiveFrequencies
      this.negativeFrequencies = result.data[0].negativeFrequencies
      this.neutralFrequencies = result.data[0].neutralFrequencies

      this.file = null

      // GET LIST OF OBJECTS FROM LIST OF LISTS FOR BOOTSTRAP-VUE TABLES
      this.posFreqDictList = this.getFrequenciesObjects(this.positiveFrequencies)
      this.negFreqDictList = this.getFrequenciesObjects(this.negativeFrequencies)
      this.neutFreqDictList = this.getFrequenciesObjects(this.neutralFrequencies)
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
      console.log(this.file)
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
    },
    // BootstrapVue table requires data to be in list of objects
    getFrequenciesObjects (frequenciesList) {
      let freqObjectsList = []
      frequenciesList.forEach(element => {
        freqObjectsList.push({word: element[0], frequency: element[1]})
      })
      return freqObjectsList
    }
  },
  computed: {
    disableBtn () {
      return this.file === null
    },
    posRows () {
      return this.positiveFrequencies.length
    },
    negRows () {
      return this.negativeFrequencies.length
    },
    neutRows () {
      return this.neutralFrequencies.length
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
.fixed {
  position: fixed;
  top: 0;
  z-index: 2;
}
</style>
